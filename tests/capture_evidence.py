import json
import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = os.getenv("BASE_URL", "http://localhost:8080")
IMG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "img")
os.makedirs(IMG_DIR, exist_ok=True)


def shot(driver, name):
    path = os.path.join(IMG_DIR, name)
    driver.save_screenshot(path)
    print(f"captura: {path}")


def wait_rows(driver, count=1):
    WebDriverWait(driver, 15).until(
        lambda d: len(d.find_elements(By.CSS_SELECTOR, "#productsTable tbody tr")) == count
    )


options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1400,900")
options.set_capability("goog:loggingPrefs", {"browser": "ALL"})

driver = webdriver.Chrome(options=options)
try:
    driver.get(BASE_URL)
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "addProduct")))
    time.sleep(1)
    shot(driver, "01-app-local.png")

    driver.find_element(By.ID, "name").send_keys("Laptop")
    driver.find_element(By.ID, "price").send_keys("15000")
    driver.find_element(By.ID, "addProduct").click()
    wait_rows(driver, 1)
    time.sleep(1)
    shot(driver, "02-manual-agregar.png")

    stored = driver.execute_script("return localStorage.getItem('products');")
    with open(os.path.join(IMG_DIR, "localstorage-local.json"), "w", encoding="utf-8") as fh:
        json.dump(json.loads(stored), fh, indent=2, ensure_ascii=False)
    print("localStorage:", stored)

    driver.refresh()
    wait_rows(driver, 1)
    time.sleep(1)
    shot(driver, "05-manual-persistencia.png")

    driver.find_element(By.CSS_SELECTOR, ".delete-btn").click()
    WebDriverWait(driver, 15).until(
        lambda d: len(d.find_elements(By.CSS_SELECTOR, "#productsTable tbody tr")) == 0
    )
    time.sleep(1)
    shot(driver, "03-manual-eliminar.png")

    driver.find_element(By.ID, "price").send_keys("0")
    driver.find_element(By.ID, "addProduct").click()
    alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert_text = alert.text
    print("alerta:", alert_text)
    with open(os.path.join(IMG_DIR, "04-manual-validacion.txt"), "w", encoding="utf-8") as fh:
        fh.write(alert_text + "\n")
    alert.accept()
    time.sleep(1)
    shot(driver, "04-manual-validacion.png")

    logs = driver.get_log("browser")
    errors = [entry for entry in logs if entry.get("level") == "SEVERE"]
    print("errores de consola:", len(errors))
finally:
    driver.quit()
