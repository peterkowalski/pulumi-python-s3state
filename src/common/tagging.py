"""Consistent tagging for Pulumi AWS resources."""

from enum import Enum
from typing import TypedDict

import pulumi

from .taggable import is_taggable


class Environment(Enum):
    """Define supported environment names."""

    DEV = "DEV"
    UAT = "UAT"
    PROD = "PROD"


class Tags(TypedDict):
    """Define tags required for each taggable AWS resource."""

    owner: str
    environment: Environment


def register_auto_tags(auto_tags):
    """Register transformation on each AWS resource.

    Args:
        auto_tags: Dictionary of tags.
    """
    pulumi.runtime.register_stack_transformation(lambda args: auto_tag(args, auto_tags))


def auto_tag(args, auto_tags):
    """Add required tags to a specific resource.

    Args:
        args: Arguments of a resource.
        auto_tags: Dictionary of tags.

    Returns:
        The result that must be returned by a resource transformation callback.
    """
    if is_taggable(args.type_):
        args.props["tags"] = {**(args.props["tags"] or {}), **auto_tags}
        return pulumi.ResourceTransformationResult(args.props, args.opts)
    return None
