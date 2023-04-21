from pynput.mouse import Button, Controller  # Handle Movement of Cursor
import pygame  # Manage Controller
from multiprocessing import Process  # Run in background
import logging  # Log outputs
import logging.handlers  # Optimize Logs
import json  # Handle External Button Map Config
import os.path  # Handle creation of the button map

# Set Mouse Controller
mouse = Controller()

# Set up rotating file handler to keep maximum 10 backup files of 1MB each
rotating_handler = logging.handlers.RotatingFileHandler(
    filename="xbxmacintegration.log",
    maxBytes=1000000,
    backupCount=1
)

# Set up logging configuration
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        rotating_handler,
        logging.StreamHandler()
    ]
)

# Controller Button Map
DEFAULT_BUTTON_MAP = {
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

# Read button map from JSON file
if os.path.isfile("button_map.json"):
    with open("button_map.json", "r") as f:
        BUTTON_MAP = {str(k): v for k, v in json.load(f).items()}
else:
    with open("button_map.json", "w") as f:
        json.dump(DEFAULT_BUTTON_MAP, f)
    BUTTON_MAP = DEFAULT_BUTTON_MAP


# Controller Setup & Detection | If Joystick is successfully found the app will launch, if else app will quit
try:
    pygame.init()
    pygame.joystick.init()
    controller = pygame.joystick.Joystick(0)
    controller.init()
except pygame.error as e:
    logging.critical("Controller could not be found.")
    exit(1)

# Joystick Variables | Set Dead-Zone (Space to travel until detected) and Sensitivity of Controller (How much to
# multiply the value of the detection)
JOYSTICK_DEADZONE = 0  # Default 0
JOYSTICK_SENSITIVITY = 3  # Default 3


def MAP_BUTTON_TO_NAME(button):
    return BUTTON_MAP.get(str(button), button)


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
            joystick_horizontal = int(joystick_x_axis * JOYSTICK_SENSITIVITY)
            mouse.move(joystick_horizontal, 0)

    elif abs(joystick_x_axis) < abs(joystick_y_axis):  # Vertical Axis
        if abs(joystick_y_axis) >= 0.2:
            joystick_vertical = int(joystick_y_axis * JOYSTICK_SENSITIVITY)
            mouse.move(0, joystick_vertical)


def log_settings():
    logging.info("=====SETTINGS=====")
    logging.info("Sensitivity", JOYSTICK_SENSITIVITY)
    logging.info("Dead-Zone", JOYSTICK_DEADZONE)
    logging.info("=====Button=Mapping=====")
    logging.info(BUTTON_MAP)


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
                elif button_down == "A":
                    mouse.press(Button.left)
                elif button_down == "Menu":
                    mouse.press(Button.right)
                else:
                    print("\"", button_down, "\"was pressed down")

            # Handle Button Release
            elif event.type == pygame.JOYBUTTONUP:
                button_up = MAP_BUTTON_TO_NAME(event.button)
                if button_up == "A":
                    mouse.release(Button.left)
                elif button_up == "Menu":
                    mouse.release(Button.right)
                print("\"", button_up, "\"was lifted up")


# Start the controller input loop in a background process
if __name__ == '__main__':
    p = Process(target=run_controller_input)
    p.start()
    logging.info("Successfully started!")
    logging.info("=====Press Select to get details, press Share to exit=====")
