# Python SeleniumWebDriver and Threads POC

This code is an example on how to use multiple threads to validate a web page using selenium web driver

## Installation
I recomed using a virutal env, which you can set up using:
```bash
python3 -m venv env
source env/bin/activate
```

You can also add system variables to the venv/bin/activate to make sure they are available for your tests.

You can use pip3 to install the needed packages:
```bash
pip3 -m install <pacakage_name> 
```

selenium

You will also have to install the chrome, safari and firefox drivers. You can find them here:
https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/

The CV example is part of this folder but the absolute path will have to be modified in the app.py file to match your path.
