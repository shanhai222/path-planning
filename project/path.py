import pickle


def print_path(node):
    if node.father is None:
        print(node.data)
        return
    print_path(node.father)
    print(node.data)


def save_path(node):
    path = list()
    while node.father is not None:
        path.insert(0, node.data)
        node = node.father
    path.insert(0, node.data)
    # print(path)
    with open('./result/path.pkl', 'wb') as file:
        pickle.dump(path, file)
    file.close()

