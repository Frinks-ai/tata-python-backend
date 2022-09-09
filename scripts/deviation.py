ground_truth_dimension={'central_hub0': 108, 'rivet_inner0': 38, 'rivet_inner1': 37, 'rivet_inner2': 37, 'rivet_inner3': 36, 'stop_pin0': 26, 'stop_pin1': 24, 'stop_pin2': 25, 'stop_pin3': 26, 'stop_pin4': 26, 'stop_pin5': 26, 'rivet_top0': 36, 'rivet_top1': 34, 'rivet_top2': 33, 'rivet_top3': 34, 'rivet_top4': 32, 'rivet_top5': 32}

ground_truth_position={'torsion_spring0': 400.6607043372235, 'torsion_spring1': 408.17643244067875, 'torsion_spring2': 406.31514862234707, 'torsion_spring3': 404.2091043012267, 'central_hub0': 0.0, 'rivet_bottom0': 733.1275468838966, 'rivet_bottom1': 738.0819737671419, 'rivet_bottom2': 740.0177362739355, 'rivet_bottom3': 736.7472429537826, 'rivet_bottom4': 733.2751870887219, 'rivet_bottom5': 731.7598649830421, 'outer_clip0': 304.5591075637043, 'outer_clip1': 311.6492419371496, 'outer_clip2': 308.50607773591753, 'outer_clip3': 303.19342011329996, 'rivet_inner0': 483.66930851564274, 'rivet_inner1': 485.7869903568847, 'rivet_inner2': 482.2468247692254, 'rivet_inner3': 480.13019067748695, 'stop_pin0': 427.68680129272167, 'stop_pin1': 509.5223253204907, 'stop_pin2': 510.0686228342222, 'stop_pin3': 429.3401914566117, 'stop_pin4': 506.7247773693329, 'stop_pin5': 507.5598486878173, 'rivet_top0': 729.6471750099496, 'rivet_top1': 732.0382503667414, 'rivet_top2': 731.3015793774823, 'rivet_top3': 728.972564641496, 'rivet_top4': 728.5615965723146, 'rivet_top5': 726.3642337009718, 'inner_clip0': 205.67024578193121, 'inner_clip1': 215.85701285804916, 'inner_clip2': 215.64090521049107, 'inner_clip3': 210.15767889848803}



def dimension_deviation(dimension_dict):

    dimension_dev={}

    for key,value in dimension_dict.items():

        if key in ground_truth_dimension.keys():
            
            dimension_dev[key]=(abs((ground_truth_dimension[key])-(dimension_dict[key])))/12

        else:
            print(f"{key}--- not present")

    return dimension_dev


def position_deviation(position_dict):

    position_dev={}


    for key,value in position_dict.items():

        if key in ground_truth_position.keys():

            if key=='stop_pin0' or key=='stop_pin1' or key=='stop_pin2' or key=='stop_pin3' or key=='stop_pin4' or key=='stop_pin5' or key=='stop_pin6':

                if value<480:
                    position_dev[key]=(abs((428)-(position_dict[key])))/12

                elif value>480:
                    position_dev[key]=(abs((508)-(position_dict[key])))/12

            else:
                position_dev[key]=(abs((ground_truth_position[key])-(position_dict[key])))/12

        else:
            print(f"{key}--- has 0 dimension")
            
    return position_dev


def part_absent(position_dict):

    parts_absent=[k for k,v in ground_truth_position.items() if k not in position_dict]

    return parts_absent



def anomalies(dimension_dict,position_dict):

    dimension_dev=dimension_deviation(dimension_dict)
    position_dev=position_deviation(position_dict)
    parts_absent=part_absent(position_dict)

    return dimension_dev, position_dev,parts_absent



