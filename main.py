from plugins.bug.wp.wpLogExp import *
from plugins.crack.password.hash import *
from plugins.finder.admin.find import *
from plugins.finder.shell.find import *
from plugins.info.cms import *
from plugins.info.hdinfo import *
from assets.banner.banner import *

if __name__ == '__main__':
    banner()
    while True:
        cmd = input(f"\n{colors.magenta} ETHOPIA => {colors.reset}")
        if cmd == '1':
            hdInfo()
        elif cmd == '2':
            wpExp()
        elif cmd == '3':
            HashPass()
        elif cmd == '4':
            cmsScanner()
        elif cmd == '5':
            shell()
        elif cmd == '6':
            AdminFinder()
        else:
            print(f"Good bye bro...")