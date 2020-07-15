from sense_hat import SenseHat
from datetime import datetime
import csv
from os import path
import time
import sys


sense = SenseHat()



def shake():

    base_values = get_base_accel()

    print(f"base values: {base_values}")

    sense.set_imu_config(False, False, True)
    red = (255, 0, 0)
    green = (0,255,0)

    #green LED means logging
    sense.show_letter(".", text_colour=green)
    while True:
        comfort = None
        stop = False

        #returns a list of current G values for x, y ,z
        acceleration = sense.get_accelerometer_raw()

        #subtract base values to get corrected G force
        x = abs(acceleration['x']-base_values[0])
        y = abs(acceleration['y']-base_values[1])
        z = abs(acceleration['z']-base_values[2])

        for event in sense.stick.get_events():
            if event.direction == 'left':
                stop = True
            if event.direction == 'down':
                comfort = 'GOOD'
                record_shake(x, y, z, comfort)
            if event.direction == 'up':
                comfort = 'POOR'
                record_shake(x, y, z, comfort)
            if event.direction == 'right':
                comfort = 'FAIR'
                record_shake(x, y, z, comfort)
        if stop == True:
            sense.clear()
            print("Stopped")
            show_time()
            break

        if x > .5 or y > .5 or z > .1:
            sense.show_letter("!", red)
            record_shake(x, y, z, comfort)
        else:
            sense.clear()



def record_shake(x, y, z, condition=None):
    cur_date = datetime.utcnow().strftime("%d%m%Y")

    if not path.exists(f'./shake_data/shake_log{cur_date}.csv'):
        with open(f'./shake_data/shake_log{cur_date}.csv', 'w') as f:
            header_writer = csv.writer(f, delimiter=',', )
            header_writer.writerow(['date', 'time', 'x', 'y', 'z', 'condition']),

    with open(f'./shake_data/shake_log{cur_date}.csv', mode='a') as f:
        time_writer = csv.writer(f, delimiter=',', )
        now = datetime.utcnow()
        print(f"{now} {x}, {y}, {z},{condition}")
        time_writer.writerow([now.strftime("%d/%m/%Y"), now.strftime("%H:%M:%S.%f"), x, y, z, condition])


def get_base_accel():
    """Function returns the base x, y, z values on current flat unmoving surface"""

    sense.set_imu_config(False, False, True)
    sense.clear()
    acceleration = sense.get_accelerometer_raw()

    x = abs(acceleration['x'])
    y = abs(acceleration['y'])
    z = abs(acceleration['z'])

    return [x, y, z]


def show_time():

    number = [
        [[0, 1, 1, 1],  # Zero
         [0, 1, 0, 1],
         [0, 1, 0, 1],
         [0, 1, 1, 1]],
        [[0, 0, 1, 0],  # One
         [0, 1, 1, 0],
         [0, 0, 1, 0],
         [0, 1, 1, 1]],
        [[0, 1, 1, 1],  # Two
         [0, 0, 1, 1],
         [0, 1, 1, 0],
         [0, 1, 1, 1]],
        [[0, 1, 1, 1],  # Three
         [0, 0, 1, 1],
         [0, 0, 1, 1],
         [0, 1, 1, 1]],
        [[0, 1, 0, 1],  # Four
         [0, 1, 1, 1],
         [0, 0, 0, 1],
         [0, 0, 0, 1]],
        [[0, 1, 1, 1],  # Five
         [0, 1, 1, 0],
         [0, 0, 1, 1],
         [0, 1, 1, 1]],
        [[0, 1, 0, 0],  # Six
         [0, 1, 1, 1],
         [0, 1, 0, 1],
         [0, 1, 1, 1]],
        [[0, 1, 1, 1],  # Seven
         [0, 0, 0, 1],
         [0, 0, 1, 0],
         [0, 1, 0, 0]],
        [[0, 1, 1, 1],  # Eight
         [0, 1, 1, 1],
         [0, 1, 1, 1],
         [0, 1, 1, 1]],
        [[0, 1, 1, 1],  # Nine
         [0, 1, 0, 1],
         [0, 1, 1, 1],
         [0, 0, 0, 1]]
    ]

    while True:
        noNumber = [0, 0, 0, 0]

        hourColor = [255, 0, 0]  # Red
        minuteColor = [0, 255, 255]  # Cyan
        empty = [0, 0, 0]  # Black/Off

        clockImage = []

        now = datetime.utcnow()
        hour = now.hour
        minute = now.minute

        for index in range(0, 4):
            if (hour >= 10):
                clockImage.extend(number[int(hour / 10)][index])
            else:
                clockImage.extend(noNumber)
            clockImage.extend(number[int(hour % 10)][index])

        for index in range(0, 4):
            clockImage.extend(number[int(minute / 10)][index])
            clockImage.extend(number[int(minute % 10)][index])

        for index in range(0, 64):
            if (clockImage[index]):
                if index < 32:
                    clockImage[index] = hourColor
                else:
                    clockImage[index] = minuteColor
            else:
                clockImage[index] = empty

        #sense.set_rotation(90)  # Optional
        sense.low_light = True  # Optional
        sense.set_pixels(clockImage)


        for event in sense.stick.get_events():
            if event.direction == 'middle':
                shake()
            if event.direction == 'left':
                sys.exit()



if __name__ == '__main__':

    #green = (0,255,0)
    sense.clear()
    show_time()
    sense.stick.direction_middle = shake

    while True:
        pass
