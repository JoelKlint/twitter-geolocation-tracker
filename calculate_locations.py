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
    return int(new_coordinate)

#Creates a matrix for a bounding box in accordance to the world
#Matrix coordinates should be given in "Tusental".
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

#Adds layers on top of another and chooses the middle highest point
def calculate_highest_point(layers, matrix_accuracy):
    nbr_rows = 360*matrix_accuracy
    nbr_cols = 180*matrix_accuracy
    result_matrix = np.zeros((nbr_rows, nbr_cols))
    for layer in layers:
        result_matrix = np.add(result_matrix, layer)

    #np.savetxt('out.txt', result_matrix, fmt='%d')

    print ('Max value is=', np.max(result_matrix))
    indices = np.where(result_matrix == result_matrix.max())
    print ('Indicies of max is: ', indices)
    long_mid = int(len(indices[0])/2)
    lat_mid = int(len(indices[1])/2)
    long = indices[0][long_mid]
    lat = indices[1][lat_mid]
    lat -= 90*matrix_accuracy
    long -= 180*matrix_accuracy

    print ('The center coordinate is: long =', long/matrix_accuracy, "lat =", lat/matrix_accuracy)


#FORM NEEDED FOR THE BOUNDING BOX: minlong, minlat, maxlong, maxlat

user = 'Sarlla'
user_bound = ul.get_bounding_box_of_user(user)
time_zone_bound = tz.get_bboxes_for_user(user)
accuracy = 10
print('Creating new matrix')
all_layers = []
if user_bound != None:
    print ('Adding user location layer')
    ul_matrix = map_boundingbox_to_matrix(user_bound, accuracy, 5)
    all_layers.append(ul_matrix)
if time_zone_bound != None:
    for bound in time_zone_bound:
        print ('Adding timezone layer')
        all_layers.append(map_boundingbox_to_matrix(bound, accuracy, 2))



calculate_highest_point(all_layers, accuracy)