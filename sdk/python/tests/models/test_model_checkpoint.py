import fake_implems
import pytest
from hypothesis import given
from hypothesis import strategies as st

import models
from jeyn import Version, errors
from jeyn.models import ModelCheckpoint


@given(
    int_value=st.integers()
)
def test_checkpoint_creation(int_value, use_case):
    checkpoint = ModelCheckpoint(
        use_case=use_case,
        version=Version.from_version_string("0.1.0"),
    )

    assert checkpoint.use_case == use_case
    assert checkpoint.version == Version(0, 1, 0)
    # model was not assigned so it is not loaded
    # and the checkpoint should raise if the model is being accessed
    assert not checkpoint.loaded

    with pytest.raises(errors.LoadingError):
        checkpoint.model

    fake_model = implems.ModelClass(int_value)
    checkpoint.update_model(fake_model)
    assert checkpoint.loaded
    assert checkpoint.model == fake_model


@given(
    int_value=st.integers()
)
def test_checkpoint_override_protection(int_value, use_case):
    """tests that the user cannot change an already saved model"""
    checkpoint = Checkpoint(
        use_case=use_case,
        version=Version.from_version_string("0.1.0"),
    )

    fake_model = implems.ModelClass(int_value)
    checkpoint.update_model(fake_model)
    model_store.save_checkpoint(checkpoint)
    checkpoint.update_model(implems.ModelClass(int_value + 1))
    with pytest.raises(errors.SaveError):
        model_store.save_checkpoint(checkpoint)


@given(
    # TODO create a hypothesis strat for versions
    major_version=st.integers,
    minor_version=st.integers,
    patch_version=st.integers,
    second_major=st.integers,
    second_minor=st.integers,
    second_patch=st.integers,
)
def test_mdoel_consistency(
        major_version,
        minor_version,
        patch_version,
        second_major,
        second_minor,
        second_patch,
        use_case
):
    version_1 = Version(major_version, minor_version, patch_version)
    version_2 = Version(second_major, second_minor, second_patch)
    checkpoint_1 = models.ModelCheckpoint(
        use_case=use_case,
        version=version_1
    )
    checkpoint_2 = models.ModelCheckpoint(
        use_case=use_case,
        version=version_2
    )

    assert checkpoint_1.version == version_1
    assert checkpoint_2.version == version_2
    assert version_1.is_compatible(version_2) == checkpoint_1.is_compatible(checkpoint_2)

