from config import connect, get_ip
from microdot import Microdot
import logger
import mrequests
import gc
import sys
import machine
from machine import Pin, Timer
from controller import SomfyController
led = Pin("LED", Pin.OUT)
led_timer = Timer()

VERSION = "1.5"

def blink(timer):
    # LED einschalten
    led.toggle()

try:
    led_timer.init(period=200, mode=Timer.PERIODIC, callback=blink)
    #Bootstrap
    connect()
    import ntptime
    ntptime.settime()
    controller = SomfyController()
    app = Microdot()

    #App Routes
    @app.post('/update')
    async def update(request):
        @request.after_request
        def reset_machine(request, response):
            print("Resetting machine")
            sys.exit()
        url = "https://raw.githubusercontent.com/bomberus/somfy_receiver/master/"
        files = [
            # Main App
            "main.py", "config.py", "controller.py", "logger.py", "storage.py",
            # Microdot
            "microdot/__init__.py", "microdot/microdot.py",
            # mRequests
            "mrequests/__init__.py", "mrequests/mrequests.py", "mrequests/urlencode.py", "mrequests/urlparseqs.py", "mrequests/urlunquote.py"]

        buf = bytearray(1024)

        for file in files:
            res = mrequests.get(url + file)
            print("Downloading: ", url + file)
            if res.status_code == 200:
                res.save(file, buf=buf)
            else:
                print("Issue downloading: ", file)

            res.close()
            gc.collect()
        
        return "Update finished, restarting..."

    
    @app.get('/status')
    async def status(request):
        return {
            "logs": logger.read_all(),
            "state": controller.status(),
            "version": VERSION
        }
    
    @app.post('/up')
    async def up(request):
        data = controller.up()
        return data, 200

    @app.post('/down')
    async def down(request):
        data = controller.down()
        return data, 200

    @app.post("/set")
    async def target(request):
        if "target" in request.args:
            if "no_action" in request.args:
                if bool(request.args["no_action"]):
                    data = controller.current_percent(int(request.args["target"]))
                    return data, 200
        
            data = controller.goal(int(request.args["target"]))
            return data, 200
        else:
            return "expect url parameter: 'target'", 402

    @app.post('/stop')
    async def stop(request):
        data = controller.stop()
        return data, 200

    try:
        logger.log("Started via IP " + get_ip())
        led_timer.deinit()
        app.run()
    except KeyboardInterrupt:
        print("Shutdown requested...")
        app.shutdown()    
    
except Exception as err:
    logger.log("ERROR: Booting failed" + str(err))


    
print("Shutdown finished")