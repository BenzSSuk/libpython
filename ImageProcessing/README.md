# ImageProcessing
Example of general algorithm and custom tool for image processing. 

How to use 
Normally we use this repo as submodule of other computer vision project.

# Add submdule to existing repository
1. Open terminal and cd to project
```
>cd .../ProjectX
```

2. Run submodule add
```
>git submodule add "ssh of repo"
```

# Import submodule in script
Append path to project repository to system path before import submodule
```
// main.py
import os
import sys

// get folder of project repository
// If open repo with vs code
folderProj = os.getcwd()
// or set manually
folderProject = '../../../ProjectX'

// append path to system path
sys.path.append(folderProject)

// Import submodule
import ImageProcessing as wedoimg

```

