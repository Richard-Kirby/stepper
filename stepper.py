import time
from collections import deque
import subprocess
import os

import pigpio
"""
This bit just gets the pigpiod daemon up and running if it isn't already.
The pigpio daemon accesses the Raspberry Pi GPIO.  
"""
p = subprocess.Popen(['pgrep', '-f', 'pigpiod'], stdout=subprocess.PIPE)
out, err = p.communicate()

if len(out.strip()) == 0:
    os.system("sudo pigpiod")
    time.sleep(3)

pi = pigpio.pi()

'''
fullStepSequence = (
  (1, 0, 0, 0),
  (0, 1, 0, 0),
  (0, 0, 1, 0),
  (0, 0, 0, 1)
)
'''


fullStepSequence = (
  (1, 1, 0, 0),
  (0, 1, 1, 0),
  (0, 0, 1, 1),
  (1, 0, 0, 1)
)



halfStepSequence = (
  (1, 0, 0, 0),
  (1, 1, 0, 0),
  (0, 1, 0, 0),
  (0, 1, 1, 0),
  (0, 0, 1, 0),
  (0, 0, 1, 1),
  (0, 0, 0, 1),
  (1, 0, 0, 1)
)


class StepperMotor:

    def __init__(self, pi, pin1, pin2, pin3, pin4, sequence=fullStepSequence, delayAfterStep=0.00015):
        if not isinstance(pi, pigpio.pi):
          raise TypeError("Is not pigpio.pi instance.")
        pi.set_mode(pin1, pigpio.OUTPUT)
        pi.set_mode(pin2, pigpio.OUTPUT)
        pi.set_mode(pin3, pigpio.OUTPUT)
        pi.set_mode(pin4, pigpio.OUTPUT)
        self.pin1 = pin1
        self.pin2 = pin2
        self.pin3 = pin3
        self.pin4 = pin4
        self.pi = pi
        self.delayAfterStep = delayAfterStep
        self.deque = deque(sequence)

    def clockwise_step(self):
        self.deque.rotate(-1)
        self.step_and_delay(self.deque[0])

    def counter_clockwise_step(self):
        self.deque.rotate(1)
        self.step_and_delay(self.deque[0])

    def step_and_delay(self, step):
        print(step)
        self.pi.write(self.pin1, step[0])
        self.pi.write(self.pin2, step[1])
        self.pi.write(self.pin3, step[2])
        self.pi.write(self.pin4, step[3])
        time.sleep(self.delayAfterStep)


if __name__ == "__main__":
    stepper = StepperMotor(pi, 26, 13, 21, 20,   sequence= halfStepSequence)

    while True:
        for i in range(200):
            print("cw", i)
            stepper.clockwise_step()
        time.sleep(0.5)

        for i in range(200):
            print("ccw", i)
            stepper.counter_clockwise_step()

        time.sleep(0.5)