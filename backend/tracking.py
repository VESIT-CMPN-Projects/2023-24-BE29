import numpy as np
import math


def get_angle(vec2, vec1):
    return (math.atan2(vec2[1], vec2[0]) - math.atan2(vec1[1], vec1[0])) * 180 / math.pi


class Camera:
    def __init__(self, id, x, y, dir):
        self.id = id
        self.coord_x = x
        self.coord_y = y
        self.direction = dir


vecs = []
curr_cam = 0
cameras = []
inter_camera_vectors = []
# car_directions = [(370, 205), (4, 3), (0, 1), (2, 3), (-3, 2), (1, -3)]


def create_car_vector(vec1, vec2):
    return [vec2[0] - vec1[0], vec1[1] - vec2[0]]
    # y coords of image increase top to bottom, and graph y coords increase bottom to top
    # so y1-y2


def set_cameras():
    global inter_camera_vectors
    cameras.append(Camera(0, 20, 30, (0, 1)))
    cameras.append(Camera(1, 21, 40, (-1, 0)))
    cameras.append(Camera(2, 27, 35, (-1, -2)))
    cameras.append(Camera(3, 30, 23, (0, -1)))
    cameras.append(Camera(4, 15, 35, (1, 0)))
    cameras.append(Camera(5, 15, 15, (1, 0)))
    inter_camera_vectors = np.zeros((len(cameras), len(cameras), 2))


def create_camera_relative_vectors():
    global inter_camera_vectors
    for a, i in enumerate(cameras):
        for b, j in enumerate(cameras):
            if a == b:
                continue
            inter_camera_vectors[a, b] = (j.coord_x - i.coord_x, j.coord_y - i.coord_y)


def choose_next_camera(curr_cam, car_direction_wrt_cam_vecs):
    cam = -1
    min = 1000
    print(f"car direction wrt cam vecs:\n {car_direction_wrt_cam_vecs}")
    for j in range(len(car_direction_wrt_cam_vecs)):
        if j == curr_cam:
            continue
        if abs(car_direction_wrt_cam_vecs[j]) < min:
            min = abs(car_direction_wrt_cam_vecs[j])
            cam = j

    return cam


def get_car_cam_vect_diff(curr_cam, car_direction):
    global inter_camera_vectors
    car_direction_wrt_cam_vecs = []
    for vec in inter_camera_vectors[curr_cam]:
        a1 = get_angle(cameras[curr_cam].direction, vec)
        a2 = get_angle(cameras[curr_cam].direction, car_direction)
        car_direction_wrt_cam_vecs.append(a1 - a2)

    return choose_next_camera(curr_cam, car_direction_wrt_cam_vecs)


def run_tracker(start_point, end_point):
    set_cameras()
    create_camera_relative_vectors()
    print(f"Inter camera vecs for selected cam: {inter_camera_vectors[curr_cam]}")
    car_direction = create_car_vector(start_point, end_point)
    print(f"Car direction: {car_direction}")
    selected_cam = get_car_cam_vect_diff(curr_cam, car_direction)
    print(f"\n\nSelected Camera: {selected_cam}")
