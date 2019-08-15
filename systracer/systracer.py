try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
from collections import namedtuple
from datetime import datetime
from struct import pack
import csv
import os, sys
import re

class SysTracerFileEntry(namedtuple('SysTracerFileEntry', [
    "Name",
    "Directory",
    "FullPath",
    "Type",
    "Date",
    "Size",
    "Info"
])):
    __slots__ = ()

    def __str__(self):
        INFO_DICT = {INFO_ADD: "add", INFO_DELETE: "del", INFO_OLD: "old", INFO_NEW: "new", INFO_MODIFY: "mod"}
        if self.Type == TYPE_DIRECTORY:
            return "Path: {}, Type: Directory, Info: {}".format(self.FullPath, INFO_DICT[self.Info])
        else:
            return "Path: {}, Type: File, Date: {}, Size: {}, Info: {}".format(self.FullPath, self.Date, self.Size,
                                                                               INFO_DICT[self.Info])


class SysTracerRegistryEntry(namedtuple('SysTracerRegistryEntry', [
    "Parameter",
    "Key",
    "FullPath",
    "Type",
    "ParameterType",
    "Data",
    "Info"
])):
    __slots__ = ()

    def __str__(self):
        INFO_DICT = {INFO_ADD: "add", INFO_DELETE: "del", INFO_OLD: "old", INFO_NEW: "new", INFO_MODIFY: "mod"}
        if self.Type == TYPE_KEY:
            return "Key: {}, Type: Key, Info: {}".format(self.FullPath, INFO_DICT[self.Info])
        elif self.Type == TYPE_PARAMETER:
            return "Key: {}, Type: Parameter, ParameterType: {}, Info: {}".format(self.FullPath, self.ParameterType,
                                                                                  INFO_DICT[self.Info])
        else:
            raise Exception("incorrect type")


TYPE_DIRECTORY = 0x0
TYPE_FILE = 0x1
TYPE_KEY = 0x2
TYPE_PARAMETER = 0x3

INFO_ADD = 0x1
INFO_DELETE = 0x2
INFO_OLD = 0x4
INFO_NEW = 0x8
INFO_MODIFY = INFO_OLD | INFO_NEW

REG_BINARY = "REG_BINARY"
REG_DWORD = "REG_DWORD"
REG_QWORD = "REG_QWORD"
REG_DWORD_LITTLE_ENDIAN = "REG_DWORD_LITTLE_ENDIAN"
REG_QWORD_LITTLE_ENDIAN = "REG_QWORD_LITTLE_ENDIAN"
REG_DWORD_BIG_ENDIAN = "REG_DWORD_BIG_ENDIAN"
REG_EXPAND_SZ = "REG_EXPAND_SZ"
REG_LINK = "REG_LINK"
REG_MULTI_SZ = "REG_MULTI_SZ"
REG_NONE = "REG_NONE"
REG_RESOURCE_LIST = "REG_RESOURCE_LIST"
REG_SZ = "REG_SZ"

def _SetCsvFieldSizeLimit():
    maxInt = sys.maxsize
    while True:
        try:
            csv.field_size_limit(maxInt)
            break
        except OverflowError:
            maxInt = int(maxInt / 10)

def _ParseRegistryParameterData(data, type):
    if type == REG_SZ or type == REG_MULTI_SZ or type == REG_EXPAND_SZ:
        return bytes(data, encoding='utf-8', errors='ignore')

    elif type == REG_NONE or len(data) == 0:
        return bytes()

    elif type == REG_LINK or type == REG_RESOURCE_LIST:
        #raise Exception("Not suppoerted parameter type")
        return bytes()

    patterns = ['(="){0,1}(([0-9a-fA-F]{2}\\s)+)("){0,1}', '(="){0,1}0x[0-9a-fA-F]+\\s\\((\\d+)\\)("){0,1}']
    for pattern in patterns:
        result = re.match(pattern, data)
        if result:
            idx = patterns.index(result.re.pattern)
            if idx == 0:
                data = bytes([int(c, 16) for c in result.group(2).split(' ') if len(c) > 0])
                break
            elif idx == 1:
                data = int(result.group(2))
                if type == REG_DWORD:
                    data = pack("I", data)
                elif type == REG_QWORD:
                    data = pack("Q", data)
                elif type == REG_DWORD_LITTLE_ENDIAN:
                    data = pack("<I", data)
                elif type == REG_DWORD_BIG_ENDIAN:
                    data = pack(">I", data)
                elif type == REG_QWORD_LITTLE_ENDIAN:
                    data = pack("<Q", data)
                break
            else:
                raise Exception("Incorrect parameter data: {}".format(data))
    return bytes(data)

def _CollapseRegistryPath(path):
    ROOT_KEYS_DICT = {
        "HKEY_CLASSES_ROOT" : "HRCR",
        "HKEY_CURRENT_USER" : "HKCU",
        "HKEY_LOCAL_MACHINE" : "HKLM",
        "HKEY_USERS" : "HKU",
        "HKEY_CURRENT_CONFIG" : "HKCC"
    }
    for key in ROOT_KEYS_DICT.keys():
        if str(path).find(key) == 0:
            return str(path).replace(key, ROOT_KEYS_DICT[key])
    return path

def _ParseCsvFileEntry(entry, context):
    FILE_PATH, FILE_DATE, FILE_SIZE, FILE_INFO = 0, 2, 3, 5
    INFO_DICT = {"add" : INFO_ADD, "del" : INFO_DELETE, "old" : INFO_OLD, "new" : INFO_NEW, "mod" : INFO_MODIFY}

    # is directory entry
    if not entry[FILE_DATE]:
        p = SysTracerFileEntry(
            Name= "",
            Directory= entry[FILE_PATH],
            FullPath= entry[FILE_PATH],
            Type= TYPE_DIRECTORY,
            Date= datetime(1, 1, 1, 0, 0), # supported only for files
            Size= 0,
            Info= INFO_DICT[entry[FILE_INFO]] if entry[FILE_INFO] in INFO_DICT else 0
        )
    # is file entry
    else:
        if not context:
            raise Exception("error parse csv file entry (null context)")
        if not entry[FILE_PATH]:
            if context.Info != INFO_OLD and not context.Name:
                Exception("error parse csv file entry")
            entry[FILE_PATH] = context.Name
        p = SysTracerFileEntry(
            Name= entry[FILE_PATH],
            Directory= context.Directory,
            FullPath= os.path.join(context.Directory, entry[FILE_PATH]),
            Type= TYPE_FILE,
            Date= datetime.strptime(entry[FILE_DATE], '="%Y-%m-%d %H:%M.%S"'),
            Size= int(entry[FILE_SIZE]),
            Info= INFO_DICT[entry[FILE_INFO]] if entry[FILE_INFO] in INFO_DICT else 0
        )
    return p

def _ParseCsvRegistryEntry(entry, context):
    REGISTRY_NAME, REGISTRY_TYPE, REGISTRY_DATA, REGYSTRY_INFO = 0, 1, 2, 3
    INFO_DICT = {"add": INFO_ADD, "del": INFO_DELETE, "old": INFO_OLD, "new": INFO_NEW, "mod": INFO_MODIFY}

    entry[REGISTRY_NAME] = _CollapseRegistryPath(entry[REGISTRY_NAME])

    # is registry key entry
    if not entry[REGISTRY_DATA] and not entry[REGISTRY_TYPE]:
        p = SysTracerRegistryEntry(
            Parameter= "",
            Key = entry[REGISTRY_NAME],
            FullPath= entry[REGISTRY_NAME],
            Type= TYPE_KEY,
            ParameterType= "",
            Data= bytes(),
            Info=INFO_DICT[entry[REGYSTRY_INFO]] if entry[REGYSTRY_INFO] in INFO_DICT else 0
        )
    # is registry parameter entry
    else:
        if not context:
            raise Exception("error parse csv registry entry (null context)")
        if not entry[REGISTRY_NAME]:
            if context.Info != INFO_OLD and not context.Parameter:
                Exception("error parse csv registry entry")
            entry[REGISTRY_NAME] = context.Parameter
        p = SysTracerRegistryEntry(
            Parameter= entry[REGISTRY_NAME],
            Key= context.Key,
            FullPath= context.Key + entry[REGISTRY_NAME],
            Type= TYPE_PARAMETER,
            ParameterType= entry[REGISTRY_TYPE],
            Data= _ParseRegistryParameterData(entry[REGISTRY_DATA], entry[REGISTRY_TYPE]),
            Info=INFO_DICT[entry[REGYSTRY_INFO]] if entry[REGYSTRY_INFO] in INFO_DICT else 0
        )
    return p

def ParseSystracerFilesCsv(filename) -> 'list[SysTracerFileEntry]':
    result = []
    context = None
    with open(filename, "rb") as f:
        data = f.read()
    data = data.decode(encoding= "utf-16", errors= "ignore")
    fp = StringIO(data)
    _SetCsvFieldSizeLimit()
    reader = csv.reader(fp, delimiter="\t")
    for row in reader:
        if (len(row) != 6):
            continue
        context = _ParseCsvFileEntry(row, context)
        #print(context)
        result.append(context)
    return result

def ParseSystracerRegistersCsv(filename) -> 'list[SysTracerRegistryEntry]':
    result = []
    context = None
    with open(filename, "rb") as f:
        data = f.read()
    data = data.decode(encoding= "utf-16", errors= "ignore")
    fp = StringIO(data)
    _SetCsvFieldSizeLimit()
    reader = csv.reader(fp, delimiter="\t")
    for row in reader:
        if len(row) != 4:
            continue
        context = _ParseCsvRegistryEntry(row, context)
        result.append(context)
    return result