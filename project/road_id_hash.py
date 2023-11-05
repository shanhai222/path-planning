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