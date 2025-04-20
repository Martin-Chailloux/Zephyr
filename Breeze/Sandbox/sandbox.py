from datetime import datetime, timedelta

if __name__ == '__main__':
    dt = datetime.now()
    print(f"{dt = }")
    print(f"{str(timedelta(seconds=1)) = }")
    print(f"{dt.microsecond = }")

