from tkinter import Tk,Label,Frame,Button, messagebox, Entry, StringVar
import time
import os
import getpass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from busquedaArchivos import buscarArchivos
from z_params import ParametrosBotAfip
#import pyautogui

def interfaz():

    global user,password

    raiz=Tk()
    raiz.title("Carga DDJJ AFIP")
    raiz.resizable(0,0)
    raiz.geometry('300x300+500+50'.format(250, 300))
    framePrincipal=Frame()
    framePrincipal = framePrincipal.config(width=500)
    textoCuit = Label(raiz,text="CUIT:")
    textoCuit.grid(row=0,column=0)
    textoContrasenia = Label(raiz,text="Contraseña:")
    textoContrasenia.grid(row=1,column=0)

    user = StringVar()  
    password = StringVar()

    userAfip=Entry(framePrincipal,textvariable=user,width=20)
    userAfip.grid(row=0,column=1,padx=10,pady=0)
    contraseniaAfip=Entry(framePrincipal,textvariable=password,width=20,show='*')
    contraseniaAfip.grid(row=1,column=1,padx=10,pady=0)
    botongenerar = Button(raiz,text="PROCESAR",command=proceso).grid(row=4,column=0)
    raiz.mainloop()


def proceso():
    
    cuit = user.get()
    contrasenia = password.get()
    usuario = getpass.getuser()

    contra = 3
    tempo = 5
    clickeo = 1
    espera = 2
    presento = 10

    parametros = ParametrosBotAfip()

    ruta_Afip = parametros.rutasAfip()
    #ruta_acuse, ruta_controladoras = parametros.rutasArchivos() #PRD

    ruta_archivos_qas = "C:\\Users\\"+usuario+"\\Desktop\\reporte_afip_QAS" #QAS
    carp_descarga = "C:\\Users\\"+usuario+"\\Desktop\\acuse_afip_QAS" #QAS

    opciones = webdriver.ChromeOptions()
    opciones.add_argument('--window-size=1920,1080')
    opciones.add_argument("--safebrowsing-disable-download-protection")
    opciones.add_argument("safebrowsing-disable-extension-blacklist")
    opciones.add_experimental_option("prefs", {
                "download.default_directory" : carp_descarga, #ruta_acuse, carp_descarga
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True
            })
        
    driver = webdriver.Chrome(service = ChromeService(ChromeDriverManager().install()),options=opciones)

    try:

        if not os.path.exists(carp_descarga): #carp_descarga QAS / ruta_acuse PRD
                os.mkdir("C:\\Users\\"+usuario+"\\Desktop\\acuse_afip_QAS") #acuse_afip_QAS QAS / acuse PRd
                time.sleep(1)
        
        driver.maximize_window()
        #Pagina principal de AFIP
        driver.get(ruta_Afip) 
        
        time.sleep(contra)

        #Obtener el bloque donde se puede ingresar el usuario
        usuario_input = driver.find_element(By.ID, value="F1:username") 
        usuario_input.send_keys(cuit)
        time.sleep(contra)

        #Obtengo el boton continuar
        siguiente_button = driver.find_element(By.ID, value="F1:btnSiguiente") 
        time.sleep(clickeo)
        siguiente_button.click()

        time.sleep(contra)

        #Obtener el bloque donde se puede ingresar la contraseña
        contrasenia_input = driver.find_element(By.ID, value="F1:password") 
        contrasenia_input.send_keys(contrasenia)
        time.sleep(contra)

        #Obtengo el boton confirmar
        submit_button = driver.find_element(by=By.ID, value="F1:btnIngresar") 
        time.sleep(clickeo)
        submit_button.click()

        time.sleep(tempo)

        #Obtengo y le doy click al boton "Ver todos", desplegando mas opciones de AFIP
        ver_todos = driver.find_element(by="css selector", value="a.roboto-font.regular.p-y-1.m-y-0.h4")
        time.sleep(clickeo)
        ver_todos.click()

        time.sleep(tempo)
        #Llego al bloque de DDJJ y le damos click

        actions = ActionChains(driver)

        print("Ingreso al portal de presentación de DDJJ")
        presentacionDDJJ = driver.find_element(by="css selector", value="a.panel.panel-default[title='setidj']")
        actions.move_to_element(presentacionDDJJ).perform()
        time.sleep(clickeo)
        presentacionDDJJ.click()

        time.sleep(tempo)
        
        #Esperar a que en el navegador se abran 2 ventanas (PORTAL CLAVE FISCAL / PRESNETACION DDJJ)
        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
        ventanas = driver.window_handles
        driver.switch_to.window(ventanas[1]) #Pasamos el driver a la ventana de PRESENTACION DDJJ

        time.sleep(tempo)

        #Capturo el boton ACEPTAR de la ventana de terminos y condiciones
        boton_aceptar = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary[type='submit'][property='aceptar'][title='Aceptar']"))
        )
        time.sleep(clickeo)
        boton_aceptar.click()
        
        time.sleep(tempo)

        print("Buscando los documentos para presentar")
        documentos = os.listdir(ruta_archivos_qas) #QAS
        #documentos = buscarArchivos() #PRD
        
        print("*"*20)

        for arc in documentos:

            print("Subiendo:...", arc)

            #DESCOMENTAR EN PRD
            arc = ruta_archivos_qas + "\\" + arc

            time.sleep(espera)

            #Elemento par apoder cargar el archivo
            input_madre = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "e-file"))
            )
            EVID = input_madre.get_attribute("id")
            nro_EVID = EVID[8:14]
            id_boton_upload = f'__EVID__' + nro_EVID + '__EV__e-file__-input'
            objeto_input = driver.find_element(By.ID, id_boton_upload)
            time.sleep(clickeo)
            objeto_input.send_keys(arc)

            time.sleep(espera)

            #Boton para presetar el documento
            boton_presentar = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH,"//BUTTON[@title='Presentar la declaración jurada seleccionada']"))
                )
            EVID = boton_presentar.get_attribute("id")
            nro_EVID_presentar = EVID[8:14]
            time.sleep(clickeo)
            id_boton_present = f'__EVID__' + nro_EVID_presentar + '__EV__e-button__'
            objeto_presentar = driver.find_element(By.ID, id_boton_present)
            time.sleep(clickeo)
            objeto_presentar.click()

            time.sleep(espera)

            #Se busca el texto verificando si es que ya se presentó el documento
            try:
                texto_presentada = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='title' and contains(text(),'La DJ seleccionada ya ha sido presentada. No puede volver a presentarla.')]"))
                    )
            except Exception as ex:
                print(ex)
                texto_presentada = ""
                pass

            #Se consulta si es que se presentó el documento, en caso que no confirmo, descargo y continúo        
            if texto_presentada == "":
                print("Documento no presentado aún, procedemos a confirmarlo")
                #Confirmo el documento a presentar
                boton_confirmar = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,"//BUTTON[@type='submit']"))
                    )
                EVID = boton_confirmar.get_attribute("id")
                nro_EVID_confirmar = EVID[8:14]
                id_boton_presentar = f'__EVID__' + nro_EVID_confirmar + '__EV__e-button__'
                object_confirmar = driver.find_element(By.ID, id_boton_presentar)
                actions.move_to_element(object_confirmar).perform()
                time.sleep(clickeo)
                object_confirmar.click()

                time.sleep(presento)

                #Buscamos el boton para descargar el PDF
                pdf_descarga = driver.find_element(By.XPATH, "//span[text()='picture_as_pdf']")
                time.sleep(clickeo)
                actions.move_to_element(pdf_descarga).perform()
                pdf_descarga.click()

                time.sleep(tempo)

                #Busco el botón continuar para poder seguir con los siguientes documentos
                boton_continuar = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,"//BUTTON[@type='submit']"))
                    )
                EVID = boton_continuar.get_attribute("id")
                nro_EVID_continuar = EVID[8:14]
                id_boton_continuar = f'__EVID__' + nro_EVID_continuar + '__EV__e-button__'
                object_continuar = driver.find_element(By.ID, id_boton_continuar)
                time.sleep(clickeo)
                actions.move_to_element(object_continuar).perform()
                object_continuar.click()
                time.sleep(clickeo)

                print("Continuo con el siguiente")

            else:
                print("Documento ya confirmado")
                #En caso de tener el documento ya presentado, realizo la descarga del acuse y vuelvo para la pantalla de presentación

                pdf_descarga = driver.find_element(By.XPATH, "//span[text()='picture_as_pdf']")
                time.sleep(clickeo)
                actions.move_to_element(pdf_descarga).perform()
                #ActionChains(driver).move_to_element(objeto_input_pdf).click(objeto_input_pdf).perform()
                pdf_descarga.click()

                #Botón para volver a la pantalla de presentación y seguir con los demas documentos
                boton_volver = driver.find_element(by="css selector", value="button:not(:disabled), [type='button']:not(:disabled), [type='reset']:not(:disabled), [type='submit']:not(:disabled)")

                boton_volver.click()

                print("Continuo con los siguientes documentos")
        
        driver.quit()

        time.sleep(tempo)

        print("Se imprimieron los siguientes acuses:")
        acuses = os.listdir(carp_descarga) #carp_descarga QAS / ruta_acuse PRD
        for i in acuses:
            print(i)
        messagebox.showinfo(title = "Fin de Ejecución", message = "Proceso terminado")

    except Exception as e:
        print(e)


interfaz()