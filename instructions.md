### Naming Conventions:
- File naming = Snake case
- Class naming = Pascal case
- Function names and Variable names = Snake case 

### Creating installer:
- Install "pyinstaller" using pip.
- If you need to add any exlusion to module list then add them to `build_scripts\exclude_modules.py`, this helps to reduce the exe build size.
- Use command `python.exe build_scripts/build_exe.py src/main.py <OPTIONAL: output_file_name>` from root dir to build exe for GUI Application.
- Use command `pyinstaller --paths=src --exclude-module PySide6 src/frontend/cmd_toolset.py` from root dir to build exe for CLI Application.
- Look inside `dist` folder after running these commands to see the executables. 
- Also excluding `PySide6` binding as multiple bindings were creating problem for the pyinstaller.
- See more at https://pyinstaller.org/en/stable/usage.html#options

### Comments:
- Currently working on CLI installer build
- GUI build completes and size is down to 176 MB from 456 MB.
- In future maybe we want to port to "PySide6" as it uses "LGPL" as license. 