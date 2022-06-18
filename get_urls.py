from scraper import *
import pandas as pd

with Scraper(debug=False) as scraper:
    if scraper.llenar_datos_prestador() == 0:
        urls = scraper.obtener_urls_prestatarios()
        df = pd.DataFrame(urls, columns=["url"])
        df.to_csv("urls.csv", index=False)
