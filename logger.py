import uos
import utime

MAX_SIZE = 100 * 1024
LOGFILE = "log.txt"

def file_exists():
    try:
        uos.stat(LOGFILE)
        return True
    except OSError:
        return False

def is_full():
    try: 
        return uos.stat(LOGFILE)[6] >= MAX_SIZE
    except OSError:
        return False
    
def get_formatted_time():
    current_time = utime.localtime()
    return "{:02d}/{:02d}/{} {:02d}:{:02d}".format(current_time[2], current_time[1], current_time[0], current_time[3], current_time[4])

def read_all():
    if not file_exists():
        return []
    
    try:
        with open(LOGFILE, "r") as log:
            return log.readlines()
    except:
        print("Could not read log file")
        
def log(str):
    try:
        with open(LOGFILE, "w" if is_full() else "a") as log:
            log.write(f"{get_formatted_time()} :: {str} \n")
    except:
        print("Could not read log file")