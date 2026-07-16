import platform
import mcproto.protos.common_pb2 as common_pb2

def detect_platform():
    system = platform.system().lower()
    machine = platform.machine().lower()

    if system == "windows":
        if "arm" in machine:
            return common_pb2.PLATFORM_WINDOWS_ARM64
        return common_pb2.PLATFORM_WINDOWS_X64

    if system == "linux":
        if "arm" in machine or "aarch64" in machine:
            return common_pb2.PLATFORM_LINUX_ARM64
        return common_pb2.PLATFORM_LINUX_X64

    if system == "darwin":  # macOS
        if "arm" in machine or "aarch64" in machine:
            return common_pb2.PLATFORM_MACOS_ARM64
        return common_pb2.PLATFORM_MACOS_X64

    return common_pb2.PLATFORM_UNSPECIFIED
