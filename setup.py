"""
RAG Chatbot - Setup Script
Project: RAG Chatbot
Developer: RSK World
Website: https://rskworld.in
Email: help@rskworld.in
Phone: +91 93305 39277
Year: 2026
Description: Setup script for installing and configuring the RAG chatbot
"""

import os
import sys
import subprocess
from pathlib import Path


def check_python_version():
    """
    Check if Python version is 3.8 or higher.
    """
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required.")
        sys.exit(1)
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")


def install_dependencies():
    """
    Install required Python packages.
    """
    print("\nInstalling dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("✗ Error installing dependencies")
        sys.exit(1)


def create_env_file():
    """
    Create .env file if it doesn't exist.
    """
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists() and env_example.exists():
        print("\nCreating .env file from .env.example...")
        with open(env_example, 'r') as f:
            content = f.read()
        with open(env_file, 'w') as f:
            f.write(content)
        print("✓ .env file created")
        print("⚠ Please edit .env and add your OpenAI API key")
    elif env_file.exists():
        print("✓ .env file already exists")
    else:
        print("⚠ .env.example not found, skipping .env creation")


def create_directories():
    """
    Create necessary directories.
    """
    directories = [
        "knowledge_base",
        "vector_db",
        "templates",
        "static/css",
        "static/js"
    ]
    
    print("\nCreating directories...")
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✓ {directory}/")


def main():
    """
    Main setup function.
    """
    print("=" * 50)
    print("RAG Chatbot Setup")
    print("=" * 50)
    
    check_python_version()
    create_directories()
    install_dependencies()
    create_env_file()
    
    print("\n" + "=" * 50)
    print("Setup completed!")
    print("=" * 50)
    print("\nNext steps:")
    print("1. Edit .env and add your OpenAI API key")
    print("2. Add documents to the knowledge_base/ directory")
    print("3. Run: python prepare_knowledge_base.py")
    print("4. Run: python app.py")
    print("5. Open http://localhost:5000 in your browser")
    print("\nFor more information, see README.md")


if __name__ == "__main__":
    main()

