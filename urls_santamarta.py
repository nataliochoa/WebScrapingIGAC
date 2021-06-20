import random
from time import sleep
from sys import path
from selenium import webdriver

carpeta_destino = 'C:/Users/NATALI OCHOA/Desktop/PASANTIA IGAC/data/urlsantamarta.json'

f = open(carpeta_destino, 'a+')

driver = webdriver.Chrome('C:/Users/NATALI OCHOA/Desktop/PASANTIA IGAC/chromedriver')
driver.get('https://www.fincaraiz.com.co/apartamento-casa/venta/santa-marta/')
#driver.get('https://www.fincaraiz.com.co/apartamento-casa/arriendo/santa-marta/')
#driver.get('https://www.fincaraiz.com.co/apartamento-casa/venta/cartagena/')
#driver.get('https://www.fincaraiz.com.co/apartamento-casa/venta/barranquilla/')
# espero que cargue la informacion dinamica
driver.find_element_by_css_selector('.AceptarCookie button').click()

i=1
while i != -1: #< 2:

    sleep(random.uniform(3.0, 4.0))

    body = driver.find_element_by_xpath('//body')
    

    divAdvert = driver.find_element_by_xpath('//div[@id="divAdverts"]')

    try:
        titlegrids = divAdvert.find_elements_by_css_selector('.title-grid a')
        for item in titlegrids:
            link = item.get_attribute('href')
            f.write(link)
            f.write('\n')
        print('Pagina ' + str(i))
        i+=1
 
            
        # busco el boton nuevamente para darle click en la siguiente iteracion
        
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