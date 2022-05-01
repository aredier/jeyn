class JeynBaseError(Exception):
    pass


class BackendError(JeynBaseError):
    pass


class MetaCreationError(BackendError):
    pass


class ArtefactMetaError(BackendError):
    pass


class RelationshipError(BackendError):
    pass

