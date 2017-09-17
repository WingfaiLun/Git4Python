# Created by Tony HAO, th2510@columbia.edu


# combine two dicts into one (former) and add value together
def Combine_dicts_number(main_dict, less_dict):
    for key, value in less_dict.iteritems():
        if key in main_dict:
            main_dict[key] = float(main_dict[key]) + value
        else:
            main_dict[key] = value
    return main_dict


# combine two dicts into one (former) and add value together
def Combine_dicts_string(main_dict, less_dict, separator):
    for key, value in less_dict.iteritems():
        if key in main_dict:
            main_dict[key] = str(main_dict[key]) + separator + value
        else:
            main_dict[key] = value
    return main_dict     