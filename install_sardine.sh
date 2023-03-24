#!/bin/bash


clear
echo -e "\033[1;32m===========================================\033[0m"
echo -e "\033[1;32mWelcome to the Sardine System Installation!\033[0m"
echo -e "\033[1;32m===========================================\033[0m"
echo -e "For more information and documentation, visit: \033[4;34mhttps://sardine.raphaelforment.fr\033[0m"
echo ""

# Function to clone and install Sardine
install_sardine() {
    echo "Do you want to install the editable (dev) version? [y/N]"
    read -r response

    case "$response" in
        [yY][eE][sS]|[yY])
            echo "Installing the editable (dev) version of Sardine..."
            python -m pip install --find-links https://thegamecracks.github.io/python-rtmidi-wheels/ -e .
            ;;
        *)
            echo "Installing the regular version of Sardine..."
            python -m pip install --find-links https://thegamecracks.github.io/python-rtmidi-wheels/ .
            ;;
    esac
}

# Function to install SuperDirt Quarks for SuperCollider
install_superdirt_quarks() {
    echo "Installing SuperDirt Quarks for SuperCollider..."

    supercollider_code="Quarks.install(\"SuperDirt\");"
    
    # Save the code to a temporary file
    echo "$supercollider_code" > install_superdirt_quarks.scd

    if [[ "$OSTYPE" == "darwin"* ]] || [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sclang install_superdirt_quarks.scd
    elif [[ "$OSTYPE" == "msys" ]]; then
        "/c/Program Files/SuperCollider/SuperCollider.exe" -a -l install_superdirt_quarks.scd
    else
        echo "Unsupported platform. Please install SuperDirt Quarks for SuperCollider manually."
    fi

    # Remove the temporary file
    rm install_superdirt_quarks.scd
}

# Function to install SuperCollider
install_supercollider() {
    if command -v sclang &> /dev/null; then
        echo "SuperCollider is already installed."
    else
        if [[ "$OSTYPE" == "darwin"* ]]; then
            echo "Installing SuperCollider on macOS..."
            brew install --cask supercollider
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            echo "Installing SuperCollider on Linux..."
            
            # Check for Arch Linux and pacman
            if command -v pacman &> /dev/null; then
                sudo pacman -Syu --needed --noconfirm supercollider
            else
                sudo apt-get update
                sudo apt-get install -y supercollider
            fi
            
        elif [[ "$OSTYPE" == "msys" ]]; then
            echo "Installing SuperCollider on Windows..."
            echo "Please download the SuperCollider installer for Windows from the following URL:"
            echo "https://github.com/supercollider/supercollider/releases"
            echo "Then, run the installer and follow the instructions to complete the installation."
            read -p "Press any key to continue after the installation is complete..." -n1 -s
            echo
        else
            echo "Unsupported platform. Please install SuperCollider manually."
        fi
    fi
}

# Function to install Git
install_git() {
    if ! command -v git &> /dev/null; then
        echo "Installing Git..."
        if [[ "$OSTYPE" == "darwin"* ]]; then
            brew install git
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            sudo apt-get update
            sudo apt-get install -y git
        elif [[ "$OSTYPE" == "msys" ]]; then
            echo "Please install Git for Windows manually: https://git-scm.com/download/win"
        else
            echo "Unsupported platform. Please install Git manually."
        fi
    fi
}

# Function to install NPM and Yarn
install_npm_yarn() {
    if ! command -v npm &> /dev/null; then
        echo "Installing NPM..."
        if [[ "$OSTYPE" == "darwin"* ]]; then
            brew install node
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            sudo apt-get update
            sudo apt-get install -y nodejs
        elif [[ "$OSTYPE" == "msys" ]]; then
            echo "Please install Node.js for Windows manually: https://nodejs.org/en/download/"
        else
            echo "Unsupported platform. Please install Node.js manually."
        fi
    fi

    if ! command -v yarn &> /dev/null; then
        echo "Installing Yarn..."
        npm install --global yarn
    fi
}

echo -e "\033[1;33m[1/3] Installing Git, NPM, Yarn and SuperCollider...\033[0m"
echo ""
install_git
install_npm_yarn
install_supercollider
install_superdirt

# Check if pyenv is installed
if ! command -v pyenv &> /dev/null; then
    echo "Installing pyenv..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew install pyenv
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        curl https://pyenv.run | bash
        # Configure pyenv for bash
        if [[ "$SHELL" == *"bash" ]]; then
            echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
            echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
            echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
            echo 'eval "$(pyenv init -)"' >> ~/.bashrc
            source ~/.bashrc
        # Configure pyenv for zsh
        elif [[ "$SHELL" == *"zsh" ]]; then
            echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
            echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
            echo 'eval "$(pyenv init --path)"' >> ~/.zshrc
            echo 'eval "$(pyenv init -)"' >> ~/.zshrc
            source ~/.zshrc
        else
            echo "Unsupported shell. Please configure pyenv manually."
        fi
    elif [[ "$OSTYPE" == "msys" ]]; then
        git clone https://github.com/pyenv-win/pyenv-win.git "$HOME/.pyenv"
        echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
        echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
        source ~/.bashrc
    else
        echo "Unsupported platform. Please install pyenv manually."
    fi
fi

# Install Python 3.11 and set it as local version
echo -e "\033[1;33m[2/3] Installing pyenv and Python 3.11...\033[0m"
echo ""
echo "Updating pyenv's list of available Python versions..."
pyenv update
pyenv install 3.11.2
pyenv local 3.11.2
echo "Upgrading pip..."
pyenv exec python -m pip install --upgrade pip
echo -e "\033[1;33m[3/3] Installing the Sardine System...\033[0m"
echo ""
install_sardine

echo -e "\033[1;32mInstallation complete! Enjoy the Sardine System!\033[0m"
