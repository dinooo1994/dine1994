from flask import Flask, render_template, request
from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# import os 
import time

app = Flask(__name__)
def click_on_elements(driver):
    try:
        # Wait for the element to be present
        first_element_to_click = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.ship-to--menuItem--WdBDsYl'))
        )
        # first_element_to_click = driver.find_element(By.CSS_SELECTOR, '.ship-to--menuItem--WdBDsYl')
        action = ActionChains(driver)
        action.move_to_element(first_element_to_click).click().perform()        
        time.sleep(0.1)

        third_element_to_click = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.select--text--1b85oDo'))
        )
        action = ActionChains(driver)
        action.move_to_element(third_element_to_click).click().perform()
        time.sleep(0.1)
        
        fourth_element_to_click = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.select--item--32FADYB'))
        )
        action = ActionChains(driver)
        action.move_to_element(fourth_element_to_click).click().perform()
        time.sleep(0.6)

        second_element_to_click = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.es--saveBtn--w8EuBuy'))
        )
        # second_element_to_click = driver.find_element(By.CSS_SELECTOR, '.es--saveBtn--w8EuBuy')
        action = ActionChains(driver)
        action.move_to_element(second_element_to_click).click().perform()
    except Exception as e:
        print(f"Error clicking on the specified elements: {e}")

def extract_numerical_value(text):
    try:
        return float(''.join(c for c in text if c.isdigit() or c in ['.', ',']))
    except ValueError:
        print("Error!! in extract_numerical_value function...")
        return 0

def scrape_and_display(product_url):
    print("============Start Selenuim==========")
    chrome_options = webdriver.ChromeOptions()
    # print("Current directory:", os.getcwd())
    # print("List files in the current directory:", os.listdir())
    # drivers_directory = "./drivers"
    # files_in_drivers = os.listdir(drivers_directory)
    # print("List files in the 'drivers' directory:", files_in_drivers)
    # chrome_options.binary_location = os.environ.get("/usr/bin/google-chrome")
    # chrome_driver_path = ChromeDriverManager().install()
    chrome_driver_path = "drivers/chromedriver"
    service = webdriver.ChromeService(executable_path= chrome_driver_path)
    
    # service = webdriver.ChromeService(executable_path= ChromeDriverManager().install())
    # chrome_options.add_argument("--window-size=1920,1080")
    # chrome_options.add_argument("--disable-extensions")
    # chrome_options.add_argument("--proxy-server='direct://'")
    # chrome_options.add_argument("--proxy-bypass-list=*")
    # chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--allow-running-insecure-content')
    chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument('--lang=de-DE')
    # user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.85 Safari/537.36'
    # chrome_options.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    result = {
        "result_text": "",
        "price": 0,
        "shipping": 0,
        "total": 0,
        "get_day": 0  
    }
    product_price = 0
    shipping_price = 0
    total_value = 0 
    try:
        driver.get(product_url)
        time.sleep(0.1)
        click_on_elements(driver)
        time.sleep(1)
        xpath = '//img[@class="price-banner--slogan--SlQzWHE pdp-comp-banner-slogan"]'
        image_elements = driver.find_elements(By.XPATH, xpath)
        target_image_url = "https://ae01.alicdn.com/kf/Sabdabe1e0ed84a179ab6c06fc9f316769/380x144.png_.webp"
        if image_elements or target_image_url in driver.page_source:
            sentence = "عرض ترحيب"
            print(sentence)
            result["result_text"] = sentence
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        product_price_element = soup.find('div', class_='es--wrap--erdmPRe')
        product_price_text = product_price_element.text.strip().replace('€', '') if product_price_element else 'Not found'
        # print("=================product_price_text============")
        # print(product_price_text, product_price_element.text)
        # print("===============================")
        shipping_price_element = soup.find('div', class_='dynamic-shipping-titleLayout')
        shipping_price_text = shipping_price_element.text.strip().replace('€', '') if shipping_price_element else 'Not found'
        relevant_shipping_info = shipping_price_text.split(':')[-1].strip()
        product_price = extract_numerical_value(product_price_text)
        shipping_price = extract_numerical_value(relevant_shipping_info)
        total_value = product_price + shipping_price
        if total_value > 0:
            if total_value < 4:
                result['get_day'] = total_value * 239 + 300
            elif total_value < 6:
                result['get_day'] = total_value * 239 + 350
            elif total_value < 7:
                result['get_day'] = total_value * 239 + 400
            elif total_value < 8:
               result['get_day'] = total_value * 239 + 450
            elif total_value < 12:
                result['get_day'] = total_value * 239 + 500
            elif total_value < 16:
                result['get_day'] = total_value * 239 + 700
            elif total_value < 20:
                 result['get_day'] = total_value * 239 + 800
            elif total_value < 24:
               result['get_day'] = total_value * 239 + 900
            elif total_value < 28:
               result['get_day'] = total_value * 239 + 1000
            elif total_value < 35:
               result['get_day'] = total_value * 239 + 1100
            elif total_value < 40:
               result['get_day'] = total_value * 239 + 1200
            elif total_value < 50:
               result['get_day'] = total_value * 239 + 1300
            elif total_value < 60:
               result['get_day'] = total_value * 239 + 1400
            elif total_value < 70:
                 result['get_day'] = total_value * 239 + 1500
            elif total_value < 80:
                result['get_day'] = total_value * 239 + 1600
            elif total_value < 90:
               result['get_day'] = total_value * 239 + 1700
            elif total_value < 100:
                result['get_day'] = total_value * 239 + 1800
            elif total_value < 110:
               result['get_day'] = total_value * 239 + 1900
            elif total_value < 120:
               result['get_day'] = total_value * 239 + 2000
            elif total_value < 130:
               result['get_day'] = total_value * 239 + 2100
            elif total_value < 140:
               result['get_day'] = total_value * 239 + 2200
            elif total_value < 150:
               result['get_day'] = total_value * 239 + 2300
            elif total_value < 160:
               result['get_day'] = total_value * 239 + 2400
            elif total_value < 170:
               result['get_day'] = total_value * 239 + 2500
            elif total_value < 180:
               result['get_day'] = total_value * 239 + 2600
            elif total_value < 190:
                result['get_day'] = total_value * 239 + 2700
            elif total_value < 200:
               result['get_day'] = total_value * 239 + 2800
            elif total_value < 230:
                result['get_day'] = total_value * 239 + 2900
            elif total_value < 260:
                result['get_day'] = total_value * 239 + 3000
            elif total_value < 280:
               result['get_day'] = total_value * 239 + 3100
            elif total_value < 300:
               result['get_day'] = total_value * 239 + 3400
            elif total_value >= 300:
                z = total_value / 100
                result['get_day'] = total_value * 239 + z * 1600
            mod = result['get_day'] % 50
            if mod != 0:
                result['get_day'] = result['get_day'] + 50 - mod
    except Exception as e:
        print(f"Error during scraping: {e}")
        result["error"] = str(e)
    finally:
        driver.quit()
    result.update({
        "price": product_price,
        "shipping": shipping_price,
        "total": total_value,
    })
    return result
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        product_url = request.form['product_url']
        result = scrape_and_display(product_url)
        return render_template('index.html', result=result)
    return render_template('index.html', result=None)
if __name__ == '__main__':
    app.run(debug=False, threaded=True)