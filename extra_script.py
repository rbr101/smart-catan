"""
Reads include/password.h (git-ignored, per-developer) and, if it defines
ENABLE_HOME_ASSISTANT, adds -DENABLE_HOME_ASSISTANT to the build flags for
this environment. This must be a compiler-wide flag (not just a #define in
main.cpp) because lib/HomeAssistant/HomeAssistantTrigger.cpp is compiled as
its own translation unit and needs to see the same macro to build its real
implementation instead of the stub.
"""

import os
import re

Import("env")

if env["PIOENV"] != "esp32dev-no-ha":
    password_header = os.path.join(env.subst("$PROJECT_INCLUDE_DIR"), "password.h")
    if os.path.isfile(password_header):
        with open(password_header) as f:
            content = f.read()
        if re.search(r"^\s*#define\s+ENABLE_HOME_ASSISTANT\b", content, re.MULTILINE):
            env.Append(BUILD_FLAGS=["-DENABLE_HOME_ASSISTANT"])
