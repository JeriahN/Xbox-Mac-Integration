from pynput.mouse import Button, Controller  # Handle Movement of Cursor
import pygame  # Manage Controller
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

try:
    # Read button map from JSON file
    if os.path.isfile("button_map.json"):
        with open("button_map.json", "r") as f:
            BUTTON_MAP = {str(k): v for k, v in json.load(f).items()}
    else:
        with open("button_map.json", "w") as f:
            json.dump(DEFAULT_BUTTON_MAP, f)
        BUTTON_MAP = DEFAULT_BUTTON_MAP

except pygame.error:
    logging.critical("Could not find Button Map and failed to create one")


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
JOYSTICK_SENSITIVITY = 4  # Default 4


# Map Buttons
def MAP_BUTTON_TO_NAME(button):
    return BUTTON_MAP.get(str(button), button)


# Get Controller Input
def run_controller_input():
    # Get Controller Input
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
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

                mouse.move(int(joystick_x_axis), int(joystick_y_axis))

            elif event.type == pygame.JOYBUTTONDOWN:
                button_down = MAP_BUTTON_TO_NAME(event.button)
                if button_down == "Exit":
                    exit(0)
                elif button_down == "A":
                    mouse.press(Button.left)
                elif button_down == "Menu":
                    mouse.press(Button.right)

            elif event.type == pygame.JOYBUTTONUP:
                button_up = MAP_BUTTON_TO_NAME(event.button)
                if button_up == "A":
                    mouse.release(Button.left)
                elif button_up == "Menu":
                    mouse.release(Button.right)


# Start the controller input loop in a background process
run_controller_input()
