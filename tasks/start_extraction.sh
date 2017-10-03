#!/bin/sh

usage() { echo "Usage: $0 -n 1|2 [-s 1-4]" 1>&2; exit 1; }

while getopts ":n:s:" opt; do
    case $opt in
        n)
            n=${OPTARG}
            if [ "$n" -ne "1" ] && [ "$n" -ne "2" ]; then
              usage
            fi
            ;;
        s)
            s=${OPTARG}
            if [ "$s" -lt "1" ] || [ "$s" -gt "4" ]; then
              usage
            fi
            ;;
        *)
            usage
            ;;
    esac
done

if [ -z "${n}" ]; then
  n=1
fi

if [ -z "${s}" ]; then
  s=1
fi

if [ "$n" -eq "1" ]; then
  echo "Book number ${s} extraction starting..."
  if [ "$s" -eq "1" ]; then
    kaira-venv/bin/python main.py -i material/siirtokarjalaiset_I.xml -o material/siirtokarjalaiset_I.json
  elif [ "$s" -eq "2" ]; then
    kaira-venv/bin/python main.py -i material/siirtokarjalaiset_II.xml -o material/siirtokarjalaiset_II.json
  elif [ "$s" -eq "3" ]; then
    kaira-venv/bin/python main.py -i material/siirtokarjalaiset_III.xml -o material/siirtokarjalaiset_III.json
  elif [ "$s" -eq "4" ]; then
    kaira-venv/bin/python main.py -i material/siirtokarjalaiset_IV.xml -o material/siirtokarjalaiset_IV.json
  fi
elif [ "$n" -eq "2" ]; then
  echo "Set number ${s}:"
  if [ "$s" -eq "1" ]; then
    echo "Book number 1 extraction starting..."
    kaira-venv/bin/python main.py -i material/siirtokarjalaiset_I.xml -o material/siirtokarjalaiset_I.json
    echo "Book number 2 extraction starting..."
    kaira-venv/bin/python main.py -i material/siirtokarjalaiset_II.xml -o material/siirtokarjalaiset_II.json
  elif [ "$s" -eq "2" ]; then
    echo "Book number 1 extraction starting..."
    kaira-venv/bin/python main.py -i material/siirtokarjalaiset_III.xml -o material/siirtokarjalaiset_III.json
    echo "Book number 2 extraction starting..."
    kaira-venv/bin/python main.py -i material/siirtokarjalaiset_IV.xml -o material/siirtokarjalaiset_IV.json
  fi
fi
