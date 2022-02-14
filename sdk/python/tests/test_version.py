from hypothesis import given, settings
from hypothesis import strategies as st

from jeyn import Version


@given(
    major=st.integers(min_value=0),
    minor=st.integers(min_value=0),
    patch=st.integers(min_value=0),
)
def test_version_creation_init(major, minor, patch):
    version = Version(major, minor, patch)
    assert version.major == major
    assert version.minor == minor
    assert version.patch == patch


@given(
    major=st.integers(min_value=0),
    minor=st.integers(min_value=0),
    patch=st.integers(min_value=0),
)
def test_version_creation_str(major, minor, patch):
    version = Version.from_version_string(f"{major}.{minor}.{patch}")
    assert version.major == major
    assert version.minor == minor
    assert version.patch == patch


def assert_greater(left, right):
    assert left > right
    assert left >= right
    assert not (left < right)
    assert not (left <= right)
    assert not (left == right)


@given(
    major=st.integers(min_value=0),
    second_major=st.integers(min_value=0),
    minor=st.integers(min_value=0),
    second_minor=st.integers(min_value=0),
    patch=st.integers(min_value=0),
    second_patch=st.integers(min_value=0)
)
@settings(max_examples=1_000)
def test_version_comparison(major, minor, patch, second_major, second_minor, second_patch):
    version = Version(major, minor, patch)
    other_version = Version(second_major, second_minor, second_patch)
    if major > second_major:
        assert_greater(version, other_version)
        return
    if major < second_major:
        assert_greater(other_version, version)
        return
    if minor > second_minor:
        assert_greater(version, other_version)
        return
    if minor < second_minor:
        assert_greater(other_version, version)
        return
    if patch > second_patch:
        assert_greater(version, other_version)
        return
    if patch < second_patch:
        assert_greater(other_version, version)
        return
    assert version == other_version


@given(
    major=st.integers(min_value=0),
    second_major=st.integers(min_value=0),
    minor=st.integers(min_value=0),
    second_minor=st.integers(min_value=0),
    patch=st.integers(min_value=0),
    second_patch=st.integers(min_value=0)
)
@settings(max_examples=1_000)
def test_version_compatibility(major, minor, patch, second_major, second_minor, second_patch):
    version = Version(major, minor, patch)
    other_version = Version(second_major, second_minor, second_patch)
    if (major == 0 and second_major == 0) and (minor != second_minor):
        assert not version.is_compatible(other_version)
        assert not other_version.is_compatible(version)
        return
    if major == second_major:
        assert version.is_compatible(other_version)
        assert other_version.is_compatible(version)
        return
    assert not version.is_compatible(other_version)
    assert not other_version.is_compatible(version)