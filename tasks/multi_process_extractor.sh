#!/bin/sh

usage() { echo "Usage: $0 -p 2|4" 1>&2; exit 1; }

while getopts ":p:" opt; do
    case $opt in
        p)
            p=${OPTARG}
            if [ "$p" -ne "2" ] && [ "$p" -ne "4" ]; then
              usage
            fi
            ;;
        *)
            usage
            ;;
    esac
done

if [ -z "${p}" ]; then
  p=4
fi

echo "Starting extraction with ${p} processes..."

if [ "$p" -eq "4" ]; then
  args="-geometry 40x5 -e tasks/start_extraction.sh -n 1"
  x-terminal-emulator $args -s 1
  x-terminal-emulator $args -s 2
  x-terminal-emulator $args -s 3
  x-terminal-emulator $args -s 4
elif [ "$p" -eq "2" ]; then
  args="-geometry 40x8 -e tasks/start_extraction.sh -n 2"
  x-terminal-emulator $args -s 1
  x-terminal-emulator $args -s 2
fi
