# Jeyn

Welcome to jeyn, jeyn is an open source framework that aims at providing an infrastructure
for production ML applications and give everything a DS team needs to be
able to hit the ground running with as little dev-ops knowledge as possible.


As of writting jeyn is still in its infency and very much not ready to be used in any
kind of production context.

## core concepts

### basic abstractions

Jeyn's python sdk is based around several main abastractions that you
will interact with to build your machine learning pipelines

#### dataset abstractions

- __dataset formula__ a dataset formula is like a cooking reciepe for
  a given dataset, it tells other jeyn users how your dataset has been built
  for instance if it is a streaming pipeline that updates files regularly. Or
  another dataset passed through a model.
- __dataset batch__: If we think of the dataset formula as a cooking reciepe 
  a dataset batch is batch of cookies made with a specific formula. A model will always
  be trained on a precise batch and record this batch for recproducability purposes.
- __data catalog__: it's the schema of any inputs, our outputs of a jeyn dataset or model.

#### model abstractions.
- __model checkpoint__: a model checkpoint is a saved model. A set of weights that have been saved
  after a training
- __model serializers__: a way of going from a python object to a checkpoint's bytes as well as the other
  way around.
- __machine learning use case__: a machine learning use case is basically a way to tell that one or several
  model checkpoints are more or less "the same". Not in that they'll produce the same output (that's a checkpoint)
  but that they should be used the same.

### artefacts, stores and relationships.

All the machine learning abstractions stated above are built withing jeyn to be converted
to two lower level abstractions: artefacts and relationships.
- an __artefact__ is basically a thing that is saved.
- a __relationship__ links two artefacts together.

when building your pipeline, your operations always need to be convert their outputs
to an artefact. To help you with this jeyn provides various stores (`model_store`, `dataset_store` that you 
can use) to save your models, checkpoints, batches, ect and they will return an artefact you can then output
so that jeyn will know how to reload them in subsequent operations.

## contributing to jeyn.
jeyn is based on 2 major open source technologies:
- dapr: a framework that abstracts cloud implementation to be able to have the same code or architecture
  running in different setps with a change of configuration
- Argo: to run your machine learning workflows.

## getting started. 