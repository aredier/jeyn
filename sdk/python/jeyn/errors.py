class DataConsistencyError(Exception):
    """
    error raised when a data inconsistency between the current and remote state of jeyn core
    services is detected
    """

class DataConversionError(DataConsistencyError):
    """
    error raised when an object cannot be converted into the desired target class
    """


class DataOverrideError(DataConsistencyError):
    """
    error raised when the user is trying to override a protected piece of data
    """
