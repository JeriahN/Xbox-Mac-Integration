# Add Integration for the XBOX ONE and SERIES Controller to Mac
from pynput.mouse import Button, Controller  # PyInput.mouse for Cursor Management
from pynput.keyboard import Key, Controller as KeyboardController  # PyInput.keyboard for Keyboard Management
import pygame  # PyGame for controller detection and input
import logging.handlers  # Logging handler for easier debugging
import json  # JSON for more readable config file
import os.path  # Filesystem for creating and managing config file
import threading  # Multithreading for better optimization
import time  # Time for delays used in smoothing
from collections import defaultdict  # Imports some dictionaries or something

# Global Variables
smoothing_factor = 0.2  # Choose smoothness of scrolling and cursor movement
JOYSTICK_DEADZONE = 0  # Change deadzone of controller
JOYSTICK_SENSITIVITY = 20  # Change speed of controller based on movement of joystick
left_joystick_speed = 1  # Initial left joystick speed multiplied
right_joystick_speed = 1  # Initial right joystick speed multiplied

# Buttons
DEBOUNCE_DELAY = 0.03  # Change delay between button presses to avoid pressing twice

# Speed
SLEEP_TIME = 0.01  # Time between each time code is run (can affect smoothness dramatically if pushed too high)

# Files
BUTTON_MAP_FILENAME = "button_map.json"  # Name of the button map
KEYBOARD_MAP_FILENAME = "button_map.json"  # Name of the keyboard map
LOG_FILENAME = "xbxmacintegration.log"  # Name of the main log, others LOG_FILENAME(1, 2, 3)

keyboard = KeyboardController()

# Set up logging configuration
logger = logging.getLogger("xbxmacintegration")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
rotating_handler = logging.handlers.RotatingFileHandler(
    filename=LOG_FILENAME,
    maxBytes=1000000,
    backupCount=10
)
rotating_handler.setFormatter(formatter)
logger.addHandler(rotating_handler)
logger.addHandler(logging.StreamHandler())

# Default button mapping
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
    15: "Share"
}

# Default keyboard mapping
DEFAULT_KEYBOARD_MAP = {
    "A": "LEFT_CLICK",
    "B": "esc",
    "X": "x",
    "Y": "y",
    "Select": "Shift",
    "Home": "f4",
    "Menu": "RIGHT_CLICK",
    "LS": "LS",
    "RS": "RS",
    "LB": "LB",
    "RB": "RB",
    "Up_Arrow": "up",
    "Down_Arrow": "down",
    "Left_Arrow": "left",
    "Right_Arrow": "right",
    "Share": "f3"
}

# Global dictionary to track button states and debounce timestamps
button_states = defaultdict(int)

exit_flag = threading.Event()


# Load button map or create a new one
def load_map_file(filename, button_map):
    logger.info("Loading button map from file: %s", filename)
    if os.path.isfile(filename):
        with open(filename, "r") as f:
            return defaultdict(str, json.load(f))
    else:
        logger.warning("Button map file not found. Creating a new one with default values.")
        with open(filename, "w") as f:
            json.dump(button_map, f)
        return button_map


# Assign name to button when pressed
def map_button_to_name(button, button_map, keyboard_map):
    return button_map.get(str(button), button)


def handle_button_down(button_down, mouse):
    logger.info("Button down: %s", button_down)
    if button_down == "Exit":
        exit_flag.set()
    elif button_down == "A":
        if button_states.get("A", 0) + DEBOUNCE_DELAY <= time.monotonic():
            button_states["A"] = time.monotonic()
            mouse.press(Button.left)  # Simulate left mouse button press
    elif button_down == "Menu":
        if button_states.get("Menu", 0) + DEBOUNCE_DELAY <= time.monotonic():
            button_states["Menu"] = time.monotonic()
            mouse.press(Button.right)  # Simulate right mouse button press


def handle_button_up(button_up, mouse):
    logger.info("Button up: %s", button_up)
    if button_up == "A":
        if button_states.get("A", 0) + DEBOUNCE_DELAY <= time.monotonic():
            button_states["A"] = time.monotonic()
            mouse.release(Button.left)  # Simulate left mouse button release
    elif button_up == "Menu":
        if button_states.get("Menu", 0) + DEBOUNCE_DELAY <= time.monotonic():
            button_states["Menu"] = time.monotonic()
            mouse.release(Button.right)  # Simulate right mouse button release


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
    right_joystick_x_axis = controller.get_axis(2)
    right_joystick_y_axis = controller.get_axis(3)

    # Apply deadzone handling
    joystick_x_axis = joystick_x_axis if abs(joystick_x_axis) >= JOYSTICK_DEADZONE else 0.0
    joystick_y_axis = joystick_y_axis if abs(joystick_y_axis) >= JOYSTICK_DEADZONE else 0.0
    right_joystick_x_axis = right_joystick_x_axis if abs(right_joystick_x_axis) >= JOYSTICK_DEADZONE else 0.0
    right_joystick_y_axis = right_joystick_y_axis if abs(right_joystick_y_axis) >= JOYSTICK_DEADZONE else 0.0

    # Apply smoothing using exponential moving average
    joystick_x_axis = joystick_x_axis * (1 - smoothing_factor) + joystick_x_axis * smoothing_factor
    joystick_y_axis = joystick_y_axis * (1 - smoothing_factor) + joystick_y_axis * smoothing_factor
    right_joystick_x_axis = right_joystick_x_axis * (1 - smoothing_factor) + right_joystick_x_axis * smoothing_factor
    right_joystick_y_axis = right_joystick_y_axis * (1 - smoothing_factor) + right_joystick_y_axis * smoothing_factor

    joystick_x_axis *= JOYSTICK_SENSITIVITY
    joystick_y_axis *= JOYSTICK_SENSITIVITY
    right_joystick_x_axis *= JOYSTICK_SENSITIVITY
    right_joystick_y_axis *= JOYSTICK_SENSITIVITY

    joystick_x_axis *= left_joystick_speed
    joystick_y_axis *= left_joystick_speed
    right_joystick_x_axis *= right_joystick_speed
    right_joystick_y_axis *= right_joystick_speed

    if (-32768 <= joystick_x_axis <= 32767) and (-32768 <= joystick_y_axis <= 32767):
        mouse.move(int(joystick_x_axis), int(joystick_y_axis))
        mouse.scroll(int(-right_joystick_x_axis), int(-right_joystick_y_axis))
        pygame.time.wait(1)  # Add a small delay for smoother movement


# Start receiving inputs
def run_controller_input(controller, mouse, button_map, keyboard_map):
    logger.info("Starting controller input loop")

    while not exit_flag.is_set():
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                button_down = map_button_to_name(event.button, button_map, keyboard_map)
                handle_button_down(button_down, mouse)
            elif event.type == pygame.JOYBUTTONUP:
                button_up = map_button_to_name(event.button, button_map, keyboard_map)
                handle_button_up(button_up, mouse)

        handle_joystick_motion(controller, mouse)

        time.sleep(SLEEP_TIME)


# Main
def main():
    mouse = Controller()
    button_map = load_map_file(BUTTON_MAP_FILENAME, DEFAULT_BUTTON_MAP)
    keyboard_map = load_map_file(KEYBOARD_MAP_FILENAME, DEFAULT_KEYBOARD_MAP)

    try:
        controller = initialize_controller()
        run_controller_input(controller, mouse, button_map, keyboard_map)
    except FileNotFoundError:
        logger.error("Button map file not found.")
    except pygame.error:
        logger.critical("Controller could not be found.")
        exit(1)


if __name__ == "__main__":
    main()
