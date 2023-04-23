from picarx import Picarx
import time
from robot_hat import TTS

tts_robot = TTS()

delay = 70 # 70 millisecond delay

def handle_obstacle(px, distance, data):
    if distance < 5 or data[0] < 100 or data[1] < 100 or data[2] < 100:
        px.stop()
        px.set_dir_servo_angle(35)
        time.sleep(100 / 1000)
        px.backward(40)
        time.sleep(1000 / 1000)
        px.set_dir_servo_angle(15)
        tts_robot.say('Obstacle avoided succesfully')
        return "exploring"
    elif distance < 25 and distance > 5:
        tts_robot.say('Incoming obstacle')
        px.forward(20)
        px.set_dir_servo_angle(-35)
    elif distance < 45 and distance > 25:
        px.set_dir_servo_angle(-25)
    elif distance < 65 and distance > 25:
        px.set_dir_servo_angle(-25)
    else:
        px.set_dir_servo_angle(15)
    return "exploring"

def handle_exploring(px, distance, data):
    px.forward(20)
    if distance > 0 and distance < 300:
        return handle_obstacle(px, distance, data)
    return "exploring"

def main():
    try:
        px = Picarx()
        state = "exploring"
        while True:
            distance = px.ultrasonic.read()
            print("distance: ",distance)
            print("grayscale data:", px.get_grayscale_data())
            data = px.get_grayscale_data()
            if state == "exploring":
                state = handle_exploring(px, distance, data)
            #time.sleep(delay / 1000)
    finally:
        px.forward(0)

if __name__ == "__main__":
    main()
