#!/usr/bin/env python3
"""
Code File Organizer - A smart tool that automatically organizes code files into directories
based on file type, project structure, and content analysis.

Copyright (c) 2023 Mahmoud Ashraf (SNO7E)
"""
import os
import shutil
import json
import argparse
from pathlib import Path
import logging
import re
import hashlib
import datetime
import collections
import subprocess
from typing import Dict, List, Optional, Set, Tuple, Counter, Any
import time
import fnmatch
import sys

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("FileOrganizer")

# Version information
__version__ = "1.0.0"
__author__ = "Mahmoud Ashraf (SNO7E)"
__license__ = "MIT"

# File type to folder mappings
DEFAULT_MAPPINGS = {
    # Web Development
    "html": "Web/HTML",
    "htm": "Web/HTML",
    "css": "Web/CSS",
    "scss": "Web/CSS",
    "sass": "Web/CSS",
    "less": "Web/CSS",
    "js": "Web/JavaScript",
    "jsx": "Web/React",
    "ts": "Web/TypeScript",
    "tsx": "Web/React",
    "php": "Web/PHP",
    
    # Programming Languages
    "py": "Python",
    "java": "Java",
    "c": "C",
    "cpp": "C++",
    "cs": "CSharp",
    "go": "Go",
    "rs": "Rust",
    "rb": "Ruby",
    "swift": "Swift",
    "kt": "Kotlin",
    
    # Data
    "json": "Data/JSON",
    "xml": "Data/XML",
    "yaml": "Data/YAML",
    "yml": "Data/YAML",
    "csv": "Data/CSV",
    "xls": "Data/Excel",
    "xlsx": "Data/Excel",
    
    # Documentation
    "md": "Documentation/Markdown",
    "txt": "Documentation/Text",
    "pdf": "Documentation/PDF",
    "docx": "Documentation/Word",
    "doc": "Documentation/Word",
    
    # Config
    "ini": "Config",
    "cfg": "Config",
    "conf": "Config",
    "env": "Config",
    "toml": "Config",
    
    # Images
    "jpg": "Media/Images",
    "jpeg": "Media/Images",
    "png": "Media/Images",
    "gif": "Media/Images",
    "svg": "Media/Images",
    "webp": "Media/Images",
    
    # Other
    "sh": "Scripts/Shell",
    "bash": "Scripts/Shell",
    "bat": "Scripts/Batch",
    "ps1": "Scripts/PowerShell",
    "sql": "Database/SQL",
}

class FileOrganizer:
    def __init__(
        self, 
        source_dir: str, 
        target_dir: Optional[str] = None,
        mappings: Optional[Dict[str, str]] = None,
        project_mode: bool = False,
        exclude_dirs: Optional[List[str]] = None,
        exclude_files: Optional[List[str]] = None,
        dry_run: bool = False
    ):
        self.source_dir = os.path.abspath(source_dir)
        self.target_dir = os.path.abspath(target_dir) if target_dir else self.source_dir
        self.mappings = mappings or DEFAULT_MAPPINGS
        self.project_mode = project_mode
        self.exclude_dirs = exclude_dirs or ['.git', '.vscode', 'node_modules', 'venv', 'env', '__pycache__']
        self.exclude_files = exclude_files or ['file_organizer.py', 'file_organizer_config.json']
        self.dry_run = dry_run
        
        # Stats
        self.stats = {
            "total_files": 0,
            "organized_files": 0,
            "skipped_files": 0,
            "unknown_extensions": set()
        }
    
    def should_exclude(self, path: str) -> bool:
        """Check if a file or directory should be excluded from organization."""
        file_name = os.path.basename(path)
        
        # Check if it's in the exclude list
        if file_name in self.exclude_files:
            return True
            
        # Check if it's a parent directory in exclude list
        for excluded_dir in self.exclude_dirs:
            if excluded_dir in path.split(os.sep):
                return True
                
        return False
    
    def get_target_path(self, file_path: str) -> Optional[str]:
        """Determine the target path for a file based on its extension."""
        # Get the file extension (without the dot)
        _, ext = os.path.splitext(file_path)
        ext = ext[1:].lower() if ext else ""
        
        if not ext:
            return None
            
        if ext in self.mappings:
            # If using project mode, keep the relative path structure
            if self.project_mode:
                rel_path = os.path.relpath(os.path.dirname(file_path), self.source_dir)
                if rel_path == ".":
                    rel_path = ""
                target_subdir = os.path.join(self.target_dir, rel_path, self.mappings[ext])
            else:
                target_subdir = os.path.join(self.target_dir, self.mappings[ext])
                
            return os.path.join(target_subdir, os.path.basename(file_path))
        
        self.stats["unknown_extensions"].add(ext)
        return None
    
    def organize_files(self):
        """Walk through the directory and organize files."""
        logger.info(f"Starting file organization from {self.source_dir} to {self.target_dir}")
        logger.info(f"Dry run: {self.dry_run}")
        
        # Detect project structure before organizing
        self.detect_project_structure()
        
        # Detect duplicate files
        self.duplicate_files = self.find_duplicate_files() if not self.dry_run else {}
        
        start_time = time.time()
        for root, dirs, files in os.walk(self.source_dir, topdown=True):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if not self.should_exclude(os.path.join(root, d))]
            
            for file in files:
                self.stats["total_files"] += 1
                file_path = os.path.join(root, file)
                
                # Skip excluded files
                if self.should_exclude(file_path):
                    logger.debug(f"Skipping excluded file: {file_path}")
                    self.stats["skipped_files"] += 1
                    continue
                
                # Check if file is a duplicate
                file_hash = self.get_file_hash(file_path) if not self.dry_run else None
                if file_hash and file_hash in self.duplicate_files and len(self.duplicate_files[file_hash]) > 1:
                    self.stats.setdefault("duplicate_files", 0)
                    self.stats["duplicate_files"] += 1
                    
                # Try smart categorization first
                target_path = self.smart_categorize_file(file_path)
                
                # Fall back to extension-based categorization
                if not target_path:
                    target_path = self.get_target_path(file_path)
                
                if not target_path:
                    logger.debug(f"No mapping found for file: {file_path}")
                    self.stats["skipped_files"] += 1
                    continue
                
                # Skip if source and destination are the same
                if os.path.normpath(file_path) == os.path.normpath(target_path):
                    logger.debug(f"Source and destination are the same: {file_path}")
                    self.stats["skipped_files"] += 1
                    continue
                
                # Create target directory if it doesn't exist
                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                
                # Move the file
                if not self.dry_run:
                    try:
                        shutil.move(file_path, target_path)
                        logger.info(f"Moved: {file_path} -> {target_path}")
                        self.stats["organized_files"] += 1
                    except Exception as e:
                        logger.error(f"Error moving {file_path}: {e}")
                        self.stats["skipped_files"] += 1
                else:
                    logger.info(f"Would move: {file_path} -> {target_path}")
                    self.stats["organized_files"] += 1
        
        # Calculate execution time
        self.stats["execution_time"] = time.time() - start_time
    
    def get_file_hash(self, file_path: str, block_size: int = 65536) -> str:
        """Generate a hash for a file to identify duplicates."""
        hasher = hashlib.md5()
        with open(file_path, 'rb') as f:
            for block in iter(lambda: f.read(block_size), b''):
                hasher.update(block)
        return hasher.hexdigest()
    
    def find_duplicate_files(self) -> Dict[str, List[str]]:
        """Find duplicate files in the source directory."""
        logger.info("Scanning for duplicate files...")
        duplicate_map = collections.defaultdict(list)
        
        for root, _, files in os.walk(self.source_dir):
            for filename in files:
                file_path = os.path.join(root, filename)
                if not self.should_exclude(file_path):
                    try:
                        file_hash = self.get_file_hash(file_path)
                        duplicate_map[file_hash].append(file_path)
                    except (IOError, OSError) as e:
                        logger.error(f"Error hashing file {file_path}: {e}")
        
        # Filter out files that don't have duplicates
        return {k: v for k, v in duplicate_map.items() if len(v) > 1}
    
    def detect_project_structure(self) -> None:
        """
        Detect the project structure to improve organization.
        Looks for common project files like package.json, requirements.txt, etc.
        """
        logger.info("Detecting project structure...")
        
        # Check if this is a git repository
        is_git_repo = self.check_git_repo(self.source_dir)
        if is_git_repo:
            logger.info("Git repository detected")
            self.stats["project_type"] = "git_repository"
        
        # Web project detection
        if os.path.exists(os.path.join(self.source_dir, 'package.json')):
            logger.info("Node.js project detected")
            self.stats["project_type"] = "nodejs"
            # Load package.json to get more project info
            try:
                with open(os.path.join(self.source_dir, 'package.json'), 'r') as f:
                    package_data = json.load(f)
                    self.stats["project_name"] = package_data.get('name', 'unknown')
                    self.stats["project_version"] = package_data.get('version', 'unknown')
            except (json.JSONDecodeError, IOError) as e:
                logger.error(f"Error reading package.json: {e}")
        
        # Python project detection
        if os.path.exists(os.path.join(self.source_dir, 'requirements.txt')) or \
           os.path.exists(os.path.join(self.source_dir, 'setup.py')):
            logger.info("Python project detected")
            self.stats["project_type"] = "python"
        
        # Other projects can be detected similarly
    
    def smart_categorize_file(self, file_path: str) -> Optional[str]:
        """
        Intelligently categorize a file based on its content and naming patterns.
        Returns the target path or None if no smart categorization is possible.
        """
        filename = os.path.basename(file_path)
        
        # Check for config files first
        if self.is_config_file(filename):
            target_subdir = os.path.join(self.target_dir, "Config", self.get_config_type(filename))
            return os.path.join(target_subdir, filename)
        
        # Try to analyze content for files that aren't too large
        file_size = os.path.getsize(file_path)
        if file_size < 500 * 1024:  # Skip files larger than 500KB
            try:
                file_type = self.detect_file_type_from_content(file_path)
                if file_type:
                    if self.project_mode:
                        rel_path = os.path.relpath(os.path.dirname(file_path), self.source_dir)
                        if rel_path == ".":
                            rel_path = ""
                        target_subdir = os.path.join(self.target_dir, rel_path, file_type)
                    else:
                        target_subdir = os.path.join(self.target_dir, file_type)
                        
                    return os.path.join(target_subdir, filename)
            except (IOError, UnicodeDecodeError) as e:
                logger.debug(f"Could not analyze content of {file_path}: {e}")
        
        return None
    
    def is_config_file(self, filename: str) -> bool:
        """Detect if a file is a configuration file based on its name."""
        config_patterns = [
            r'\.config(\.\w+)?$',
            r'\.conf$',
            r'\.ini$',
            r'\.env(\.\w+)?$',
            r'config\.\w+$',
            r'\.ya?ml$',
            r'\.toml$',
            r'settings\.\w+$',
        ]
        
        return any(re.search(pattern, filename, re.IGNORECASE) for pattern in config_patterns)
    
    def get_config_type(self, filename: str) -> str:
        """Determine the type of configuration file."""
        if re.search(r'\.ya?ml$', filename, re.IGNORECASE):
            return "YAML"
        elif re.search(r'\.toml$', filename, re.IGNORECASE):
            return "TOML"
        elif re.search(r'\.json$', filename, re.IGNORECASE):
            return "JSON"
        elif re.search(r'\.env', filename, re.IGNORECASE):
            return "Environment"
        elif re.search(r'\.ini$', filename, re.IGNORECASE):
            return "INI"
        else:
            return "General"
    
    def detect_file_type_from_content(self, file_path: str) -> Optional[str]:
        """Analyze file content to determine its type."""
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        # Special handling for scripts
        if ext in ['.py', '.js', '.sh', '.bash', '.pl', '.rb']:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    first_line = f.readline().strip()
                    
                    # Look for shebang
                    if first_line.startswith('#!'):
                        if 'python' in first_line:
                            return "Python/Scripts"
                        elif 'node' in first_line:
                            return "Web/JavaScript/Scripts"
                        elif any(shell in first_line for shell in ['bash', 'sh', 'zsh']):
                            return "Scripts/Shell"
                        elif 'ruby' in first_line:
                            return "Ruby/Scripts"
                        elif 'perl' in first_line:
                            return "Perl/Scripts"
            except UnicodeDecodeError:
                pass  # Not a text file
        
        # Try to identify based on common content patterns
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read(4096)  # Read the first 4KB
                
                # HTML detection
                if re.search(r'<!DOCTYPE\s+html>|<html\b', content, re.IGNORECASE):
                    return "Web/HTML"
                
                # CSS detection
                if re.search(r'@import\s+url|@media\b|\bbody\s*{', content):
                    return "Web/CSS"
                
                # JavaScript/TypeScript detection
                if re.search(r'import\s+.*\bfrom\b|\bexport\b.*\bclass\b|\bfunction\b', content):
                    if 'React' in content or 'jsx' in content:
                        return "Web/React"
                    if 'interface ' in content or ': string' in content:
                        return "Web/TypeScript"
                    return "Web/JavaScript"
                
                # SQL detection
                if re.search(r'SELECT\s+.*\bFROM\b|CREATE\s+TABLE|INSERT\s+INTO', content, re.IGNORECASE):
                    return "Database/SQL"
        
        except (UnicodeDecodeError, IOError):
            pass  # Not a text file or couldn't read
            
        return None
    
    def print_stats(self):
        """Print statistics about the organization process."""
        logger.info("\n--- File Organization Statistics ---")
        logger.info(f"Total files scanned: {self.stats['total_files']}")
        logger.info(f"Files organized: {self.stats['organized_files']}")
        logger.info(f"Files skipped: {self.stats['skipped_files']}")
        
        if 'duplicate_files' in self.stats:
            logger.info(f"Duplicate files found: {self.stats['duplicate_files']}")
        
        if 'project_type' in self.stats:
            logger.info(f"Project type detected: {self.stats['project_type']}")
            if 'project_name' in self.stats:
                logger.info(f"Project name: {self.stats['project_name']}")
        
        if 'execution_time' in self.stats:
            logger.info(f"Execution time: {self.stats['execution_time']:.2f} seconds")
        
        if self.stats["unknown_extensions"]:
            logger.info(f"Unknown extensions: {', '.join(sorted(self.stats['unknown_extensions']))}")
        
        logger.info("----------------------------------")
        
    def generate_report(self, report_file: str = "organization_report.json") -> None:
        """Generate a detailed report of the organization process."""
        if self.dry_run:
            logger.info("Report generation skipped in dry run mode")
            return
            
        report = {
            "timestamp": datetime.datetime.now().isoformat(),
            "source_directory": self.source_dir,
            "target_directory": self.target_dir,
            "project_mode": self.project_mode,
            "statistics": self.stats,
            "version": __version__
        }
        
        report_path = os.path.join(self.target_dir, report_file)
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
            
        logger.info(f"Report generated at: {report_path}")
    
    def save_config(self, config_file="file_organizer_config.json"):
        """Save current configuration to a JSON file."""
        config = {
            "source_dir": self.source_dir,
            "target_dir": self.target_dir,
            "mappings": self.mappings,
            "project_mode": self.project_mode,
            "exclude_dirs": self.exclude_dirs,
            "exclude_files": self.exclude_files
        }
        
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=4)
        
        logger.info(f"Configuration saved to {config_file}")
    
    @classmethod
    def load_config(cls, config_file="file_organizer_config.json"):
        """Load configuration from a JSON file."""
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            logger.info(f"Configuration loaded from {config_file}")
            return cls(**config)
        except FileNotFoundError:
            logger.warning(f"Config file {config_file} not found. Using defaults.")
            return None
        except json.JSONDecodeError:
            logger.error(f"Error parsing config file {config_file}. Using defaults.")
            return None
    
    @staticmethod
    def check_git_repo(directory: str) -> bool:
        """Check if the directory is a git repository."""
        try:
            result = subprocess.run(
                ["git", "-C", directory, "rev-parse", "--is-inside-work-tree"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False
            )
            return result.returncode == 0
        except FileNotFoundError:
            # Git not installed
            return False
    
    @staticmethod
    def get_project_version() -> str:
        """Return the current version of the file organizer."""
        return __version__


def main():
    parser = argparse.ArgumentParser(description="Organize code files into directories based on file type or project structure.")
    parser.add_argument("source_dir", nargs="?", default=os.getcwd(), help="Source directory to organize (default: current directory)")
    parser.add_argument("--target-dir", "-t", help="Target directory to move files to (default: same as source)")
    parser.add_argument("--project-mode", "-p", action="store_true", help="Maintain project structure while organizing files")
    parser.add_argument("--dry-run", "-d", action="store_true", help="Show what would be done without making changes")
    parser.add_argument("--save-config", "-s", action="store_true", help="Save current settings to config file")
    parser.add_argument("--load-config", "-l", action="store_true", help="Load settings from config file")
    parser.add_argument("--config-file", "-c", default="file_organizer_config.json", help="Config file path")
    parser.add_argument("--report", "-r", action="store_true", help="Generate a detailed report after organization")
    parser.add_argument("--report-file", default="organization_report.json", help="Path to save the report file")
    parser.add_argument("--no-smart", action="store_true", help="Disable smart categorization and use only extensions")
    parser.add_argument("--no-duplicates", action="store_true", help="Disable duplicate file detection")
    parser.add_argument("--exclude-dir", action="append", help="Additional directories to exclude, can be specified multiple times")
    parser.add_argument("--exclude-file", action="append", help="Additional files to exclude, can be specified multiple times")
    parser.add_argument("--version", "-v", action="version", version=f"Code File Organizer v{__version__} by {__author__}")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    
    args = parser.parse_args()
    
    # Configure logging level
    if args.verbose:
        logging.getLogger("FileOrganizer").setLevel(logging.DEBUG)
    
    # Initialize organizer
    if args.load_config:
        organizer = FileOrganizer.load_config(args.config_file)
        if not organizer:
            organizer = FileOrganizer(args.source_dir, args.target_dir, project_mode=args.project_mode, dry_run=args.dry_run)
    else:
        # Prepare exclude lists
        exclude_dirs = ['.git', '.vscode', 'node_modules', 'venv', 'env', '__pycache__']
        exclude_files = ['file_organizer.py', 'file_organizer_config.json', 'organize.py']
        
        if args.exclude_dir:
            exclude_dirs.extend(args.exclude_dir)
        if args.exclude_file:
            exclude_files.extend(args.exclude_file)
        
        organizer = FileOrganizer(
            args.source_dir, 
            args.target_dir, 
            project_mode=args.project_mode, 
            dry_run=args.dry_run,
            exclude_dirs=exclude_dirs,
            exclude_files=exclude_files
        )
    
    # Display banner
    print(f"""
┌──────────────────────────────────────────────┐
│          Code File Organizer v{__version__}           │
│       Created by {__author__}        │
└──────────────────────────────────────────────┘
    """)
    
    # Save config if requested
    if args.save_config:
        organizer.save_config(args.config_file)
    
    # Execute organization
    try:
        organizer.organize_files()
        organizer.print_stats()
        
        # Generate report if requested
        if args.report and not args.dry_run:
            organizer.generate_report(args.report_file)
    except KeyboardInterrupt:
        logger.warning("Organization interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An error occurred during organization: {e}")
        import traceback
        logger.debug(traceback.format_exc())
        sys.exit(1)
    
    logger.info("Organization completed successfully")


if __name__ == "__main__":
    main() 