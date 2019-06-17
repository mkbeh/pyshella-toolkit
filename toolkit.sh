#!/bin/bash
set -e
shopt -s extglob

# Extra funcs.
function logFileChecker {
    file=/pyshella-toolkit/logs/toolkit.log

    while :
	do
	    if [[ -f "$file" ]]; then
            break
        fi
		sleep 4s
	done
}

function logOutput {
	logFileChecker
	tail -f /pyshella-toolkit/logs/toolkit.log
}

function removeSourceCode {
    rm -rf !("wordlists"|"logs")
}
function getLatestPackageInDir {
    local package=$(ls dist/ | sort -V | tail -n 1)
    echo ${package}
}

function installToolkit {
    python3.7 setup.py bdist_egg --exclude-source-files
    package=$(getLatestPackageInDir)
    python3.7 -m easy_install --install-dir /usr/local/lib/python3.7/site-packages/ --prefix=$HOME/.local dist/${package}

    echo -e "\e[1;32mRemoving source code from container...\e[0m"
    sleep 2s
    removeSourceCode
}
# Check toolkit package.
package=$(pip list | grep pyshella-toolkit) &

# Check if the toolkit is not installed.
if ! [[ ${package} ]]; then
    echo -e "\e[1;32mToolkit is not installed...\e[0m"
    echo -e "\e[1;32mRunning code obfuscation and installing toolkit...\e[0m"
    sleep 5s

    installToolkit
fi

# Selects the startup mode.
if [[ "$ENV" = 'DEBUG' ]]; then
    echo -e "\e[1;32mRunning Toolkit in DEBUG mode...\e[0m"
    echo -e "\e[1;32mFiles with log are located by host path ~/pyshella-toolkit/logs/\e[0m"
    sed -i 's/.*nodaemon=true.*/nodaemon=false/' /etc/supervisor/conf.d/toolkit.conf

    /usr/bin/supervisord
    logOutput

else
    echo -e "\e[1;32mRunning Toolkit in BATTLE mode...\e[0m"
    echo -e "\e[1;32mFiles with log are located by host path ~/pyshella-toolkit/logs/\e[0m"
    sleep 4s
    /usr/bin/supervisord
fi
