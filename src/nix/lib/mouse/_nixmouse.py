# -*- coding: utf-8 -*-
import struct
from subprocess import check_output
import re
from ._nixcommon import EV_KEY, EV_REL, EV_MSC, EV_SYN, EV_ABS, aggregate_devices, ensure_root
from ._mouse_event import ButtonEvent, WheelEvent, MoveEvent, LEFT, RIGHT, MIDDLE, X, X2, UP, DOWN

import ctypes
import ctypes.util
from ctypes import c_uint32, c_uint, c_int, c_void_p, byref

display = None
window = None
x11 = None


def build_display():
    global display, window, x11
    if display and window and x11:
        return
    x11 = ctypes.cdll.LoadLibrary(ctypes.util.find_library('X11'))
    # Required because we will have multiple threads calling x11,
    # such as the listener thread and then main using "move_to".
    x11.XInitThreads()
    # Explicitly set XOpenDisplay.restype to avoid segfault on 64 bit OS.
    # http://stackoverflow.com/questions/35137007/get-mouse-position-on-linux-pure-python
    x11.XOpenDisplay.restype = c_void_p
    display = c_void_p(x11.XOpenDisplay(0))
    window = x11.XDefaultRootWindow(display)


def get_position():
    build_display()
    root_id, child_id = c_void_p(), c_void_p()
    root_x, root_y, win_x, win_y = c_int(), c_int(), c_int(), c_int()
    mask = c_uint()
    ret = x11.XQueryPointer(display, c_uint32(window), byref(root_id), byref(child_id),
                            byref(root_x), byref(root_y),
                            byref(win_x), byref(win_y), byref(mask))
    return root_x.value, root_y.value


def move_to(x, y):
    build_display()
    x11.XWarpPointer(display, None, window, 0, 0, 0, 0, x, y)
    x11.XFlush(display)


REL_X = 0x00
REL_Y = 0x01
REL_Z = 0x02
REL_HWHEEL = 0x06
REL_WHEEL = 0x08

ABS_X = 0x00
ABS_Y = 0x01

BTN_MOUSE = 0x110
BTN_LEFT = 0x110
BTN_RIGHT = 0x111
BTN_MIDDLE = 0x112
BTN_SIDE = 0x113
BTN_EXTRA = 0x114

button_by_code = {
    BTN_LEFT: LEFT,
    BTN_RIGHT: RIGHT,
    BTN_MIDDLE: MIDDLE,
    BTN_SIDE: X,
    BTN_EXTRA: X2,
}
code_by_button = {button: code for code, button in button_by_code.items()}

device = None


def build_device():
    global device
    if device:
        return
    ensure_root()
    device = aggregate_devices('mouse')


def listen(queue):
    build_device()

    while True:
        time, type, code, value = device.read_event()
        if type == EV_SYN or type == EV_MSC:
            continue

        event = None
        arg = None

        if type == EV_KEY:
            event = ButtonEvent(DOWN if value else UP,
                                button_by_code.get(code, '?'), time)
        elif type == EV_REL:
            value, = struct.unpack('i', struct.pack('I', value))

            if code == REL_WHEEL:
                event = WheelEvent(value, time)
            elif code in (REL_X, REL_Y):
                x, y = get_position()
                event = MoveEvent(x, y, time)

        if event is None:
            # Unknown event type.
            continue

        queue.put(event)
