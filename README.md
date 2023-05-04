# scraper-ss-ipn
Scraper para extraer datos de todas las actividades de prestatarios disponibles en https://serviciosocial.ipn.mx

## Requisitos
1. Tener instalado la última versión del navegador Google Chrome
2. python 3.x

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
![alt tabla con datos de prestatarios](https://github.com/NicolasSaG/scraper-ss-ipn/blob/main/images/datos.PNG)


## 5 Revisión de actividades de servicio social para el inicio del segundo semestre 2022
![alt analisis tableau](https://github.com/NicolasSaG/scraper-ss-ipn/blob/main/images/sevicio_social_2do_semestre_2022.png)
