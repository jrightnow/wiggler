"""
wiggler.py

A configurable windows utility to periodically wiggle the mouse cursor 
"""
import time
import win32api
import win32con
import random

# inputs
motionthreshold = 5    # seconds
wiggletime = 2  # seconds
wiggleintensity = 50  # pixels
debug = True
wiggleperiod = 0.100

# inits
previousposition = [0,0]
motionless = False
starttime = time.time()

mouseeventflags = win32con.MOUSEEVENTF_MOVE
while True:
    currenttime = time.time()
    # GetCursorPos returns tuple of (x, y). Origin is top left corner
    currentposition = list(win32api.GetCursorPos())
    if debug:
        print(currenttime, currentposition)
    # if already in the 'motionless' state, check if still motionless and update timer
    if motionless:
        if currentposition == previousposition:
            # elapsed time since cursor has became motionless
            et = currenttime - starttime
            if debug:
                print("    Motionless ET: %s" % et)
        else:
            motionless = False
        # when the cursor has been motionless long enough, wiggle it.
        if et > motionthreshold:
            if debug:
                print("~wiggle~"*3)
            # wiggle
            dt = 0
            while dt < wiggletime:
                dt = time.time() - currenttime
                # movement values in pixels
                xmove = int(wiggleintensity*(random.random() - 0.5))
                ymove = int(wiggleintensity*(random.random() - 0.5))
                currentposition[0] += xmove
                currentposition[1] += ymove
                # move cursor location
                win32api.SetCursorPos(currentposition)
                # trigger mouse event with zero relative offset
                win32api.mouse_event(mouseeventflags,0,0)
                time.sleep(wiggleperiod)
            motionless = False
    # if not in the 'motionless' state yet, check for motion and set starttime
    else:
        if currentposition == previousposition:
            motionless = True
            starttime = currenttime
            et = 0
    # update latest position and sample once per second
    previousposition = currentposition
    time.sleep(1)
