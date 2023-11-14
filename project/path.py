import pickle

def close_list(node, cl):
    if node.father is None:
        cl.append(node)
        return cl

    cl = close_list(node.father, cl)
    cl.append(node)

    return cl


def save_path(node):
    path = list()
    while node.father is not None:
        path.insert(0, node.data)
        node = node.father
    path.insert(0, node.data)
    with open('./result/path.pkl', 'ab') as file:
        pickle.dump(path, file)
    file.close()


def save_path_contrast(node):
    path = list()
    while node.father is not None:
        path.insert(0, node.data)
        node = node.father
    path.insert(0, node.data)
    with open('./result/path_contrast.pkl', 'wb') as file:
        pickle.dump(path, file)
    file.close()