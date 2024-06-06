input_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,"div.card-body.d-flex.justify-content-center.align-items-center.flex-column.mb-4"))
            )

input_element_3 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,"label.e-file-input-label.w-100.d-flex.flex-column.align-items-center.text-center.font-weight-bold.e-file-input-label--copy"))
            )


input_element_4 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,"//label[@class='e-file-input-label w-100 d-flex flex-column align-items-center text-center font-weight-bold e-file-input-label--copy']"))
            )