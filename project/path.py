
def print_path(node):
    if node.father is None:
        print(node.data)
        return
    print_path(node.father)
    print(node.data)