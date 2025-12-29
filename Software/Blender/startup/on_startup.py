import sys

# externalize logs
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)
sys.path.append('C:/Users/marti/OneDrive/Documents/__work/_dev/Zephyr/Software/Abstract')
sys.path.append('C:/Users/marti/OneDrive/Documents/__work/_dev/Zephyr/Software/Blender')

from startup import zephyr_menu


def run():
    print("CREATE MENU...")
    zephyr_menu.create()


if __name__ == '__main__':
    run()
