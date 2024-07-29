from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("disable-infobars")
    options.add_argument("start-maximized")
    options.add_argument("disable-dev-shm-usage")
    options.add_argument("no-sandbox")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("disable-blink-features=AutomationControlled")
    
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    }
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1200, 900)
    driver.get("https://www.promofarma.com/")
    return driver

def main():
    driver = get_driver()
    wait = WebDriverWait(driver, 10)  # Esperar hasta 10 segundos

    try:
        # Aceptar todas las cookies
        accept_cookies_btn = wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
        accept_cookies_btn.click()

        # Hacer clic en el botón "mi cuenta"
        account_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/main/div[1]/div/div[2]/div[2]/div[1]/div[1]/span")))
        account_btn.click()

        # Hacer clic en el enlace "Iniciar sesión"
        login_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Iniciar sesión')]")))
        login_link.click()

        # Encontrar y completar los campos de nombre de usuario y contraseña
        username_input = wait.until(EC.visibility_of_element_located((By.ID, "username")))
        username_input.send_keys("angelmaria76@gmail.com")
        login_submit_btn = driver.find_element(By.ID, "login_submit")
        login_submit_btn.click()
        password_input = wait.until(EC.visibility_of_element_located((By.ID, "login_password")))
        password_input.send_keys("angelottipavarotti" + Keys.RETURN)

        # Buscar el producto
        search_input = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/main/div[1]/div/div[2]/div[3]/div/input")))
        search_input.send_keys("somatoline reductor 7 noches gel fresco 400ml" + Keys.RETURN)

        # Seleccionar el producto correcto de la lista de resultados
        product_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Somatoline® Reductor 7 Noches Gel Fresco 400ml')]")))
        product_link.click()

        # Obtener el precio del producto
        price_element = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/section/section[1]/div[1]/div[2]/div[1]/div/div/div/div[1]/div[1]/span")))
        product_price = price_element.text

        current_url = driver.current_url
    except Exception as e:
        print(f"An error occurred: {e}")
        current_url, product_price = None, "Price not found"
    finally:
        driver.quit()

    return current_url, product_price

if __name__ == "__main__":
    logged_in_url, product_price = main()
    print(f"URL: {logged_in_url}")
    print(f"Precio: {product_price}")

    # Construir la ruta al archivo en la raíz del proyecto
    project_root = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(project_root, "logged_in_prices.txt")

    # Agregar la URL y el precio al archivo
    with open(file_path, "a") as file:
        file.write(f"{logged_in_url} - Precio: {product_price}\n")
