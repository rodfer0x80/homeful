#!/usr/bin/python3

import os
import sys

MAIN_MODULE = "src/__main__.py"

def main():
    if len(sys.argv) != 2:
        main_module = MAIN_MODULE
    else:
        main_module = sys.argv[1]
    cdir = "."
    #dirs = __file__.split("/")[1:-1]
    #cdir = ""
    #for d in dirs:
    #    cdir = f"{cdir}/{d}"
    cmd = f"source {cdir}/venv/bin/activate && echo 'True' > src/.env &&\
            python {cdir}/{main_module} > debug.log 2>&1"
    os.system(cmd)
    return 0

if __name__ == '__main__':
    sys.exit(main())
