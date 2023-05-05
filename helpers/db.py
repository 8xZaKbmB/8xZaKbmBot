import json
from udelinelogging import log

def db_get(filename):
    with open(filename, 'r') as f:
        try:
            datatemp = json.load(f)
        except Exception:
            log(f"Error loading JSON \"{filename}\"", "error")
        f.close() 
        return datatemp
        
def db_write(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)
    f.close()
