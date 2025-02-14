# Copyright (c) 2025 Jonathan S. Pollack (https://github.com/JPPhoto)

import errno
import locale
import os
from typing import Literal

import yaml

from invokeai.invocation_api import (
    BaseInvocation,
    InputField,
    InvocationContext,
    StringOutput,
    invocation,
)


def get_presets() -> dict:
    curdir = os.path.dirname(os.path.abspath(__file__))
    yaml_path = os.path.join(curdir, "presets.yaml")

    if not os.path.exists(yaml_path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), yaml_path)

    with open(yaml_path, "rt", encoding=locale.getpreferredencoding()) as file:
        presets = yaml.safe_load(file)

    return presets


@invocation("preset_to_string", title="Preset to String", tags=["preset_to_string", "string"], version="1.0.0")
class PresetToStringInvocation(BaseInvocation):
    """Looks up and returns a string when a preset is selected"""

    preset: Literal[tuple(get_presets().keys())] = InputField(
        default=list(get_presets().keys())[0],
        description="The preset to use",
    )

    def invoke(self, context: InvocationContext) -> StringOutput:
        return StringOutput(value=get_presets()[self.preset])
