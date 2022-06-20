from .backend.errors import JeynBaseError


class IOException(JeynBaseError):
    pass


class LoadingError(IOException):
    """
    error raised when there is an error returning the raw data corresponding to a metadata already
    loaded in memory
    """


class SaveError(IOException):
    """
    error raised when a peice of data cannot be persisted on the jeyn backend.
    """


class SerializationError(JeynBaseError):
    """
    error raised when jeyn cannot (de)serialize an object or piece of data before saving or loading
    it.
    """


class DataValidationError(JeynBaseError):
    """
    error raised when a specific piece of data does not respect it's contract
    """


class DataConsistencyError(JeynBaseError):
    """
    error raised when data is inconsistent
    """