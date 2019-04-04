from geopy.distance import geodesic
import json
from scipy.spatial.distance import cdist
import numpy as np

class Geo(object):
    distances = np.array([])
    def distance_center(self, center, coordinates):
        for coordinate in coordinates:
            distance = geodesic(center, coordinate).km
            self.distances = np.append(self.distances, distance)
        return self.distances
    def distance_points(self, coords_1, coords_2 ):
        distance_matrix = cdist(coords_1, coords_2, lambda u, v: geodesic(u,v).km)
        print("")
        return distance_matrix
