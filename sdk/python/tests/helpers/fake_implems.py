import attr


class Serializer:
    serializer_version: Version

    def to_bytes(self,  ml_model) -> bytes:
        return str(ml_model.weights).encode("utf-8")

    def from_bytes(self, model_bytes: bytes):
        return FakeModelClass(int(model_bytes.decode("utf-8")))


@attr.s()
class ModelClass:
    weights: int = attr.field()

    @weights.validator
    def _validate_model(self, attribute, value):
        if not isinstance(value, int):
            raise ValueError("bad init")
