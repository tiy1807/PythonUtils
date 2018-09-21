import requests
from live_info.display_item import DisplayItem

class TrafficInfo(DisplayItem):
    # Put your own API key here
    GOOGLE_MAPS_API_KEY = 'INVALID'
    GOOGLE_DIST_MATRIX_URL = 'https://maps.googleapis.com/maps/api/distancematrix/json'

    def __init__(self, expiry_duration, origin, destination, departure_time='now'):
        DisplayItem.__init__(self, expiry_duration)
        self.payload = {'origins': origin,
                   'destinations': destination,
                   'departure_time': departure_time,
                   'key': TrafficInfo.GOOGLE_MAPS_API_KEY}

    def set_origin(self, new_origin):
        self.payload['origins'] = new_origin

    def set_destination(self, new_dest):
        self.payload['destinations'] = new_dest

    def set_departure_time(self, dep_time):
        self.payload['departure_time'] = dep_time

    def get_info(self):
        results = self.find_duration()
        return ("From " + self.payload['origins'] + " to " + self.payload['destinations'] + "\n" +
                "Duration: " + results['duration'] + "\n" +"With traffic: " +
                results['traffic_duration'])

    def find_duration(self):
        resp = requests.get(TrafficInfo.GOOGLE_DIST_MATRIX_URL, params=self.payload)

        content = resp.json()
        no_traffic_duration = ((content.get("rows")[0]).get("elements")[0]).get("duration").get("text")
        traffic_duration = ((content.get("rows")[0]).get("elements")[0]).get("duration_in_traffic").get("text")

        return {'duration' : no_traffic_duration, 'traffic_duration' : traffic_duration}
