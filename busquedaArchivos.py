import os
from getpass import getuser
from z_params import ParametrosBotAfip

def buscarArchivos():
        
    #Obtengo rutas de la carpeta reporte_afip
    parametros = ParametrosBotAfip()
    ruta_acu, ruta_cont = parametros.rutasArchivos()

    #Ingreso a la carpeta de las controladoras fiscales
    carpetas_controladoras = os.listdir(ruta_cont)

    #Creo array para poder devolver los documentos a subir como DDJJ
    retorno_archivos = []

    #Defino el contador que va a guardar las variables de las contadoras
    i = 0

    #Busco dentro de la carpetas de las controladoras los archivos y los agrego a la matriz a devolver
    for controladora in carpetas_controladoras:
        j = 0
        if controladora in carpetas_controladoras: 
            try:
                ruta_sub_carpeta = ruta_cont + controladora
                sub_carpeta = os.listdir(ruta_sub_carpeta)
                archivos_subir = os.listdir(ruta_sub_carpeta + "/" + str(sub_carpeta[0]))
                ruta = (ruta_sub_carpeta + '\\' + str(sub_carpeta[0]))
                for arc in archivos_subir:
                    print("Archivo: ",arc)
                    nombre_archivo = str(arc)
                    #@audit En caso que sea F8010 no se va a subir, lo excluimos del array
                    if not nombre_archivo[:5] == "F8010":
                        retorno_archivos.append(ruta + '\\' +arc)
                        j+=1
                        print("DOC: " + arc + " para subir")
                    else:
                        print("Archivo F8010 no se sube")
                        print(arc)
            except Exception as ex:
                print(ex)
                pass
            i+=1

    return retorno_archivos

# parametros = ParametrosBotAfip()
# ruta_acuse, ruta_carpeta = parametros.rutasArchivos()

# print("Resultado de archivos")
# archivos = buscarArchivos()