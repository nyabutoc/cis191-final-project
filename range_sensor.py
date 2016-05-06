import RPi.GPIO as GPIO
import subprocess
import time
from time import sleep  # pull in the sleep function from time module
GPIO.setmode(GPIO.BCM)

TRIG = 23 
ECHO = 24

print ("Distance Measurement In Progress")

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(25, GPIO.OUT)# set GPIO 25 as output for white led
white = GPIO.PWM(25, 100) # create object white for PWM on port 25 at 100 Hertz

white.start(0) # start white led on 0 percent duty cycle (off)
var =1
try:

  while var ==1:
    GPIO.output(TRIG, False)
    print ("Waiting For Sensor To Settle")
    time.sleep(2)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO)==0:
      pulse_start = time.time()

    while GPIO.input(ECHO)==1:
      pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150

    distance = round(distance,1 )

    print ("Distance:",distance,"cm")
    if distance < 7:
      status = subprocess.check_output(["mpc","status"])
      status = status.decode(encoding='UTF-8')
      white.ChangeDutyCycle(0)
      print (status)
      #status = eval('[' + status + ']')
      if status.find('playing') >= 0:
        subprocess.call("mpc pause", shell=True)
      else:
        print ("play")
        subprocess.call("mpc play", shell=True)
    if distance > 7 and distance < 12:
      print ("next")
      subprocess.call("mpc next", shell=True)
    if distance > 12.5 and  distance < 25:
      subprocess.call('mpc %s %i' % ("volume",((int(distance)-12.5)*8),), shell=True)
      white.ChangeDutyCycle(int(distance)*4)
except KeyboardInterrupt:
    white.stop()
    GPIO.cleanup()
