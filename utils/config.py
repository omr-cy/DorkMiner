
APP_VERSION = '1.0'

BANNER = (rf"""
    {'\033[95m'}
    ___  ____ ____ _  _      _  _ _ _  _ ____ ____ 
    |  \ |  | |__/ |_/   __  |\/| | |\ | |___ |__/ 
    |__/ |__| |  \ | \_      |  | | | \| |___ |  \ 
    {'\033[0m'}
    """ + rf"""
    Copyright © 2025 Omar Ashraf, known as {'\033[94m'}omr{'\033[0m'}
    Version {'\033[92m'}{APP_VERSION}{'\033[0m'}
""")

MSG = {
    'INIT'  : f"{'\033[95m'}[INIT]{'\033[0m'}",    # Purple
    'INFO'  : f"{'\033[94m'}[INFO]{'\033[0m'}",    # Blue
    'SUCC'  : f"{'\033[92m'}[SCSS]{'\033[0m'}",    # Green
    'DONE'  : f"{'\033[92m'}[DONE]{'\033[0m'}",    # Green
    'WARN'  : f"{'\033[93m'}[WARN]{'\033[0m'}",    # Yellow
    '!ERR'  : f"{'\033[91m'}[!ERR]{'\033[0m'}",    # Red
    'TAP4'  : "    "
}