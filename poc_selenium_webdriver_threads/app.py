from distutils.command.upload import upload
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
import utils


def test_career_portal_yes_violations_path(browser, url):
    driver = None
    # You can customize here and add more browser support
    if browser == "safari":
        driver = webdriver.Safari()
    elif browser == "firefox":
        driver = webdriver.Firefox()
    elif browser == "chrome":
        driver = webdriver.Chrome()

    if driver == None:
        exit()

    # launch career portal site
    driver.get(url)

    lets_go_button = utils.waitForElementCss(
        driver, ".mt-10 button.secondary[tabindex='-1']"
    )
    lets_go_button.click()

    page_title = utils.waitForElementCss(driver, ".slick-active .slick-active h1")
    assert page_title.text == "Have you had any moving violations in the last 5 years?"

    yes_button = utils.waitForElementCss(
        driver,
        ".slick-active .slick-active button:nth-of-type(2)",
    )
    yes_button.click()

    three_button = utils.waitForElementCss(
        driver, ".slick-active .career-action-vertical-buttons button:nth-of-type(3)"
    )
    three_button.click()

    page_title = utils.waitForElementCss(driver, ".slick-active .slick-active h1")
    assert (
        page_title.text
        == "Thanks, we’ll need more information around your moving violations at your interview."
    )

    continue_button = utils.waitForElementCss(
        driver, ".slick-current[data-index='2'] .career-action-buttons button.secondary"
    )
    continue_button.click()

    page_title = utils.waitForElementCss(driver, ".slick-active .slick-active h1")
    assert (
        page_title.text == "Have you been in any traffic accidents in the past 5 years?"
    )

    yes_button = utils.waitForElementCss(
        driver,
        ".slick-active .slick-active button:nth-of-type(2)",
    )
    yes_button.click()

    one_button = utils.waitForElementCss(
        driver, ".slick-active .career-action-vertical-buttons button:nth-of-type(1)"
    )
    one_button.click()

    page_title = utils.waitForElementCss(driver, ".slick-active .slick-active h1")
    assert (
        page_title.text
        == "Thanks, we’ll need more information around your traffic accidents at your interview."
    )

    continue_button = utils.waitForElementCss(
        driver, ".slick-active .slick-current[data-index='2'] .career-action-buttons"
    )
    continue_button.click()

    page_title = utils.waitForElementCss(driver, ".slick-active .slick-active h1")
    assert (
        page_title.text
        == "Have you had a suspended or revoked license in the last 3 years?"
    )

    no_button = utils.waitForElementCss(
        driver,
        ".slick-active .slick-active button:nth-of-type(1)",
    )
    no_button.click()

    page_title = utils.waitForElementCss(driver, ".slick-active .slick-active h1")
    assert (
        page_title.text
        == "Have you ever been convicted of driving under the influence?"
    )

    no_button = utils.waitForElementCss(
        driver,
        ".slick-active .slick-active button:nth-of-type(1)",
    )
    no_button.click()

    page_title = utils.waitForElementCss(driver, ".slick-active .slick-active h1")
    assert (
        page_title.text
        == "Do you have any driving or DOT regulated jobs in the past 10 years?"
    )

    yes_button = utils.waitForElementCss(
        driver,
        ".slick-active .slick-active button:nth-of-type(2)",
    )
    yes_button.click()

    resume_box = utils.waitForElementCss(
        driver,
        ".slick-active .dot-upload-box",
    )
    resume_box.click()

    upload_title = utils.waitForElementCss(driver, ".slick-active .text-xl")
    assert upload_title.text == "Upload a file"

    utils.waitForElementCss(driver, ".slick-active label.upload-type-button")

    upload_button = driver.find_element(By.CSS_SELECTOR, "#input-file")

    upload_button.send_keys(
        "/Users/teresa.rivas/Documents/CR England/CAR_AUTOMATION_PYTHON/lizbennetcv.png"
    )

    upload_info = utils.waitForElementCss(
        driver, ".upload-file-info-container .upload-file-info-name"
    )
    assert "lizbennetcv" in upload_info.text

    # Close the browser and exit webdriver
    driver.quit()
