from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os

def get_driver():
    # Configurar opciones para hacer la navegación más sencilla
    options = webdriver.ChromeOptions()
    options.add_argument("disable-infobars")  # Deshabilitar las barras de información
    options.add_argument("start-maximized")  # Iniciar navegador maximizado
    options.add_argument("disable-dev-shm-usage")  # Evitar el uso compartido de la memoria
    options.add_argument("no-sandbox")  # Desactivar el modo sandbox para evitar problemas de seguridad
    options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Excluir switches de automatización
    options.add_argument("disable-blink-features=AutomationControlled")  # Deshabilitar las características de automatización de blink
    
    # Desactivar el mensaje de guardar contraseña
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    }
    options.add_experimental_option("prefs", prefs)

    # Inicializar el driver de Chrome con las opciones configuradas
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1200, 900)  # Configurar el tamaño de la ventana (mitad del tamaño típico de la pantalla)
    # Posicionar la ventana en la esquina superior derecha de la pantalla
    # driver.set_window_position(730, 0)  # Ajustar la coordenada x según la resolución de la pantalla

    # Navegar a la página principal
    driver.get("https://www.promofarma.com/")
    return driver

def main():
    driver = get_driver()
    time.sleep(2)  # Esperar 2 segundos para que la página cargue completamente

    # Aceptar todas las cookies
    driver.find_element(by="id", value="onetrust-accept-btn-handler").click()
    time.sleep(1)  # Esperar 2 segundos para que las cookies sean aceptadas
    
    # Hacer clic en el botón "mi cuenta"
    driver.find_element(by='xpath', value="/html/body/main/div[1]/div/div[2]/div[2]/div[1]/div[1]/span").click()
    time.sleep(1)
    
    # Hacer clic en el enlace "Iniciar sesión"
    driver.find_element(by='xpath', value="//a[contains(text(),'Iniciar sesión')]").click()
    time.sleep(2)  # Esperar 2 segundos para que la página de inicio de sesión cargue

    # Encontrar y completar los campos de nombre de usuario y contraseña
    driver.find_element(by="id", value="username").send_keys("angelmaria76@gmail.com")
    time.sleep(1)
    driver.find_element(by='id', value="login_submit").click()
    time.sleep(1)
    driver.find_element(by="id", value="login_password").send_keys("angelottipavarotti" + Keys.RETURN)
    time.sleep(1)  # Esperar 2 segundos para que el login se procese
    # Estoy dentro de promofarma
    driver.find_element(by='xpath', value="/html/body/main/div[1]/div/div[2]/div[3]/div/input").send_keys("somatoline reductor 7 noches gel fresco 400ml" + Keys.RETURN)
    time.sleep(3)

    price_element = driver.find_element(by='xpath', value="/html/body/div[1]/div[2]/section/div[3]/div[2]/section/div/div[1]/article/div[3]/div[2]/div/div[2]/span")
    product_price = price_element.text
    time.sleep(2)

    # Obtener la URL actual después de seleccionar el producto
    current_url = driver.current_url
    driver.quit()
    
    return current_url, product_price

if __name__ == "__main__":
    # Ejecutar la función principal y obtener la URL y el precio del producto
    logged_in_url, product_price = main()
    print(f"URL: {logged_in_url}")
    print(f"Precio: {product_price}")
    
    # Construir la ruta al archivo en la raíz del proyecto
    project_root = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(project_root, "logged_in_prices.txt")
    
    # Agregar la URL y el precio al archivo
    with open(file_path, "a") as file:
        file.write(f"{logged_in_url} - Precio: {product_price}\n")