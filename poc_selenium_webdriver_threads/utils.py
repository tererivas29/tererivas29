from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions


def waitForElementCss(driver, cssSelector):
    return WebDriverWait(driver, timeout=3).until(
        expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, cssSelector))
    )


def waitForElementText(driver, text):
    pass
