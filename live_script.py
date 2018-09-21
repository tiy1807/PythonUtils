
from live_info.live_manager import Display
from live_info.live_email import EmailInfo
from live_info.live_speed import InternetInfo
from live_info.live_rail import RailInfo
from live_info.live_traffic import TrafficInfo

from user_input import UserInput

tui_rail = UserInput("Please enter the 3 character station code")
tui_rail.request_input()
rail = RailInfo(10, tui_rail.answer)

tui_traffic_start = UserInput("Please enter postcode of origin")
tui_traffic_start.request_input()
tui_traffic_end = UserInput("Please enter postcode of destination")
tui_traffic_end.request_input()
traffic = TrafficInfo(20, tui_traffic_start.answer, tui_traffic_end.answer)

internet = InternetInfo(1)

tui_num_messages = UserInput("Enter number of emails")
tui_num_messages.request_input()
email = EmailInfo(60, tui_num_messages.answer)

display = Display([email, internet, traffic, rail])
display.show_display()
