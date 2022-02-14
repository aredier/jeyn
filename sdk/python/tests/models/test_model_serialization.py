import pytest
from hypothesis import given
from hypothesis import strategies as st

from jeyn import models, errors
import fake_implems




def test_protocol_detection():
    assert isinstance(fake_implems.Serializer, models.ModelSerilizer)


@given(
    int_value=st.integers()
)
def test_serializer_registration(int_value):
    model_store = models.ModelStore()
    model_store.register_serializer(fake_implems.Serializer, [fake_implems.ModelClass])
    model_bytes = model_store.serialize(fake_implems.Serializer(int_value))
    assert isinstance(model_bytes, bytes)
    assert model_bytes == fake_implems.Serializer().to_bytes(fake_implems.ModelClass(int_value))
    assert isinstance(model_store.get_class_serializer(fake_implems.ModelClass), fake_implems.Serializer)


@given(
    int_value=st.integers()
)
def test_serializer_registration_errors(int_value):
    model_store = models.ModelStore()
    with pytest.raises(errors.SerilizationError):
        model_store.serialize(fake_implems.ModelClass(int_value))
    with pytest.raises(errors.ProtocolEror):
        model_store.register_serializer(
            fake_implems.ModelClass  # fake model does not implement the serializer protocol
        )


@given(
    int_value=st.integers()
)
def test_model_store_serialization(int_value: int):
    model_store = models.ModelStore()
    model_store.register_serializer(fake_implems.Serializer, [fake_implems.ModelClass])
    model_bytes = model_store.serialize(fake_implems.ModelClass(int_value))
    assert isinstance(model_bytes, bytes)
    assert model_bytes == fake_implems.ModelClass().to_bytes(fake_implems.ModelClass(int_value))
    assert model_store.get_class_serializer(fake_implems.ModelClass).from_bytes(model_bytes) == int_value
