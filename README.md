# scraper-ss-ipn
Scraper para extraer datos de todos las actividades de prestatarios disponibles en https://serviciosocial.ipn.mx

## Requisitos
Tener instalado la última versión del navegador Google Chrome
python 3.x

## 1 Crear entorno virtual
```
python -m venv venv
```

## 2 Iniciar el entorno e instalar librerías
```
source venv/Scripts/activate
pip install -r requirements.txt
```

## 3 Obtener urls 
Generar el archivo de urls de todas los prestatarios. Antes se debe modificar en el código los campos de nivel, area y carrera para obtener los valores correspondientes a tu servicio social. Por defecto está en la ingeniería de ISC Guiarse con [Vacantes por carrera](https://serviciosocial.ipn.mx/infoServSoc/InfoServSocListaPerfiles.do)

```
python get_urls.py
```
Salida: urls.csv

## 4 Extraer información
```
python get_data.py 
```
Salida: servicio_social.csv
