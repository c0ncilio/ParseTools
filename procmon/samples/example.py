import os,sys
path = os.path.join(os.getcwd(), "..")
sys.path.append(path)
from procmon import *

def procmon_dump(filename):
    entries = ParseProcmonCsv(filename)
    for entry in entries:
        if entry.EventClass == EVENT_CLASS_REGISTRY and entry.Operation == OPERATION_REG_QUERY_VALUE:
            if entry.Result == RESULT_SUCCESS:
                print(entry.ProcessName, entry.PID, entry.Integrity)

procmon_dump("procmon.csv")
