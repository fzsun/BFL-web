from geopy.distance import geodesic
import json

class Geo(object):
    distances = []
    def distance_center(self, center, coordinates):
        for coordinate in coordinates:
            distance = geodesic(center, coordinate).miles
            self.distances.append(distance)
        return json.dumps({"distances": self.distances})

