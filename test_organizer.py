#!/usr/bin/env python3
"""
Test script for the Code File Organizer
This script creates a temporary test directory with various file types,
then runs the organizer on it and verifies the results.

Copyright (c) 2023 Mahmoud Ashraf (SNO7E)
"""
import os
import shutil
import tempfile
import unittest
import subprocess
import sys
import json
from pathlib import Path

class TestFileOrganizer(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        
        # Create some test files with different extensions
        self.create_test_files()
        
    def tearDown(self):
        # Clean up the temporary directory
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir)
        
    def create_test_files(self):
        """Create test files with different extensions"""
        # Create files at root level
        open(os.path.join(self.test_dir, "script.py"), "w").write("print('Hello, World!')")
        open(os.path.join(self.test_dir, "index.html"), "w").write("<html><body>Hello</body></html>")
        open(os.path.join(self.test_dir, "styles.css"), "w").write("body { color: black; }")
        open(os.path.join(self.test_dir, "data.json"), "w").write('{"key": "value"}')
        open(os.path.join(self.test_dir, "readme.md"), "w").write("# Test Project")
        
        # Create a subdirectory with files
        sub_dir = os.path.join(self.test_dir, "src")
        os.makedirs(sub_dir, exist_ok=True)
        open(os.path.join(sub_dir, "app.js"), "w").write("console.log('Hello');")
        open(os.path.join(sub_dir, "utils.py"), "w").write("def hello(): return 'Hello'")
        
        # Create another subdirectory with more files
        sub_dir2 = os.path.join(self.test_dir, "docs")
        os.makedirs(sub_dir2, exist_ok=True)
        open(os.path.join(sub_dir2, "guide.md"), "w").write("# User Guide")
        open(os.path.join(sub_dir2, "config.json"), "w").write('{"debug": true}')
        
        # Create files for smart detection testing
        self.create_smart_detection_test_files()
    
    def create_smart_detection_test_files(self):
        """Create files that can be detected by content analysis"""
        # React component with js extension
        react_dir = os.path.join(self.test_dir, "components")
        os.makedirs(react_dir, exist_ok=True)
        react_content = """
import React from 'react';

const Button = ({ onClick, text }) => {
  return (
    <button className="btn" onClick={onClick}>
      {text}
    </button>
  );
};

export default Button;
"""
        open(os.path.join(react_dir, "Button.js"), "w").write(react_content)
        
        # Config file
        config_content = """
# App configuration
DEBUG=true
API_URL=https://api.example.com
SECRET_KEY=abcdef123456
"""
        open(os.path.join(self.test_dir, "app.config"), "w").write(config_content)
        
        # Script with shebang
        script_content = """#!/usr/bin/env python3
import sys
print(f"Arguments: {sys.argv}")
"""
        open(os.path.join(self.test_dir, "run.sh"), "w").write(script_content)
        
        # SQL file
        sql_content = """
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE
);

INSERT INTO users (name, email) VALUES ('John Doe', 'john@example.com');
"""
        open(os.path.join(self.test_dir, "database.txt"), "w").write(sql_content)
        
        # Duplicate files for testing
        duplicate_content = "This is a duplicate file for testing purposes."
        open(os.path.join(self.test_dir, "original.txt"), "w").write(duplicate_content)
        open(os.path.join(self.test_dir, "copy.txt"), "w").write(duplicate_content)
    
    def test_organizer_standard_mode(self):
        """Test the organizer in standard mode"""
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "file_organizer.py")
        
        # Run the organizer on the test directory
        subprocess.run([sys.executable, script_path, self.test_dir], check=True)
        
        # Verify the files have been organized correctly
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "Python", "script.py")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "Python", "utils.py")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "Web", "HTML", "index.html")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "Web", "CSS", "styles.css")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "Web", "JavaScript", "app.js")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "Data", "JSON", "data.json")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "Data", "JSON", "config.json")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "Documentation", "Markdown", "readme.md")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "Documentation", "Markdown", "guide.md")))

    def test_organizer_project_mode(self):
        """Test the organizer in project mode"""
        # First, restore the original structure
        self.tearDown()
        self.setUp()
        
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "file_organizer.py")
        
        # Run the organizer on the test directory with project mode
        subprocess.run([sys.executable, script_path, self.test_dir, "--project-mode"], check=True)
        
        # Verify the files have been organized while maintaining project structure
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "Python", "script.py")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "src", "Python", "utils.py")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "Web", "HTML", "index.html")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "Web", "CSS", "styles.css")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "src", "Web", "JavaScript", "app.js")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "Data", "JSON", "data.json")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "docs", "Data", "JSON", "config.json")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "Documentation", "Markdown", "readme.md")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "docs", "Documentation", "Markdown", "guide.md")))
    
    def test_smart_detection(self):
        """Test the smart detection features"""
        # First, restore the original structure
        self.tearDown()
        self.setUp()
        
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "file_organizer.py")
        report_file = os.path.join(self.test_dir, "report.json")
        
        # Run the organizer with a report
        subprocess.run([
            sys.executable, 
            script_path, 
            self.test_dir, 
            "--report", 
            "--report-file", 
            report_file
        ], check=True)
        
        # Check smart detection results
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "Web", "React", "Button.js")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "Config", "General", "app.config")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "Python", "Scripts", "run.sh")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "Database", "SQL", "database.txt")))
        
        # Check if report file was created
        self.assertTrue(os.path.exists(report_file))
        
        # Load and verify report contents
        with open(report_file, 'r') as f:
            report = json.load(f)
            self.assertIn('statistics', report)
            self.assertIn('version', report)
            
        # Test duplicate file detection (should be in the report)
        self.assertIn('duplicate_files', report['statistics'])

if __name__ == "__main__":
    unittest.main() 