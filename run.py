from scraper import *


with Scraper(debug=True) as scraper:
    print("iniciando scraper...")
    if scraper.llenar_datos_prestador() == 0:
        scraper.obtener_prestatarios()
    print("fin de scraper")