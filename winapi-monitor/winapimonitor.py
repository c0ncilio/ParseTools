from csv import DictReader
from collections import namedtuple

WinApiOverrideEntry = namedtuple('WinApiOverrideEntry', [
    'Id',
    'Dir',
    'Call',
    'RetValue',
    'CallerAddress',
    'CallerRelativeAddress',
    'ProcessId',
    'ThreadId',
    'LastError',
    'RegistersBeforeCall',
    'RegistersAfterCall',
    'DoubleRet',
    'FloatRet',
    'StartTIme',
    'Duration',
    'ModuleName',
    'ApiName',
    'CallerFullPath'
])


class WinApiOverrideDump:

    def __init__(self):
        self.entries = []
        
    def __sub__(self, other):
        result = WinApiOverrideDump()
        other_api_names = { entry.ApiName for entry in other.entries }
        for entry in self.entries:
            if entry.ApiName not in other_api_names:
                result.entries.append(entry)
        return result


    def load_from_csv(self, filename):
        self.entries.clear()
        with open(filename, "r") as fp:
            #fp.read(1) # skip first u\xfe\xff unicode symbol
            reader = DictReader(fp, delimiter=';')
            for row in reader:
                print(row)
            #    entry = self.make_entry(row)
            #    self.entries.append(entry)
                
    def make_entry(self, record):
        #entry = WinApiOverrideEntry(
        #    *(list(record.values())[:-1])
        #)
        
        entry = WinApiOverrideEntry(
            int(record["Id"]),
            record["Dir"],
            record["Call"],
            record["Ret Value"],
            record["Caller Addr"],
            record["Caller Relative Addr"],
            int(record["ProcessID"], 16) if record["ProcessID"] else 0xffffffff,
            int(record["ThreadID"], 16) if record["ThreadID"] else 0xffffffff,
            int(record["Last Error"], 16) if record["Last Error"] else 0xffffffff,
            self.make_regs(record["Registers Before Call"]),
            self.make_regs(record["Registers After Call"]),
            record["Double Ret"],
            record["Float Ret"],
            record["Start Time"],
            record["Duration (us)"],
            record["Module Name"],
            record["API Name"],
            record["Caller Full Path"]
        )
        
        return entry
        
    def make_regs(self, record):
        regs = {}
        if record:
            reg_items = record.split(', ')
            for item in reg_items:
                name, value = item.split('=')
                regs[name] = int(value, 16)            
        return regs
        
    def dump(self):
        for entry in self.entries:
            print(entry)
            print()
