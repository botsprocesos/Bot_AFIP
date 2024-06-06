from tkinter import Tk,Label,Frame,Button, messagebox, Entry, StringVar
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from busquedaArchivos import buscarArchivos
from z_params import ParametrosBotAfip

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

    contra = 3
    tempo = 5
    clickeo = 1
    espera = 2

    parametros = ParametrosBotAfip()

    ruta_Afip = parametros.rutasAfip()

    #Rutas doc PRD
    # ruta_acuse, ruta_controladoras = parametros.rutasArchivos()

    #Rutas doc QAS
    ruta_archivos_qas = "C:\\Users\\rgonzalez\\Desktop\\reporte_afip_QAS"
    carp_descarga = "C:\\Users\\rgonzalez\\Desktop\\acuse_afip_QAS"

    opciones = webdriver.ChromeOptions()
    opciones.add_argument('--window-size=1920,1080')
    opciones.add_experimental_option("prefs", {
                "download.default_directory" : carp_descarga
            })
        
    driver = webdriver.Chrome(service = ChromeService(ChromeDriverManager().install()),options=opciones)

    try:
        
        driver.maximize_window()
        driver.get(ruta_Afip) #Pagina principal de AFIP
        
        time.sleep(contra)

        usuario_input = driver.find_element(By.ID, value="F1:username") #Obtener el bloque donde se puede ingresar el usuario
        usuario_input.send_keys(cuit)
        time.sleep(contra)

        siguiente_button = driver.find_element(By.ID, value="F1:btnSiguiente") #Obtengo el boton continuar
        time.sleep(clickeo)
        siguiente_button.click()

        time.sleep(contra)

        contrasenia_input = driver.find_element(By.ID, value="F1:password") #Obtener el bloque donde se puede ingresar la contraseña
        contrasenia_input.send_keys(contrasenia)
        time.sleep(contra)

        submit_button = driver.find_element(by=By.ID, value="F1:btnIngresar") #Obtengo el boton confirmar
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

        #Documentos QAS
        documentos = os.listdir(ruta_archivos_qas)
        #Documentos PRD
        #documentos = buscarArchivos()
        
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

            #Boton para realizar la presentación del documento
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

            #texto_presentada = driver.find_element(by="css selector", value='div.title[style="margin-bottom: 20px;"]').text
            
            #descomentar boton confirmar CUANDO SE CORRA EN PRD
            
            #Boton para confirmar la presentación
            # boton_confirmar = WebDriverWait(driver, 10).until(
            #     EC.presence_of_element_located((By.XPATH,"//BUTTON[@type='submit']"))
            #     )
            # EVID = boton_confirmar.get_attribute("id")
            # nro_EVID_confirmar = EVID[8:14]
            # id_boton_presentar = f'__EVID__' + nro_EVID_confirmar + '__EV__e-button__'
            # object_confirmar = driver.find_element(By.ID, id_boton_presentar)
            # actions.move_to_element(object_confirmar).perform()
            # time.sleep(clickeo)
            # object_confirmar.click()

            #aceptada = driver.find_element(By.XPATH, "//div[text()='Aceptada']").text
            #print("DOCUMENTACION: " + aceptada)
            #Si esta aceptada, descargamos el acuse

            time.sleep(tempo)

            #Botón para realizar la descarga del PDF, se guarda en la carpeta de Acuse
            pdf_descarga = driver.find_element(By.XPATH, "//span[text()='picture_as_pdf']")
            time.sleep(clickeo)
            actions.move_to_element(pdf_descarga).perform()
            pdf_descarga.click()

            time.sleep(espera)

            #Botón para poder continuar y darle fluidez al desarrollo, yendo en cada una de las carpetas de las controladoras
            # boton_continuar = WebDriverWait(driver, 10).until(
            #     EC.presence_of_element_located((By.XPATH,"//BUTTON[@type='submit']"))
            #     )
            # EVID = boton_continuar.get_attribute("id")
            # nro_EVID_continuar = EVID[8:14]
            # id_boton_continuar = f'__EVID__' + nro_EVID_continuar + '__EV__e-button__'
            # object_continuar = driver.find_element(By.ID, id_boton_continuar)
            # time.sleep(clickeo)
            # actions.move_to_element(object_continuar).perform()
            # object_continuar.click()

            #En caso que este presentada tocar en boton volver
            boton_volver = driver.find_element(by="css selector", value="button:not(:disabled), [type='button']:not(:disabled), [type='reset']:not(:disabled), [type='submit']:not(:disabled)")

            boton_volver.click()
        
        driver.quit()

        time.sleep(tempo)

        print("Se imprimieron los siguientes acuses:")
        acuses = os.listdir(carp_descarga)
        for i in acuses:
            print(i)

        # Excepciones:
            # Dentro del main
                # En caso que ya este presentada la DDJJ, realizar una busqueda dentro de la carpeta si el acuse no esta descargado, poder descargarlo y guardarlo. Sino continuar
                # Problema de tiempo de inactividad, ¿cerrar el driver y en la expceción poder ejecutar de nuevo el metodo?
            # Busqueda de Archivos
                # Controladora con documentos vacios
                # Recorrer solamente las controladoras, en  caso de tener otra carpeta no ingresar

    except Exception as e:
        print(e)


interfaz()