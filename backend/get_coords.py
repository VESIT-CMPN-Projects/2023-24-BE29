
class GetCoords():
    def __init__(self) -> None:
        pass


    def get_coords(self,image_files_list,txt_dir):
        first_frame = image_files_list[0].split('.')[0]
        filename = txt_dir + '/' + first_frame + '.txt'
        with open(filename, 'r') as file:
        # Read lines from the file
            lines = file.readlines()
        coordinates = []
        for line in lines:
    # Split the line into x and y coordinates
            x, y = map(int, line.strip().split(','))
            # Append the coordinates as a tuple to the list
            coordinates.append((x, y))
        first_frame_centers = []
        first_frame_centers.append(self.compute_center(coordinates))
        # print(f'First Frame centers: {first_frame_centers}')
    ######### Final Frame Co-ordinates Extraction #############
        last_frame = image_files_list[-1].split('.')[0]
        filename = txt_dir + '/' + last_frame + '.txt'
        with open(filename, 'r') as file:
        # Read lines from the file
            lines = file.readlines()
        coordinates = []
        for line in lines:
    # Split the line into x and y coordinates
            x, y = map(int, line.strip().split(','))
            # Append the coordinates as a tuple to the list
            coordinates.append((x, y))
        last_frame_centers = []
        last_frame_centers.append(self.compute_center(coordinates))
        # print(f'Last Frame centers: {last_frame_centers}')

        return first_frame_centers,last_frame_centers

    def compute_center(self, coordinates):
        center_x = (coordinates[0][0] + coordinates[1][0]) / 2
        center_y = (coordinates[0][1] + coordinates[1][1]) / 2
        return center_x,center_y