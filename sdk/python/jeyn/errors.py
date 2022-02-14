class IOException(Exception):
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