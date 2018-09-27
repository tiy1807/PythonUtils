from PythonUtils.live_info.live_email import EmailInfo
from live_info.live_manager import Display

def test_basic_email():
    # Sets an hour as the expiry duration of the information
    # and requests the last 10 messages
    email = EmailInfo(60, 10)

    # displays in the terminal
    display = Display([email])
    display.show_display()
