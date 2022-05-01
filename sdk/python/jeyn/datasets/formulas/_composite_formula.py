from typing import List

from jeyn import datasets


class CompositeFormula(datasets.DatasetFormula):
    """
    dataset formula for composite dataset. This is useful for models that have several inputs.
    """

    _formulas: List[datasets.DatasetFormula]

    def __init__(self, formulas: List[datasets.DatasetFormula]):
        self._formulas = formulas

        # figure out the version
