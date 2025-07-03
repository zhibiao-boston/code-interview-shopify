"""
Demonstration script for the FileSystem class.

This script showcases various features and use cases of the production-level
in-memory file system implementation.
"""

from filesystem import FileSystem, FileSystemError, FileNotFoundError, DirectoryNotFoundError, InvalidPathError


def print_section(title: str) -> None:
    """Print a formatted section header."""
    print(f"\n{'=' * 60}")
    print(f" {title}")
    print('=' * 60)


def print_subsection(title: str) -> None:
    """Print a formatted subsection header."""
    print(f"\n--- {title} ---")


def demonstrate_basic_operations():
    """Demonstrate basic file system operations."""
    print_section("BASIC FILE SYSTEM OPERATIONS")
    
    fs = FileSystem()
    
    print_subsection("Initial State")
    print(f"Root directory contents: {fs.ls('/')}")
    print(f"Root exists: {fs.exists('/')}")
    print(f"Root is directory: {fs.is_directory('/')}")
    
    print_subsection("Creating Directories")
    fs.mkdir("/documents")
    fs.mkdir("/projects/python/filesystem")
    print(f"Root contents after mkdir: {fs.ls('/')}")
    print(f"Projects structure: {fs.ls('/projects')}")
    print(f"Python projects: {fs.ls('/projects/python')}")
    
    print_subsection("Creating and Writing Files")
    fs.addContentToFile("/documents/readme.txt", "Welcome to the file system!")
    fs.addContentToFile("/projects/python/filesystem/main.py", "# Main filesystem implementation\n")
    fs.addContentToFile("/projects/python/filesystem/main.py", "from filesystem import FileSystem\n")
    
    print(f"Documents: {fs.ls('/documents')}")
    print(f"Filesystem project: {fs.ls('/projects/python/filesystem')}")
    
    print_subsection("Reading File Contents")
    readme_content = fs.readContentFromFile("/documents/readme.txt")
    main_content = fs.readContentFromFile("/projects/python/filesystem/main.py")
    
    print(f"README content: '{readme_content}'")
    print(f"Main.py content:\n{main_content}")
    
    return fs


def demonstrate_requirements_example():
    """Demonstrate the exact example from the requirements."""
    print_section("REQUIREMENTS EXAMPLE")
    
    fs = FileSystem()
    
    print("Executing the exact example from requirements:")
    print("fs.mkdir('/a/b/c')")
    fs.mkdir("/a/b/c")
    
    print("fs.addContentToFile('/a/b/c/d', 'hello')")
    fs.addContentToFile("/a/b/c/d", "hello")
    
    result1 = fs.ls("/")
    print(f"fs.ls('/'): {result1}")
    
    result2 = fs.ls("/a/b/c")
    print(f"fs.ls('/a/b/c'): {result2}")
    
    content1 = fs.readContentFromFile("/a/b/c/d")
    print(f"fs.readContentFromFile('/a/b/c/d'): '{content1}'")
    
    print("fs.addContentToFile('/a/b/c/d', ' world')")
    fs.addContentToFile("/a/b/c/d", " world")
    
    content2 = fs.readContentFromFile("/a/b/c/d")
    print(f"fs.readContentFromFile('/a/b/c/d'): '{content2}'")
    
    return fs


def demonstrate_complex_scenarios():
    """Demonstrate complex file system scenarios."""
    print_section("COMPLEX SCENARIOS")
    
    fs = FileSystem()
    
    print_subsection("Building a Project Structure")
    # Create a typical software project structure
    directories = [
        "/myproject/src/main",
        "/myproject/src/test",
        "/myproject/docs",
        "/myproject/config",
        "/myproject/scripts",
        "/myproject/data/input",
        "/myproject/data/output"
    ]
    
    for directory in directories:
        fs.mkdir(directory)
        print(f"Created: {directory}")
    
    print_subsection("Adding Project Files")
    # Add various project files
    files_and_content = [
        ("/myproject/readme.md", "# My Project\n\nThis is a sample project demonstrating the file system."),
        ("/myproject/src/main/app.py", "#!/usr/bin/env python3\n\ndef main():\n    print('Hello, World!')\n\nif __name__ == '__main__':\n    main()"),
        ("/myproject/src/test/testapp.py", "import unittest\nfrom main.app import main\n\nclass TestApp(unittest.TestCase):\n    def test_main(self):\n        # Test implementation here\n        pass"),
        ("/myproject/config/settings.json", '{\n  "debug": true,\n  "version": "1.0.0"\n}'),
        ("/myproject/scripts/build.sh", "#!/bin/bash\necho 'Building project...'\npython -m pytest"),
        ("/myproject/data/input/sample.txt", "Sample input data for processing"),
        ("/myproject/docs/api.md", "# API Documentation\n\n## Functions\n\n### main()\nEntry point of the application.")
    ]
    
    for file_path, content in files_and_content:
        fs.addContentToFile(file_path, content)
        print(f"Created file: {file_path} ({len(content)} chars)")
    
    print_subsection("Exploring the Project Structure")
    print("Project root:")
    for item in fs.ls("/myproject"):
        path = f"/myproject/{item}"
        if fs.is_directory(path):
            print(f"  📁 {item}/")
        else:
            content_length = len(fs.readContentFromFile(path))
            print(f"  📄 {item} ({content_length} chars)")
    
    print("\nSource code structure:")
    for item in fs.ls("/myproject/src"):
        src_path = f"/myproject/src/{item}"
        print(f"  📁 {item}/")
        for subitem in fs.ls(src_path):
            file_path = f"{src_path}/{subitem}"
            content_length = len(fs.readContentFromFile(file_path))
            print(f"    📄 {subitem} ({content_length} chars)")
    
    print_subsection("File Content Examples")
    print("README.md content:")
    print(fs.readContentFromFile("/myproject/readme.md"))
    
    print("\nSettings.json content:")
    print(fs.readContentFromFile("/myproject/config/settings.json"))
    
    return fs


def demonstrate_file_operations():
    """Demonstrate various file operations."""
    print_section("FILE OPERATIONS")
    
    fs = FileSystem()
    
    print_subsection("Log File Simulation")
    log_file = "/var/log/application.log"
    
    # Simulate log entries being added over time
    log_entries = [
        "[2024-01-01 10:00:00] INFO: Application started",
        "[2024-01-01 10:00:01] INFO: Loading configuration",
        "[2024-01-01 10:00:02] INFO: Database connection established",
        "[2024-01-01 10:05:30] WARNING: High memory usage detected",
        "[2024-01-01 10:10:15] INFO: Processing user request",
        "[2024-01-01 10:10:16] ERROR: Failed to process request - timeout",
        "[2024-01-01 10:10:17] INFO: Retrying request",
        "[2024-01-01 10:10:18] INFO: Request processed successfully"
    ]
    
    for entry in log_entries:
        fs.addContentToFile(log_file, entry + "\n")
        print(f"Added log entry: {entry}")
    
    print(f"\nFinal log file content ({len(fs.readContentFromFile(log_file))} chars):")
    print(fs.readContentFromFile(log_file))
    
    print_subsection("Configuration File Management")
    config_file = "/etc/app.conf"
    
    # Build configuration file incrementally
    config_sections = [
        "[database]\n",
        "host=localhost\n",
        "port=5432\n",
        "name=myapp\n",
        "\n[logging]\n",
        "level=INFO\n",
        "file=/var/log/application.log\n",
        "\n[features]\n",
        "enable_cache=true\n",
        "max_connections=100\n"
    ]
    
    for section in config_sections:
        fs.addContentToFile(config_file, section)
    
    print("Configuration file content:")
    print(fs.readContentFromFile(config_file))
    
    return fs


def demonstrate_error_handling():
    """Demonstrate error handling scenarios."""
    print_section("ERROR HANDLING")
    
    fs = FileSystem()
    
    print_subsection("Path Validation Errors")
    invalid_operations = [
        ("Invalid path format", lambda: fs.ls("relative/path")),
        ("Uppercase in name", lambda: fs.mkdir("/Invalid")),
        ("Special characters", lambda: fs.addContentToFile("/file@name.txt", "content")),
        ("Empty path component", lambda: fs.mkdir("/a//b")),
    ]
    
    for description, operation in invalid_operations:
        try:
            operation()
            print(f"❌ {description}: Should have failed!")
        except InvalidPathError as e:
            print(f"✅ {description}: {e}")
        except Exception as e:
            print(f"❓ {description}: Unexpected error: {e}")
    
    print_subsection("File System State Errors")
    # Set up some initial state
    fs.mkdir("/testdir")
    fs.addContentToFile("/testfile.txt", "content")
    
    state_errors = [
        ("Read non-existent file", lambda: fs.readContentFromFile("/nonexistent.txt")),
        ("List non-existent directory", lambda: fs.ls("/nonexistent")),
        ("Write to directory", lambda: fs.addContentToFile("/testdir", "content")),
        ("Read directory as file", lambda: fs.readContentFromFile("/testdir")),
        ("Create directory over file", lambda: fs.mkdir("/testfile.txt")),
    ]
    
    for description, operation in state_errors:
        try:
            operation()
            print(f"❌ {description}: Should have failed!")
        except (FileNotFoundError, DirectoryNotFoundError, FileSystemError) as e:
            print(f"✅ {description}: {e}")
        except Exception as e:
            print(f"❓ {description}: Unexpected error: {e}")


def demonstrate_tree_visualization():
    """Demonstrate the tree structure visualization."""
    print_section("TREE STRUCTURE VISUALIZATION")
    
    fs = FileSystem()
    
    # Create a sample directory structure
    fs.mkdir("/home/user/documents/projects")
    fs.mkdir("/home/user/downloads")
    fs.mkdir("/usr/local/bin")
    fs.mkdir("/var/log")
    
    fs.addContentToFile("/home/user/documents/resume.pdf", "PDF content here")
    fs.addContentToFile("/home/user/documents/projects/todo.txt", "1. Finish filesystem\n2. Write tests\n3. Create demo")
    fs.addContentToFile("/home/user/downloads/installer.dmg", "Binary installer data")
    fs.addContentToFile("/usr/local/bin/myscript.sh", "#!/bin/bash\necho 'Hello World'")
    fs.addContentToFile("/var/log/system.log", "System log entries...")
    
    print("Complete file system tree structure:")
    print(fs.get_tree_structure())
    
    print_subsection("Subtree Visualization")
    print("User home directory structure:")
    print(fs.get_tree_structure("/home/user"))


def demonstrate_performance_scenarios():
    """Demonstrate performance with larger datasets."""
    print_section("PERFORMANCE DEMONSTRATION")
    
    fs = FileSystem()
    
    print_subsection("Creating Many Files")
    import time
    
    start_time = time.time()
    
    # Create 1000 files
    for i in range(1000):
        filename = f"/file{i:04d}.txt"
        content = f"This is file number {i} with some content to make it realistic."
        fs.addContentToFile(filename, content)
    
    creation_time = time.time() - start_time
    print(f"Created 1000 files in {creation_time:.3f} seconds")
    
    print_subsection("Directory Listing Performance")
    start_time = time.time()
    file_list = fs.ls("/")
    listing_time = time.time() - start_time
    
    print(f"Listed {len(file_list)} files in {listing_time:.3f} seconds")
    print(f"First 10 files: {file_list[:10]}")
    print(f"Last 10 files: {file_list[-10:]}")
    
    print_subsection("Deep Directory Structure")
    deep_path = "/level0"
    for i in range(1, 50):
        deep_path += f"/level{i}"
    
    start_time = time.time()
    fs.mkdir(deep_path)
    deep_creation_time = time.time() - start_time
    
    print(f"Created 50-level deep directory structure in {deep_creation_time:.3f} seconds")
    
    # Add a file at the deepest level
    deep_file = deep_path + "/deep.txt"
    fs.addContentToFile(deep_file, "Content at the deepest level!")
    
    start_time = time.time()
    content = fs.readContentFromFile(deep_file)
    deep_read_time = time.time() - start_time
    
    print(f"Read file from 50-level deep structure in {deep_read_time:.3f} seconds")
    print(f"Content: '{content}'")


def main():
    """Main demonstration function."""
    print("🗂️  FileSystem Production-Level Implementation Demo")
    print("=" * 60)
    print("This demonstration showcases a comprehensive in-memory file system")
    print("implementation with production-level features and error handling.")
    
    try:
        # Run all demonstrations
        demonstrate_basic_operations()
        demonstrate_requirements_example()
        demonstrate_complex_scenarios()
        demonstrate_file_operations()
        demonstrate_error_handling()
        demonstrate_tree_visualization()
        demonstrate_performance_scenarios()
        
        print_section("DEMONSTRATION COMPLETE")
        print("✅ All demonstrations completed successfully!")
        print("\nKey Features Demonstrated:")
        print("• Basic file and directory operations")
        print("• Nested directory creation")
        print("• File content management (create, append, read)")
        print("• Path validation and error handling")
        print("• Lexicographical sorting")
        print("• Tree structure visualization")
        print("• Performance with large datasets")
        print("• Production-level error handling")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
