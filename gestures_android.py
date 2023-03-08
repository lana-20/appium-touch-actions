from os import path
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.interaction import POINTER_TOUCH
from selenium.webdriver.common.actions.mouse_button import MouseButton

CUR_DIR = path.dirname(path.abspath(__file__))
APP = path.join(CUR_DIR, 'TheApp.apk')
APPIUM = 'http://localhost:4723'
CAPS = {
    'platformName': 'Android',
    'deviceName': 'Android Emulator',
    'automationName': 'UiAutomator2',
    'app': APP,
}

driver = webdriver.Remote(APPIUM, CAPS)
try:
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located(
        (MobileBy.ACCESSIBILITY_ID, 'List Demo'))).click()
    wait.until(EC.presence_of_element_located(
        (MobileBy.ACCESSIBILITY_ID, 'Altocumulus')))

    actions = ActionBuilder(driver)
    finger = actions.add_pointer_input(POINTER_TOUCH, "finger")
    finger.create_pointer_move(duration=0, x=100, y=500)
    finger.create_pointer_down(MouseButton.LEFT)
    finger.create_pointer_move(duration=250, x=0, y=-500, origin="pointer")
    finger.create_pointer_up(MouseButton.LEFT)
    actions.perform()

    driver.find_element(MobileBy.ACCESSIBILITY_ID, 'Stratocumulus')
finally:
    driver.quit()
