"""Information about Pulumi project and stack."""

from typing import TypedDict


class Metadata(TypedDict):
    """Dictionary describing Pulumi project and stack."""

    project: str
    stack: str
    region: str
