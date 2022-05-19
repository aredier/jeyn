import glob
import os
import datetime as dt
from typing import Type, List

import attr

from ... import datasets


@attr.define
class StreamingFormula(datasets.DatasetFormula):

    data_dir: str

    @property
    def formula_kwargs(self):
        return {"data_dir": self.data_dir}

    @property
    def batch_type(self) -> Type["datasets.DatasetBatch"]:
        return datasets.batches.FileBatch

    def get_new_batch(self) -> "datasets.batches.FileBatch":
        store = datasets.DatasetStore()
        latest_batch = store.get_latest_formula_batch(self)
        batch_files = []
        for file_path in glob.iglob(os.path.join(self.data_dir, "**")):
            if not os.path.exists(file_path):
                continue
            if latest_batch is None or self.get_date_from_path(file_path) > latest_batch.max_date:
                batch_files.append(file_path)
        return datasets.batches.FileBatch(files=batch_files, formula=self)

    def get_latest_batch(self, dataset_store: datasets.DatasetStore) -> "datasets.batches.FileBatch":
        # get the latest batch
        batches: List[datasets.batches.FileBatch] = dataset_store.get_formula_batches(self)
        files_in_other_batches = {file for batch in batches for file in batch.files}
        all_files = set(os.listdir(self.data_dir))
        files_in_batch = all_files - files_in_other_batches
        return datasets.batches.FileBatch(list(files_in_batch))

    def get_date_from_path(self, path: str) -> dt.datetime:
        pass
