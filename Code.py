import os
import sys
import curses
import time
import RPi.GPIO as GPIO
 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

SF_FORWARD = 3
SF_BACKWARD = 16
M1_RIGHT = 4
M1_LEFT = 17
M2_RIGHT = 27
M2_LEFT = 22
 

def setup(*ports):
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    for port in ports:
        GPIO.setup(port, GPIO.OUT)
        GPIO.output(port, GPIO.LOW)
    GPIO.setup(SF_FORWARD, GPIO.IN)
    GPIO.setup(SF_BACKWARD, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def stop_all():
    GPIO.output(M1_LEFT, GPIO.LOW)
    GPIO.output(M1_RIGHT, GPIO.LOW)
    GPIO.output(M2_LEFT, GPIO.LOW)
    GPIO.output(M2_RIGHT, GPIO.LOW)

def get_back():
    GPIO.output(M1_LEFT, GPIO.HIGH)
    GPIO.output(M1_RIGHT, GPIO.LOW)
    GPIO.output(M2_LEFT, GPIO.HIGH)
    GPIO.output(M2_RIGHT, GPIO.LOW)

def get_high():
    GPIO.output(M1_LEFT, GPIO.LOW)
    GPIO.output(M1_RIGHT, GPIO.HIGH)
    GPIO.output(M2_LEFT, GPIO.LOW)
    GPIO.output(M2_RIGHT, GPIO.HIGH)

def go_left():
    GPIO.output(M1_LEFT, GPIO.LOW)
    GPIO.output(M1_RIGHT, GPIO.HIGH)
    GPIO.output(M2_LEFT, GPIO.HIGH)
    GPIO.output(M2_RIGHT, GPIO.LOW)

def go_right():
    GPIO.output(M1_LEFT, GPIO.HIGH)
    GPIO.output(M1_RIGHT, GPIO.LOW)
    GPIO.output(M2_LEFT, GPIO.LOW)
    GPIO.output(M2_RIGHT, GPIO.HIGH)
 

##def rotate(motor=1, mode='s'):

    stop_all()
    if motor == 1:
        if mode == 'r':
            GPIO.output(M1_RIGHT, GPIO.HIGH)
        elif mode == 'l':
            GPIO.output(M1_LEFT, GPIO.HIGH)
    elif motor == 2:
        if mode == 'r':
            GPIO.output(M2_RIGHT, GPIO.HIGH)
        elif mode == 'l':
            GPIO.output(M2_LEFT, GPIO.HIGH)
 

setup(M1_RIGHT, M1_LEFT, M2_RIGHT, M2_LEFT)
 

stdscr = curses.initscr()
curses.cbreak()
stdscr.keypad(1)
stdscr.nodelay(1)

stdscr.addstr(0, 10, "Hit 'q' to quit")
stdscr.addstr(2, 10, "A - M1 Left, D - M1 Right")
stdscr.addstr(3, 10, "< - M2 Left, > - M2 Right")
stdscr.addstr(4, 10, "S - stop")
stdscr.refresh()

while True:
    if SF_FORWARD==0:
        stdscr.addstr(6, 10, "Obstacle forward")
        get_back()
        time.sleep(0.5)
        stop_all()
    elif SF_BACKWARD==0:
        stdscr.addstr(6, 10, "Obstacle backward")
        get_high()
        time.sleep(0.5)
        stop_all()
    key = stdscr.getch()
    if key != -1:
	    if key == ord('w'):
            stdscr.addstr(6, 10, "FORWARD")
            get_high()
        elif key == ord('a'):
            stdscr.addstr(6, 10, "M1 <---")
	        go_left()
        elif key == ord('d'):
            stdscr.addstr(6, 10, "M1 --->")
            go_right()
        elif key == ord('s'):
            stdscr.addstr(6, 10, "Backing")
            get_back()
	    elif key == ord('x'):
            stdscr.addstr(6, 10, "Full stop")
            stop_all()
        elif key == ord('q'):
            stdscr.keypad(0)
            curses.echo()
            curses.endwin()
            os.system('clear')
            sys.exit()
        stdscr.refresh()
        time.sleep(0.01)
