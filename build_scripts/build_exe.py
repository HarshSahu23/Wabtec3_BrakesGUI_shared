import PyInstaller.__main__
import os
import sys
from exclude_modules import exclude_modules

def build_minimal_exe(script_path, output_name=None):
    """
    Build a minimal executable from a Python script

    Args:
        script_path: Path to your main Python script
        output_name: Name of output exe (without .exe extension)
    """
    if output_name is None:
        output_name = os.path.splitext(os.path.basename(script_path))[0]
    command = [
        script_path,
        '--noconsole',  # No console window. Disable this = logs the python output to console. 
        '--clean',  # Clean cache before building
        # '--noupx',  # Disable UPX compression (can sometimes increase size)
    ]
    command.extend(['--specpath', 'build_scripts'])
    
    # Excluding unecessary modules
    command.extend(['--exclude-module' if i % 2 == 0 else exclude_modules[i // 2] for i in range(2 * len(exclude_modules))])
    command.extend(['--python-option', 'O', '--name', output_name])
    PyInstaller.__main__.run(command)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python build_exe.py <path_to_script> [output_name]")
        sys.exit(1)

    script_path = sys.argv[1]
    output_name = sys.argv[2] if len(sys.argv) > 2 else None
    build_minimal_exe(script_path, output_name)
