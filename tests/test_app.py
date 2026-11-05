import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = os.getenv("BASE_URL", "http://localhost:8080")
IMG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "img")
os.makedirs(IMG_DIR, exist_ok=True)


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1400,900")
    browser = webdriver.Chrome(options=options)
    browser.get(BASE_URL)
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.ID, "addProduct")))
    browser.execute_script("localStorage.clear();")
    browser.refresh()
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.ID, "addProduct")))
    yield browser
    browser.quit()


def add_product(browser, name, price):
    browser.find_element(By.ID, "name").send_keys(name)
    browser.find_element(By.ID, "price").send_keys(str(price))
    browser.find_element(By.ID, "addProduct").click()


def test_add_product(driver):
    add_product(driver, "Laptop", 15000)
    row = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#productsTable tbody tr"))
    )
    assert "Laptop" in row.text
    assert "15000" in row.text
    driver.save_screenshot(os.path.join(IMG_DIR, "11-selenium-agregar.png"))


def test_delete_product(driver):
    add_product(driver, "Mouse", 250)
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#productsTable tbody tr"))
    )
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".delete-btn"))
    ).click()
    WebDriverWait(driver, 30).until(
        lambda d: len(d.find_elements(By.CSS_SELECTOR, "#productsTable tbody tr")) == 0
    )
    driver.save_screenshot(os.path.join(IMG_DIR, "11-selenium-eliminar.png"))


def test_persistence_after_reload(driver):
    add_product(driver, "Teclado", 500)
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#productsTable tbody tr"))
    )
    driver.refresh()
    row = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#productsTable tbody tr"))
    )
    assert "Teclado" in row.text
    driver.save_screenshot(os.path.join(IMG_DIR, "11-selenium-persistencia.png"))
