
# # externalize logs
# sys.stdout.reconfigure(line_buffering=True)
# sys.stderr.reconfigure(line_buffering=True)

def register():
    print("CREATE MENU...")
    import zephyr_menu
    zephyr_menu.create()


if __name__ == '__main__':
    register()
