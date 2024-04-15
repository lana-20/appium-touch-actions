from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.interaction import POINTER_TOUCH
from selenium.webdriver.common.actions.mouse_button import MouseButton

APP = 'https://github.com/appium/android-apidemos/releases/download/v3.1.0/ApiDemos-debug.apk'
APPIUM = 'http://localhost:4723'
CAPS = {
    "platformName": "Android",
    "appium:options": {
        "platformVersion": "14.0",      # optional
        "deviceName": "Android Emulator",
        "automationName": "UiAutomator2",
        'app': APP
    }
}
OPTIONS = AppiumOptions().load_capabilities(CAPS)

driver = webdriver.Remote(
    command_executor=APPIUM,
    options=OPTIONS
)

try:
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located(
        (AppiumBy.ACCESSIBILITY_ID, 'Views'))).click()
    wait.until(EC.presence_of_element_located(
        (AppiumBy.ACCESSIBILITY_ID, 'Animation')))

    print(driver.get_window_size())     # {'width': 1080, 'height': 2201}

    actions = ActionBuilder(driver)
    finger = actions.add_pointer_input(POINTER_TOUCH, 'finger')
    finger.create_pointer_move(duration=0, x=100, y=1600)    # move_to_start
    finger.create_pointer_down(button=MouseButton.LEFT)    # press_down
    finger.create_pointer_move(duration=250, x=100, y=-1600, origin='pointer')    # move_to_end
    finger.create_pointer_up(button=MouseButton.LEFT)      # press_up
    actions.perform()

    driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Visibility')
    driver.get_screenshot_as_file('screencap.png')
finally:
    driver.quit()
