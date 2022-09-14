import cv2
from spring_model import main_springs
import numpy as np
from direct_test import load_model, predict
import torch




# bboxcoords={'torsion_spring': [[1206, 1274, 1563, 1518], [816, 847, 1043, 1219], [1633, 749, 1859, 1117], [1099, 456, 1476, 697]], 'outer_clip': [[1528, 1125, 1648, 1247], [1028, 727, 1149, 849], [1476, 673, 1589, 796], [1085, 1179, 1197, 1299]], 'central_hub': [[1228, 871, 1457, 1100]], 'rivet_bottom': [[1076, 1668, 1161, 1759], [550, 1115, 638, 1206], [1812, 1492, 1897, 1581], [770, 384, 853, 474], [2033, 767, 2117, 857], [1518, 211, 1598, 301]], 'rivet_inner': [[975, 1322, 1058, 1410], [1675, 1262, 1760, 1352], [1618, 560, 1702, 649], [917, 620, 997, 706]], 'rivet_top': [[619, 604, 695, 684], [1930, 531, 2005, 608], [1970, 1284, 2043, 1363], [665, 1363, 744, 1443], [1343, 1700, 1415, 1774], [1254, 187, 1332, 267]], 'inner_clip': [[1520, 985, 1597, 1047], [1280, 1166, 1336, 1245], [1080, 920, 1160, 987], [1338, 736, 1394, 808]], 'stop_pin': [[1635, 1368, 1695, 1433], [980, 535, 1042, 604], [1096, 1343, 1158, 1406], [1721, 626, 1783, 692], [896, 1279, 957, 1344], [1521, 563, 1583, 626]]}

# bboxcoords={'torsion_spring': [[1141, 1264, 1486, 1497], [1591, 784, 1809, 1157], [798, 822, 1012, 1177], [1112, 472, 1464, 688]], 'central_hub': [[1193, 873, 1423, 1096]], 'rivet_bottom': [[581, 663, 664, 750], [1945, 1209, 2029, 1297], [1368, 1666, 1450, 1754], [683, 1392, 763, 1475], [1842, 483, 1919, 566], [1161, 211, 1240, 296]], 'outer_clip': [[1027, 714, 1135, 824], [1476, 1133, 1582, 1242], [1462, 703, 1565, 811], [1042, 1152, 1146, 1261]], 'rivet_inner': [[1606, 597, 1685, 683], [1605, 1279, 1687, 1367], [924, 1279, 1004, 1361], [926, 596, 1008, 683]], 'stop_pin': [[921, 714, 976, 774], [998, 522, 1056, 586], [850, 1228, 910, 1291], [1555, 1374, 1614, 1436], [1701, 672, 1757, 732], [1635, 1187, 1691, 1248]], 'rivet_top': [[540, 920, 610, 992], [1612, 1587, 1684, 1661], [1650, 324, 1721, 397], [924, 301, 995, 375], [1999, 966, 2066, 1037], [883, 1561, 956, 1637]], 'inner_clip': [[1324, 738, 1378, 809], [1062, 902, 1132, 958], [1475, 1002, 1538, 1056], [1228, 1148, 1282, 1229]]}

device = "cuda" if torch.cuda.is_available() else "cpu"

# position_dict = {}

# dimension_dict = {}


model = load_model(checkpoint_path='/home/frinks1/10_model.pth', device=device)

# frame=cv2.imread('/home/rishabh/frinks/tata_comms/tata_demo/2000.bmp')

def dimensioning_parts(frame, bboxcoords):

    position_dict = {}

    dimension_dict = {}

    device = "cuda" if torch.cuda.is_available() else "cpu"


    for old_key, old_value in bboxcoords.items():

        if old_key == 'torsion_spring':

            count_spring = 0
            for key, coord in old_value.items():

                image = frame[coord[1]-10:coord[3]+10, coord[0]-10:coord[2]+10]
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                imask = main_springs(image)
                gray = cv2.cvtColor(imask, cv2.COLOR_BGR2GRAY)
                M = cv2.moments(gray)
                if (M['m00'] != 0):
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    new_cX = cX+coord[0]-10
                    new_cY = cY+coord[1]-10

                count_spring += 1
                position_dict[key] = (new_cX, new_cY)

            # if count_spring<4:
            #     print(f"{}")

        if old_key == 'rivet_top':

            for key, coord in old_value.items():

                image = frame[coord[1]:coord[3], coord[0]:coord[2]]
                image = predict(model, image, device=device)

                circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 1, 20,
                                           param1=50, param2=30, minRadius=27, maxRadius=42)

                if circles is not None:
                    circles = np.uint16(np.around(circles))
                    for x, i in enumerate(circles[0, :]):
                        value = (i[0]+coord[0], i[1]+coord[1])
                        size = i[2]

                        position_dict[key] = value

                        dimension_dict[key] = size/12

                else:
                    value = ((coord[0]+coord[2])/2, (coord[1]+coord[3])/2)

                    position_dict[key] = value

                    dimension_dict[key] = 34/12

        if old_key == 'rivet_inner':

            for key, coord in old_value.items():

                image = frame[coord[1]:coord[3], coord[0]:coord[2]]
                image = predict(model, image, device=device)
                circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 1, 20,
                                           param1=50, param2=30, minRadius=35, maxRadius=44)

                if circles is not None:
                    circles = np.uint16(np.around(circles))
                    for x, i in enumerate(circles[0, :]):
                        value = (i[0]+coord[0], i[1]+coord[1])
                        size = i[2]

                        position_dict[key] = value

                        dimension_dict[key] = size/12

                else:
                    value = ((coord[0]+coord[2])/2, (coord[1]+coord[3])/2)

                    position_dict[key] = value

                    dimension_dict[key] = 37/12

        if old_key == 'rivet_bottom':

            for key, coord in old_value.items():

                image = frame[coord[1]:coord[3], coord[0]:coord[2]]

                value = ((coord[0]+coord[2])/2, (coord[1]+coord[3])/2)

                position_dict[key] = value

        if old_key == 'stop_pin':

            for key, coord in old_value.items():

                image = frame[coord[1]:coord[3], coord[0]:coord[2]]
                image = predict(model, image, device=device)
                circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 1, 20,
                                           param1=50, param2=30, minRadius=10, maxRadius=30)
                if circles is not None:
                    circles = np.uint16(np.around(circles))
                    for x, i in enumerate(circles[0, :]):
                        value = (i[0]+coord[0], i[1]+coord[1])
                        size = i[2]

                        position_dict[key] = value

                        dimension_dict[key] = size/12

                else:
                    value = ((coord[0]+coord[2])/2, (coord[1]+coord[3])/2)

                    position_dict[key] = value

                    dimension_dict[key] = 25/12

        if old_key == 'central_hub':

            for key, coord in old_value.items():

                image = frame[coord[1]:coord[3], coord[0]:coord[2]]
                image = predict(model, image, device=device)
                circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 1, 126,
                                           param1=150, param2=22, minRadius=95, maxRadius=120)
                if circles is not None:
                    circles = np.uint16(np.around(circles))
                    for x, i in enumerate(circles[0, :]):
                        value = (i[0]+coord[0], i[1]+coord[1])
                        size = i[2]

                        position_dict[key] = value

                        dimension_dict[key] = size/12

                else:
                    value = ((coord[0]+coord[2])/2, (coord[1]+coord[3])/2)

                    position_dict[key] = value

                    dimension_dict[key] = 110/12

        if old_key == 'outer_clip':

            for key, coord in old_value.items():

                image = frame[coord[1]:coord[3], coord[0]:coord[2]]

                value = ((coord[0]+coord[2])/2, (coord[1]+coord[3])/2)

                position_dict[key] = value

        if old_key == 'inner_clip':

            for key, coord in old_value.items():

                image = frame[coord[1]:coord[3], coord[0]:coord[2]]

                value = ((coord[0]+coord[2])/2, (coord[1]+coord[3])/2)

                position_dict[key] = value

    return position_dict, dimension_dict


# print(position_dict)
# print(dimension_dict)
