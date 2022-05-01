from typing import List

import attr

from ... import datasets, backend


@attr.define
class FileBatch(datasets.DatasetBatch):
    files: List[str]

    def get_batch_kwargs(self) -> backend.typing.JSON:
        return {"files": self.files}

    @classmethod
    def from_json(cls, batch_kwargs: backend.typing.JSON) -> "datasets.DatasetBatch":
        return cls(**batch_kwargs)
