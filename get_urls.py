from scraper import *
import pandas as pd

with Scraper(debug=True) as scraper:

    if scraper.llenar_datos_prestador(nivel="SUPERIOR", area="FÍSICO-MATEMÁTICAS", carrera="ESCOM INGENIERO EN SISTEMAS COMPUTACIONALES") == 0:
        urls = scraper.obtener_urls_prestatarios()
        df = pd.DataFrame(urls, columns=["url"])
        df.to_csv("urls.csv", index=False)
