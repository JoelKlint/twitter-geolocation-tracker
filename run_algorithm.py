from database.database import Database
import layers_method.user_locations as user_locations
import create_bounding_box_matrixes as bbtomatrix
import numpy as np
import layers_method.tweet_lang as lang

def get_users_data():
    db = Database('twitter-geo')
    return db.select_everything_from_users()

#Adds layers on top of another and chooses the middle highest point
def calculate_highest_point(layers, matrix_accuracy):
    nbr_rows = 360*matrix_accuracy
    nbr_cols = 180*matrix_accuracy
    result_matrix = np.zeros((nbr_rows, nbr_cols))
    for layer in layers:
        result_matrix = np.add(result_matrix, layer)

    max = np.max(result_matrix)
    indices = np.where(result_matrix == result_matrix.max())
    long_mid = int(len(indices[0])/2)
    lat_mid = int(len(indices[1])/2)
    long = indices[0][long_mid]
    lat = indices[1][lat_mid]
    lat -= 90*matrix_accuracy
    long -= 180*matrix_accuracy

    return [lat, long, max]


users = get_users_data()
accuracy = 1
user_location_value = 5
language_value = 2

#Create layers for each user and print thier highest point
for user in users:
    all_layers = []
    user_name = user[2]
    user_lang = user[8]

    user_name_bb = user_locations.get_bounding_box_of_user(user_name)
    if user_name_bb != None:
        layer = bbtomatrix.map_boundingbox_to_matrix(user_name_bb, accuracy, user_location_value)
        all_layers.append(layer)

    if len(all_layers) > 0:
        result = calculate_highest_point(all_layers, accuracy)
        print ('The user:', user_name, 'is located at: lat=',
               result[0], 'long=', result[1], 'with maxvalue=', result[2])
    else:
        print ('Could not calculate any layer for user:', user_name)