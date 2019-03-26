from geopy.distance import distance
import json
from scipy.spatial.distance import cdist
import numpy as np

class Geo(object):
    distances = np.array([])
    def distance_center(self, center, coordinates):
        for coordinate in coordinates:
            distance = np.linalg.norm(center - coordinate)
            #geodesic(center, coordinate).kilometers
            self.distances = np.append(self.distances, distance)
        return self.distances
    def distance_points(self, coords_1, coords_2 ):
        distance_matrix = cdist(coords_1, coords_2, lambda u, v: np.linalg.norm(u-v))
        print("")
        return distance_matrix
