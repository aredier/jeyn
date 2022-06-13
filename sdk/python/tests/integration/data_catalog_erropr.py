import os
import tempfile
from typing_utils import Any
import datetime as dt

import pandas as pd
from sklearn.datasets import load_breast_cancer
import tensorflow as tf

import datasets
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


def init_dataset(store: jeyn.datasets.DatasetStore):
    new_batch = load_breast_cancer()
    batch_df = pd.DataFrame(new_batch.data)
    batch_df.columns = new_batch.feature_names
    batch_df["targets"] = new_batch.target
    dataset_path = "/tmp/jeyn/datasets/breasts"
    os.makedirs(dataset_path, exist_ok=True)
    batch_df.to_csv(f"{dataset_path}/{dt.datetime.utcnow().isoformat()}.csv")
    dataset_formula = store.get_formula_from_name("test_formula", jeyn.datasets.formulas.StreamingFormula)
    if dataset_formula is None:
        dataset_formula = jeyn.datasets.formulas.StreamingFormula(
            "test_formula", version=None, schema=None, data_dir=dataset_path
        )
        dataset_formula.save()


if __name__ == '__main__':
    store = datasets.DatasetStore()
    init_dataset(store)
    dataset_formula = store.get_formula_from_name("test_formula", jeyn.datasets.formulas.StreamingFormula)
    training_data = dataset_formula.get_new_batch()

    dataset = pd.read_csv(training_data.files[-1])
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(32, input_shape=(None, dataset.shape[1] -1)),
        tf.keras.layers.Dense(1, activation="relu")
    ])
    model.compile("adam", "mse")
    model.fit(dataset.drop("targets", axis=1), dataset["targets"])

    store = jeyn.models.ModelStore()
    serializer = KerasSerializer()
    store.register_serializer(tf.keras.Model, serializer)
    use_case = jeyn.models.MlUseCase(
        name="test_use_case",
        description="a use case just for tests",
        output_schema=None
    )
    store.save_use_case(use_case)
    checkpoint = jeyn.models.ModelCheckpoint(
        use_case=use_case,
        version=jeyn.Version.from_version_string("0.1.0"),
        dataset_batch=training_data,
        model=model
    )
    store.save_checkpoint(checkpoint)

    reloaded_use_case = store.get_use_case(name="test_use_case")
    print(reloaded_use_case)
    reloaded_checkpoint = store.get_latest_use_case_checkpoint(reloaded_use_case)
    print(reloaded_checkpoint)
    new_model = store.load_model_from_checkpoint(reloaded_checkpoint, serializer=serializer)
    dataset = pd.read_csv(training_data.files[-1])
    print(new_model.predict(dataset.drop("targets", axis=1)))