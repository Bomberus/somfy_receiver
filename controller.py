from machine import Pin, Timer
from storage import load, save, INIT_STATE

STOP = 0
UP = 1
DOWN = 2

relay_up = Pin(6, Pin.OUT) #Up
relay_down = Pin(7, Pin.OUT) #Down

class SomfyController:
    def __init__(self) -> None:
        state = load()
        self.state = state if state is not None else INIT_STATE
        self.timer = Timer()
        self.action = STOP
        self.target = 0
        relay_down(0)
        relay_up(0)

    def current(self, target):
        self.state["current"] = target
        save(self.state)
        return self.status()

    def current_percent(self, target_percent):
        self.state["current"] = round(target_percent * int(self.state["max"]) / 100)
        save(self.state)
        return self.status()
    
    def goal(self, target_percent):
        if self.action != STOP:
            self.stop()
        
        self.target = round(target_percent * int(self.state["max"]) / 100)
        
        if self.target == self.state["current"]:
            return
        
        if self.target > self.state["current"]:
            self.action = UP
        elif self.target < self.state["current"]:
            self.action = DOWN

        self._start_timer()
        return self.status()

    def status(self):
        return { 
            "current": self.state["current"],
            "percent":  self.state["current"] * 100 / int(self.state["max"]),
            "max": self.state["max"],
            "target": self.target,
            "action": self.action,
            "relay_up": True if relay_up.value() == 1 else False,
            "relay_down": True if relay_down.value() == 1 else False
        }

    def up(self):
        if self.action != STOP:
            self.stop()
        
        self.target = self.state["max"]
        self.action = UP
        self._start_timer()
        return self.status()

    def down(self):
        if self.action != STOP:
            self.stop()

        self.target = 0
        self.action = DOWN
        self._start_timer()
        return self.status()

    def stop(self):
        self._stop_timer()
        self.action = STOP
        relay_down(0)
        relay_up(0)
        return self.status()

    def _tick(self):
        if self.action == STOP:
            self.stop()
            return
        
        if self.target == self.state["current"]:
            self.stop()
            return
        
        if self.state["current"] == 0 and self.action == DOWN:
            self.stop()
            return

        if self.state["current"] == self.state["max"] and self.action == UP:
            self.stop()
            return

        if self.action == UP:
            relay_down(0)
            relay_up(1)
            self.state["current"] = self.state["current"] +1

        if self.action == DOWN:
            relay_up(0)
            relay_down(1)
            self.state["current"] = self.state["current"] -1

        save(self.state)

        print("Current / Target: ", self.state["current"], "/", self.target)
        print("Max: ", self.state["max"])
        print("Action (STOP, UP, DOWN): ", self.action)


    def _start_timer(self):
        self.timer.init(
            period=1000, 
            mode=Timer.PERIODIC, 
            callback=lambda _:self._tick())
    
    def _stop_timer(self):
        self.timer.deinit()