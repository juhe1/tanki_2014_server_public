# key=rank_index, value max_range_length
rank_to_range = {
    0:5,
    1:5,
    2:5,
    3:5,
    4:6,
    5:6,
    6:6,
    7:7,
    8:7,
    9:8,
    10:8,
    11:8,
    12:9,
    13:9,
    14:10,
    15:10,
    16:10,
    17:10,
    18:10,
    19:11,
    20:11,
    21:11,
    22:11,
    23:11,
    24:11,
    25:12,
    26:13,
    27:14,
    28:15,
    29:16,
}

def get_range_by_rank_index(rank_index):
    return rank_to_range[rank_index]
