from geopy.distance import geodesic
import json
from scipy.spatial.distance import cdist

class Geo(object):
    distances = []
    def distance_center(self, center, coordinates):
        for coordinate in coordinates:
            distance = geodesic(center, coordinate).miles
            self.distances.append(distance)
        return json.dumps({"distances": self.distances})
    def distance_points(self, coords_1, coords_2 ):
        distance_matrix = cdist(coords_1, coords_2, lambda u, v: geodesic(u,v).miles)
        print(distance_matrix)
        return "hello"
