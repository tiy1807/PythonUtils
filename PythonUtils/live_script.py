
from live_info.live_manager import Display
from live_info.live_email import EmailInfo
from live_info.live_speed import InternetInfo
from live_info.live_rail import RailInfo
# from live_info.live_traffic import TrafficInfo
from text_input import TextInput
import datetime

tui_rail = TextInput("Please enter the 3 character station code")
tui_rail.request_input()
rail = RailInfo(20, tui_rail.answer)

# tui_traffic_start = TextInput("Please enter postcode of origin")
# tui_traffic_start.request_input()
# tui_traffic_end = TextInput("Please enter postcode of destination")
# tui_traffic_end.request_input()
# traffic = TrafficInfo(20, tui_traffic_start.answer, tui_traffic_end.answer)

internet = InternetInfo(30)

tui_num_messages = TextInput("Enter number of emails")
tui_num_messages.request_input()
email = EmailInfo(60, tui_num_messages.answer)

display = Display([email, internet, rail])
display.set_active_time(datetime.time(6,30),datetime.time(8,00))
display.show_display()
