#!/usr/bin/env python3
"""Print the runtime allocation without exposing environment values."""
from __future__ import annotations

import json
import os
import platform
from pathlib import Path


def read_limit(path: str) -> str:
    file = Path(path)
    return file.read_text().strip() if file.exists() else "unavailable"


affinity = len(os.sched_getaffinity(0)) if hasattr(os, "sched_getaffinity") else None
print(json.dumps({
    "python": platform.python_version(),
    "platform": platform.platform(),
    "cpu_affinity_count": affinity,
    "cpu_quota": read_limit("/sys/fs/cgroup/cpu.max"),
    "memory_limit_bytes": read_limit("/sys/fs/cgroup/memory.max"),
    "accelerator_requested": False,
}, sort_keys=True))
