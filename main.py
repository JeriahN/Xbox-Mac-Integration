import pyautogui  # Manage Cursor
import pygame  # Manage Controller
from multiprocessing import Process  # Run in background
import logging  # Log outputs

# Set up logging configuration
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("xbxmacintegration.log"),
        logging.StreamHandler()
    ]
)

# Controller Setup & Detection | If Joystick is successfully found the app will launch, if else app will quit
try:
    pygame.init()
    pygame.joystick.init()
    controller = pygame.joystick.Joystick(0)
    controller.init()
except pygame.error as e:
    logging.critical("Controller could not be found.")
    print("Controller not found:")
    exit(1)

# Joystick Variables | Set Dead-Zone (Space to travel until detected) and Sensitivity of Controller (How much to
# multiply the value of the detection)
JOYSTICK_DEADZONE = 0.25  # Default 0.25
JOYSTICK_SENSITIVITY = 10  # Default 10

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


logging.info("Button Map Loaded!", BUTTON_MAP)


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
    if abs(joystick_x_axis) > abs(joystick_y_axis):  # Horizontal Axis
        if abs(joystick_x_axis) >= 0.2:
            print("Horizontal", joystick_x_axis)

    elif abs(joystick_x_axis) < abs(joystick_y_axis):  # Vertical Axis
        if abs(joystick_y_axis) >= 0.2:
            print("Vertical", joystick_y_axis)


def log_settings():
    print("=====SETTINGS=====")
    print("Sensitivity", JOYSTICK_SENSITIVITY)
    print("Dead-Zone", JOYSTICK_DEADZONE)
    print("=====Button=Mapping=====")
    print(BUTTON_MAP)


# Define a function to run the controller input loop in a background process
def run_controller_input():
    # Get Controller Input
    while True:
        for event in pygame.event.get():
            # Handle joystick axis motion
            if event.type == pygame.JOYAXISMOTION:
                detect_joystick_axis()

            # Handle Button Press
            elif event.type == pygame.JOYBUTTONDOWN:
                button_down = MAP_BUTTON_TO_NAME(event.button)
                if button_down == "Exit":
                    exit(0)
                elif button_down == "Select":
                    log_settings()
                else:
                    print("\"", button_down, "\"was pressed down")

            # Handle Button Release
            elif event.type == pygame.JOYBUTTONUP:
                button_up = MAP_BUTTON_TO_NAME(event.button)
                print("\"", button_up, "\"was lifted up")


# Start the controller input loop in a background process
if __name__ == '__main__':
    p = Process(target=run_controller_input)
    p.start()
    logging.info("Successfully started!")
    print("=====Press Select to get details, press Share to exit=====")
