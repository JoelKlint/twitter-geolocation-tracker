import numpy as np
import layers_method.user_locations as ul
import layers_method.timezones as tz


#Removes additional decimals to match accuracy
def remove_coordinate_decimals(coordinate, nbr_of_numbers_to_keep):
    str_coordinate = str(coordinate)
    integer = str_coordinate.split('.')[0]
    decimal = str_coordinate.split('.')[1]
    new_coordinate = ""
    for nbr in integer:
        if nbr == '-':
            new_coordinate += '-'
        else:
            new_coordinate += nbr
    for i, nbr in enumerate(decimal):
        if i < nbr_of_numbers_to_keep:
            new_coordinate += nbr
    return float(new_coordinate)

#Creates a matrix for a bounding box in accordance to the world
#Matrix coordinates should be given in "Tusental".
#BoundingBox Form: min_long, min_lat, max_long, max_lat
def map_boundingbox_to_matrix(boudning_box, matrix_accuracy, scale):
    nbr_rows = 360*matrix_accuracy
    nbr_cols = 180*matrix_accuracy
    matrix_coordinates = np.zeros((nbr_rows, nbr_cols))
    coordinate_accuracy = str(matrix_accuracy)
    nbr_of_zeros = len(coordinate_accuracy.split("0"))-1
    rounded_boundingbox = []
    if nbr_of_zeros > 0:
        for coordinate in boudning_box:
            rounded_coordinate = remove_coordinate_decimals(coordinate, nbr_of_zeros)
            rounded_boundingbox.append(rounded_coordinate)
    else:
        for coordinate in boudning_box:
            rounded_coordinate = int(coordinate)
            rounded_boundingbox.append(rounded_coordinate)

    min_long = rounded_boundingbox[0]
    min_lat = rounded_boundingbox[1]
    max_long = rounded_boundingbox[2]
    max_lat = rounded_boundingbox[3]

    min_long += 180*matrix_accuracy
    max_long += 180*matrix_accuracy
    min_lat += 90*matrix_accuracy
    max_lat += 90*matrix_accuracy

    for current_long in range(min_long, max_long, 1):
        for current_lat in range(min_lat, max_lat, 1):
            matrix_coordinates[current_long, current_lat] = scale

    return matrix_coordinates


