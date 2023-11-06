import gol

# 把数组index转换为真实的id
def id_hash(ind):
    road_id = gol.get_value('road_id')
    for i in range(1448):
        if i == ind:
            return road_id[i]

# 把真实id转换为index
def ind_hash(_id):
    road_id = gol.get_value('road_id')
    for i in range(1448):
        if road_id[i] == _id:
            return i


# 将路段id映射index为一个字典
def road_id_map(road_id):
    road_id_mapping = {}
    for index, real_id in enumerate(road_id):
        road_id_mapping[real_id] = index
    return road_id_mapping


# id_map_index
def get_index(_id):
    road_id_mapping = gol.get_value('road_id_mapping')
    return road_id_mapping[_id]


# index_map_id:
def get_id(index):
    road_id = gol.get_value('road_id')
    return road_id[index]


# path(Nodes -> road_ids)
def transfer_path_to_road_id(find_ways):
    path = []
    for node in find_ways:
        path.append(node.data)
    return path
