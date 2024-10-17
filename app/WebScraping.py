import time
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Función para inicializar el driver de Selenium
def iniciar_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ejecutar en modo headless (sin GUI)
    chrome_options.add_argument("--no-sandbox")  # Evitar problemas de permisos en contenedores
    chrome_options.add_argument("--disable-dev-shm-usage")  # Solucionar problemas de almacenamiento en /dev/shm
    chrome_options.add_argument("--disable-gpu")  # Desactivar GPU (opcional para mejorar estabilidad)
    chrome_options.add_argument("--window-size=1920,1080")  # Tamaño de ventana para evitar problemas de renderizado
    chrome_options.add_argument("--disable-software-rasterizer")  # Acelerar el renderizado en contenedores

    driver = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=chrome_options)
    
    return driver

def avanzar_siguiente_pagina(driver):
    try:
        # Intentar encontrar el botón "Next"
        next_button = driver.find_element(By.XPATH, "//a[@aria-label='Next']")
        
        previous_li = next_button.find_element(By.XPATH, "./../preceding-sibling::li[1]")
        if previous_li.get_attribute('class') == 'active':
            print("Última página alcanzada. Terminando proceso de scraping.")
            return False  # Detener la paginación

        actions = ActionChains(driver)
        actions.move_to_element(next_button).perform()
        next_button.click()
        time.sleep(2)  # Esperar a que la página cargue
        return True

    except NoSuchElementException:
        print("Terminando proceso de scraping.")
        return False

    except Exception as e:
        print(f"Error al intentar avanzar de página: {e}")
        return False

def almacenar_datos(nombre, precio, url_detalle, direccion):
    try:
        conn = sqlite3.connect('propiedades.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS propiedades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT,
                precio TEXT,
                url_detalle TEXT,
                direccion TEXT
            )
        ''')
        cursor.execute('''
            INSERT INTO propiedades (nombre, precio, url_detalle, direccion)
            VALUES (?, ?, ?, ?)
        ''', (nombre, precio if precio else None, url_detalle, direccion if direccion else None))

        conn.commit()
        conn.close()
        print(f"Propiedad '{nombre}' almacenada correctamente.")
    except Exception as e:
        print(f"Error al almacenar la propiedad: {e}")

def ejecutar_scraping():
    driver = iniciar_driver()
    
    url = 'https://www.cbcworldwide.com/search/lease?product_types[]=industrial&country=United+States&market=lease'
    driver.get(url)
    
    # Esperar a que las propiedades se carguen
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'sc-wrap cbc1')]")))
    time.sleep(5)  # Pausa adicional para asegurar que todo el contenido se haya cargado

    while True:
        propiedades = driver.find_elements(By.XPATH, "//div[contains(@class, 'sc-wrap cbc1')]")
        for propiedad in propiedades:
            nombre = propiedad.find_element(By.XPATH, ".//a").text
            link = propiedad.find_element(By.XPATH, ".//a").get_attribute('href')

            driver.get(link)
            time.sleep(2)  # Esperar a que la página cargue
            
            # Capturar y mostrar parte del HTML
            html_content = driver.page_source  # Captura el HTML de la página actual
            print(html_content[:1000])  # Imprime los primeros 1000 caracteres del HTML
            
            try:
                nombre_detalle = driver.find_element(By.XPATH, "//h1[@class='ps-title']").text
            except:
                nombre_detalle = None

            try:
                precio = driver.find_element(By.XPATH, "//div[@class='ps-price']").text
            except:
                precio = None

            try:
                direccion = driver.find_element(By.XPATH, "//p[@class='ps-address']").text
            except:
                direccion = None
            
            almacenar_datos(nombre_detalle, precio, link, direccion)
            
            driver.back()
            time.sleep(2)

        if not avanzar_siguiente_pagina(driver):
            print("Última página alcanzada. Terminando proceso de scraping.")
            break

    driver.quit()

if __name__ == "__main__":
    ejecutar_scraping()