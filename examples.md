# Code File Organizer - Examples

This file provides examples of how the intelligent file detection features work in the Code File Organizer.

## Smart Content Detection

### Example 1: Detecting React Components

The tool can automatically detect React components even if they have unusual extensions:

```jsx
// File: Component.js
import React from 'react';

const MyComponent = () => {
  return (
    <div className="container">
      <h1>Hello World</h1>
    </div>
  );
};

export default MyComponent;
```

Even though this file has a `.js` extension, the content analyzer would detect JSX syntax and place it in the `Web/React` directory.

### Example 2: Identifying Configuration Files

The tool can identify various configuration files by name patterns:

```json
// File: app.config.json
{
  "apiUrl": "https://api.example.com",
  "timeout": 5000,
  "retryCount": 3
}
```

This would be detected as a configuration file and placed in `Config/JSON`.

### Example 3: Detecting Scripts by Shebang

For script files, the tool detects the language based on the shebang line:

```bash
#!/bin/bash
# File: deploy.sh

echo "Deploying application..."
npm run build
scp -r dist/ user@server:/var/www/app
```

This would be categorized as `Scripts/Shell` because of the `#!/bin/bash` shebang.

```python
#!/usr/bin/env python3
# File: process.py

import sys

def main():
    print("Processing data...")
    
if __name__ == "__main__":
    main()
```

This would be categorized as `Python/Scripts` based on the python shebang.

## Project Structure Detection

### Example: Node.js Project

If your directory contains a `package.json` file, the tool will detect it as a Node.js project:

```json
// File: package.json
{
  "name": "my-awesome-app",
  "version": "1.0.0",
  "description": "An example app",
  "main": "index.js",
  "scripts": {
    "start": "node index.js",
    "test": "jest"
  },
  "dependencies": {
    "express": "^4.17.1"
  }
}
```

The organizer will add this information to the organization report and can use it to make better organization decisions.

## Duplicate File Detection

The tool detects duplicate files by calculating MD5 hashes:

```
Original.txt and Copy.txt have the same content:
"This is a test file with exactly the same content."

The organizer will identify these as duplicates in the report.
```

## Custom Organization Examples

### Example 1: Frontend/Backend Split

You can define custom mappings to organize files by frontend and backend:

```json
{
  "mappings": {
    "js": "Frontend/Scripts",
    "jsx": "Frontend/React",
    "ts": "Frontend/TypeScript",
    "tsx": "Frontend/React",
    "css": "Frontend/Styles",
    "scss": "Frontend/Styles",
    "html": "Frontend/HTML",
    
    "py": "Backend/Python",
    "java": "Backend/Java",
    "go": "Backend/Go",
    "php": "Backend/PHP",
    
    "json": "Data/JSON",
    "xml": "Data/XML",
    "yml": "Data/YAML"
  }
}
```

### Example 2: By Project Type

```json
{
  "mappings": {
    "js": "Web",
    "html": "Web",
    "css": "Web",
    
    "py": "Scripts",
    "sh": "Scripts",
    "bat": "Scripts",
    
    "jpg": "Assets",
    "png": "Assets",
    "svg": "Assets"
  }
}
``` 