class node:
    def __init__(self):
        self.children = [None] * 26
        self.edgeLabel = [None] * 26
        self.isEnd = False
        self.bitNumber = 0
        self.data = None
        self.leftChild = None
        self.rightChild = None


class CompressedNode:
    pass


class CompressedNode:
    # Root Node
    root = CompressedNode.CompressedNode()

    MaxBits = 10

    # Constructor
    def __init__(self):
        self.root = None

    # Function to check if empty
    def isEmpty(self):
        return self.root == None

    # Function to clear
    def makeEmpty(self):
        self.root = None
