
import pydirectinput
import pyautogui
import keyboard
import threading

alt_pressed = False
pyautogui.FAILSAFE=False
pyautogui.FAILSAFE=False
pyautogui.FAILSAFE=False
def move_mouse_to(x, y):
    current_x, current_y = pyautogui.position()
    dx = x - 1280
    dy = y - 720
    pydirectinput.moveRel(dx, dy)

def move_mouse_thread():
    while True:
        if alt_pressed:
            move_mouse_to(0, 0)

def on_key_event(e):
    global alt_pressed

    if e.event_type == keyboard.KEY_DOWN:
        if e.name == 'alt':
            alt_pressed = True
    elif e.event_type == keyboard.KEY_UP:
        if e.name == 'alt':
            alt_pressed = False

keyboard.on_press_key('alt', on_key_event)
keyboard.on_release_key('alt', on_key_event)

mouse_thread = threading.Thread(target=move_mouse_thread)
mouse_thread.start()
mouse_thread.join()






