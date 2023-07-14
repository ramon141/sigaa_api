from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from xpaths import *

def createDriver() -> webdriver.Chrome:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    prefs = {"profile.managed_default_content_settings.images":2}
    chrome_options.headless = True


    chrome_options.add_experimental_option("prefs", prefs)
    myDriver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    return myDriver

def getGoogleHomepage(driver: webdriver.Chrome) -> str:
    driver.get("https://www.google.com")
    return driver.page_source

def doBackgroundTask(inp):
    print("Doing background task")
    print(inp.msg)
    print("Done")

def get_user(driver: webdriver.Chrome, username, password, institution='ufopa'):
    user = {
        'name': '',
        'institute': '',
        'course': '',
        'role': '',
        'picture': ''
    }

    base_path = 'https://sigaa.' + institution + '.edu.br'
    login(driver, base_path, username, password)
    
    user['name'] = driver.find_element(By.XPATH, MAIN_SPAN_NAME).text
    user['picture'] = driver.find_element(By.XPATH, MAIN_IMG_USER).screenshot_as_base64
    user['role'] = 'discente'
    user['course'] = driver.find_element(By.XPATH, MAIN_SPAN_COURSE).text
    user['institute'] = driver.find_element(By.XPATH, MAIN_SPAN_INSTITUTE).text

    return user

def login(driver: webdriver.Chrome, base_path, user, password):
    driver.get(base_path + '/sigaa/verTelaLogin.do')
    driver.find_element(By.XPATH, LOGIN_INPUT_USER).send_keys(user)
    driver.find_element(By.XPATH, LOGIN_INPUT_PASSWORD).send_keys(password)
    driver.find_element(By.XPATH, LOGIN_BUTTON_SUBMIT).click()

    WebDriverWait(driver, 10).until(
        # Espera até o nome aparecer
        EC.presence_of_element_located((By.XPATH, MAIN_SPAN_NAME))
    )

    driver.find_element(By.XPATH, BTN_TO_MENU_STUDENT).click()
    WebDriverWait(driver, 10).until(
        # Espera até o nome aparecer
        EC.presence_of_element_located((By.XPATH, BTN_UPDATE_PERSONAL_DATA))
    )