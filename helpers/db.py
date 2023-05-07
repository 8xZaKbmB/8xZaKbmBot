import json
from udelinelogging import log
import os

def db_get(filename):
    if not os.path.isfile(filename):
        f = open(filename, "a")
        f.write("{}")
        f.close()
    with open(filename, 'r') as f:
        try:
            datatemp = json.load(f)
        except Exception:
            log(f"Error loading JSON \"{filename}\"", "error")
        f.close() 
        return datatemp
        
def db_write(data, filename):
    if not os.path.isfile(filename):
        raise SystemError(f"Error while writing to file {filename}, file does not exist.")
    with open(filename, 'w') as f:
        json.dump(data, f)
    f.close()
