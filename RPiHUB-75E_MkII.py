# RPiHUB-75E_MkII.py
# Updated version of the original HUB75E display driver script
# Compatible with modern Python 3, pygame 2.x, and performance improvements

import RPi.GPIO as GPIO
import pygame
import time
import os
import numpy as np

# GPIO pin definitions
R1 = 17
G1 = 18
B1 = 22
R2 = 23
G2 = 24
B2 = 25
A = 12
B = 16
C = 20
D = 21
CLK = 5
LAT = 6
OE = 13

# Display configuration
DISPLAY_ROWS = 32
DISPLAY_COLS = 64
NUM_FRAMES = 4
FRAME_DELAY = 0.1

# Setup GPIO
GPIO.setmode(GPIO.BCM)
OUTPUT_PINS = [R1, G1, B1, R2, G2, B2, A, B, C, D, CLK, LAT, OE]
for pin in OUTPUT_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

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

            GPIO.output(R1, top_pixel[0] > 127)
            GPIO.output(G1, top_pixel[1] > 127)
            GPIO.output(B1, top_pixel[2] > 127)

            GPIO.output(R2, bottom_pixel[0] > 127)
            GPIO.output(G2, bottom_pixel[1] > 127)
            GPIO.output(B2, bottom_pixel[2] > 127)

            pulse(CLK)

        GPIO.output(OE, 1)
        pulse(LAT)
        GPIO.output(OE, 0)

pygame.init()
screen = pygame.display.set_mode((1, 1))  # Dummy surface for loading images

# Load images and convert to numpy arrays
frames = []
for i in range(1, NUM_FRAMES + 1):
    path = f"FrameImage{i}.png"
    if os.path.exists(path):
        image = pygame.image.load(path).convert()
        frame_array = pygame.surfarray.array3d(image).transpose(1, 0, 2)
        frames.append(frame_array)
    else:
        print(f"Missing frame: {path}")

try:
    while True:
        for frame in frames:
            display_frame(frame)
            time.sleep(FRAME_DELAY)

except KeyboardInterrupt:
    print("\nExiting and cleaning up GPIO...")
    GPIO.cleanup()
    pygame.quit()
