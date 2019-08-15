from collections import namedtuple
from csv import DictReader
from datetime import datetime

# TODO add date and time parsing for DateTime, TimeOfDay, RelativeTime, CompletionTime

ProcessMonitorEntry = namedtuple('ProcessMonitorEntry', [
        # Application Details
        'ProcessName',
        'ImagePath',
        'CommandLine',
        'Company',
        'Description',
        'Version',
        'Architecture',
        # Event Details
        'Sequence',
        'EventClass',
        'Operation',
        'DateTime',
        'TimeOfDay',
        'Category',
        'Path',
        'Detail',
        'Result',
        'RelativeTime',
        'Duration',
        'CompletionTime',
        # Process Management
        'User',
        'Session',
        'AuthenticationID',
        'Integrity',
        'PID',
        'TID',
        'ParentPID',
        'Virtualized'
    ])

def _ParseCsvEntry(entry):
    p = ProcessMonitorEntry(
        entry['Process Name'] if 'Process Name' in entry else "",
        entry['Image Path'] if 'Image Path' in entry else "",
        entry['Command Line'] if 'Command Line' in entry else "",
        entry['Company'] if 'Company' in entry else "",
        entry['Description'] if 'Description' in entry else "",
        entry['Version'] if 'Version' in entry else "",
        entry['Architecture'] if 'Architecture' in entry else "",

        entry['Sequence'] if 'Sequence' in entry else "",
        entry['Event Class'] if 'Event Class' in entry else "",
        entry['Operation'] if 'Operation' in entry else "",
        entry['Date & Time'] if 'Date & Time' in entry else"",
        entry['Time of Day'] if'Time of Day' in entry else "",
        entry['Category'] if 'Category' in entry else "",
        entry['Path'] if 'Path' in entry else "",
        entry['Detail'] if 'Detail' in entry else "",
        entry['Result'] if 'Result' in entry else "",
        entry['Relative Time'] if 'Relative Time' in entry else "",
        entry['Duration'] if 'Duration' in entry else "",
        entry['Completion Time'] if 'Completion Time' in entry else "",

        entry['User'] if 'User' in entry else "",
        entry['Session'] if 'Session' in entry else "",
        entry['Authentication ID'] if 'Authentication ID' in entry else "",
        entry['Integrity'] if 'Integrity' in entry else "",
        entry['PID'] if 'PID' in entry else "",
        entry['TID'] if 'TID' in entry else "",
        entry['Parent PID'] if 'Parent PID' in entry else "",
        entry['Virtualized'] if 'Virtualized' in entry else ""
    )

    #if entry['Completion Time']:
    #    val = datetime.strptime(entry['Completion Time'], '2:%M:%S.1358473 %p')
    #    print(val)
    #    exit()
    #for key in p._fields:
    #    if not getattr(p, key):
    #        print("WARNING: parameter {} not found (add this column in Process Monitor)".format(key))
    return p

def ParseProcmonCsv(filename : str) -> 'list[ProcessMonitorEntry]':
    result = list()
    with open(filename, "r", encoding='utf-8', errors='ignore') as fp:
        fp.read(1) # skip first u\xfe\xff unicode symbol
        reader = DictReader(fp)
        for row in reader:
            result.append(_ParseCsvEntry(row))
    return result

# ARCHITECTURE
ARCHITECTURE_32_BIT = "32-bit"
ARCHITECTURE_64_BIT = "64-bit"

# CATEGORY
CATEGORY_READ = "Read"
CATEGORY_READ_METADATA = "Read Metadata"
CATEGORY_WRITE = "Write"
CATEGORY_WRITE_METADATA = "Write Metadata"

# EVENT_CLASS
EVENT_CLASS_REGISTRY = "Registry"
EVENT_CLASS_FILE_SYSTEM = "File System"
EVENT_CLASS_PROFILING = "Profiling"
EVENT_CLASS_PROCESS = "Process"
EVENT_CLASS_NETWORK = "Network"

# OPERATION
OPERATION_CANCEL_REMOVE_DEVICE = "CancelRemoveDevice"
OPERATION_CANCEL_STOP_DEVICE = "CancelStopDevice"
OPERATION_CLOSE_FILE = "CloseFile"
OPERATION_CREATE_FILE = "CreateFile"
OPERATION_CREATE_FILE_MAPPING = "CreateFileMapping"
OPERATION_CREATE_MAIL_SLOT = "CreateMailSlot"
OPERATION_CREATE_PIPE = "CreatePipe"
OPERATION_DEBUG_OUTPUT_PROFILING = "Debug Output Profiling"
OPERATION_DEVICE_CHANGE = "DeviceChange"
OPERATION_DEVICE_IO_CONTROL = "DeviceIoControl"
OPERATION_DEVICE_USAGE_NOTIFICATION = "DeviceUsageNotification"
OPERATION_EJECT = "Eject"
OPERATION_FILE_SYSTEM_CONTROL = "FileSystemControl"
OPERATION_FILTER_RESOURCE_REQUIREMENTS = "FilterResourceRequirements"
OPERATION_FLUSH_BUFFERS_FILE = "FlushBuffersFile"
OPERATION_INTERNAL_DEVICE_IO_CONTROL = "InternalDeviceIoControl"
OPERATION_LOAD_IMAGE = "Load Image"
OPERATION_LOCK_FILE = "LockFile"
OPERATION_NOTIFY_CHANGE_DIRECTORY = "NotifyChangeDirectory"
OPERATION_POWER = "Power"
OPERATION_PROCESS_CREATE = "Process Create"
OPERATION_PROCESS_EXIT = "Process Exit"
OPERATION_PROCESS_PROFILING = "Process Profiling"
OPERATION_PROCESS_START = "Process Start"
OPERATION_PROCESS_STATISTICS = "Process Statistics"
OPERATION_QUERY_ALL_INFORMATION_FILE = "QueryAllInformationFile"
OPERATION_QUERY_ATTRIBUTE_CACHE_INFORMATION = "QueryAttributeCacheInformation,"
OPERATION_QUERY_ATTRIBUTE_INFORMATION_VOLUME = "QueryAttributeInformationVolume"
OPERATION_QUERY_ATTRIBUTE_TAG = "QueryAttributeTag"
OPERATION_QUERY_ATTRIBUTE_TAG_FILE = "QueryAttributeTagFile"
OPERATION_QUERY_BASIC_INFORMATION_FILE = "QueryBasicInformationFile"
OPERATION_QUERY_BUS_INFORMATION = "QueryBusInformation"
OPERATION_QUERY_CAPABILITIES = "QueryCapabilities"
OPERATION_QUERY_COMPRESSION_INFORMATION_FILE = "QueryCompressionInformationFile"
OPERATION_QUERY_CONTROL_INFORMATION_VOLUME = "QueryControlInformationVolume"
OPERATION_QUERY_DESIRED_STORAGE_CLASS_INFORMATION = "QueryDesiredStorageClassInformation"
OPERATION_QUERY_DEVICE_INFORMATION_VOLUME = "QueryDeviceInformationVolume"
OPERATION_QUERY_DEVICE_RELATIONS = "QueryDeviceRelations"
OPERATION_QUERY_DEVICE_TEXT = "QueryDeviceText"
OPERATION_QUERY_DIRECTORY = "QueryDirectory"
OPERATION_QUERY_EA_FILE = "QueryEAFile"
OPERATION_QUERY_EA_INFORMATION_FILE = "QueryEaInformationFile"
OPERATION_QUERY_END_OF_FILE = "QueryEndOfFile"
OPERATION_QUERY_FILE_INTERNAL_INFORMATION_FILE = "QueryFileInternalInformationFile"
OPERATION_QUERY_FILE_QUOTA = "QueryFileQuota"
OPERATION_QUERY_FULL_SIZE_INFORMATION_VOLUME = "QueryFullSizeInformationVolume"
OPERATION_QUERY_HARD_LINK_FULL_ID_INFORMATION = "QueryHardLinkFullIdInformation"
OPERATION_QUERY_ID = "QueryId"
OPERATION_QUERY_ID_BOTH_DIRECTORY = "QueryIdBothDirectory"
OPERATION_QUERY_ID_EXTD_BOTH_DIRECTORY_INFORMATION = "QueryIdExtdBothDirectoryInformation"
OPERATION_QUERY_ID_EXTD_DIRECTORY_INFORMATION = "QueryIdExtdDirectoryInformation"
OPERATION_QUERY_ID_GLOBAL_TX_DIRECTORY_INFORMATION = "QueryIdGlobalTxDirectoryInformation"
OPERATION_QUERY_ID_INFORMATION = "QueryIdInformation"
OPERATION_QUERY_INFORMATION_VOLUME = "QueryInformationVolume"
OPERATION_QUERY_INTERFACE = "QueryInterface"
OPERATION_QUERY_IO_PIORITY_HINT = "QueryIoPiorityHint"
OPERATION_QUERY_IS_REMOTE_DEVICE_INFORMATION = "QueryIsRemoteDeviceInformation"
OPERATION_QUERY_LABEL_INFORMATION_VOLUME = "QueryLabelInformationVolume"
OPERATION_QUERY_LEGACY_BUS_INFORMATION = "QueryLegacyBusInformation"
OPERATION_QUERY_LINK_INFORMATION_BYPASS_ACCESS_CHECK = "QueryLinkInformationBypassAccessCheck"
OPERATION_QUERY_LINKS = "QueryLinks"
OPERATION_QUERY_MEMORY_PARTITION_INFORMATION = "QueryMemoryPartitionInformation"
OPERATION_QUERY_MOVE_CLUSTER_INFORMATION_FILE = "QueryMoveClusterInformationFile"
OPERATION_QUERY_NAME_INFORMATION_FILE = "QueryNameInformationFile"
OPERATION_QUERY_NETWORK_OPEN_INFORMATION_FILE = "QueryNetworkOpenInformationFile"
OPERATION_QUERY_NETWORK_PHYSICAL_NAME_INFORMATION_FILE = "QueryNetworkPhysicalNameInformationFile"
OPERATION_QUERY_NORMALIZED_NAME_INFORMATION_FILE = "QueryNormalizedNameInformationFile"
OPERATION_QUERY_NUMA_NODE_INFORMATION = "QueryNumaNodeInformation"
OPERATION_QUERY_OBJECT_ID_INFORMATION_VOLUME = "QueryObjectIdInformationVolume"
OPERATION_QUERY_OPEN = "QueryOpen"
OPERATION_QUERY_PNP_DEVICE_STATE = "QueryPnpDeviceState"
OPERATION_QUERY_POSITION_INFORMATION_FILE = "QueryPositionInformationFile"
OPERATION_QUERY_REMOTE_PROTOCOL_INFORMATION = "QueryRemoteProtocolInformation"
OPERATION_QUERY_REMOVE_DEVICE = "QueryRemoveDevice"
OPERATION_QUERY_RENAME_INFORMATION_BYPASS_ACCESS_CHECK = "QueryRenameInformationBypassAccessCheck"
OPERATION_QUERY_RESOURCE_REQUIREMENTS = "QueryResourceRequirements"
OPERATION_QUERY_RESOURCES = "QueryResources"
OPERATION_QUERY_SECURITY_FILE = "QuerySecurityFile"
OPERATION_QUERY_SHORT_NAME_INFORMATION_FILE = "QueryShortNameInformationFile"
OPERATION_QUERY_SIZE_INFORMATION_VOLUME = "QuerySizeInformationVolume"
OPERATION_QUERY_STANDARD_INFORMATION_FILE = "QueryStandardInformationFile"
OPERATION_QUERY_STANDARD_LINK_INFORMATION = "QueryStandardLinkInformation"
OPERATION_QUERY_STAT_INFORMATION = "QueryStatInformation"
OPERATION_QUERY_STOP_DEVICE = "QueryStopDevice"
OPERATION_QUERY_STREAM_INFORMATION_FILE = "QueryStreamInformationFile"
OPERATION_QUERY_VALID_DATA_LENGTH = "QueryValidDataLength"
OPERATION_QUERY_VOLUME_NAME_INFORMATION = "QueryVolumeNameInformation"
OPERATION_READ_CONFIG = "ReadConfig"
OPERATION_READ_FILE = "ReadFile"
OPERATION_REG_CLOSE_KEY = "RegCloseKey"
OPERATION_REG_CREATE_KEY = "RegCreateKey"
OPERATION_REG_DELETE_KEY = "RegDeleteKey"
OPERATION_REG_DELETE_VALUE = "RegDeleteValue"
OPERATION_REG_ENUM_KEY = "RegEnumKey"
OPERATION_REG_ENUM_VALUE = "RegEnumValue"
OPERATION_REG_FLUSH_KEY = "RegFlushKey"
OPERATION_REG_LOAD_KEY = "RegLoadKey"
OPERATION_REG_OPEN_KEY = "RegOpenKey"
OPERATION_REG_QUERY_KEY = "RegQueryKey"
OPERATION_REG_QUERY_KEY_SECURITY = "RegQueryKeySecurity"
OPERATION_REG_QUERY_MULTIPLE_VALUE_KEY = "RegQueryMultipleValueKey"
OPERATION_REG_QUERY_VALUE = "RegQueryValue"
OPERATION_REG_RENAME_KEY = "RegRenameKey"
OPERATION_REG_SET_INFO_KEY = "RegSetInfoKey"
OPERATION_REG_SET_KEY_SECURITY = "RegSetKeySecurity"
OPERATION_REG_SET_VALUE = "RegSetValue"
OPERATION_REG_UNLOAD_KEY = "RegUnloadKey"
OPERATION_REMOVE_DEVICE = "RemoveDevice"
OPERATION_SET_ALLOCATION_INFORMATION_FILE = "SetAllocationInformationFile"
OPERATION_SET_BASIC_INFORMATION_FILE = "SetBasicInformationFile"
OPERATION_SET_DISPOSITION_INFORMATION_EX = "SetDispositionInformationEx"
OPERATION_SET_DISPOSITION_INFORMATION_FILE = "SetDispositionInformationFile"
OPERATION_SET_EA_FILE = "SetEAFile"
OPERATION_SET_END_OF_FILE_INFORMATION_FILE = "SetEndOfFileInformationFile"
OPERATION_SET_FILE_QUOTA = "SetFileQuota"
OPERATION_SET_FILE_STREAM_INFORMATION = "SetFileStreamInformation"
OPERATION_SET_LINK_INFORMATION_FILE = "SetLinkInformationFile"
OPERATION_SET_LOCK = "SetLock"
OPERATION_SET_PIPE_INFORMATION = "SetPipeInformation"
OPERATION_SET_POSITION_INFORMATION_FILE = "SetPositionInformationFile"
OPERATION_SET_RENAME_INFORMATION_EX = "SetRenameInformationEx"
OPERATION_SET_RENAME_INFORMATION_EX_BYPASS_ACCESS_CHECK = "SetRenameInformationExBypassAccessCheck"
OPERATION_SET_RENAME_INFORMATION_FILE = "SetRenameInformationFile"
OPERATION_SET_REPLACE_COMPLETION_INFORMATION = "SetReplaceCompletionInformation"
OPERATION_SET_SECURITY_FILE = "SetSecurityFile"
OPERATION_SET_SHORT_NAME_INFORMATION = "SetShortNameInformation"
OPERATION_SET_VALID_DATA_LENGTH_INFORMATION_FILE = "SetValidDataLengthInformationFile"
OPERATION_SET_VOLUME_INFORMATION = "SetVolumeInformation"
OPERATION_SHUTDOWN = "Shutdown"
OPERATION_START_DEVICE = "StartDevice"
OPERATION_STOP_DEVICE = "StopDevice"
OPERATION_SURPRISE_REMOVAL = "SurpriseRemoval"
OPERATION_SYSTEM_STATISTICS = "System Statistics"
OPERATION_SYSTEM_CONTROL = "SystemControl"
OPERATION_TCP_ACCEPT = "TCP Accept"
OPERATION_TCP_CONNECT = "TCP Connect"
OPERATION_TCP_DISCONNECT = "TCP Disconnect"
OPERATION_TCP_OTHER = "TCP Other"
OPERATION_TCP_RECEIVE = "TCP Receive"
OPERATION_TCP_RECONNECT = "TCP Reconnect"
OPERATION_TCP_RETRANSMIT = "TCP Retransmit"
OPERATION_TCP_SEND = "TCP Send"
OPERATION_TCP_TCP_COPY = "TCP TCPCopy"
OPERATION_TCP_UNKNOWN = "TCP Unknown"
OPERATION_THREAD_CREATE = "Thread Create"
OPERATION_THREAD_EXIT = "Thread Exit"
OPERATION_THREAD_PROFILE = "Thread Profile"
OPERATION_THREAD_PROFILING = "Thread Profiling"
OPERATION_UDP_ACCEPT = "UDP Accept"
OPERATION_UDP_CONNECT = "UDP Connect"
OPERATION_UDP_DISCONNECT = "UDP Disconnect"
OPERATION_UDP_OTHER = "UDP Other"
OPERATION_UDP_RECEIVE = "UDP Receive"
OPERATION_UDP_RECONNECT = "UDP Reconnect"
OPERATION_UDP_RETRANSMIT = "UDP Retransmit"
OPERATION_UDP_SEND = "UDP Send"
OPERATION_UDP_TCP_COPY = "UDP TCPCopy"
OPERATION_UDP_UNKNOWN = "UDP Unknown"
OPERATION_UNLOCK_FILE_ALL = "UnlockFileAll"
OPERATION_UNLOCK_FILE_BY_KEY = "UnlockFileByKey"
OPERATION_UNLOCK_FILE_SINGLE = "UnlockFileSingle"
OPERATION_VOLUME_DISMOUNT = "VolumeDismount"
OPERATION_VOLUME_MOUNT = "VolumeMount"
OPERATION_WRITE_CONFIG = "WriteConfig"
OPERATION_WRITE_FILE = "WriteFile"

# RESULT
RESULT_SUCCESS = "SUCCESS"
RESULT_ACCESS_DENIED = "ACCESS DENIED"
RESULT_SHARING_VIOLATION = "SHARING VIOLATION"
RESULT_NAME_COLLISION = "NAME COLLISION"
RESULT_NAME_NOT_FOUND = "NAME NOT FOUND"
RESULT_PATH_NOT_FOUND = "PATH NOT FOUND"
RESULT_NO_SUCH_FILE = "NO SUCH FILE"
RESULT_NAME_INVALID = "NAME INVALID"
RESULT_NO_MORE_ENTRIES = "NO MORE ENTRIES"
RESULT_NO_MORE_FILES = "NO MORE FILES"
RESULT_END_OF_FILE = "END OF FILE"
RESULT_BUFFER_TOO_SMALL = "BUFFER TOO SMALL"
RESULT_BUFFER_OVERFLOW = "BUFFER OVERFLOW"
RESULT_REPARSE = "REPARSE"
RESULT_NOT_REPARSE_POINT = "NOT REPARSE POINT"
RESULT_FAST_IO_DISALLOWED = "FAST IO DISALLOWED"
RESULT_FILE_LOCKED_WITH_ONLY_READERS = "FILE LOCKED WITH ONLY READERS"
RESULT_FILE_LOCKED_WITH_WRITERS = "FILE LOCKED WITH WRITERS"
RESULT_IS_DIRECTORY = "IS DIRECTORY"
RESULT_INVALID_DEVICE_REQUEST = "INVALID DEVICE REQUEST"
RESULT_INVALID_PARAMETER = "INVALID PARAMETER"
RESULT_NOT_GRANTED = "NOT GRANTED"
RESULT_CANCELLED = "CANCELLED"
RESULT_BAD_NETWORK_PATH = "BAD NETWORK PATH"
RESULT_BAD_NETWORK_NAME = "BAD NETWORK NAME"
RESULT_MEDIA_WRITE_PROTECTED = "MEDIA WRITE PROTECTED"
RESULT_KEY_DELETED = "KEY DELETED"
RESULT_NOT_IMPLEMENTED = "NOT IMPLEMENTED"
RESULT_NO_EAS_ON_FILE = "NO EAS ON FILE"
RESULT_OPLOCK_NOT_GRANTED = "OPLOCK NOT GRANTED"
