import jeyn

from .lib import operations


@jeyn.pipelines.pipeline
def build_dataset():
    operations.train_model()


@jeyn.pipelines.pipeline
def train_model_and_export_predictions():

    model = operations.train_model()
    blessed_model = operations.evaluate_and_bless_model()
    operations.export_predictions(blessed_model)
