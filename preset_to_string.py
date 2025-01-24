# Copyright (c) 2025 Jonathan S. Pollack (https://github.com/JPPhoto)

import errno
import locale
import os
import pathlib
import yaml
from typing import Literal

from invokeai.invocation_api import (
    BaseInvocation,
    BaseInvocationOutput,
    InputField,
    InvocationContext,
    OutputField,
    invocation,
    invocation_output,
    StringOutput,
)


def get_presets() -> dict:
    curdir = pathlib.Path(__file__).parent
    yaml_path = os.path.join(curdir, "presets.yaml")
    if not os.path.exists(yaml_path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), yaml_path)
    with open(yaml_path, "rt", encoding=locale.getpreferredencoding()) as file:
        presets = yaml.safe_load(file)
    return presets

get_presets.presets = None

@invocation("preset_to_string", title="Preset to String", tags=["preset_to_string", "string"], version="1.0.0")
class PresetToStringInvocation(BaseInvocation):
    """Looks up and returns a string when a preset is selected"""

    preset: Literal[tuple(get_presets().keys())] = InputField(
        default=list(get_presets().keys())[0],
        description="The preset to use",
    )

    def invoke(self, context: InvocationContext) -> StringOutput:
        return StringOutput(value=get_presets()[self.preset])
