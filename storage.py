import ujson as json
import uos

INIT_STATE = {
    "current": 0,
    "max" : 100
}

FILENAME = "data.json"


def file_exists():
    try:
        uos.stat(FILENAME)
        return True
    except OSError:
        return False

def save(data):
    try:
        with open(FILENAME, 'w') as f:
            json.dump(data, f)
    except:
        print("Error! Could not save data")
        
        
def load():
    if not file_exists():
        return INIT_STATE
    
    try:
        with open(FILENAME, 'r') as f:
            return json.loads(f.read())
    except:
        print("Error! Could not save data")