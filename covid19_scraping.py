# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 08:29:18 2020

@author: Harry Loaiza
"""

import requests
from lxml.html import fromstring
import pandas as pd
import time
import schedule


#Definimos la tarea que se va a repetir diariamente
def job(t):
    #Definimos la url para trabajar e incluimos un web-agent
    url = "https://www.worldometers.info/coronavirus"

    header = {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36"
        }

    req = requests.get(url, headers=header)

    #parseamos el html obtenido con requests
    base = fromstring(req.text)

    #extraemos la tabla que nos interesa, en este caso contiene id = 'main_table_countries_today'
    tabla = base.xpath(".//table[@id='main_table_countries_today']")[0]

    #extraemos las filas de encabezado de la tabla
    encabezado = tabla.xpath(".//thead/tr/th")

    #creamos las columnas del dataset
    columnas = list()

    for col in encabezado:
        columnas.append(col.text_content().replace('\n', '').replace(u'\xa0', u'').strip())

    #extraemos los valores de las filas que contienen las cifras para cada columna
    filas = tabla.xpath(".//tbody/tr")

    etiquetas = list()
    valores = list()

    for fila in filas:
        etiqueta = fila.xpath(".//td/a")
        if len(etiqueta) > 0:
            etiquetas.append(etiqueta[0].get('href').strip().replace('country/', '').replace('/', ''))
            valores.append([valor.text_content().strip() for valor in fila.xpath(".//td")])

    #creamos el dataframe
    df = pd.DataFrame(valores, columns=columnas)

    #removemos los simbolos de "+" y las comas de las cifras para volverlas numericas
    cols = ['TotalCases','NewCases','TotalDeaths','NewDeaths','TotalRecovered',"NewRecovered","ActiveCases","Serious,Critical",'TotCases/1M pop',"Deaths/1M pop",'TotalTests',
            'Tests/1M pop','Population', '1 Caseevery X ppl','1 Deathevery X ppl','1 Testevery X ppl' ]

    df[cols] = df[cols].replace({'\+': '', ',': '',"N/A":'' }, regex=True)

    #convertimos a numericas las columnas
    df[cols] = df[cols].apply(pd.to_numeric)
    df.dtypes

    #df.describe().transpose()
   
    #elimino los valores y totales de continentes, y hago un sort por total de casos
    df = df.sort_values(by=['TotalCases'], ascending=False)

    #agregamos un campo de fecha actual al dataframe
  
    df['Date'] = pd.to_datetime('today').strftime("%m/%d/%Y")


    #exportamos el dataset con nombre usando la fecha del dia

    fecha_hoy = time.strftime("%d-%m-%Y")
    csv_con_fecha = fecha_hoy + " covid19.csv"

    df.to_csv(csv_con_fecha, index=False)
    print('Recolección realizada')
    return
#Fijamos una hora diaria de actualización para obtener un nuevo csv con datos diarios
schedule.every().day.at("09:00").do(job,'Actualización diaria de casos COVID')

#Indicamos al script que espere a la hora designada y arroje mensajes para indicar que el script se está ejecutando correctamente
while True:
    schedule.run_pending()
    print('Script en funcionamiento, esperando a la hora designada para la actualización')
    time.sleep(60) # wait one minute
