import platform
# Import definition of message and constants
from .sys_msg import *


# Find OS (operating system) run python program
def os_check():
    os_type = platform.platform()
    # Linux-4.15.0-54-generic-x86_64-with-Ubuntu-18.04-bionic
    # Windows-10-10.0.17134-SP0

    if os_type.find("Linux") != -1:
        return LINUX_PLATFORM
    elif os_type.find("Windows") != -1:
        return WINDOWS_PLATFORM
    else:
        return UNKNOWN_PLATFORM

    # Check release of operating system
    # platform.release()
        # 4.15.0-54-generic
        # 10

    # Check version of operating system
    # platform.version()
        # #58-Ubuntu SMP Mon Jun 24 10:55:24 UTC 2019
        # 10.0.17134
