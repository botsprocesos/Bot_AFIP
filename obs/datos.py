# fechaHoy = datetime.today()
    # fechaPasada = fechaHoy - timedelta(days=10)
    # fechaPasada = fechaPasada.strftime("%d") + "/" + fechaPasada.strftime("%m") + "/" + fechaPasada.strftime("%Y")
    # #if (fechaPasada[0] == "0"):
    # #fechaPasada = fechaPasada[1:]
    # fechaHoy = fechaHoy.strftime("%d") + "/" + fechaHoy.strftime("%m") + "/" + fechaHoy.strftime("%Y")

#service = Service(executable_path=r"C:\Users\rgonzalez\Desktop\chromedriver_win32\chromedriver")

#driver.get("https://portaldroguerias.globalfarm.com.ar:8287/") #Pagina de global
#driver.get("https://portaldroguerias.globalfarm.com.ar") #Pagina de global

#usuario_input = WebDriverWait(driver,10).until(EC.element_selection_state_to_be(usuario_input,True))

#contrasenia_input = WebDriverWait(driver,10).until(EC.visibility_of_element_located(By.ID, value="loginPassword"))

#boton = driver.find_element(By.CLASS_NAME,value='button')

#script = "window.scrollTo(0, 3055)"  # Cambia 500 por la posición vertical deseada

#boton_confirmar = driver.find_element(by=By.ID, value="__EVID__027978__EV__e-button__")
    #boton_confirmar = driver.find_element(By.CSS_SELECTOR, ".btn.btn-primary[title='Presentar la declaración jurada seleccionada']")
    #contenedor_confirmacion = driver.find_element(by=By.ID,value="confirmacionNoDuplicado")
    #boton_confirmar = driver.find_element(by=By.XPATH,value=".//button[@id='__EVID__696624__EV__e-button__']")
    # boton_confirmar = WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary[type='submit'][id='__EVID__696624__EV__e-button__']"))
    # )
    #boton_confirmar = driver.find_element(by=By.XPATH,value="//div[@id='confirmacionNoDuplicado']//button[@id='__EVID__696624__EV__e-button__']")

# driver.find_element(By.CSS_SELECTOR, "mt-1 btn btn-sm btn-outline-primary").click()
            # # 16 | click | id=__EVID__778733__EV__e-button__ | 
            # #driver.find_element(By.ID, "__EVID__448085__EV__e-file__-btnSearch").click()
            # # 17 | click | id=__EVID__075149__EV__e-button__ | 
            # driver.find_element(By.CLASS_NAME, "mt-1 btn btn-sm btn-outline-primary").send_keys("C:\\fakepath\\Carga de Facturas - vf.pdf")
    

            #file_input = driver.find_element(by=By.ID, value="__EVID__140785__EV__e-file__-input")

            # script = "arguments[0].scrollIntoView();"

            # wait = WebDriverWait(driver, 10)
            # file_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.e-file-input-label [for="__EVID__737098__EV__e-file__-input"]')))
            # driver.implicitly_wait(10)
            # driver.execute_script(script,file_input)
            # driver.implicitly_wait(10)
            

            # input_element = WebDriverWait(driver, 10).until(
            # EC.presence_of_element_located((By.XPATH, "//label[@for='__EVID__776896__EV__e-file__-input']"))
            # )

            # input_element = WebDriverWait(driver, 10).until(
            # EC.presence_of_element_located((By.CLASS_NAME, "e-file-input-label"))
            # )

#Script que me permite scrollear hasta donde este el elemento que yo necesite
        #script = "arguments[0].scrollIntoView();"
#driver.execute_script(script,presentacionDDJJ)


# archivo_txt = "C:/Users/rgonzalez/Desktop/reporte_afip/acuse/" + c + "/" + archivos[cantArchivos][num_archivo][:5]+".txt"
                # with open(archivo_txt,'w') as archivo:
                #     archivo.write("TXT de controladora" + c)
                # num_archivo+=1
                # cantArchivos+=1

# cantArchivos = 0

        # for c in carpetas:
        #     print("Tengo la carpeta: ", c)
        #     ruta_carpeta_controladora = os.path.join(ruta_acuse, c)
        #     num_archivo = 0
        #     os.mkdir(ruta_carpeta_controladora)
        #     while(num_archivo < 2):
        #         arc = archivos[cantArchivos][num_archivo]
                
        #         print("Voy a tratar el archivo" + arc)

        #         ruta = ruta_controladoras + '\\' + c + '\\' + arc

        #         time.sleep(2)

        #         #Elemento par apoder cargar el archivo
        #         input_madre = WebDriverWait(driver, 10).until(
        #         EC.presence_of_element_located((By.CLASS_NAME, "e-file"))
        #         )
        #         EVID = input_madre.get_attribute("id")
        #         nro_EVID = EVID[8:14]
        #         id_boton_upload = f'__EVID__' + nro_EVID + '__EV__e-file__-input'
        #         objeto_input = driver.find_element(By.ID, id_boton_upload)
        #         objeto_input.send_keys(ruta)

        #         time.sleep(2)

        #         boton_presentar = driver.find_element(by="css selector", value=".btn.btn-primary[title='Presentar la declaración jurada seleccionada']")
        #         time.sleep(1)
        #         boton_presentar.click()

        #         time.sleep(2)

        #         #texto_presentada = driver.find_element(by="css selector", value='div.title[style="margin-bottom: 20px;"]').text
                
        #         #descomentar boton confirmar
        #         #boton_confirmar = driver.find_element(by="css selector", value="#confirmacionNoDuplicado button.btn.btn-primary[type='submit']")

        #         #time.sleep(1)
            
        #         #boton_confirmar.click()

        #         #time.sleep(1)

        #         aceptada = driver.find_element(By.XPATH, "//div[text()='Aceptada']").text

        #         print("DOCUMENTACION: " + aceptada)
        #         #Si esta aceptada, descargamos el acuse

        #         time.sleep(1)

        #         opciones.add_experimental_option("prefs", {
        #         "download.default_directory" : ruta_carpeta_controladora
        #         })

        #         webdriver.Chrome(options=opciones)

        #         pdf_descarga = driver.find_element(By.CLASS_NAME, "e-icon")
        #         pdf_descarga = driver.find_element(By.XPATH, "//span[text()='picture_as_pdf']")
        #         time.sleep(2)
        #         ActionChains(driver).move_to_element(pdf_descarga).perform()
        #         #BAJAR A EL BOTON DE PDF
        #         pdf_descarga.click()

        #         time.sleep(1)

        #         #En caso que este presentada tocar en boton volver
        #         boton_volver = driver.find_element(by="css selector", value="button:not(:disabled), [type='button']:not(:disabled), [type='reset']:not(:disabled), [type='submit']:not(:disabled)")

        #         time.sleep(1)

        #         boton_volver.click()


#boton_presentar = driver.find_element(by="css selector", value=".btn.btn-primary[title='Presentar la declaración jurada seleccionada']")
           
            #boton_presentar = driver.find_element(By.XPATH,"//BUTTON[@title='Presentar la declaración jurada seleccionada']")

            #wait = WebDriverWait(driver, 10)
            #boton_presentar = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".btn.btn-primary[title='Presentar la declaración jurada seleccionada']")))