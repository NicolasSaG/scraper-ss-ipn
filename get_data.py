import asyncio
import aiohttp
import time
import datetime
import csv
import re
from bs4 import BeautifulSoup

field_names = ["actividad", "prestatario", "vacantes", "nombre_largo", "nombre_del_programa", "fecha_inicio",
               "fecha_termino", "objetivo", "justificación", "domicilio", "representante", "medios_de_contacto_con_el_representante", "apoyos"]


async def save_activity(data):
    with open('servicio_social.csv', 'a', newline="") as csv_file:
        dictwriter_object = csv.DictWriter(csv_file, fieldnames=field_names)
        dictwriter_object.writerow(data)


async def scrape(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            body = await response.text()
            soup = BeautifulSoup(body, "html.parser")

            activity_info = {}

            actividad = re.sub("\s", " ", soup.select_one('.subtitulo').text)
            prestatario = re.sub(
                "\s", " ", soup.select_one('.subtitulo2').text)

            actividad = re.sub(" +", " ", actividad)
            prestatario = re.sub(" +", " ", prestatario)

            actividad = actividad.strip()
            prestatario = prestatario.strip()

            activity_info["actividad"] = actividad
            activity_info["prestatario"] = prestatario

            campos = soup.find(class_="cuerpo").find(
                class_="tabla").find_all(class_="fila")

            for campo in campos:
                key = re.sub("\s", " ", campo.text)
                key = re.sub(" +", " ", key)
                key = key.strip()
                if key != "" and key != "Regresar":
                    if key.split(":", 1)[0] == "Fecha inicio":
                        try:
                            fechas = re.match(
                                ".+: (?P<fecha_inicio>(\d{1,2}\/\d{1,2}\/\d{4})) .+: (?P<fecha_termino>(\d{1,2}\/\d{1,2}\/\d{4}))", key)
                            for key, value in fechas.groupdict().items():

                                activity_info[key] = datetime.datetime.strptime(
                                    value, "%d/%m/%Y").strftime("%Y-%m-%d")
                        except:
                            pass

                    # elif key.split(":", 1)[0] == "Medios de Contacto con el Representante":
                    #     try:
                    #         contactos = re.match(
                    #             ".+: (?P<email>([a-z]+@[a-z.]+)).+: (?P<telefono>([0-9-]+)).+: (?P<fax>([0-9-]+))", key)
                    #         for key, value in contactos.groupdict().items():
                    #             activity_info[key] = value
                    #     except:
                    #         pass
                    else:
                        value = key.split(":", 1)[1].strip()
                        key = key.split(":", 1)[0].lower().replace(" ", "_")
                        activity_info[key] = value
            # print(activity_info)
            await save_activity(activity_info)
    return


async def main():
    with open('servicio_social.csv', 'w', newline="") as csv_file:
        dictwriter_object = csv.DictWriter(csv_file, fieldnames=field_names)
        dictwriter_object.writeheader()

    start_time = time.time()
    tasks = []
    print("Iniciando scraping")
    with open('urls.csv') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            task = asyncio.create_task(scrape(row['url']))
            tasks.append(task)
    await asyncio.gather(*tasks)

    time_difference = time.time() - start_time
    print(f'Total: %.4f segundos' % time_difference)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
