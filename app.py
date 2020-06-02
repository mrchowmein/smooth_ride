#from sense_hat import SenseHat
from datetime import datetime
import csv



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
        else:
            sense.clear()

def record_shake():
    now = datetime.now()


    # with open('time.csv', mode='a') as f:
    #     time_writer = csv.writer(f, delimiter=',', )
    #
    #     while True:
    #         now = datetime.now()
    #         print(now)
    #         time_writer.writerow([now.strftime("%d/%m/%Y"), now.strftime("%H:%M:%S.%f")])


record_shake()