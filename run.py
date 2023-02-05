import sys
from lib.tools import *
from rich import print
from prettytable import PrettyTable

if __name__ == '__main__':
    if len(sys.argv) > 1:
        set_update_config()
        from src import main
        if sys.argv[1] == "token":
            Vars.cfg.data['refresh_token'] = sys.argv[2]
            print("your refresh token is: " + Vars.cfg.data['refresh_token'])
            Vars.cfg.save()
        elif sys.argv[1] == "show":  # show all config
            table_head, table_body = [], []
            for k, v in Vars.cfg.data.items():
                table_head.append(k)
                table_body.append(v)
            table = PrettyTable(table_head)
            table.add_row(table_body)
            print(table)

        else:
            main.main()  # main function for main.py
        sys.exit()
    else:
        from src import main
        main.main()  # main function for main.py
