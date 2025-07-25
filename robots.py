"""
Comprehensive unit tests for the FileSystem class.
"""

import unittest
import sys
import os

# Add the current directory to the path so we can import the FileSystem class
sys.path.insert(0, os.path.dirname(__file__))

from filesystem import (
    FileSystem, FileSystemNode, FileSystemError, FileNotFoundError,
    DirectoryNotFoundError, InvalidPathError
)


class TestFileSystemNode(unittest.TestCase):
    """Test cases for the FileSystemNode class."""
    
    def test_directory_node_creation(self):
        """Test creating a directory node."""
        node = FileSystemNode("test", is_file=False)
        self.assertEqual(node.name, "test")
        self.assertFalse(node.is_file)
        self.assertIsNone(node.parent)
        self.assertIsNone(node.content)
        self.assertEqual(node.children, {})
    
    def test_file_node_creation(self):
        """Test creating a file node."""
        node = FileSystemNode("test.txt", is_file=True)
        self.assertEqual(node.name, "test.txt")
        self.assertTrue(node.is_file)
        self.assertIsNone(node.parent)
        self.assertEqual(node.content, "")
        self.assertIsNone(node.children)
    
    def test_add_child_to_directory(self):
        """Test adding a child to a directory node."""
        parent = FileSystemNode("parent", is_file=False)
        child = FileSystemNode("child", is_file=False)
        
        parent.add_child(child)
        
        self.assertIn("child", parent.children)
        self.assertEqual(parent.children["child"], child)
        self.assertEqual(child.parent, parent)
    
    def test_add_child_to_file_raises_error(self):
        """Test that adding a child to a file raises an error."""
        file_node = FileSystemNode("file.txt", is_file=True)
        child = FileSystemNode("child", is_file=False)
        
        with self.assertRaises(FileSystemError):
            file_node.add_child(child)
    
    def test_add_duplicate_child_raises_error(self):
        """Test that adding a duplicate child raises an error."""
        parent = FileSystemNode("parent", is_file=False)
        child1 = FileSystemNode("child", is_file=False)
        child2 = FileSystemNode("child", is_file=False)
        
        parent.add_child(child1)
        
        with self.assertRaises(FileSystemError):
            parent.add_child(child2)
    
    def test_get_child(self):
        """Test getting a child node."""
        parent = FileSystemNode("parent", is_file=False)
        child = FileSystemNode("child", is_file=False)
        parent.add_child(child)
        
        retrieved_child = parent.get_child("child")
        self.assertEqual(retrieved_child, child)
        
        non_existent = parent.get_child("nonexistent")
        self.assertIsNone(non_existent)
    
    def test_get_child_from_file_returns_none(self):
        """Test that getting a child from a file returns None."""
        file_node = FileSystemNode("file.txt", is_file=True)
        result = file_node.get_child("anything")
        self.assertIsNone(result)
    
    def test_list_children(self):
        """Test listing children of a directory."""
        parent = FileSystemNode("parent", is_file=False)
        child1 = FileSystemNode("b", is_file=False)
        child2 = FileSystemNode("a", is_file=True)
        child3 = FileSystemNode("c", is_file=False)
        
        parent.add_child(child1)
        parent.add_child(child2)
        parent.add_child(child3)
        
        children = parent.list_children()
        self.assertEqual(children, ["a", "b", "c"])  # Should be sorted
    
    def test_list_children_from_file_returns_empty(self):
        """Test that listing children from a file returns empty list."""
        file_node = FileSystemNode("file.txt", is_file=True)
        children = file_node.list_children()
        self.assertEqual(children, [])
    
    def test_append_content_to_file(self):
        """Test appending content to a file."""
        file_node = FileSystemNode("file.txt", is_file=True)
        
        file_node.append_content("hello")
        self.assertEqual(file_node.content, "hello")
        
        file_node.append_content(" world")
        self.assertEqual(file_node.content, "hello world")
    
    def test_append_content_to_directory_raises_error(self):
        """Test that appending content to a directory raises an error."""
        dir_node = FileSystemNode("dir", is_file=False)
        
        with self.assertRaises(FileSystemError):
            dir_node.append_content("content")
    
    def test_get_content_from_file(self):
        """Test getting content from a file."""
        file_node = FileSystemNode("file.txt", is_file=True)
        file_node.append_content("test content")
        
        content = file_node.get_content()
        self.assertEqual(content, "test content")
    
    def test_get_content_from_directory_raises_error(self):
        """Test that getting content from a directory raises an error."""
        dir_node = FileSystemNode("dir", is_file=False)
        
        with self.assertRaises(FileSystemError):
            dir_node.get_content()


class TestFileSystem(unittest.TestCase):
    """Test cases for the FileSystem class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.fs = FileSystem()
    
    def test_initialization(self):
        """Test file system initialization."""
        self.assertIsNotNone(self.fs.root)
        self.assertEqual(self.fs.root.name, "/")
        self.assertFalse(self.fs.root.is_file)
    
    def test_validate_name_valid_names(self):
        """Test name validation with valid names."""
        valid_names = ["a", "test", "file.txt", "a.b.c", "abcdefghijklmnopqrstuvwxyz", "123", "file123.txt", "a1b2c3"]
        
        for name in valid_names:
            with self.subTest(name=name):
                self.assertTrue(self.fs._validate_name(name))
    
    def test_validate_name_invalid_names(self):
        """Test name validation with invalid names."""
        invalid_names = ["", "Test", "file_name", "file-name", "file name", "file@name"]
        
        for name in invalid_names:
            with self.subTest(name=name):
                self.assertFalse(self.fs._validate_name(name))
    
    def test_parse_path_valid_paths(self):
        """Test path parsing with valid paths."""
        test_cases = [
            ("/", []),
            ("/a", ["a"]),
            ("/a/b", ["a", "b"]),
            ("/a/b/c", ["a", "b", "c"]),
            ("/file.txt", ["file.txt"]),
            ("/a/file.txt", ["a", "file.txt"])
        ]
        
        for path, expected in test_cases:
            with self.subTest(path=path):
                result = self.fs._parse_path(path)
                self.assertEqual(result, expected)
    
    def test_parse_path_invalid_paths(self):
        """Test path parsing with invalid paths."""
        invalid_paths = [
            "relative/path",  # Doesn't start with /
            "/a//b",         # Empty component
            "/A",            # Uppercase letter
            "/file_name",    # Underscore
            "/file-name",    # Hyphen
            123,             # Not a string
            None             # None value
        ]
        
        for path in invalid_paths:
            with self.subTest(path=path):
                with self.assertRaises(InvalidPathError):
                    self.fs._parse_path(path)
    
    def test_ls_root_directory(self):
        """Test listing root directory when empty."""
        result = self.fs.ls("/")
        self.assertEqual(result, [])
    
    def test_ls_nonexistent_path(self):
        """Test listing a nonexistent path."""
        with self.assertRaises(DirectoryNotFoundError):
            self.fs.ls("/nonexistent")
    
    def test_mkdir_single_directory(self):
        """Test creating a single directory."""
        self.fs.mkdir("/test")
        
        result = self.fs.ls("/")
        self.assertEqual(result, ["test"])
        
        self.assertTrue(self.fs.exists("/test"))
        self.assertTrue(self.fs.is_directory("/test"))
    
    def test_mkdir_nested_directories(self):
        """Test creating nested directories."""
        self.fs.mkdir("/a/b/c")
        
        self.assertTrue(self.fs.exists("/a"))
        self.assertTrue(self.fs.exists("/a/b"))
        self.assertTrue(self.fs.exists("/a/b/c"))
        
        self.assertEqual(self.fs.ls("/"), ["a"])
        self.assertEqual(self.fs.ls("/a"), ["b"])
        self.assertEqual(self.fs.ls("/a/b"), ["c"])
    
    def test_mkdir_existing_directory(self):
        """Test creating a directory that already exists."""
        self.fs.mkdir("/test")
        # Should not raise an error
        self.fs.mkdir("/test")
        
        result = self.fs.ls("/")
        self.assertEqual(result, ["test"])
    
    def test_mkdir_invalid_path(self):
        """Test creating directory with invalid path."""
        with self.assertRaises(InvalidPathError):
            self.fs.mkdir("/Invalid")
    
    def test_addContentToFile_new_file(self):
        """Test adding content to a new file."""
        self.fs.addContentToFile("/test.txt", "hello")
        
        self.assertTrue(self.fs.exists("/test.txt"))
        self.assertTrue(self.fs.is_file("/test.txt"))
        
        content = self.fs.readContentFromFile("/test.txt")
        self.assertEqual(content, "hello")
        
        result = self.fs.ls("/")
        self.assertEqual(result, ["test.txt"])
    
    def test_addContentToFile_existing_file(self):
        """Test adding content to an existing file."""
        self.fs.addContentToFile("/test.txt", "hello")
        self.fs.addContentToFile("/test.txt", " world")
        
        content = self.fs.readContentFromFile("/test.txt")
        self.assertEqual(content, "hello world")
    
    def test_addContentToFile_with_intermediate_directories(self):
        """Test adding content to file with intermediate directories."""
        self.fs.addContentToFile("/a/b/c/file.txt", "content")
        
        self.assertTrue(self.fs.exists("/a"))
        self.assertTrue(self.fs.exists("/a/b"))
        self.assertTrue(self.fs.exists("/a/b/c"))
        self.assertTrue(self.fs.exists("/a/b/c/file.txt"))
        
        content = self.fs.readContentFromFile("/a/b/c/file.txt")
        self.assertEqual(content, "content")
    
    def test_addContentToFile_to_directory_raises_error(self):
        """Test that adding content to a directory raises an error."""
        self.fs.mkdir("/test")
        
        with self.assertRaises(FileSystemError):
            self.fs.addContentToFile("/test", "content")
    
    def test_addContentToFile_invalid_content_type(self):
        """Test adding non-string content raises error."""
        with self.assertRaises(InvalidPathError):
            self.fs.addContentToFile("/test.txt", 123)
    
    def test_readContentFromFile_existing_file(self):
        """Test reading content from an existing file."""
        self.fs.addContentToFile("/test.txt", "test content")
        
        content = self.fs.readContentFromFile("/test.txt")
        self.assertEqual(content, "test content")
    
    def test_readContentFromFile_nonexistent_file(self):
        """Test reading content from a nonexistent file."""
        with self.assertRaises(FileNotFoundError):
            self.fs.readContentFromFile("/nonexistent.txt")
    
    def test_readContentFromFile_from_directory(self):
        """Test reading content from a directory raises error."""
        self.fs.mkdir("/test")
        
        with self.assertRaises(FileSystemError):
            self.fs.readContentFromFile("/test")
    
    def test_ls_file_returns_filename(self):
        """Test that ls on a file returns the filename."""
        self.fs.addContentToFile("/test.txt", "content")
        
        result = self.fs.ls("/test.txt")
        self.assertEqual(result, ["test.txt"])
    
    def test_ls_directory_returns_sorted_contents(self):
        """Test that ls on a directory returns sorted contents."""
        self.fs.mkdir("/c")
        self.fs.mkdir("/a")
        self.fs.addContentToFile("/b.txt", "content")
        
        result = self.fs.ls("/")
        self.assertEqual(result, ["a", "b.txt", "c"])
    
    def test_exists_method(self):
        """Test the exists method."""
        self.assertFalse(self.fs.exists("/nonexistent"))
        
        self.fs.mkdir("/test")
        self.assertTrue(self.fs.exists("/test"))
        
        self.fs.addContentToFile("/file.txt", "content")
        self.assertTrue(self.fs.exists("/file.txt"))
    
    def test_is_file_method(self):
        """Test the is_file method."""
        self.fs.mkdir("/dir")
        self.fs.addContentToFile("/file.txt", "content")
        
        self.assertFalse(self.fs.is_file("/dir"))
        self.assertTrue(self.fs.is_file("/file.txt"))
        self.assertFalse(self.fs.is_file("/nonexistent"))
    
    def test_is_directory_method(self):
        """Test the is_directory method."""
        self.fs.mkdir("/dir")
        self.fs.addContentToFile("/file.txt", "content")
        
        self.assertTrue(self.fs.is_directory("/dir"))
        self.assertFalse(self.fs.is_directory("/file.txt"))
        self.assertFalse(self.fs.is_directory("/nonexistent"))
    
    def test_example_from_requirements(self):
        """Test the exact example from the requirements."""
        fs = FileSystem()
        
        fs.mkdir("/a/b/c")
        fs.addContentToFile("/a/b/c/d", "hello")
        
        self.assertEqual(fs.ls("/"), ["a"])
        self.assertEqual(fs.ls("/a/b/c"), ["d"])
        self.assertEqual(fs.readContentFromFile("/a/b/c/d"), "hello")
        
        fs.addContentToFile("/a/b/c/d", " world")
        self.assertEqual(fs.readContentFromFile("/a/b/c/d"), "hello world")
    
    def test_complex_file_system_operations(self):
        """Test complex file system operations."""
        # Create a complex directory structure
        self.fs.mkdir("/home/user/documents")
        self.fs.mkdir("/home/user/downloads")
        self.fs.mkdir("/var/log")
        
        # Add files
        self.fs.addContentToFile("/home/user/documents/readme.txt", "This is a readme file")
        self.fs.addContentToFile("/home/user/documents/config.txt", "config=value")
        self.fs.addContentToFile("/var/log/system.log", "System started")
        
        # Test directory listings
        self.assertEqual(self.fs.ls("/"), ["home", "var"])
        self.assertEqual(self.fs.ls("/home"), ["user"])
        self.assertEqual(self.fs.ls("/home/user"), ["documents", "downloads"])
        self.assertEqual(sorted(self.fs.ls("/home/user/documents")), ["config.txt", "readme.txt"])
        
        # Test file content
        self.assertEqual(self.fs.readContentFromFile("/home/user/documents/readme.txt"), "This is a readme file")
        self.assertEqual(self.fs.readContentFromFile("/var/log/system.log"), "System started")
        
        # Append to log file
        self.fs.addContentToFile("/var/log/system.log", "\nUser logged in")
        self.assertEqual(self.fs.readContentFromFile("/var/log/system.log"), "System started\nUser logged in")
    
    def test_get_tree_structure(self):
        """Test the tree structure visualization."""
        self.fs.mkdir("/a/b")
        self.fs.addContentToFile("/a/file.txt", "content")
        self.fs.addContentToFile("/a/b/nested.txt", "nested content")
        
        tree = self.fs.get_tree_structure()
        
        # Check that the tree contains expected elements
        self.assertIn("/", tree)
        self.assertIn("a/", tree)
        self.assertIn("b/", tree)
        self.assertIn("file.txt", tree)
        self.assertIn("nested.txt", tree)
    
    def test_edge_cases(self):
        """Test various edge cases."""
        # Root directory operations
        self.assertEqual(self.fs.ls("/"), [])
        self.assertTrue(self.fs.exists("/"))
        self.assertTrue(self.fs.is_directory("/"))
        self.assertFalse(self.fs.is_file("/"))
        
        # Empty content
        self.fs.addContentToFile("/empty.txt", "")
        self.assertEqual(self.fs.readContentFromFile("/empty.txt"), "")
        
        # File with periods in name
        self.fs.addContentToFile("/file.with.dots.txt", "content")
        self.assertTrue(self.fs.exists("/file.with.dots.txt"))
        self.assertEqual(self.fs.readContentFromFile("/file.with.dots.txt"), "content")


class TestFileSystemErrorHandling(unittest.TestCase):
    """Test error handling in the FileSystem class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.fs = FileSystem()
    
    def test_invalid_path_formats(self):
        """Test various invalid path formats."""
        invalid_operations = [
            lambda: self.fs.ls("relative/path"),
            lambda: self.fs.mkdir("relative/path"),
            lambda: self.fs.addContentToFile("relative/path", "content"),
            lambda: self.fs.readContentFromFile("relative/path"),
        ]
        
        for operation in invalid_operations:
            with self.subTest(operation=operation):
                with self.assertRaises(InvalidPathError):
                    operation()
    
    def test_operations_on_nonexistent_paths(self):
        """Test operations on nonexistent paths."""
        with self.assertRaises(DirectoryNotFoundError):
            self.fs.ls("/nonexistent")
        
        with self.assertRaises(FileNotFoundError):
            self.fs.readContentFromFile("/nonexistent.txt")
    
    def test_type_conflicts(self):
        """Test operations that create type conflicts."""
        # Create a file, then try to create a directory with the same name
        self.fs.addContentToFile("/test", "content")
        
        with self.assertRaises(FileSystemError):
            self.fs.mkdir("/test")
        
        # Create a directory, then try to write to it as a file
        self.fs.mkdir("/dir")
        
        with self.assertRaises(FileSystemError):
            self.fs.addContentToFile("/dir", "content")
        
        # Try to read a directory as a file
        with self.assertRaises(FileSystemError):
            self.fs.readContentFromFile("/dir")


class TestFileSystemPerformance(unittest.TestCase):
    """Performance-related tests for the FileSystem class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.fs = FileSystem()
    
    def test_large_directory_listing(self):
        """Test listing a directory with many files."""
        # Create many files
        for i in range(100):
            filename = f"file{i:03d}.txt"
            self.fs.addContentToFile(f"/{filename}", f"content {i}")
        
        # List should be sorted and contain all files
        result = self.fs.ls("/")
        self.assertEqual(len(result), 100)
        self.assertEqual(result[0], "file000.txt")
        self.assertEqual(result[-1], "file099.txt")
    
    def test_deep_directory_structure(self):
        """Test operations on deeply nested directories."""
        # Create a deep directory structure
        deep_path = "/" + "/".join([f"level{i}" for i in range(20)])
        self.fs.mkdir(deep_path)
        
        # Add a file at the deepest level
        file_path = deep_path + "/deep.txt"
        self.fs.addContentToFile(file_path, "deep content")
        
        # Verify the file exists and can be read
        self.assertTrue(self.fs.exists(file_path))
        self.assertEqual(self.fs.readContentFromFile(file_path), "deep content")
    
    def test_large_file_content(self):
        """Test handling large file content."""
        # Create a large content string
        large_content = "x" * 10000
        
        self.fs.addContentToFile("/large.txt", large_content)
        
        # Verify content is stored correctly
        retrieved_content = self.fs.readContentFromFile("/large.txt")
        self.assertEqual(len(retrieved_content), 10000)
        self.assertEqual(retrieved_content, large_content)
        
        # Append more content
        self.fs.addContentToFile("/large.txt", "y" * 5000)
        final_content = self.fs.readContentFromFile("/large.txt")
        self.assertEqual(len(final_content), 15000)


if __name__ == '__main__':
    # Run the tests with detailed output
    unittest.main(verbosity=2)
