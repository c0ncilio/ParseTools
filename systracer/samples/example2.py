import os,sys
path = os.path.join(os.getcwd(), "..")
sys.path.append(path)
from systracer import *

def systracer_reg_dump(filename):
    entries = ParseSystracerRegistersCsv(filename)
    for entry in entries:
        if entry.Type == TYPE_PARAMETER and entry.ParameterType == REG_BINARY:
            print(entry.FullPath)

systracer_reg_dump("regs.csv")