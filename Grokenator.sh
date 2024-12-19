#!/bin/bash

# Check if the script is run with root privileges
if [ "$(id -u)" == "0" ]; then
   echo "This script should not be run as root. Please run as a regular user."
   exit 1
fi

# Function to install necessary files and libraries
install_dependencies() {
    echo "Creating necessary directories..."
    mkdir -p data/sessions data/uploads

    echo "Creating virtual environment..."
    if [ ! -d "./venv" ]; then
        python3 -m venv ./venv || { echo "Failed to create virtual environment."; exit 1; }
    fi

    echo "Activating virtual environment..."
    source ./venv/bin/activate || { echo "Failed to activate virtual environment."; exit 1; }

    echo "Installing requirements..."
    pip install --upgrade pip

    if [ ! -f "requirements.txt" ]; then
        echo "Error: 'requirements.txt' file not found. Please create one with necessary dependencies."
        exit 1
    fi

    pip install -r requirements.txt || { echo "Failed to install requirements."; exit 1; }

    echo "Installation completed successfully."
}

# Function to run the program
run_program() {
    echo "Activating virtual environment..."
    source ./venv/bin/activate || { echo "Failed to activate virtual environment."; exit 1; }

    echo "Running Grokenator..."
    if [ -f "main_program.py" ]; then
        python main_program.py
    else
        echo "Error: 'main_program.py' not found. Please ensure the file exists in the current directory."
        exit 1
    fi
}

# Main menu loop
while true; do
    echo "Grokenator Menu:"
    echo "1. Run Grokenator"
    echo "2. Install Files/Libraries"
    echo "x. Exit"
    read -p "Choose an option (1, 2, or x): " option

    case $option in
        1)
            run_program
            ;;
        2)
            install_dependencies
            ;;
        x|X)
            echo "Exiting Grokenator..."
            exit 0
            ;;
        *)
            echo "Invalid option. Please choose 1, 2, or x."
            ;;
    esac
done
