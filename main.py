from pynput.mouse import Button, Controller
import pygame
import logging.handlers
import json
import os.path
import threading

# Constants
JOYSTICK_DEADZONE = 0
JOYSTICK_SENSITIVITY = 5
BUTTON_MAP_FILENAME = "button_map.json"
LOG_FILENAME = "xbxmacintegration.log"

# Set up rotating file handler to keep maximum 10 backup files of 1MB each
rotating_handler = logging.handlers.RotatingFileHandler(
    filename=LOG_FILENAME,
    maxBytes=1000000,
    backupCount=10
)

# Set up logging configuration
logger = logging.getLogger("xbxmacintegration")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
rotating_handler.setFormatter(formatter)
logger.addHandler(rotating_handler)
logger.addHandler(logging.StreamHandler())

# Default button map
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

exit_flag = threading.Event()


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


def map_button_to_name(button, button_map):
    return button_map.get(str(button), button)


def handle_button_down(button_down, mouse):
    logger.info("Button down: %s", button_down)
    if button_down == "Exit":
        exit_flag.set()
    elif button_down == "A":
        mouse.press(Button.left)
    elif button_down == "Menu":
        mouse.press(Button.right)


def handle_button_up(button_up, mouse):
    logger.info("Button up: %s", button_up)
    if button_up == "A":
        mouse.release(Button.left)
    elif button_up == "Menu":
        mouse.release(Button.right)


def initialize_controller():
    logger.info("Initializing pygame and joystick")
    pygame.init()
    pygame.joystick.init()
    controller = pygame.joystick.Joystick(0)
    controller.init()
    return controller


def run_controller_input(controller, mouse, button_map):
    logger.info("Starting controller input loop")
    while not exit_flag.is_set():
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                button_down = map_button_to_name(event.button, button_map)
                handle_button_down(button_down, mouse)

            elif event.type == pygame.JOYBUTTONUP:
                button_up = map_button_to_name(event.button, button_map)
                handle_button_up(button_up, mouse)

            elif event.type == pygame.JOYAXISMOTION:
                handle_joystick_motion(controller, mouse)


def handle_joystick_motion(controller, mouse):
    joystick_x_axis = controller.get_axis(0)
    joystick_y_axis = controller.get_axis(1)

    if abs(joystick_x_axis) < JOYSTICK_DEADZONE:
        joystick_x_axis = 0.0
    if abs(joystick_y_axis) < JOYSTICK_DEADZONE:
        joystick_y_axis = 0.0

    joystick_x_axis *= JOYSTICK_SENSITIVITY
    joystick_y_axis *= JOYSTICK_SENSITIVITY

    mouse.move(int(joystick_x_axis), int(joystick_y_axis))


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
