from markup_ansi import getc
from datetime import datetime

def log(message, type):
    prefixes = "LOG", "WARN", "ERROR"
    prefix = ""
    if type == "log":
            prefix = "[" + getc("white","1") + prefixes[0] + getc("clear","0") + "]   "
    elif type == "warn":
            prefix = "[" + getc("yellow","1") + prefixes[1] + getc("clear","0") + "]  "
    elif type == "error":
            prefix = "[" + getc("red","1") + prefixes[2] + getc("clear","0") + "] "

    print(datetime.now().strftime("%H:%M:%S ") + prefix + message)
