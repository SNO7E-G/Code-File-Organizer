#!/usr/bin/env python3
"""
Simple wrapper script for file_organizer.py

Copyright (c) 2023 Mahmoud Ashraf (SNO7E)
"""
import os
import sys
import subprocess

__version__ = "1.0.0"
__author__ = "Mahmoud Ashraf (SNO7E)"

def main():
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to the main organizer script
    organizer_script = os.path.join(script_dir, "file_organizer.py")
    
    # Make sure the file exists
    if not os.path.exists(organizer_script):
        print(f"Error: Could not find {organizer_script}")
        sys.exit(1)
    
    # Display banner
    print(f"""
┌──────────────────────────────────────────────┐
│          Code File Organizer v{__version__}           │
│       Created by {__author__}        │
└──────────────────────────────────────────────┘
    """)
    
    # Pass all arguments to the main script
    cmd = [sys.executable, organizer_script] + sys.argv[1:]
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        sys.exit(e.returncode)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(130)

if __name__ == "__main__":
    main() 