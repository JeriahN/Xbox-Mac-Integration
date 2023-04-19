import pyautogui
import pygame

# Controller Setup
try:
    pygame.init()
    pygame.joystick.init()
    controller = pygame.joystick.Joystick(0)
    controller.init()
except pygame.error as e:
    print("Controller not found:")
    exit(1)
    # raise an exception or exit the program if the controller is not available

last_input_time = pygame.time.get_ticks()

# To get mouse position
pyautogui.moveTo(100, 200)

DEADZONE = 0.25
SENSITIVITY = 2


# Button Identities
def MAP_BUTTON_TO_NAME(button):
    if button == 0:
        return "A"
    elif button == 1:
        return "B"
    elif button == 2:
        return "X"
    elif button == 3:
        return "Y"
    elif button == 4:
        return "Select"
    elif button == 5:
        return "Home"
    elif button == 6:
        return "Menu"
    elif button == 7:
        return "LS"
    elif button == 8:
        return "RS"
    elif button == 9:
        return "LB"
    elif button == 10:
        return "RB"
    elif button == 11:
        return "Up_Arrow"
    elif button == 12:
        return "Down_Arrow"
    elif button == 13:
        return "Left_Arrow"
    elif button == 14:
        return "Right_Arrow"
    elif button == 15:
        exit(0)
    else:
        return button


# Get Controller Input
while True:
    for event in pygame.event.get():
        cursorPosition = pyautogui.position()
        if event.type == pygame.JOYAXISMOTION:
            # Horizontal
            # Get the input state
            joystick_x_axis = controller.get_axis(0)

            # Apply dead zones
            if abs(joystick_x_axis) < DEADZONE:
                input_state = 0.0

            # Apply sensitivity settings
            joystick_x_axis *= SENSITIVITY

            # Vertical
            # Get the input state
            joystick_y_axis = controller.get_axis(1)

            # Apply dead zones
            if abs(joystick_y_axis) < DEADZONE:
                joystick_y_axis = 0.0

            # Apply sensitivity settings
            joystick_y_axis *= SENSITIVITY

            # Test and Setup
            if abs(joystick_x_axis) > abs(joystick_y_axis):
                if abs(joystick_x_axis) >= 0.2:
                    print("Horizontal", joystick_x_axis)
            elif abs(joystick_x_axis) < abs(joystick_y_axis):
                if abs(joystick_y_axis) >= 0.2:
                    joystick_y_axis *= -1
                    print("Vertical", joystick_y_axis)

        elif event.type == pygame.JOYBUTTONDOWN:
            button_down = MAP_BUTTON_TO_NAME(event.button)
            print(button_down, "was pressed down")

        elif event.type == pygame.JOYBUTTONUP:
            button_up = MAP_BUTTON_TO_NAME(event.button)
            print(button_up, "was lifted up")
