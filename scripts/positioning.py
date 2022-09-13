from scipy.spatial import distance as dist


# positioning={'torsion_spring': [(1330, 1379), (1711, 966), (899, 991), (1291, 573)], 'central_hub': [(1305, 979)], 'rivet_bottom': [(623, 707), (1993, 1253), (1410, 1708), (729, 1438), (1874, 521), (1199, 257)], 'outer_clip': [(1081.0, 769.0), (1529.0, 1187.5), (1513.5, 757.0), (1094.0, 1206.5)], 'rivet_inner': [(1648, 641), (1647, 1323), (964, 1319), (968, 640)], 'stop_pin': [(947, 742), (1026, 556), (880, 1258), (1585, 1406), (1727, 702), (1661, 1217)], 'rivet_top': [(576, 958), (1648, 1623), (1682, 358), (958, 339), (2031, 1000), (921, 1599)], 'inner_clip': [(1351.0, 773.5), (1097.0, 930.0), (1506.5, 1029.0), (1255.0, 1188.5)]}

relative_position = {}


def positioning_parts(frame, positioning):

    reff_coord = positioning['central_hub0']

    d1 = reff_coord[0]
    d2 = reff_coord[1]

    for key, values in positioning.items():

        distance = dist.euclidean((d1, d2), (values[0], values[1]))

        relative_position[key] = distance

    return relative_position


# print(relative_position)
