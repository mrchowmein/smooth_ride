from sense_hat import SenseHat
from datetime import datetime
import csv
from os import path

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
            sense.clear((0,255,0))
            break

        if x > .5 or y > .5 or z > .3:
            sense.show_letter("!", red)
            record_shake(x, y, z, comfort)
        else:
            sense.clear()


def record_shake(x, y, z, condition=None):
    cur_date = datetime.now().strftime("%d%m%Y")

    if not path.exists(f'./shake_data/shake_log{cur_date}.csv'):
        with open(f'./shake_data/shake_log{cur_date}.csv', 'w') as f:
            header_writer = csv.writer(f, delimiter=',', )
            header_writer.writerow(['date', 'time', 'x', 'y', 'z', 'condition']),

    with open(f'./shake_data/shake_log{cur_date}.csv', mode='a') as f:
        time_writer = csv.writer(f, delimiter=',', )
        now = datetime.now()
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


if __name__ == '__main__':

    green = (0,255,0)
    sense.clear(green)
    sense.stick.direction_middle = shake

    while True:
        pass
