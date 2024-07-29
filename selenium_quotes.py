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

    # Configurar el perfil de usuario de Chrome
    user_data_dir = "C:/Users/Person 1/AppData/Local/Google/Chrome/User Data"  # Ruta a la carpeta User Data de Chrome
    options.add_argument(f"user-data-dir={user_data_dir}")  # Usar el perfil de usuario

    # Inicializar el driver de Chrome con las opciones configuradas
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(800, 900)  # Configurar el tamaño de la ventana (mitad del tamaño típico de la pantalla)
    # Posicionar la ventana en la esquina superior derecha de la pantalla
    driver.set_window_position(730, 0)  # Ajustar la coordenada x según la resolución de la pantalla

    # Navegar a la página principal
    driver.get("https://quotes.toscrape.com/")
    return driver

def main():
    driver = get_driver()
    time.sleep(2)  # Esperar 2 segundos para que la página cargue completamente
    
    # Hacer clic en el enlace de login
    driver.find_element(by='xpath', value="/html/body/div/div[1]/div[2]/p/a").click()
    time.sleep(2)  # Esperar 2 segundos para que la página de login cargue

    # Encontrar y completar los campos de nombre de usuario y contraseña
    driver.find_element(by="id", value="username").send_keys("admin")
    time.sleep(2)
    driver.find_element(by="id", value="password").send_keys("admin" + Keys.RETURN)
    time.sleep(2)  # Esperar 2 segundos para que el login se procese

    # Encontrar y hacer clic en el primer enlace de Goodreads
    driver.find_element(by="xpath", value="/html/body/div/div[2]/div[1]/div[1]/span[2]/a[2]").click()
    time.sleep(2)  # Esperar 2 segundos para que la página de Goodreads cargue
    
    # Obtener la URL actual (la de Goodreads) y cerrar el navegador
    current_url = driver.current_url
    driver.quit()
    return current_url

if __name__ == "__main__":
    # Ejecutar la función principal y obtener la URL de Goodreads
    goodreads_url = main()
    print(goodreads_url)
    
    # Construir la ruta al archivo en la raíz del proyecto
    project_root = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(project_root, "goodreads_urls.txt")
    
    # Agregar la URL al archivo
    with open(file_path, "a") as file:
        file.write(goodreads_url + "\n")
