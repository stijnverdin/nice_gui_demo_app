from selenium import webdriver
import time, pytest
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from .nice_gui_UI import NiceGuiUI
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
    driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))   
    yield driver
    # Teardown: close the WebDriver
    driver.quit() 

def test_my_app(browser):
    browser.get("http://127.0.0.1:8081")
    print(browser.title)
    time.sleep(3)
    system_planner_label = browser.find_element(By.XPATH, '//div[text()="PV System Planner"]')
    default_selection = browser.find_element(By.ID,'add_device_dropdown_selection')
    assert default_selection.text == "Fridge"

    "row-id"
def test_consumers_table(browser):
    browser.get("http://127.0.0.1:8081")
    selected_consumers_table = browser.find_element(By.ID,'selected_consumers_table')
    amount_of_rows = len(selected_consumers_table.find_elements(By.XPATH, "//*[@row-id]"))
    assert amount_of_rows == 0
    add_device_button = browser.find_element(By.ID,'add_selected_device_button')
    add_device_button.click()
    amount_of_rows = len(selected_consumers_table.find_elements(By.XPATH, "//*[@row-id]"))
    time.sleep(1)
    assert amount_of_rows == 1
    remove_last_button = browser.find_element(By.ID,'remove_last_device_button')
    remove_last_button.click()
    amount_of_rows = len(selected_consumers_table.find_elements(By.XPATH, "//*[@row-id]"))
    time.sleep(1)
    assert amount_of_rows == 0

@pytest.mark.skip(reason="Awaiting implementation")
def test_requirement():
    """
    Test to...
    TODO: Come up with a simple requirement
    
    """
    return

@pytest.mark.skip(reason="Awaiting implementation")
def test_your_own_idea():
    """ Implement your own test """
    return