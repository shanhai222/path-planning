import Node
import gol
import road_id_hash

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
        self.find_way = []

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
        id = gol.get_value('road_id')
        time = gol.get_value('time_after')
        # 忽略封闭列表
        if self.nodeInCloselist(node):
            return

        # 如果不在openList中，就加入openlist
        if self.nodeInOpenlist(node) == False:
            node.setG(self.find_way)  #计算G值
            node.setH(self.endNode)  #计算H值
            self.openList.append(node)
            node.father = self.currentNode
        # 如果在openList中，判断currentNode到当前点的G是否更小
        # 如果更小，就重新计算g值，并且改变father
        else:
            self_ind = id.index(node.data)
            time_node = time[self_ind][1]
            if self.currentNode.g + time_node < node.g:
                node.g = self.currentNode.g + time_node
                node.father = self.currentNode

        return

    """
    搜索下一个可以变化到的状态，即邻接矩阵不为0的位置
    """
    def searchNear(self):
        id = gol.get_value('road_id')
        adj_matrix = gol.get_value('adj_matrix')
        road_next = []  # 从当前路段可到达的所有路段id
        ind = id.index(self.currentNode.data)
        for i in range(1448):
            if adj_matrix[ind][i] != 0:
                road_id = road_id_hash.id_hash(i)
                road_next.append(road_id)

        for road in road_next:
            self.searchOneNode(Node.Node(road))

        return

    """
    寻路
    """
    def start(self):
        self.startNode.setH(self.endNode)  # 计算初始节点的h值
        self.startNode.setG(self.find_way)  # 计算初始节点的g值
        self.openList.append(self.startNode)  # 将初始节点加入开放列表

        while len(self.openList) != 0:
            # 获取当前开放列表里F值最小的节点
            self.currentNode = self.getMinFNode()
            self.find_way.append(self.currentNode.data)
            if self.currentNodeIsEndNode():
                self.find_way.append(self.currentNode)
            else:
                self.closeList.append(self.currentNode)
                self.openList.remove(self.currentNode)
                #self.step = self.currentNode.getG()
                self.searchNear()
        gol.set_value('find_way', self.find_way)

        return True