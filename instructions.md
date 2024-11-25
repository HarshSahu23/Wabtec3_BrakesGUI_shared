### Naming Conventions:
- File naming = Snake case
- Class naming = Pascal case
- Function names and Variable names = Snake case 

### Creating installer:
- Install "pyinstaller" using pip.
- If you need to add any exlusion to module list then add them to `build_scripts\exclude_modules.py`, this helps to reduce the exe build size.
- Use command `python.exe build_scripts/build_exe.py src/main.py <OPTIONAL: output_file_name>` from root dir to build exe for both the GUI and CLI Applications.
- Look inside `dist` folder after running these commands to see the executables. 
- Also excluding `PySide6` binding as multiple bindings were creating problem for the pyinstaller.
- See more at https://pyinstaller.org/en/stable/usage.html#options

### Comments:
- Complete build size down to 176 MB from 480 MB.
- In future maybe we want to port to "PySide6" as it uses "LGPL" as license. 

### To run final application:
- Simple double click on `main.exe` in `dist/main`. This open GUI.
- Open cmd in the directory where `main.exe` is located.
    - Type `main.exe gui` = opens GUI 
    - Type `main.exe cli` = opens CLI
    - Type `main.exe` = open GUI