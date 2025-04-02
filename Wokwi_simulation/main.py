import machine
import time
import struct
import math
from machine import I2C,Pin,PWM
from ssd1306 import SSD1306_I2C
import framebuf, sys
from gsheet import add_entry,time_now

# Function to toggle LEDs (blink effect)
def toggle_led(led_pin, duration):
    start_time = time.time()
    while time.time() - start_time < duration:
        led_pin.value(not led_pin.value())  # Toggle LED state
        time.sleep(blink_interval)

# Function to stop the buzzer
def buzzer_off():
    buzzer.duty_u16(0)  # Stop generating sound

# Function to make the buzzer sound (alerting)
def buzzer_alerts(offense):
    if offense == "Harsh Braking":
        buzzer.freq(500)  # Low frequency (Deep tone)
        buzzer.duty_u16(32768)
        time.sleep(0.5)
        buzzer_off()
    
    elif offense == "Hard Acceleration":
        buzzer.freq(1500)  # Higher frequency (Sharp tone)
        buzzer.duty_u16(32768)
        time.sleep(0.3)
        buzzer_off()
    
    elif offense == "Sharp Turn":
        for _ in range(3):  # Beeping effect
            buzzer.freq(1000)  
            buzzer.duty_u16(32768)
            time.sleep(0.2)
            buzzer_off()
            time.sleep(0.2)
    else:
        buzzer_off()

#Function to text on OLED Screen
def show_oled(text):
    # Clear the screen
    oled.fill(0)
    oled.show()
    # Display  content
    oled.text(text, 10, 20)
    oled.show()

def read_accel_data():
    # Read 6 bytes of accelerometer data (X, Y, Z)
    data = i2c.readfrom_mem(MPU_ADDR, ACCEL_XOUT_H, 6) 
    # Unpack data into X, Y, Z acceleration values (16-bit signed integers)
    x, y, z = struct.unpack('>hhh', data)
    
    return x, y, z

def detect_unsafe_driving(x, y, z):
    # Harsh Braking Detection
    if x < HARSH_BRAKING_THRESHOLD:
        print("Unsafe Driving: Harsh Braking Detected")
        #log_data("Harsh Braking",DRIVER_NAME,VEHICLE_NUMBER)
        toggle_led(alert_led1,2)
        #buzzer_alert(duration=0.1) 
        buzzer_alerts("Harsh Braking") 
        show_oled("Harsh Braking !!")
    else:
        alert_led1.off()
        buzzer_off()
    
    # Hard Acceleration Detection
    if x > HARD_ACCELERATION_THRESHOLD:
        print("Unsafe Driving: Hard Acceleration Detected")
        #log_data("Hard Acceleration",DRIVER_NAME,VEHICLE_NUMBER)
        toggle_led(alert_led2,2)
        buzzer_alerts("Hard Acceleration")
        show_oled("Hard Acceleration !!")
    else:
        alert_led2.off()
        buzzer_off()
    
    # Sharp Turn Detection (large change in Y-axis)
    if abs(y) > SHARP_TURN_THRESHOLD:
        print("Unsafe Driving: Sharp Turn Detected")
        #log_data("Sharp Turn",DRIVER_NAME,VEHICLE_NUMBER)
        toggle_led(alert_led3,2)
        buzzer_alerts("Sharp Turn")
        show_oled("Sharp Turn !!")
    else:
        alert_led3.off()
        buzzer_off()


#<---------Alerting Leds------->
alert_led1 = Pin(25, Pin.OUT)
alert_led2 = Pin(26, Pin.OUT)
alert_led3 = Pin(27, Pin.OUT)
# Blink interval for alerting LEDs (in seconds)
blink_interval = 0.25  # LED toggles every 0.5 seconds

#<------------------------>


#<---------Buzzer---------->

# Set up the buzzer pin
buzzer_pin = Pin(13, Pin.OUT)  # Change the GPIO pin if necessary
# Set up PWM on the buzzer pin to generate sound
buzzer = PWM(buzzer_pin)
#<------------------------>

#<------Oled Screen ------>
# I2C for OLED initiliastion
i2c_oled = I2C(0, scl=Pin(18), sda=Pin(19))
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c_oled)

#<------------------------>

#<-------MPU6050 Sensor --->
# MPU6050 Registers and Addresses
MPU_ADDR = 0x68
ACCEL_XOUT_H = 0x3B
ACCEL_XOUT_L = 0x3C
ACCEL_YOUT_H = 0x3D
ACCEL_YOUT_L = 0x3E
ACCEL_ZOUT_H = 0x3F
ACCEL_ZOUT_L = 0x40
PWR_MGMT_1 = 0x6B

# Set up I2C for MPU6050 Sensor
i2c = I2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=400000)
# Wake up MPU6050
i2c.writeto_mem(MPU_ADDR, PWR_MGMT_1, b'\x00')

#<------------------------>

# Define thresholds (These need to be adjusted for your use case)
HARSH_BRAKING_THRESHOLD = -10000   # Negative acceleration (X-axis)
HARD_ACCELERATION_THRESHOLD = 10000  # Positive acceleration (X-axis)
SHARP_TURN_THRESHOLD = 15000      # Y-axis threshold for sharp turns
DRIVER_NAME = "ANMOL"
VEHICLE_NUMBER = "PB02-0041"

#sent data to google sheets via HTTP
def log_data(event,driver,vechicle_number):
    data = [time_now(),driver,vechicle_number,event]
    try:
        add_entry(data) ## Adding unsafe event to google sheet 
    except:
        print("Error in sending data to cloud!!!")
    
    
def main():
    while True:
        # Read accelerometer data
        x, y, z = read_accel_data()
       
        # Print accelerometer data (for debugging purposes)
        print("X: {}, Y: {}, Z: {}".format(x, y, z))
        
        # Detect unsafe driving
        detect_unsafe_driving(x, y, z)
        
        time.sleep(0.2)  # Adjust the interval as needed

if __name__ == '__main__':
    main()
