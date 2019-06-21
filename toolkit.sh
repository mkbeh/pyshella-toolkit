#!/bin/bash
set -e
shopt -s extglob
echo "export PYTHONPATH=/pyshella-toolkit" >> ~/.bashrc && . ~/.bashrc

# Extra funcs.
log=/pyshella-toolkit/logs/toolkit.log
install_pkg_dir=/usr/local/lib/python3.7/site-packages/
wordlistsDir = /pyshella-toolkit/share/wordlists

function logFileChecker {
    while :
	do
	    if [[ -f "$log" ]]; then
            break
        fi
		sleep 4s
	done
}

function logOutput {
	logFileChecker
	tail -f ${log}
}

function wordlistsChecker {
    if ! [[ -n "$(ls -A ${wordlistsDir})" ]]; then
	    echo -e "\e[1;32m:> No dictionary files added to the" \
	     "directory ~/pyshella-toolkit/shared/wordlists on the host...\e[0m"
	    exit 1
    fi
}
function makeWordlistsUnique {
    for file in $(find share/wordlists/ -name "*.*")
    do
	    sort -u -o ${file} ${file}
    done

}
function removeSourceCode {
    rm -rf !("shared"|"btt_spider")
}

function installScrapy {
    if [[ "$CRAWLER" = 'ACTIVATE' ]]; then
        python3.7 -m pip install scrapy
    fi
}

function getLatestPackageInDir {
    local package=$(ls dist/ | sort -V | tail -n 1)
    echo ${package}
}

function installToolkit {
    python3.7 setup.py bdist_egg --exclude-source-files
    package=$(getLatestPackageInDir)
    python3.7 -m easy_install --install-dir ${install_pkg_dir} --prefix=$HOME/.local dist/${package}
    installScrapy

    echo -e "\e[1;32m:> Removing source code from container...\e[0m" && sleep 3s
    removeSourceCode
}
# Check toolkit package.
package=$(pip list | grep pyshella-toolkit) &

# Check if the toolkit is not installed.
if ! [[ ${package} ]]; then
    echo -e "\e[1;32m:> Toolkit is not installed...\e[0m"
    echo -e "\e[1;32m:> Running code obfuscation and installing toolkit...\e[0m" && sleep 5s

    installToolkit
fi

# Selects the crawler mode.
if [[ "$CRAWLER" = 'ACTIVATE' ]]; then
    python3.7 -m pip install scrapy      # ONLY FOR TEST // REMOVE IT LATER
    python3.7 -m pip install loguru      # ONLY FOR TEST // REMOVE IT LATER

    echo -e "\e[1;32m:> Running parsing credentials from bitcointalk.org of ANN section....\e[0m" && sleep 5s
    cd btt_spider && scrapy crawl creds_crawler && makeWordlistsUnique
else
    echo -e "\e[1;32m:> Crawler not activated...\e[0m"
    wordlistsChecker
    echo -e "\e[1;32m:> Using wordlists that defined in toolkit.conf...\e[0m"
fi

## Selects the startup mode.
if [[ "$ENV" = 'DEBUG' ]]; then
    echo -e "\e[1;32m:> Running Toolkit in DEBUG mode...\e[0m"
    echo -e "\e[1;32m:> Files with log are located by host path ~/pyshella-toolkit/logs/\e[0m"
    sed -i 's/.*nodaemon=true.*/nodaemon=false/' /etc/supervisor/conf.d/toolkit.conf

    /usr/bin/supervisord && logOutput

else
    echo -e "\e[1;32m:> Running Toolkit in BATTLE mode...\e[0m"
    echo -e "\e[1;32m:> Files with log are located by host path ~/pyshella-toolkit/logs/\e[0m" && sleep 5s

    /usr/bin/supervisord
fi
