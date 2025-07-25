from collections import defaultdict

class Node:
    def __init__(self):
        self.children = defaultdict(Node)
        self.content = ""
        self.is_file = False
    
class FileSystem:
    def __init__(self):
        self.root = Node()
    
    def _traverse(self, path, create=False):
        curr = self.root
        if path == "/":
            return curr
        parts = path.strip("/").split("/")
        for name in parts:
            if name not in curr.children:
                if create:
                    curr.children[name] = Node()
                else:
                    raise FileNotFoundError(f"Path '{path}' does not exist.")
            curr = curr.children
        
        return curr
  
    def ls(self, path):
        node = self._traverse(path)
        if node.is_file:
            return [path.split("/")[-1]]
        return sorted(node.children.keys())
    
    def mkdir(self, path):
        self._traverse(path, create=True)
    
    def addContentToFile(self, filePath, content):
        node = self._traverse(filePath)
        node.is_file = True
        node.content += content
    
    def readContentFromFile(self, filePath):
        node = self._traverse(filePath)
        return node.content