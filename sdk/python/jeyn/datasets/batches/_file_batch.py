from typing import List

import attr

from ... import datasets, typing_utils


@attr.define
class FileBatch(datasets.DatasetBatch):
    files: List[str]

    def get_batch_kwargs(self) -> typing_utils.JSON:
        return {"files": self.files}

    @classmethod
    def from_json(cls, formula: datasets.DatasetFormula, batch_kwargs: typing_utils.JSON) -> "datasets.DatasetBatch":
        return cls(formula=formula, **batch_kwargs)
