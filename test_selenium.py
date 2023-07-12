from selenium import webdriver
import time, pytest, os
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from .nice_gui_UI import NiceGuiUI, potential_consumers
from selenium.webdriver.common.by import By


@pytest.fixture(scope="session", autouse=True)
def web_service(request):
    print("Start APP")
    # Start the web service process
    nicegui_ui = NiceGuiUI()
    nicegui_ui.start_UI()
    time.sleep(2)  # Give some time for the web service to start up
    yield
    # Teardown: close the web service process
    print("Kill APP")
    nicegui_ui.stop_UI()

@pytest.fixture
def browser():
    # Setup: initialize the WebDriver
    browser_options = Options()
    if os.environ.get('HEADLESS', False): browser_options.add_argument('--headless=new')
    driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=browser_options)   
    yield driver
    # Teardown: close the WebDriver
    driver.quit() 

def test_default_selection(browser):
    browser.get("http://127.0.0.1:8081")
    print(browser.title)
    time.sleep(1)
    default_selection = browser.find_element(By.ID,'add_device_dropdown_selection')
    assert default_selection.text == "Fridge"

def test_consuption_preview(browser):
    browser.get("http://127.0.0.1:8081")
    device = potential_consumers[1]
    peak_power_label = browser.find_element(By.ID,'daily_consumption_label')
    add_device_dropdown_selection = browser.find_element(By.ID,'add_device_dropdown_selection')
    add_device_dropdown_selection.click()
    time.sleep(1)
    option_xpath = f"//div[@class='q-item__label']/span[contains(text(), '{device['device_name']}')]"
    option = browser.find_element(By.XPATH, option_xpath)
    option.click()
    assert peak_power_label.text == f"Daily consumption: {device['peak_power']} wH"

def test_consumers_table(browser):
    browser.get("http://127.0.0.1:8081")
    selected_consumers_table = browser.find_element(By.ID,'selected_consumers_table')
    amount_of_rows = len(selected_consumers_table.find_elements(By.XPATH, "//*[@row-id]"))
    assert amount_of_rows == 0
    add_device_button = browser.find_element(By.ID,'add_selected_device_button')
    add_device_button.click()
    time.sleep(1)
    add_device_button.click()
    amount_of_rows = len(selected_consumers_table.find_elements(By.XPATH, "//*[@row-id]"))
    assert amount_of_rows == 1
    remove_last_button = browser.find_element(By.ID,'remove_last_device_button')
    remove_last_button.click()
    amount_of_rows = len(selected_consumers_table.find_elements(By.XPATH, "//*[@row-id]"))
    time.sleep(1)
    assert amount_of_rows == 0

@pytest.mark.skip(reason="Awaiting implementation")
def test_maximum_peak_power_calculation():
    """
    Add 3 devices from the list and check if the "Maximum peak power" label ('id=maximum_peak_power_label') is the sum of the individual devices peak power.
    """
    return

@pytest.mark.skip(reason="Awaiting implementation")
def test_remove_last_device_button():
    """
    Checks if 'remove last device' button ('id=remove_last_device_button') removes from list the last added device.
    """
    return

@pytest.mark.skip(reason="Awaiting implementation")
def test_your_own_idea():
    """ Implement your own test """
    return

