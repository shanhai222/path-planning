import Node
import gol
import road_id_hash
import path
import pickle

#A* 算法
class A_star:
    def __init__(self, startNode, endNode):
        # 开放列表
        self.openList = []
        # 封闭列表
        self.closeList = []
        # 起点
        self.startNode = startNode
        # 终点
        self.endNode = endNode
        # 当前处理的节点
        self.currentNode = startNode
        # step步
        #self.step = 0
        # 找到路径
        # self.find_way = []

        return

    """
    获得openlist中F值最小的节点
    """
    def getMinFNode(self):
        nodeTemp = self.openList[0]
        for node in self.openList:
            if node.getF() < nodeTemp.getF():
                nodeTemp = node
        return nodeTemp

    def nodeInOpenlist(self, node):
        for nodeTmp in self.openList:
            if nodeTmp.data == node.data:
                return True
        return False

    def nodeInCloselist(self, node):
        for nodeTmp in self.closeList:
            if nodeTmp.data == node.data:
                return True
        return False

    def currentNodeIsEndNode(self):
        if self.currentNode.data == self.endNode.data:
            return True
        else:
            return False

    """
    搜索一个节点
    """
    def searchOneNode(self, node):
        # id = gol.get_value('road_id')
        time = gol.get_value('time_after')
        # 忽略封闭列表
        if self.nodeInCloselist(node):
            return

        # 如果不在openList中，就加入openlist
        if self.nodeInOpenlist(node) == False:
            node.father = self.currentNode
            node.setG()  #计算G值
            node.setH(self.endNode)  #计算H值
            self.openList.append(node)
        # 如果在openList中，判断currentNode到当前点的G是否更小
        # 如果更小，就重新计算g值，并且改变father
        else:
            # self_ind = id.index(node.data)
            self_ind = node.index
            time_node = time[self_ind][0]
            if self.currentNode.g + time_node < node.g:
                node.g = self.currentNode.g + time_node
                node.father = self.currentNode

        return

    """
    搜索下一个可以变化到的状态，即邻接矩阵不为0的位置
    """
    def searchNear(self):
        #id = gol.get_value('road_id')
        adj_matrix = gol.get_value('adj_matrix')
        num_nodes = adj_matrix.shape[0]
        road_next = []  # 从当前路段可到达的所有路段id
        # ind = id.index(self.currentNode.data)
        ind = self.currentNode.index

        for i in range(num_nodes):
            if adj_matrix[ind][i] != 0:
                # road_id = road_id_hash.id_hash(i)
                road_id = road_id_hash.get_id(i)
                road_next.append(road_id)

        for road in road_next:
            self.searchOneNode(Node.Node(road))

        return

    """
    寻路
    """
    def start(self):
        self.startNode.setH(self.endNode)  # 计算初始节点的h值
        self.startNode.setG()  # 计算初始节点的g值
        self.openList.append(self.startNode)  # 将初始节点加入开放列表

        while len(self.openList) != 0:
            # 获取当前开放列表里F值最小的节点
            self.currentNode = self.getMinFNode()
            # self.find_way.append(self.currentNode.data)
            #self.find_way.append(self.currentNode)
            if self.currentNodeIsEndNode():
                return True
            else:
                self.closeList.append(self.currentNode)
                self.openList.remove(self.currentNode)
                self.searchNear()

        #path = road_id_hash.transfer_path_to_road_id(self.find_way)  # 将node转化为road_id组成的path
        #gol.set_value('find_way', path)

    def path(self):
        path.save_path_contrast(self.currentNode)

    def next_close_list(self):
        cl = []
        return path.close_list(self.currentNode.father, cl)
