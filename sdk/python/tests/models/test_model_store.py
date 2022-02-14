import fake_implems


def test_save_reload_checkpoint(checkpoint, model_store):

    model_store.register_serializer(fake_implems.Serializer, [fake_implems.ModelClass])
    model_store.save(checkpoint)

    use_case = model_store.get_use_case(name=checkpoint.use_case.name)
    new_checkpoint = use_case.get_latest_checkpoint()
    assert not new_checkpoint.loaded
    reloaded_checkpoint = model_store.load_checkpoint_model(checkpoint)
    assert reloaded_checkpoint.loaded
    test_utils.assert_equal_models(reloaded_checkpoint.model, checkpoint.model)


def test_save_reload_checkpoint_with_renamed_classes(checkpoint, model_store):

    model_store.register_serializer(fake_implems.Serializer, [fake_implems.ModelClass])
    model_store.save(checkpoint)

    del model_store

    new_model_store = ModelStore()

    class RenamedModelClass(fake_implems.ModelClass):
        pass

    new_model_store.register_serializer(
        fake_implems.Serializer,
        [RenamedModelClass],
        backward_compatibility_class_names=[fake_implems.ModelClass.__class__.__name__]
    )
    use_case = new_model_store.get_use_case(name = checkpoint.use_case.name)
    new_checkpoint = use_case.get_latest_checkpoint()
    reloaded_model = new_model_store.load(checkpoint)
    test_utils.assert_equal_models(reloaded_model, checkpoint.model)
