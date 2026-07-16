# updater/__init__.py
from .utils.platform import detect_platform
from .core import (
    download_full_client,
    download_full_assets,
    download_full_java
)

__all__ = [
    "download_full_client",
    "download_full_assets",
    "download_full_java",
    "detect_platform"
]