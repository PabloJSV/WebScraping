# Web Scraping
Web Scraping de datos de covid-19.

## Descripción

Este proyecto hace parte de la práctica de Web Scraping del curso *Tipología y ciclo de vida de los datos*, del master en *Ciencia de Datos* de la UOC, la cual consiste en la construcción de un dataset de estadísticas de covid-19 mediante el uso de técnicas de Web Scraping usando la página web *Worldometers*.

## Integrantes del equipo
La actividad fue realizada por Jhon Harry Loaiza y Pablo Jesús Sánchez Vargas.

## Ficheros del código fuente
*covid19_scraping.py* es el archivo que ejecuta el scraping y crea el archivo csv con la información del día por países. 

## Ejecución
Para la ejecución del script es necesario instalar las siguientes librerias:
```python
pip install requests
pip install lxml
pip install time
pip install pandas
pip install schedule
```
El fichero se ejecuta con el comando:

```python
python covid19_scraping.py
```

El resultado es un archivo que cuyo nombre contiene la fecha de ejecución, con la estructura *"dd-mm-yyyy covid19.csv"*.  

## Recursos
* Subirats, L., Calvo, M. (2018). Web Scraping. Editorial UOC.
* Lawson, R. (2015). Web Scraping with Python. Packt Publishing Ltd. Chapter 2. Scraping the Data.
