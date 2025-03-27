import os
import subprocess
import platform

def create_virtual_environment():
    """Create a virtual environment for packaging."""
    subprocess.run(['python', '-m', 'venv', 'venv'], check=True)

def install_dependencies():
    """Install dependencies in the virtual environment."""
    pip_path = 'venv/Scripts/pip' if platform.system() == 'Windows' else 'venv/bin/pip'
    subprocess.run([pip_path, 'install', '-r', 'requirements.txt'], check=True)
    subprocess.run([pip_path, 'install', 'pyinstaller'], check=True)

def build_executable():
    """Build standalone executable using PyInstaller."""
    pyinstaller_path = 'venv/Scripts/pyinstaller' if platform.system() == 'Windows' else 'venv/bin/pyinstaller'
    
    subprocess.run([
        pyinstaller_path, 
        '--onefile', 
        '--windowed',
        '--add-data', 'assets:assets',
        '--name', 'AISummarizer',
        'main.py'
    ], check=True)

def main():
    create_virtual_environment()
    install_dependencies()
    build_executable()
    print("Packaging complete! Check the 'dist' directory.")

if __name__ == '__main__':
    main()