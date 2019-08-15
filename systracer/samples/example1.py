import os,sys
path = os.path.join(os.getcwd(), "..")
sys.path.append(path)
from systracer import *

def systracer_files_dump(filename ):
    entries = ParseSystracerFilesCsv(filename)
    for entry in entries:
        print(entry.FullPath)

systracer_files_dump("files.csv")