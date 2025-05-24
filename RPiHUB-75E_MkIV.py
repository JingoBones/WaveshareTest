# RPiHUB-75E_MkIV.py
# Updated version for test pattern output on HUB75E display

import RPi.GPIO as GPIO
import time
import numpy as np

# GPIO pin definitions
R1 = 11
G1 = 27
B1 = 7
R2 = 8
G2 = 9
B2 = 10
A = 22
B = 23
C = 24
D = 25
CLK = 17
LAT = 4
OE = 18

# Display configuration
DISPLAY_ROWS = 32
DISPLAY_COLS = 64
FRAME_DELAY = 0.01 # previously 0.1
ROW_DELAY = 0.0001

# Setup GPIO
GPIO.setmode(GPIO.BCM)
OUTPUT_PINS = [R1, G1, B1, R2, G2, B2, A, B, C, D, CLK, LAT, OE]
for pin in OUTPUT_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)
GPIO.output(OE, 1)

def pulse(pin):
    GPIO.output(pin, 1)
    GPIO.output(pin, 0)

def select_row(row):
    GPIO.output(A, row & 0x01)
    GPIO.output(B, (row >> 1) & 0x01)
    GPIO.output(C, (row >> 2) & 0x01)
    GPIO.output(D, (row >> 3) & 0x01)

def display_frame(frame):
    for row in range(DISPLAY_ROWS // 2):
        select_row(row)
        for col in range(DISPLAY_COLS):
            top_pixel = frame[row, col]
            bottom_pixel = frame[row + DISPLAY_ROWS // 2, col]

            GPIO.output(R1, bool(top_pixel[0] > 127))
            GPIO.output(G1, bool(top_pixel[1] > 127))
            GPIO.output(B1, bool(top_pixel[2] > 127))

            GPIO.output(R2, bool(bottom_pixel[0] > 127))
            GPIO.output(G2, bool(bottom_pixel[1] > 127))
            GPIO.output(B2, bool(bottom_pixel[2] > 127))
            
            GPIO.output(OE, 0)
            GPIO.output(CLK, 1)
            #pulse(CLK)
            time.sleep(ROW_DELAY)
            GPIO.output(OE, 1)
            GPIO.output(CLK, 0)

        pulse(LAT)

# Create a simple test pattern: vertical RGB stripes
frame = np.zeros((DISPLAY_ROWS, DISPLAY_COLS, 3), dtype=np.uint8)
#frame[:, :] = [0, 0, 255] # blue test of blue LEDs when this line is uncommented and the rest of the pattern is commented out.
#for x in range(DISPLAY_COLS):
    #if x % 3 == 0:
    #    frame[:, x] = [255, 0, 0]  # Red
    #elif x % 3 == 1:
    #    frame[:, x] = [0, 255, 0]  # Green
    #else:
    #    frame[:, x] = [0, 0, 255]  # Blue
for y in range(DISPLAY_ROWS):
    if y % 3 == 0:
        frame[y, :] = [255, 0, 0]  # Red
    elif y % 3 == 1:
        frame[y, :] = [0, 255, 0]  # Green
    else:
        frame[y, :] = [0, 0, 255]  # Blue
    

try:
    while True:
        display_frame(frame)
        time.sleep(FRAME_DELAY)

except KeyboardInterrupt:
    print("\nExiting and cleaning up GPIO...")
    GPIO.cleanup()
