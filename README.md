# File system design task with python
Suppose you are the expert in designing real-world file system with python, please provide a production level, clean python code with comments if need

## Design and implement a class called FileSystem that simulates a simple in-memory file system.
Your class should support the following methods:
class FileSystem:

    def __init__(self):
        pass

    def ls(self, path: str) -> List[str]:
        pass

    def mkdir(self, path: str) -> None:
        pass

    def addContentToFile(self, filePath: str, content: str) -> None:
        pass

    def readContentFromFile(self, filePath: str) -> str:
        pass

## Functionality Requirements：
1, Initialization:
Create an empty file system with only a root directory "/".

2, ls(path):
If path is a file path, return a list containing only the file's name.
If path is a directory path, return the list of file and directory names inside that directory, sorted in lexicographical order.

3, mkdir(path):
Creates a directory and all intermediate-level directories needed to contain it.

4, addContentToFile(filePath, content):
If the file does not exist, create it and write the content.
If the file exists, append the content to the existing content.

5, readContentFromFile(filePath):
Returns the current content of the file at filePath.

## Constraints:
Path components are separated by slashes ("/") and always start with a slash.
File and directory names contain only lowercase letters and periods (a-z, .).
No duplicate file or directory names at the same path level.
Lexicographical sorting is required for ls.

## Example Usage:
fs = FileSystem()

fs.mkdir("/a/b/c")
fs.addContentToFile("/a/b/c/d", "hello")
fs.ls("/")             # Returns ["a"]
fs.ls("/a/b/c")        # Returns ["d"]
fs.readContentFromFile("/a/b/c/d")  # Returns "hello"
fs.addContentToFile("/a/b/c/d", " world")
fs.readContentFromFile("/a/b/c/d")  # Returns "hello world"