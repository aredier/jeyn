import attr

import typing_utils


@attr.s(frozen=True, eq=True, order=True)
class Version:
    """
    jeyn versions are the way jeyn checks compatibility
    between datasets, models, ect.

    Versions are user provided (and not magically infered) and should follow semantic versioniong conventions:
    * a major version update means the clients of the versioned objects need to be updated to take
      into account the new version. For instance a major dataset version update means models trained on previous
      versions cannot be used for inference on the new version of the dataset.
    * a minor version update means there is a significant performance update with the new version but old
      clients can still safely use our model or dataset.
    * a patch update means a small/insignificant bug fix or tweak.

    >>> my_version = Version("3.2.1")
    >>> new_version = my_version.update_patch()
    >>> new_version
    "<Version 3.2.2>"
    >>> new_version.is_compatible(my_version)
    True
    >>> new_version = my_version.update_minor()
    "<Version 3.3.1>"
    >>> new_version.is_compatible(my_version)
    True
    >>> my_version = Version("3.2.1")
    >>> new_version = my_version.update_major()
    >>> new_version
    "<Version 4.2.1>"
    >>> new_version.is_compatible(my_version)
    False
    """

    major: int = attr.field()
    minor: int = attr.field()
    patch: int = attr.field()

    @minor.validator
    @major.validator
    @patch.validator
    def _validate_version(self, attribute, value):
        if value < 0:
            raise ValueError(f"version numbers should be positive integers, got {value} for {attribute.name} version")

    @staticmethod
    def get_version_json_schema() -> typing_utils.JSON:
        return {
            "type": "object",
            "properties": {
                "major": {"type": "number"},
                "minor": {"type": "number"},
                "patch": {"type": "number"},
            },
            "required": [
                "major", "minor", "patch"
            ]
        }

    @classmethod
    def from_version_string(cls, version_string: str) -> "Version":
        return cls(*map(int, version_string.split(".")))

    def to_version_string(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

    def to_json(self) -> typing_utils.JSON:
        return {"major": self.major, "minor": self.minor, "patch": self.patch}

    def is_compatible(self, other: "Version") -> bool:
        if self.major == 0 and other.major == 0:
            return self.minor == other.minor
        return self.major == other.major

    def update_major(self) -> "Version":
        return Version(self.major + 1, self.minor, self.patch)

    def update_minor(self) -> "Version":
        return Version(self.major, self.minor + 1, self.patch)

    def update_patch(self) -> "Version":
        return Version(self.major, self.minor, self.patch + 1)


if __name__ == "__main__":
    foo = Version(0, 1, 0)
    print(foo)
    bar = Version(0, 2, 0)
    print(foo.is_compatible(bar))
