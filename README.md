# Xbox Controller Integration for Mac (or linux or pc)

This project provides integration between Xbox One and Xbox Series controllers with Mac computers. It allows you to use your Xbox controller as a mouse and keyboard input device on your Mac.

## Features
- Cursor control: Use the left joystick of your Xbox controller to move the mouse cursor on your Mac screen.
- Mouse clicks: Use the Xbox controller buttons to simulate left and right mouse button clicks.
- Scroll functionality: Utilize the right joystick of your Xbox controller to scroll vertically and horizontally.
- Button mapping: Customize the button assignments to match your preferences using a JSON configuration file.
- Debounce handling: Prevent accidental button triggers with a configurable debounce delay.
- Smoothing and sensitivity control: Apply smoothing algorithms and adjust sensitivity to fine-tune the controller's responsiveness.

## Requirements
- A controller supported with `PyGame`
- `Python 3`
- `Pygame library`
- `pynput library`

## Build & Run [Or download a release](https://github.com/JeriahN/Xbox-Mac-Integration/releases)
1. Connect your Xbox controller to your Mac.
2. Install the required Python libraries: Pygame and pynput.
3. Download or clone this repository: `git clone https://github.com/JeriahN/Xbox-Mac-Integration.git`.
4. Customize the button mappings in the `button_map.json` file if desired.
5. Run the `xbxmacintegration.py` script.
6. Enjoy using your Xbox controller as a mouse and keyboard on your Mac!

## License
This project is licensed under the [MIT License](LICENSE).

Feel free to contribute by submitting bug reports, feature requests, or pull requests. Any feedback and contributions are greatly appreciated!
