import sys
from tools import *

from src import main

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "token":
            Vars.cfg.data['refresh_token'] = sys.argv[2]
            print("your refresh token is: " + Vars.cfg.data['refresh_token'])
            Vars.cfg.save()
        else:
            main.main()  # main function for main.py
        sys.exit()

    main.main()  # main function for main.py
