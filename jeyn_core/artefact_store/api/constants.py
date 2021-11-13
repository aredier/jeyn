import enum

PUB_SUB_NAME = "pubsub"


class PUB_SUB_TOPICS(enum.Enum):
    ARTEFACT_CREATED = "artefact-created"
    ARTEFACT_CREATION_FAILED = "artefact-creation-failure"

    ARTEFACT_CLASS_CREATED = "artefact-class-created"
    ARTEFACT_CLASS_CREATION_FAILED = "artefact-class-creation-failure"
