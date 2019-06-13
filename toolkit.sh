#!/bin/bash
set -e

function logFileChecker {
	while :
	file=$(ls /pyshella-toolkit/logs/)

	do
		if [[ ${file} ]]; then
			break
		fi
		sleep 4s
	done

	tail -f /pyshella-toolkit/logs/toolkit.log
}

# Check toolkit package.
package=$(pip list | grep pyshella-toolkit) &

# Check if the toolkit is not installed.
if ! [[ ${package} ]]; then
    echo -e "\e[1;32mToolkit is not installed. Installing toolkit...\e[0m"
    sleep 4s
    python setup.py install --user
fi

# Selects the startup mode.
if [[ "$ENV" = 'DEBUG' ]]; then
    echo -e "\e[1;32mRunning Toolkit in DEBUG mode...\e[0m"
    echo -e "\e[1;32mFiles with logs are located by host path ~/.local/share/pyshella-toolkit/\e[0m"
    sed -i 's/.*nodaemon=true.*/nodaemon=false/' /etc/supervisor/conf.d/toolkit.conf

    /usr/bin/supervisord
    logFileChecker

else
    echo -e "\e[1;32mRunning Toolkit in BATTLE mode...\e[0m"
    sleep 4s
    /usr/bin/supervisord
fi
