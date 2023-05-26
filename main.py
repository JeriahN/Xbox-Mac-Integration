# Add Integration for the XBOX ONE and SERIES Controller to Mac
from pynput.mouse import Button, Controller  # PyInput.mouse for Cursor Management
from pynput.keyboard import Key, Controller as KeyboardController  # PyInput.keyboard for Keyboard Management
import pygame  # PyGame for controller detection and input
import logging.handlers  # Logging handler for easier debugging
import json  # JSON for more readable config file
import os.path  # Filesystem for creating and managing config file
import threading  # Multithreading for better optimization
import time  # Time for delays used in smoothing

# Global Variables
# Joystick
joystick_x_velocity = 0.0  # Rate at how much faster the horizontal axis gets
joystick_y_velocity = 0.0  # Rate at how much faster the vertical axis gets
smoothing_factor = 0.2  # Adjust this value for smoother or more responsive input
JOYSTICK_DEADZONE = 0  # At what point to start detecting the cursor movement to avoid drift (0 by default)
JOYSTICK_SENSITIVITY = 5  # How much to make movements affect the input (5 by default)

# Buttons
DEBOUNCE_DELAY = 0.03  # Debounce delay

# Speed
SLEEP_TIME = 0.005

# Files
BUTTON_MAP_FILENAME = "button_map.json"  # Name of the button map file ("button_map.json" by default)
LOG_FILENAME = "xbxmacintegration.log"  # Name of the main logfile ("xbxmacintegration.log" by default)

keyboard = KeyboardController()


# Set up  an unreasonably optimized for controller input rotating file handler to keep maximum 10 backup files of 1MB
# each
rotating_handler = logging.handlers.RotatingFileHandler(
    filename=LOG_FILENAME,
    maxBytes=1000000,  # How many bytes for the main logfile to move onto the next (1000000 by default)
    backupCount=10  # How many backups of the log to keep (10 by default)
)

# Set up logging configuration
logger = logging.getLogger("xbxmacintegration")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
rotating_handler.setFormatter(formatter)
logger.addHandler(rotating_handler)
logger.addHandler(logging.StreamHandler())

# Default button mapping (Used to create config file, recommended not edit this version instead the automatically
# created one)
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


# Global dictionary to track button states and debounce timestamps
button_states = {}


exit_flag = threading.Event()


# Load button map or if it does not exist, create it
def load_button_map(filename):
    logger.info("Loading button map from file: %s", filename)
    if os.path.isfile(filename):
        with open(filename, "r") as f:
            return {str(k): v for k, v in json.load(f).items()}
    else:
        logger.warning("Button map file not found. Creating a new one with default values.")
        with open(filename, "w") as f:
            json.dump(DEFAULT_BUTTON_MAP, f)
        return DEFAULT_BUTTON_MAP


# Assign name to button when pressed
def map_button_to_name(button, button_map):
    return button_map.get(str(button), button)


# Do action when button is pressed
def handle_button_down(button_down, mouse):
    logger.info("Button down: %s", button_down)
    if button_down == "Exit":
        exit_flag.set()
    elif button_down == "A":
        if button_states.get("A", 0) + DEBOUNCE_DELAY <= time.monotonic():
            button_states["A"] = time.monotonic()
            mouse.press(Button.left)
    elif button_down == "Menu":
        if button_states.get("Menu", 0) + DEBOUNCE_DELAY <= time.monotonic():
            button_states["Menu"] = time.monotonic()
            mouse.press(Button.right)
    elif button_down == "B":  # Added "B" button action
        if button_states.get("B", 0) + DEBOUNCE_DELAY <= time.monotonic():
            button_states["B"] = time.monotonic()
            keyboard.press(Key.esc)  # Simulate pressing the "Esc" key
    else:
        return


# Do action when button is released
def handle_button_up(button_up, mouse):
    logger.info("Button up: %s", button_up)
    if button_up == "A":
        if button_states.get("A", 0) + DEBOUNCE_DELAY <= time.monotonic():
            button_states["A"] = time.monotonic()
            mouse.release(Button.left)
    elif button_up == "Menu":
        if button_states.get("Menu", 0) + DEBOUNCE_DELAY <= time.monotonic():
            button_states["Menu"] = time.monotonic()
            mouse.release(Button.right)
    elif button_up == "B":  # Added "B" button action
        if button_states.get("B", 0) + DEBOUNCE_DELAY <= time.monotonic():
            button_states["B"] = time.monotonic()
            keyboard.release(Key.esc)  # Simulate releasing the "Esc" key
    else:
        return


# Detect Controller
def initialize_controller():
    logger.info("Initializing pygame and joystick")
    pygame.init()
    pygame.joystick.init()
    controller = pygame.joystick.Joystick(0)
    controller.init()
    return controller


# Detect Axis
def handle_joystick_motion(controller, mouse):
    joystick_x_axis = controller.get_axis(0)
    joystick_y_axis = controller.get_axis(1)

    # Apply deadzone handling
    if abs(joystick_x_axis) < JOYSTICK_DEADZONE:
        joystick_x_axis = 0.0
    if abs(joystick_y_axis) < JOYSTICK_DEADZONE:
        joystick_y_axis = 0.0

    # Apply smoothing using exponential moving average
    smoothing_factor = 0.2  # Adjust this value for smoother or more responsive input
    joystick_x_axis = joystick_x_axis * (1 - smoothing_factor) + joystick_x_axis * smoothing_factor
    joystick_y_axis = joystick_y_axis * (1 - smoothing_factor) + joystick_y_axis * smoothing_factor

    joystick_x_axis *= JOYSTICK_SENSITIVITY
    joystick_y_axis *= JOYSTICK_SENSITIVITY

    # Check if the joystick velocities are within a valid range
    if not (-32768 <= joystick_x_axis <= 32767) or not (-32768 <= joystick_y_axis <= 32767):
        return

    mouse.move(int(joystick_x_axis), int(joystick_y_axis))


# Start receiving inputs
def run_controller_input(controller, mouse, button_map):
    logger.info("Starting controller input loop")

    # Initialize joystick velocities
    joystick_x_velocity = 0.0
    joystick_y_velocity = 0.0

    while not exit_flag.is_set():
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                button_down = map_button_to_name(event.button, button_map)
                handle_button_down(button_down, mouse)

            elif event.type == pygame.JOYBUTTONUP:
                button_up = map_button_to_name(event.button, button_map)
                handle_button_up(button_up, mouse)

        handle_joystick_motion(controller, mouse)

        # Reset velocities when joystick is released
        if joystick_x_velocity == 0.0 and joystick_y_velocity == 0.0:
            joystick_x_velocity = 0.0
            joystick_y_velocity = 0.0

        time.sleep(SLEEP_TIME)


# Main
def main():
    # Set up mouse controller
    mouse = Controller()

    # Load button map
    button_map = load_button_map(BUTTON_MAP_FILENAME)

    try:
        controller = initialize_controller()
        run_controller_input(controller, mouse, button_map)
    except FileNotFoundError:
        logger.error("Button map file not found.")
    except pygame.error:
        logger.critical("Controller could not be found.")
        exit(1)


if __name__ == "__main__":
    main()
