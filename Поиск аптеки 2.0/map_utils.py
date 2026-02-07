def get_toponym_size(toponym):
    envelope = toponym["boundedBy"]["Envelope"]
    lower_corner = list(map(float, envelope["lowerCorner"].split()))
    upper_corner = list(map(float, envelope["upperCorner"].split()))
    delta_longitude = abs(upper_corner[0] - lower_corner[0])
    delta_latitude = abs(upper_corner[1] - lower_corner[1])
    return delta_longitude, delta_latitude

def calculate_map_params(toponym, padding_factor=1.5):
    delta_longitude, delta_latitude = get_toponym_size(toponym)
    toponym_coordinates = toponym["Point"]["pos"]
    longitude, latitude = map(float, toponym_coordinates.split())
    spn_longitude = delta_longitude * padding_factor
    spn_latitude = delta_latitude * padding_factor
    min_size = 0.005
    spn_longitude = max(spn_longitude, min_size)
    spn_latitude = max(spn_latitude, min_size)
    max_size = 0.5
    spn_longitude = min(spn_longitude, max_size)
    spn_latitude = min(spn_latitude, max_size)
    return {
        "ll": f"{longitude},{latitude}",
        "spn": f"{spn_longitude},{spn_latitude}"}
