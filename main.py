import threading
import pyautogui
import pygame

# Controller Setup & Detection
try:
    pygame.init()
    pygame.joystick.init()
    controller = pygame.joystick.Joystick(0)
    controller.init()
except pygame.error as e:
    print("Controller not found:")
    exit(1)

last_input_time = pygame.time.get_ticks()

# To get mouse position
pyautogui.moveTo(100, 200)

# Joystick Variables
JOYSTICK_DEADZONE = 0.25
JOYSTICK_SENSITIVITY = 10

# Controller Button Map
BUTTON_MAP = {
    0: "A",
    1: "B",
    2: "X",
    3: "Y",
    4: "Select",
    5: "Home",
    6: "Menu",
    7: "LS",
    8: "RS",
    9: "LB",
    10: "RB",
    11: "Up_Arrow",
    12: "Down_Arrow",
    13: "Left_Arrow",
    14: "Right_Arrow",
    15: "Exit"
}


def MAP_BUTTON_TO_NAME(button):
    return BUTTON_MAP.get(button, button)


# Handle Cursor Axis and Value
def detect_joystick_axis():
    # Get horizontal and vertical axis states
    joystick_x_axis = controller.get_axis(0)
    joystick_y_axis = controller.get_axis(1)

    # Apply dead-zones
    if abs(joystick_x_axis) < JOYSTICK_DEADZONE:
        joystick_x_axis = 0.0
    if abs(joystick_y_axis) < JOYSTICK_DEADZONE:
        joystick_y_axis = 0.0

    # Apply sensitivity settings
    joystick_x_axis *= JOYSTICK_SENSITIVITY
    joystick_y_axis *= JOYSTICK_SENSITIVITY

    # Determine which axis to use
    if abs(joystick_x_axis) > abs(joystick_y_axis):
        if abs(joystick_x_axis) >= 0.2:
            print("Horizontal", joystick_x_axis)

    elif abs(joystick_x_axis) < abs(joystick_y_axis):
        if abs(joystick_y_axis) >= 0.2:
            print("Vertical", joystick_y_axis)


def get_controller_input():
    while True:
        for event in pygame.event.get():
            # Handle joystick axis motion
            if event.type == pygame.JOYAXISMOTION:
                detect_joystick_axis()

            # Handle Button Press
            elif event.type == pygame.JOYBUTTONDOWN:
                button_down = MAP_BUTTON_TO_NAME(event.button)
                print(button_down, "was pressed down")

            # Handle Button Release
            elif event.type == pygame.JOYBUTTONUP:
                button_up = MAP_BUTTON_TO_NAME(event.button)
                print(button_up, "was lifted up")


def run_in_background():
    t = threading.Thread(target=get_controller_input)
    t.start()


if __name__ == '__main__':
    run_in_background()
