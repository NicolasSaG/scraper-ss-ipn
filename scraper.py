from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

ss_url = "https://serviciosocial.ipn.mx/infoServSoc/InfoServSocListaPerfiles.do"
INTENTOS_MAX = 10 
class Scraper:
    def __init__(self, debug = False):
        self.debug = debug
        self.driver = self.__get_driver()
    
    
    def __llenar_datos_prestador(self, url, nivel="SUPERIOR", area="FÍSICOMATEMÁTICAS", carrera="ESCOM INGENIERO EN SISTEMAS COMPUTACIONALES"):
        self.driver.get(url)
        prestatarios_cargados = False
        intentos = 0
        while not prestatarios_cargados and intentos < INTENTOS_MAX:
            try:
                select_nivel = self.driver.find_element(By.NAME, 'cveNivel')
                select_object = Select(select_nivel)
                select_object = select_by_visible_text(nivel)
                
                time.sleep(10)
                
                
            except Exception as e:
                tries += 1
                self.logger.warn('Error al llenar cve')

            # error al abrir menu dropdown
            if tries == MAX_RETRY:
                return -1
        return 0
    
    # def obtener_prestatarios(self, url):
    #     self.driver.get(url)
    #     response = BeautifulSoup(self.driver.page_source, 'html.parser')
    #     rblock = response.find_all('div', class_='jftiEf L6Bbsd fontBodyMedium')
        
        
    
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
        chrome_driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        return input_driver