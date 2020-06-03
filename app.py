from sense_hat import SenseHat
from datetime import datetime
import csv
from os import path

def shake():
    sense = SenseHat()

    red = (255, 0, 0)

    while True:
        acceleration = sense.get_accelerometer_raw()
        x = acceleration['x']
        y = acceleration['y']
        z = acceleration['z']

        x = abs(x)
        y = abs(y)
        z = abs(z)

        if x > 1 or y > 1 or z > 1:
            sense.show_letter("!", red)
            record_shake(x, y, z)
        else:
            sense.clear()

def record_shake(x, y, z):
    cur_date = datetime.now().strftime("%d%m%Y")

    if not path.exists(f'shake_data/shake_log{cur_date}.csv'):
        with open(f'shake_log{cur_date}.csv', 'w') as f:
            header_writer = csv.writer(f, delimiter=',', )
            header_writer.writerow(['date', 'time', 'x', 'y', 'z']),

    with open(f'shake_data/shake_log{cur_date}.csv', mode='a') as f:
        time_writer = csv.writer(f, delimiter=',', )
        now = datetime.now()
        print(f"{now} {x}, {y}, {z}")
        time_writer.writerow([now.strftime("%d/%m/%Y"), now.strftime("%H:%M:%S.%f"), x, y, z])


shake()