from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from bs4 import BeautifulSoup
import time
import re
import sys
import os
# from bs4 import BeautifulSoup

ss_url = "https://serviciosocial.ipn.mx/infoServSoc/InfoServSocListaPerfiles.do"
INTENTOS_MAX = 10
TIEMPO_MAX = 30


class Scraper:
    def __init__(self, debug=False):
        self.debug = debug
        self.driver = self.__get_driver()

    def __enter__(self):
        return self

    def llenar_datos_prestador(self, nivel="SUPERIOR", area="FÍSICO-MATEMÁTICAS", carrera="ESCOM INGENIERO EN SISTEMAS COMPUTACIONALES"):
        self.driver.get(ss_url)

        wait = WebDriverWait(self.driver, TIEMPO_MAX)

        prestador_values = [nivel, area, carrera]
        select_names = ["cveNivel", "cveArea", "cveProgEst"]
        for (select_name, prestador_value) in zip(select_names, prestador_values):
            dato_cargado = False
            intentos = 0
            while not dato_cargado and intentos < INTENTOS_MAX:
                try:
                    flag_select = wait.until(expected_conditions.element_to_be_clickable(
                        (By.NAME, select_name)))
                    select = self.driver.find_element(By.NAME, select_name)
                    select_object = Select(select)
                    select_object.select_by_visible_text(prestador_value)
                    dato_cargado = True
                except Exception as e:
                    intentos += 1
                    print(f"Error al llenar {select_name}: {e}")

                # error al abrir menu dropdown
                if intentos == INTENTOS_MAX:
                    return -1
        try:
            flag_link = wait.until(expected_conditions.element_to_be_clickable(
                (By.LINK_TEXT, "Ver Prestatarios")))
            flag_link.click()
        except Exception as e:
            print(f"Error al ver prestatarios: {e}")
        return 0

    def obtener_urls_prestatarios(self):
        urls = []
        try:
            response = BeautifulSoup(self.driver.page_source, 'html.parser')
            prestatarios = response.find_all('a')
            for index, prestatario in enumerate(prestatarios):
                if prestatario.get_text() == "Ver":
                    urls.append(
                        f"https://serviciosocial.ipn.mx{prestatario.get('href')}")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print("datos: ", exc_type, exc_tb.tb_lineno)
            print(f"Error al obtener url de prestatarios: {e}")
        return urls

    def obtener_prestatarios(self):
        prestatarios_data = []
        try:
            print("obteniendo prestatarios...")
            response = BeautifulSoup(self.driver.page_source, 'html.parser')
            prestatarios = response.find_all('a')
            for index, prestatario in enumerate(prestatarios):
                if prestatario.get_text() == "Ver":
                    url_prestatario = prestatario.get("href")
                    ver_link = self.driver.find_element(By.CSS_SELECTOR, f"a[href='{url_prestatario}']")
                    ver_link.click()
                    elem = WebDriverWait(self.driver, 30).until(
                        expected_conditions.presence_of_element_located((By.LINK_TEXT, "Regresar")))
                    # time.sleep(4)
                    # codigo para obtener datos
                    prestatario_datos = self.__obtener_datos_prestatario()
                    prestatarios_data.append(prestatario_datos)
                    self.driver.back()
                    # time.sleep(3)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print("datos: ", exc_type, exc_tb.tb_lineno)
            print(f"Error al obtener prestatarios: {e}")
        return prestatarios_data

    def __obtener_datos_prestatario(self):
        prestatario = {}
        
        actividad = self.driver.find_element(By.CLASS_NAME, "subtitulo").text
        actividad = actividad.split(":")[1][1:]

        prestatario_nombre = self.driver.find_element(By.CLASS_NAME, "subtitulo2").text
        prestatario_nombre = prestatario_nombre.split(":")[1]
        prestatario_num = prestatario_nombre.rsplit(" ", 1)[1]
        prestatario_num = prestatario_num.replace(")", "").replace("(", "")
        prestatario_nombre = prestatario_nombre.rsplit(" ", 1)[0][1:]

        datos = self.driver.find_elements(By.CLASS_NAME, "fila")
        for dato in datos:
            try:
                name = dato.text.split(":")[0].lower()
                name = name.replace(" ", "_")
                if name == "fecha_inicio":
                    name_fecha_inicio = name
                    value_fecha_inicio = dato.text.split(":", 1)[1][1:]
                    value_fecha_inicio = re.sub(
                        " +", " ", value_fecha_inicio)
                    name_fecha_termino = value_fecha_inicio.split(" ", 1)[
                        1].split(":")[0]
                    name_fecha_termino = name_fecha_termino.lower().replace(" ", "_").replace("é", "e")
                    value_fecha_termino = value_fecha_inicio.split(" ", 1)[
                        1].split(":")[1][1:]
                    value_fecha_inicio = value_fecha_inicio.split(" ", 1)[0]

                    prestatario[name_fecha_inicio] = value_fecha_inicio
                    prestatario["fecha_termino"] = value_fecha_termino
                else:
                    value = dato.text.split(":", 1)[1][1:]
                    prestatario[name] = value
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print("datos: ", exc_type, exc_tb.tb_lineno)
                print(f"Error obtener datos de prestador: {e}")

        prestatario["actividad"] = actividad
        prestatario["prestatario_nombre"] = prestatario_nombre
        prestatario["prestatario_num"] = prestatario_num
        print(prestatario)
        return prestatario

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            print(f"Excepcion: {exc_type}, {exc_value}, {tb}")
        self.driver.close()
        self.driver.quit()
        return True

    def __get_driver(self, debug=False):
        options = Options()

        if self.debug:
            options.add_argument("--window-size=1366,768")
        else:
            options.add_argument("--no-sandbox")
            options.add_argument("--headless")
            options.add_argument("--disable-dev-shm-usage")

        options.add_argument("--disable-notifications")
        options.add_argument("--lang=es-419")
        chrome_driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=options)

        return chrome_driver
