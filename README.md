<h2>Xbox Mac Integration</h2>
 A small python script that improves upon the Xbox controller Integration in MacOS.
<h2>How to use</h2>
<ul>
<li>Download Source or download latest from releases</li>
<li>NOTE: If you download from source make sure to install pyinput</li>
<li>Run the <code>Xbox-Mac-Integration</code> file from the <code>.zip</code> archive downloaded</li>
<li>NOTE: If you download from source run <code>python3 main.py</code></li>
</ul>
<ul>
<li>Move <code>left joystick</code> to move the cursor</li>
<li>Press <code>A</code> to left-click</li>
<li>Press <code>Menu</code> to right-click</li>
<li>Hold <code>Button</code> to hold</li>
</ul>
<h2>Build from source</h2>
<ul>
<li>Go to same directory as <code>main.py</code> and run <code>pyinstaller --onefile --noconsole main.py</code></li>
<li>NOTE: Make sure to installer <code>PyInstaller</code> <code>(pip3 install pyinstaller)</code></li>
<li>Output file will be in <code>dist</code> folder</li>
<li>Run the <code>main</code> file</li>
</ul>
<h2>ChatGPT's Interpretation</h2>
<span>
This is a Python script that allows a user to control their computer mouse using an Xbox controller. The script uses the <b>'pygame'</b> library to handle the controller input and the <b>'pynput'</b> library to handle the mouse movements and clicks. The script also uses the <b>'logging'</b> library to log outputs and <b>'json'</b> library to handle an external button map configuration.

The script first sets up a rotating file handler for the logs, which keeps a maximum of 10 backup files of 1MB each. Then, the logging configuration is set up to include the level, time, log message, and the handlers.

Next, the script defines a default button map, which maps the Xbox controller buttons to their corresponding names. It then reads the button map from a JSON file, or creates one with the default button map if the file does not exist. If an error occurs while reading the button map or creating a new one, the script logs an error and loads the default button map.

After that, the script initializes the <b>'pygame'</b> and <b>'pynput'</b> libraries, and detects the Xbox controller. It sets the dead-zone and sensitivity variables for the controller input.

The script then defines a function <b>'MAP_BUTTON_TO_NAME'</b>, which takes a button as an argument and returns the corresponding button name based on the button map.

Finally, the script defines a function run_controller_input to continuously run a loop that handles the controller input. It listens for the joystick axis motion and joystick button events, applies dead-zones and sensitivity settings, and moves the mouse or performs clicks based on the corresponding button mapping. The loop exits if the "Exit" button is pressed, which terminates the program.

The script then starts the <b>'run_controller_input'</b> function in a background process.
</span>
