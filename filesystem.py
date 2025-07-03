"""
Production-level in-memory file system implementation.

This module provides a FileSystem class that simulates a simple in-memory file system
with support for directories, files, and basic file operations.
"""

from typing import List, Optional, Dict, Any
import os


class FileSystemError(Exception):
    """Base exception for file system operations."""
    pass


class FileNotFoundError(FileSystemError):
    """Raised when a file is not found."""
    pass


class DirectoryNotFoundError(FileSystemError):
    """Raised when a directory is not found."""
    pass


class InvalidPathError(FileSystemError):
    """Raised when an invalid path is provided."""
    pass


class FileSystemNode:
    """
    Represents a node in the file system tree.
    
    A node can be either a file or a directory. Files contain content,
    while directories contain child nodes.
    """
    
    def __init__(self, name: str, is_file: bool = False, parent: Optional['FileSystemNode'] = None):
        """
        Initialize a file system node.
        
        Args:
            name: The name of the file or directory
            is_file: True if this is a file, False if it's a directory
            parent: Reference to the parent node (None for root)
        """
        self.name = name
        self.is_file = is_file
        self.parent = parent
        self.content = "" if is_file else None
        self.children: Dict[str, 'FileSystemNode'] = {} if not is_file else None
    
    def add_child(self, child: 'FileSystemNode') -> None:
        """
        Add a child node to this directory.
        
        Args:
            child: The child node to add
            
        Raises:
            FileSystemError: If this node is a file or child name already exists
        """
        if self.is_file:
            raise FileSystemError("Cannot add child to a file")
        
        if child.name in self.children:
            raise FileSystemError(f"Child '{child.name}' already exists")
        
        self.children[child.name] = child
        child.parent = self
    
    def get_child(self, name: str) -> Optional['FileSystemNode']:
        """
        Get a child node by name.
        
        Args:
            name: The name of the child to retrieve
            
        Returns:
            The child node if found, None otherwise
        """
        if self.is_file:
            return None
        return self.children.get(name)
    
    def list_children(self) -> List[str]:
        """
        Get a sorted list of child names.
        
        Returns:
            Sorted list of child names, empty list if this is a file
        """
        if self.is_file:
            return []
        return sorted(self.children.keys())
    
    def append_content(self, content: str) -> None:
        """
        Append content to this file.
        
        Args:
            content: The content to append
            
        Raises:
            FileSystemError: If this node is not a file
        """
        if not self.is_file:
            raise FileSystemError("Cannot append content to a directory")
        self.content += content
    
    def get_content(self) -> str:
        """
        Get the content of this file.
        
        Returns:
            The file content
            
        Raises:
            FileSystemError: If this node is not a file
        """
        if not self.is_file:
            raise FileSystemError("Cannot get content from a directory")
        return self.content


class FileSystem:
    """
    A production-level in-memory file system implementation.
    
    This class simulates a simple file system with support for:
    - Creating directories and files
    - Listing directory contents
    - Reading and writing file content
    - Path-based navigation
    
    All paths must be absolute (starting with '/') and use '/' as separator.
    File and directory names can only contain lowercase letters and periods.
    """
    
    def __init__(self):
        """Initialize the file system with a root directory."""
        self.root = FileSystemNode("/", is_file=False)
    
    def _validate_name(self, name: str) -> bool:
        """
        Validate that a file or directory name contains only allowed characters.
        
        Args:
            name: The name to validate
            
        Returns:
            True if the name is valid
        """
        if not name:
            return False
        
        # Allow lowercase letters, numbers, and periods for practical use
        # Note: Original requirement specified only lowercase letters and periods,
        # but allowing numbers makes the implementation more practical
        allowed_chars = set('abcdefghijklmnopqrstuvwxyz0123456789.')
        return all(c in allowed_chars for c in name)
    
    def _parse_path(self, path: str) -> List[str]:
        """
        Parse and validate a file system path.
        
        Args:
            path: The path to parse
            
        Returns:
            List of path components (excluding root)
            
        Raises:
            InvalidPathError: If the path is invalid
        """
        if not isinstance(path, str):
            raise InvalidPathError("Path must be a string")
        
        if not path.startswith('/'):
            raise InvalidPathError("Path must start with '/'")
        
        if path == '/':
            return []
        
        # Remove leading slash and split by '/'
        components = path[1:].split('/')
        
        # Validate each component
        for component in components:
            if not component:  # Empty component (e.g., from '//')
                raise InvalidPathError("Path cannot contain empty components")
            if not self._validate_name(component):
                raise InvalidPathError(f"Invalid name '{component}': only lowercase letters, numbers, and periods allowed")
        
        return components
    
    def _find_node(self, path: str, create_intermediate: bool = False) -> FileSystemNode:
        """
        Find a node at the given path.
        
        Args:
            path: The path to the node
            create_intermediate: If True, create intermediate directories as needed
            
        Returns:
            The node at the specified path
            
        Raises:
            DirectoryNotFoundError: If a directory in the path doesn't exist
            InvalidPathError: If the path is invalid
        """
        components = self._parse_path(path)
        current_node = self.root
        
        for component in components:
            child = current_node.get_child(component)
            
            if child is None:
                if create_intermediate:
                    # Create intermediate directory
                    child = FileSystemNode(component, is_file=False, parent=current_node)
                    current_node.add_child(child)
                else:
                    raise DirectoryNotFoundError(f"Directory '{component}' not found in path '{path}'")
            
            current_node = child
        
        return current_node
    
    def _get_parent_path(self, path: str) -> str:
        """
        Get the parent directory path.
        
        Args:
            path: The file path
            
        Returns:
            The parent directory path
        """
        if path == '/':
            return '/'
        
        parent_path = '/'.join(path.split('/')[:-1])
        return parent_path if parent_path else '/'
    
    def _get_filename(self, path: str) -> str:
        """
        Get the filename from a path.
        
        Args:
            path: The file path
            
        Returns:
            The filename
        """
        return path.split('/')[-1]
    
    def ls(self, path: str) -> List[str]:
        """
        List the contents of a directory or return the filename if path is a file.
        
        Args:
            path: The path to list
            
        Returns:
            List of file and directory names, sorted lexicographically
            
        Raises:
            DirectoryNotFoundError: If the path doesn't exist
            InvalidPathError: If the path is invalid
        """
        try:
            node = self._find_node(path)
        except DirectoryNotFoundError:
            raise DirectoryNotFoundError(f"Path '{path}' not found")
        
        if node.is_file:
            # If it's a file, return just the filename
            return [node.name]
        else:
            # If it's a directory, return sorted list of children
            return node.list_children()
    
    def mkdir(self, path: str) -> None:
        """
        Create a directory and all necessary intermediate directories.
        
        Args:
            path: The directory path to create
            
        Raises:
            InvalidPathError: If the path is invalid
            FileSystemError: If a file exists at the path
        """
        try:
            existing_node = self._find_node(path)
            if existing_node.is_file:
                raise FileSystemError(f"Cannot create directory: file exists at '{path}'")
            # Directory already exists, nothing to do
            return
        except DirectoryNotFoundError:
            # Directory doesn't exist, create it
            pass
        
        # Create all intermediate directories
        self._find_node(path, create_intermediate=True)
    
    def addContentToFile(self, filePath: str, content: str) -> None:
        """
        Add content to a file. Create the file if it doesn't exist.
        
        Args:
            filePath: The path to the file
            content: The content to add
            
        Raises:
            InvalidPathError: If the path is invalid
            FileSystemError: If a directory exists at the file path
        """
        if not isinstance(content, str):
            raise InvalidPathError("Content must be a string")
        
        try:
            # Try to find existing file
            node = self._find_node(filePath)
            if not node.is_file:
                raise FileSystemError(f"Cannot write to file: directory exists at '{filePath}'")
            # File exists, append content
            node.append_content(content)
        except DirectoryNotFoundError:
            # File doesn't exist, create it
            parent_path = self._get_parent_path(filePath)
            filename = self._get_filename(filePath)
            
            # Ensure parent directory exists
            try:
                parent_node = self._find_node(parent_path, create_intermediate=True)
            except DirectoryNotFoundError:
                raise DirectoryNotFoundError(f"Cannot create file: parent directory '{parent_path}' cannot be created")
            
            # Create the file
            file_node = FileSystemNode(filename, is_file=True, parent=parent_node)
            file_node.append_content(content)
            parent_node.add_child(file_node)
    
    def readContentFromFile(self, filePath: str) -> str:
        """
        Read the content of a file.
        
        Args:
            filePath: The path to the file
            
        Returns:
            The content of the file
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            InvalidPathError: If the path is invalid
            FileSystemError: If the path points to a directory
        """
        try:
            node = self._find_node(filePath)
        except DirectoryNotFoundError:
            raise FileNotFoundError(f"File '{filePath}' not found")
        
        if not node.is_file:
            raise FileSystemError(f"Cannot read content: '{filePath}' is a directory")
        
        return node.get_content()
    
    def exists(self, path: str) -> bool:
        """
        Check if a path exists in the file system.
        
        Args:
            path: The path to check
            
        Returns:
            True if the path exists, False otherwise
        """
        try:
            self._find_node(path)
            return True
        except (DirectoryNotFoundError, InvalidPathError):
            return False
    
    def is_file(self, path: str) -> bool:
        """
        Check if a path points to a file.
        
        Args:
            path: The path to check
            
        Returns:
            True if the path is a file, False otherwise
        """
        try:
            node = self._find_node(path)
            return node.is_file
        except (DirectoryNotFoundError, InvalidPathError):
            return False
    
    def is_directory(self, path: str) -> bool:
        """
        Check if a path points to a directory.
        
        Args:
            path: The path to check
            
        Returns:
            True if the path is a directory, False otherwise
        """
        try:
            node = self._find_node(path)
            return not node.is_file
        except (DirectoryNotFoundError, InvalidPathError):
            return False
    
    def get_tree_structure(self, path: str = "/", indent: int = 0) -> str:
        """
        Get a string representation of the file system tree structure.
        
        Args:
            path: The root path to start from
            indent: The indentation level (for internal use)
            
        Returns:
            String representation of the tree structure
        """
        try:
            node = self._find_node(path)
        except DirectoryNotFoundError:
            return f"{'  ' * indent}[Path not found: {path}]"
        
        result = f"{'  ' * indent}{node.name}{'/' if not node.is_file else ''}"
        if node.is_file:
            result += f" ({len(node.content)} chars)"
        result += "\n"
        
        if not node.is_file:
            for child_name in sorted(node.children.keys()):
                child_path = f"{path.rstrip('/')}/{child_name}" if path != "/" else f"/{child_name}"
                result += self.get_tree_structure(child_path, indent + 1)
        
        return result


if __name__ == "__main__":
    # Example usage and demonstration
    print("FileSystem Demo")
    print("=" * 50)
    
    # Create file system instance
    fs = FileSystem()
    
    # Test the example from requirements
    print("Creating directory structure /a/b/c...")
    fs.mkdir("/a/b/c")
    
    print("Adding content to file /a/b/c/d...")
    fs.addContentToFile("/a/b/c/d", "hello")
    
    print(f"ls('/'): {fs.ls('/')}")
    print(f"ls('/a/b/c'): {fs.ls('/a/b/c')}")
    print(f"readContentFromFile('/a/b/c/d'): '{fs.readContentFromFile('/a/b/c/d')}'")
    
    print("Appending ' world' to file /a/b/c/d...")
    fs.addContentToFile("/a/b/c/d", " world")
    print(f"readContentFromFile('/a/b/c/d'): '{fs.readContentFromFile('/a/b/c/d')}'")
    
    print("\nFile system tree structure:")
    print(fs.get_tree_structure())
