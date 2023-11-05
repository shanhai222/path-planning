import gol
import road_id_hash

# 描述A*算法中的结点数据(当前数据，父节点，步数）
class Node:
    def __init__(self, data, step=0, h=0):
        self.data = data
        self.father = None # 父节点
        self.g = step  # g值
        self.h = h  # h值

    # 启发函数（出发地和目的地之间的距离）
    def setH(self, goal):
        id = gol.get_value('road_id')
        dis = gol.get_value('road_dis')
        startnode = id.index(self.data)
        endnode = id.index(goal.data)
        self.h = dis[startnode][endnode]

    # 实际代价（时间）
    def setG(self, find_ways):
        id = gol.get_value('road_id')
        time = gol.get_value('time_after')
        for i in find_ways:
            ind = id.index(i)
            self.g += time[ind][1]
        self_ind = id.index(self.data)
        self.g += time[self_ind][1]

    def setFather(self, node):
        self.father = node

    def getG(self):
        return self.g

    def getF(self):
        return self.g + self.h