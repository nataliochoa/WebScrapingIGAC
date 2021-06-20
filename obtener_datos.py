import re
import random
from typing import Hashable
from numpy import true_divide
from selenium import webdriver
from time import sleep

driver = webdriver.Chrome('C:/Users/NATALI OCHOA/Desktop/PASANTIA IGAC/chromedriver')#Lanza el buscador
#Definir carpeta de destino, nombre y tipo del archivo 
carpeta_destino = 'C:/Users/NATALI OCHOA/Desktop/PASANTIA IGAC/data/venta_snt_marta.json' 
#carpeta_destino = 'C:/Users/usuario/Downloads/PAS/WEBSCRAPING_MERCADOLIBRE/datos_arriendo.csv'
#carpeta_destino = 'C:/Users/usuario/Downloads/PAS/WEBSCRAPING_MERCADOLIBRE/datos_venta_barranquilla.json' 

f = open(carpeta_destino, 'w')#abre la carpeta de destino con permiso para escribir (write)
#log = open(carpeta_destino, 'w')
#creamos 3 funciones para buscar, llamar y limpiar los datos 
#Funcion 1, Analiza las ofertas y se enfoca en proyectos viejos y no nuevos
def is_new(body): 
    try:
        body.find_element_by_css_selector('#ctl00_phMasterPage_cAdvert_ucMultimedias_icoNewBuilding')
        return True
    except:
        return False

# url no existe, error 404! """"
def urlcaida(context, url): #context tiene funciones de busqueda
    try:
        context.find_element_by_css_selector('.MasterPageContent .cont_notfound_alert .cont_text .numero_b')
        print('url DAÑADA '+ url)
        return True
    except:
        print('url OK '+ url)
        return False

#Funcion 2, Limpia texto y reemplaza saltos de linea, tabulaciones etc por espacio
def limpiarTexto(search, texto):
    value = re.sub(r'[\n \r : /]', ' ' ,texto)
    return re.sub(search, '', value).strip()

#Funcion 3, va a buscar cada valor pedido en el codigo
def obtener_info(content,search):
    value = ''
    for item in content:
        if re.search(search, item.text) != None: #item.text == search:
            value = item.text
    return limpiarTexto(search, value)    
#Definimos el separador para el archivo de salida
sep = '|'

#Definimos titulos de la tabla
f.write('tipo' + sep + 'price'+ sep +'habitaciones'+ sep +'baños'+ sep +'parqueaderos'+ sep +'area_conts'+ sep +'area_priv'+ sep +'precio_m²'+ sep +'administracion'+ sep 
+'estrato'+ sep +'estado'+ sep +'antiguedad'+ sep +'descripcion'+ sep + 'piso' + sep +'latitud' + sep + 'longitud' + '\n')

#definimos las urls de donde se van a extraer los datos
urls = open('C:/Users/NATALI OCHOA/Desktop/PASANTIA IGAC/data/urlsantamarta.json', "r")
#pruebas urls = open('C:/Users/usuario/Downloads/PAS/WEBSCRAPING_MERCADOLIBRE/prueba.csv', "r")
i = 0
#Definiendo que trae las ofertas viejas de la funcion 1
while(True):
    try:   
        #Entra en el archivo .csv y lee linea por linea
        url = urls.readline() 
        """if len(url) is 0:
            break   """             
        try:  
            driver.get(url)
            body = driver.find_element_by_xpath('//body')

            if urlcaida(body,url) is False and is_new(body) is False:           
            
                 
                sleep(random.uniform(0.0, 0.1))
                dic = {}#se crea diccionario para guardar las variables
                #con dic[]se  incluye cada variable en el diccionario         
                tipo = body.find_element_by_css_selector('.detail .title h1').text
                dic['tipo'] = tipo.replace('\n',' ')
                precio_i = body.find_element_by_css_selector('.detail .price h2').text 
                dic['price'] = precio_i.replace("$ ", '')
                content1 = body.find_elements_by_css_selector('#ctl00_phMasterPage_cAdvert_Details_1 .features span')
                dic['habs'] = obtener_info(content1, 'Habitaciones')
                dic['banos'] = obtener_info(content1, 'Baños')
                dic['parqueadero'] = obtener_info(content1, 'Parqueaderos')
                content2 = body.find_elements_by_css_selector('.row.features_2 ul li')
                area_C = obtener_info(content2, 'Área Const.')
                dic['area_const'] = area_C.replace(" m²",'')
                if obtener_info(content2, 'Área privada') == '':
                    dic['area_priv'] = dic['area_const']
                else:
                    area_p = obtener_info(content2, 'Área privada')
                    dic['area_priv'] = area_p.replace(" m²",'')
                precio1 = obtener_info(content2, 'Precio m')
                precio2 = precio1.replace("² ",'')
                precio = precio2.replace(" m²",'')
                dic['precio_m2'] = precio.replace(" ", '')
                dic['administracion'] = obtener_info(content2, 'Admón')
                dic['estrato'] = obtener_info(content2, 'Estrato')
                dic['estado'] = obtener_info(content2, 'Estado')
                dic['antiguedad'] = obtener_info(content2, 'Antigüedad')
                dic['piso']= obtener_info(content2, 'Piso')
                dic['descripcion'] = body.find_element_by_css_selector('.description p').text
                latitud = str(driver.execute_script('return MapFR.latitude'))
                longitud = str(driver.execute_script('return MapFR.longitude'))
                dic['latitud'] = latitud.replace(".", ",")
                dic['longitud'] = longitud.replace(".", ",")
                #escribimos los nombres de cada columna en el archivo
                f.write(dic['tipo'] + sep + dic['price'] + sep + dic['habs'] + sep + dic['banos'] + sep + dic['parqueadero'] + sep + dic['area_const'] + sep + dic['area_priv'] + sep +
                dic['precio_m2'] + sep + dic['administracion'] + sep + dic['estrato'] + sep + dic['estado'] + sep + dic['antiguedad'] + sep + dic['descripcion'] + sep + dic['piso'] + 
                sep + dic['latitud'] + sep + dic['longitud'] + '\n')
                print('Pagina ' + str(i))
                i+=1
                #log.write( url+' ok ' + str(i) +'\n')
        except NameError:
            print('1***************1')
            print(NameError)
            print('***************')
            #log.write( url+' error ' + str(i) + '\n') 
    except NameError:
        i=-1

        print('2***************2')
        print(NameError)
        print('***************')
        #log.write( url+' error' + '\n')
        break
f.write('\n')
urls.close()
f.close()
driver.quit()
print('***************')