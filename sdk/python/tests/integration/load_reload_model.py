import os.path
from typing_utils import Any
import tempfile

import numpy as np
import tensorflow as tf
import jeyn


class KerasSerializer:

    def to_bytes(self, model_object: Any) -> bytes:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file = os.path.join(temp_dir, "model.h5")
            model_object.save(temp_file)
            with open(temp_file, "rb") as model_bytes:
                return model_bytes.read()

    def from_bytes(self, model_bytes: bytes) -> Any:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file = os.path.join(temp_dir, "model.h5")
            with open(temp_file, "wb") as model_file:
                model_file.write(model_bytes)
            return tf.keras.models.load_model(temp_file)


if __name__ == "__main__":
    dataset = np.random.random((1024, 2))
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(32, input_shape=(None, 2)),
        tf.keras.layers.Dense(1, activation="relu")
    ])
    model.compile("adam", "mse")
    model.fit(dataset, dataset[:, 0] > 0)

    store = jeyn.models.ModelStore()
    serializer = KerasSerializer()
    store.register_serializer(tf.keras.Model, serializer)
    use_case = jeyn.models.MlUseCase(
        name="test_use_case",
        description="a use case just for tests",
        output_schem=None
    )
    store.save_use_case(use_case)
    checkpoint = jeyn.models.ModelCheckpoint(
        use_case=use_case,
        version=jeyn.Version.from_version_string("0.1.0"),
        dataset_batch=None,
        model=model
    )
    store.save_checkpoint(checkpoint)

    reloaded_use_case = store.get_use_case(name="test_use_case")
    print(reloaded_use_case)
    reloaded_checkpoint = store.get_latest_use_case_checkpoint(reloaded_use_case)
    print(reloaded_checkpoint)
    new_model = store.load_model_from_checkpoint(reloaded_checkpoint, serializer=serializer)
    print(new_model.predict(dataset))
