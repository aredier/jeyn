import os
import tempfile
from typing_utils import Any
import datetime as dt

import pandas as pd
from sklearn.datasets import load_breast_cancer
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


class InputDataCatalog(jeyn.catalogs.DataCatalog):
    mean_radius = jeyn.catalogs.Feature(name="mean radius", dtype=jeyn.catalogs.Dtypes.FLOAT32, shape=(-1, 1))
    mean_texture = jeyn.catalogs.Feature(name="mean texture", dtype=jeyn.catalogs.Dtypes.FLOAT32, shape=(-1, 1))
    mean_perimeter = jeyn.catalogs.Feature(name="mean perimeter", dtype=jeyn.catalogs.Dtypes.FLOAT32, shape=(-1, 1))


class InferenceDataCatalog(jeyn.catalogs.DataCatalog):
    breast_cancer_proba = jeyn.catalogs.Feature(dtype=jeyn.catalogs.Dtypes.FLOAT32, shape=(-1, 1))


def init_dataset(store: jeyn.datasets.DatasetStore):
    new_batch = load_breast_cancer()
    batch_df = pd.DataFrame(new_batch.data)
    batch_df.columns = new_batch.feature_names
    batch_df["targets"] = new_batch.target
    dataset_path = "/tmp/jeyn/datasets/breasts"
    os.makedirs(dataset_path, exist_ok=True)
    batch_df.to_csv(f"{dataset_path}/{dt.datetime.utcnow().isoformat()}.csv")
    dataset_formula = store.get_fromula(
        formula_cls=jeyn.datasets.formulas.StreamingFormula, name="test_formula"
    )
    if dataset_formula is None:
        dataset_formula = jeyn.datasets.formulas.StreamingFormula(
            "test_formula", version="0.1.0", output_catalog=InputDataCatalog(), data_dir=dataset_path
        )
        dataset_formula.save()


if __name__ == '__main__':
    dataset_store = jeyn.datasets.DatasetStore()
    init_dataset(dataset_store)
    dataset_formula = dataset_store.get_fromula(
        formula_cls=jeyn.datasets.formulas.StreamingFormula, name="test_formula"
    )
    training_data = dataset_formula.get_new_batch()

    dataset = pd.read_csv(training_data.files[-1])
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(32, input_shape=(None, 3)),
        tf.keras.layers.Dense(1, activation="relu", name="breast_cancer_proba")
    ])
    model.compile("adam", "mse")
    model.fit(dataset.loc[:, ["mean radius", "mean texture", "mean perimeter"]], dataset["targets"])
    dataset_store.save_batch(training_data)

    store = jeyn.models.ModelStore()
    serializer = KerasSerializer()
    store.register_serializer(tf.keras.Model, serializer)
    use_case = jeyn.models.MlUseCase(
        name="test_use_case",
        description="a use case just for tests"
    )
    store.save_use_case(use_case)
    checkpoint = jeyn.models.ModelCheckpoint(
        use_case=use_case,
        version=jeyn.Version.from_version_string("0.1.0"),
        output_catalog=InferenceDataCatalog(),
        input_catalog=InputDataCatalog(),
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
    print(new_model.predict(dataset.loc[:, ["mean radius", "mean texture", "mean perimeter"]]))
