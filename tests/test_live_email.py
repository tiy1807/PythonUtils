from PythonUtils.live_info.live_email import EmailInfo
from PythonUtils.live_info.live_manager import Display

import pytest

@pytest.mark.skip(reason="not currently relevant")
def test_basic_email():
    # Sets an hour as the expiry duration of the information
    # and requests the last 10 messages
    email = EmailInfo(60, 10)

    email.get_results()
