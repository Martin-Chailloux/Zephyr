import tkinter


def copy_to_clipboard(text: str):
    """source: https://stackoverflow.com/questions/579687/how-do-i-copy-a-string-to-the-clipboard"""

    print(f"Copying to clipboard ... '{text}'")
    r = tkinter.Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(text)
    r.update()  # now it stays on the clipboard after the window is closed
    r.destroy()
