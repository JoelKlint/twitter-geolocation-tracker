import numpy as np

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
    new_coordinate += '.'
    for i, nbr in enumerate(decimal):
        if i <= nbr_of_numbers_to_keep:
            new_coordinate += nbr
    return float(new_coordinate)

#Matrix coordinates should be given in "Tusental".
def map_boundingbox_to_matrix(boudning_box, matrix_accuracy, scale):
    nbr_rows = 180*matrix_accuracy
    nbr_cols = 360*matrix_accuracy
    matrix_coordinates = np.zeros((nbr_rows, nbr_cols))
    coordinate_accuracy = str(matrix_accuracy)
    nbr_of_zeros = len(coordinate_accuracy.split("0"))-1
    rounded_boundingbox = []
    for coordinate in boudning_box:
        rounded_coordinate = remove_coordinate_decimals(coordinate, nbr_of_zeros)
        rounded_boundingbox.append(rounded_coordinate)

    min_long = rounded_boundingbox[0]
    min_lat = rounded_boundingbox[1]
    max_long = rounded_boundingbox[2]
    max_lat = rounded_boundingbox[3]
    for i in range(min_lat, max_lat, 1/matrix_accuracy):
        for j in range(min_long, max_long, 1/matrix_accuracy):
            

#minlong, minlat, maxlong, maxlat
test = [-12.3020, -0.02392, 103.2783, 0.20201]
map_boundingbox_to_matrix(test, 1000)