""" Programa desarrollado en el marco de la pasantia denominada Metodología para la obtención y explotación de datos inmobiliarios 
    obtenidos mediante fuentes alternativas contribuyendo a los métodos de evaluación masiva en el CIAF.
    
por: Sindy Natali Ochoa Torres"""

import random
from time import sleep
from sys import path
from selenium import webdriver

# Establecer el directorio, nombre y formato del archivo de salida (.csv, .json, .txt...)

carpeta_destino = 'C:/Users/NATALI OCHOA/Desktop/PASANTIA IGAC/data/urlsantamarta.json' 

f = open(carpeta_destino, 'a+') ##Crea Accion abrir carpeta y da permisos de lectura, escritura

# Invoca el web driver, este debe ser previamente instalado, la ruta se refiere a la del ejecutador)

driver = webdriver.Chrome('C:/Users/NATALI OCHOA/Desktop/PASANTIA IGAC/chromedriver')

# Se selecciona la pagina web que vamos a manipular con el webdriver.

driver.get('https://www.fincaraiz.com.co/apartamento-casa/venta/santa-marta/')

# El webdriver clica en el boton de "aceptar cookies".
driver.find_element_by_css_selector('.AceptarCookie button').click()

#se inicia contador para leer todas las paginas.

i=1
while i != -1: 

    #se incluye esta funcion para que el web driver se tarde entre 2 y 3 segundos por pagina y no sea detectada como un bot.
    
    sleep(random.uniform(2.0, 3.0))

    
    #inspeccion de la estructura HTML para localizar la URL que direccione a la oferta. 
    
    body = driver.find_element_by_xpath('//body') ##by_xpath ubicacion por ruta
    divAdvert = driver.find_element_by_xpath('//div[@id="divAdverts"]')

    try:
        titlegrids = divAdvert.find_elements_by_css_selector('.title-grid a') # "." para las clases y "#" para id
        for item in titlegrids:
            link = item.get_attribute('href')
            
            #escribe el link que esta almacenado en el atributo "href", y luego salta de linea
            
            f.write(link)
            f.write('\n')
        print('Pagina ' + str(i))
        i+=1
 
            
        # localiza el boton "ir a la pagina siguiente para continuar extrayendo las urls de las ofertas inmobiliarias (en cada pagina aparece aproximadamente 48 ofertas)
        
        try:
            boton = driver.find_element_by_css_selector('#divPaginator a[title="Ir a la pagina Siguiente"]')
            boton.click()
        except:
            break
    except NameError:
        i=-1
        print(NameError)
        break
    
f.close()

print('***************')
driver.quit()
