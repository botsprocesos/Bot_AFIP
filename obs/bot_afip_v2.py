from tkinter import Tk,Label,Frame,Button, messagebox, Entry, StringVar
import datetime
import os, time
import requests
from getpass import getuser
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
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
    contra = password.get()
    user = getuser()
    # cuit = '20052221294'
    # contra = 'Medifarm2023'


    parametros = ParametrosBotAfip()

    ruta_Afip = parametros.rutasAfip()
    ruta_acuse, ruta_archivos = parametros.rutasArchivos()

    ruta_acuse_qas = f"C:/Users/{user}/Desktop/Asana/bot_afip"
    ruta_archivos_qas = f"C:/Users/{user}/Desktop/bot_afip"

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_experimental_option("prefs", {
                "download.default_directory"
            })
    chrome_options.add_argument(f"--download.default_directory={ruta_acuse_qas}")
    
    # Objeto driver
    driver = webdriver.Chrome(service = ChromeService(ChromeDriverManager().install()))

    try:
        driver.maximize_window()
        #Pagina principal de AFIP
        driver.get(ruta_Afip) 

        driver.implicitly_wait(5)

        #Obtener el bloque donde se puede ingresar el usuario
        usuario_input = driver.find_element(By.ID, value="F1:username") 
        usuario_input.send_keys(cuit)
        driver.implicitly_wait(5)

        #Obtengo el boton continuar
        siguiente_button = driver.find_element(By.ID, value="F1:btnSiguiente") 
        driver.implicitly_wait(5)
        siguiente_button.click()

        #Obtener el bloque donde se puede ingresar la contraseña
        contrasenia_input = driver.find_element(By.ID, value="F1:password") 
        contrasenia_input.send_keys(contra)
        driver.implicitly_wait(5)

        #Obtengo el boton confirmar
        submit_button = driver.find_element(by=By.ID, value="F1:btnIngresar") 
        driver.implicitly_wait(5)
        submit_button.click()

        driver.implicitly_wait(20)
        time.sleep(5)
        #Obtengo y le doy click al boton "Ver todos", desplegando mas opciones de AFIP
        ver_todos = driver.find_element(by="css selector", value="a.roboto-font.regular.p-y-1.m-y-0.h4")
        driver.implicitly_wait(10)
        ver_todos.click()
        time.sleep(5)
        driver.implicitly_wait(10)
        #Script que me permite scrollear hasta donde este el elemento que yo necesite
        script = "arguments[0].scrollIntoView();"
        
        driver.implicitly_wait(10)

        #Llego al bloque de DDJJ y le damos click
        presentacionDDJJ = driver.find_element(by="css selector", value="a.panel.panel-default[title='setidj']")
        driver.execute_script(script,presentacionDDJJ)
        driver.implicitly_wait(10)
        time.sleep(3)
        presentacionDDJJ.click()

        #driver.implicitly_wait(10)
        #Esperar a que en el navegador se abran 2 ventanas (PORTAL CLAVE FISCAL / PRESNETACION DDJJ)
        time.sleep(12)
        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))

        ventanas = driver.window_handles
        driver.switch_to.window(ventanas[1]) #Pasamos el driver a la ventana de PRESENTACION DDJJ

        driver.implicitly_wait(10)

        #wait = WebDriverWait(driver, 10)  # Esperar hasta 10 segundos
        #Vamos a verificar si este tipo de espera funciona
        #Capturo el boton ACEPTAR de la ventana de terminos y condiciones
        boton_aceptar = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary[type='submit'][property='aceptar'][title='Aceptar']"))
        )
        boton_aceptar.click()
        driver.implicitly_wait(5)

        #carpetas, archivos = buscarArchivos()
        #cantArchivos = 0
        # OK
        archivos = os.listdir(ruta_archivos_qas)

        # for c in carpetas:
        #     print("Tengo la carpeta: ", c)
        #     ruta_carpeta_controladora = os.path.join(ruta_acuse, c)
        #     num_archivo = 0
        #     os.mkdir(ruta_carpeta_controladora)
        #     while(num_archivo < 2):
        #         print("Voy a tratar el archivo" + archivos[cantArchivos][num_archivo])
        #         archivo_txt = "C:/Users/rgonzalez/Desktop/reporte_afip/acuse/" + c + "/" + archivos[cantArchivos][num_archivo][:5]+".txt"
        #         with open(archivo_txt,'w') as archivo:
        #             archivo.write("TXT de controladora" + c)
        #         num_archivo+=1
        #         cantArchivos+=1

        for arc in archivos:
            print("Subiendo:...", arc)

            # ------------------ Lucho
            ruta = ruta_acuse_qas + "/" + arc
            input_madre = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "e-file"))
            )
            EVID = input_madre.get_attribute("id")
            nro_EVID = EVID[8:14]
            id_boton_upload = f'__EVID__' + nro_EVID + '__EV__e-file__-input'
            objeto_input = driver.find_element(By.ID, id_boton_upload)
            objeto_input.send_keys(ruta)
            # ---------------- Lucho
            
            """ CONTINUAR CON EL RESTO: PRESENTAR + DESCARGAR (LO DEJO COMENTADO)
            """

        #     driver.implicitly_wait(5)

        #     boton_presentar = driver.find_element(by="css selector", value=".btn.btn-primary[title='Presentar la declaración jurada seleccionada']")
        #     driver.implicitly_wait(5)
        #     boton_presentar.click()

        #     driver.implicitly_wait(5)

        #     #texto_presentada = driver.find_element(by="css selector", value='div.title[style="margin-bottom: 20px;"]').text
        #     #descomentar boton confirmar
        #     boton_confirmar = driver.find_element(by="css selector", value="#confirmacionNoDuplicado button.btn.btn-primary[type='submit']")
        #     driver.implicitly_wait(5)
        #     boton_confirmar.click()
        #     driver.implicitly_wait(5)
        #     aceptada = elemento_anterior = driver.find_element(By.XPATH, "//div[text()='Aceptada']").text
        #     print(aceptada)
        #     #Si esta aceptada descargar

        #     pdf_descarga = driver.find_element(By.CLASS_NAME, "e-icon")
        #     pdf_descarga = driver.find_element(By.XPATH, "//span[text()='picture_as_pdf']")
        #     driver.implicitly_wait(5)
        #     pdf_descarga.click()

        #     driver.implicitly_wait(5)

        #     #En caso que este presentada tocar en boton volver
        #     boton_volver = driver.find_element(by="css selector", value="button:not(:disabled), [type='button']:not(:disabled), [type='reset']:not(:disabled), [type='submit']:not(:disabled)")

        #     driver.implicitly_wait(5)

        #     boton_volver.click()

        # driver.quit()

        # url_pdf = driver.current_url
        # response = requests.get(url_pdf)

        #Ruta= carpetaAcuse / Numero Carpeta de Controladora / url_pdf
        #nombre_archivo = os.path.join(ruta, "nombre_del_impuesto.pdf")
        # with open(nombre_archivo, 'wb') as f:
        #     f.write(response.content)

        #FALTA:
        
        # Ajustar funcionalidad de boton volver, en caso que las DDJJ ya esten presentadas y poder continuar con el código
        # LOG DE EJECUCIÓN, para que tenga un control Martin
        # Boton aceptar para volver a la parte de subir los archivos -> validar con Martin en una prueba si ese boton permite volver a la pagina de DDJJ
        # Mail de ejecucion del bot
        # Excepciones:
            # Dentro del main
                # En caso que ya este presentada la DDJJ, realizar una busqueda dentro de la carpeta si el acuse no esta descargado, poder descargarlo y guardarlo. Sino continuar
                # Problema de tiempo de inactividad, ¿cerrar el driver y en la expceción poder ejecutar de nuevo el metodo?
            # Busqueda de Archivos
                # Controladora con documentos vacios
                # Recorrer solamente las controladoras, en  caso de tener otra carpeta no ingresar

            
        # - boton aceptar para volver a la parte de subir los archivos -
        # puede ser el boton de abajo
        #   wait = WebDriverWait(driver, 10)  # Esperar hasta 10 segundos
        #boton_aceptar = WebDriverWait(driver, 10).until(
        #EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary[type='submit'][property='aceptar'][title='Aceptar']"))    #)

    except Exception as e:
        print(e)


# if __name__ == '__main__':
#     # interfaz()  
#     #proceso()  