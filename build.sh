#!/bin/bash
jupyter-book build --all book
python3 ./book/chattutor_setup/install.py
bold=$(tput bold)
normal=$(tput sgr0)
GREEN='\033[1;32m'
NC='\033[0m' # No Color
echo "
"
printf "${GREEN}===============================================================================${NC}

The course is now built and ${bold}chattutor ${normal}is added to it. 

• To bypass CORS issue when testing on a local server/
    static page (if ${bold}TEST_MODE ${normal}is set to false in
    ${bold}chattutor.config.js${normal}), start chrome with --disable-security
    option:

Examples:

• ${bold}MACOS${normal}: 
    $ open -n -a /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --args --user-data-dir="/tmp/chrome_dev_test" --disable-web-security

• ${bold}LINUX${normal}:
    $ google-chrome --disable-web-security
    
    (*) If you need access to local files for dev purposes like AJAX or JSON, you can use --allow-file-access-from-files flag.
"
echo "
• ${bold}WINDOWS${normal}:
    $ "C:\Program Files\Google\Chrome\Application\chrome.exe" --disable-web-security --disable-gpu --user-data-dir=%LOCALAPPDATA%\Google\chromeTemp


! Since Chrome 22+ you will get an error message that says:

⚠ You are using an unsupported command-line flag: --disable-web-security. Stability and security will suffer.
"
echo "
However you can just ignore that message while developing.
"