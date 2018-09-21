import sys
sys.path.append("C:\\Users\\owner\\Documents")
from zeep import Client
from user_input import UserInput
from live_info.display_item import DisplayItem

# WSDL location of the LDBWS rail information. The most up to date version is
# detailed here: http://lite.realtime.nationalrail.co.uk/openldbws/
LDBWS_WSDL = "https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx?ver=2017-10-01"

# Access token to be supplied in the SOAP header in all web service requests
# Set access token here
ACCESS_TOKEN = "INVALID"

class RailInfo(DisplayItem):
    def __init__(self, expiry_duration, station_code):
        DisplayItem.__init__(self, expiry_duration)
        self.client = Client(LDBWS_WSDL)
        self.token = {"AccessToken": {"TokenValue": ACCESS_TOKEN}}
        self.station_code = station_code

    def get_info(self):
        dep_board = self.client.service.GetDepartureBoard(15,
                                                          self.station_code,
                                                          _soapheaders=self.token)
        services = dep_board.trainServices.service
        return_string = ""
        for service in services:
            loc = service.destination.location
            dest_name = loc[0].locationName
            return_string += "-----------------------------\n"
            return_string += service["std"] + " to " + dest_name + "\n"

            if service.etd == "On time":
                return_string += "This service is on time\n"
            elif service.etd == "Delayed":
                return_string += "This service is delayed\n"
                details = self.client.service.GetServiceDetails(service.serviceID, _soapheaders=self.token)
            else:
                return_string += "Estimated arrival " + service.etd + "\n"

            if service.isCancelled != None:
                return_string += "This service is cancelled\n"

        return_string += "-----------------------------\n"
        return return_string

if __name__ == "__main__":
    tui = UserInput("Which station would you like to see the departures of? "
                    "Please enter the 3 character station code.")
    rc = tui.request_input()
    if rc == UserInput.SUCCESS:
        rail_client = RailInfo(tui.answer)
        print(rail_client.live_departure_string())
