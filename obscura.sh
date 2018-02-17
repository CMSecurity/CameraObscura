#! /bin/sh

if [ ! -f configuration.cfg ]; then
  python3 ./main.py init
fi

python3 ./main.py