import subprocess
import sys
import platform

def install_requirements(requirements_file):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
    except subprocess.CalledProcessError as e:
        print(f"Failed to install requirements from {requirements_file}: {e}")

def main():
    # Install common requirements
    install_requirements("requirements.txt")

    # Conditionally install Windows-specific requirements
    if platform.system() == "Windows":
        install_requirements("requirements-windows.txt")

if __name__ == "__main__":
    main()
