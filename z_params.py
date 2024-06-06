from getpass import getuser

class ParametrosBotAfip:

    def rutasArchivos(self):

        user = getuser()

        #@audit #Ruta Controladoras (obtener documentos) y Ruta Acuse (depositar pdf acuse)
        ruta_controladoras = "C:\\Users\\"+ user +"\\Desktop\\reporte_afip\\"

        ruta_acuse = "C:\\Users\\" + user +"\\Desktop\\acuse\\"

        return ruta_acuse,ruta_controladoras
    
    def rutasAfip(self):

        user = getuser()

        #@audit #Ruta Controladoras (obtener documentos) y Ruta Acuse (depositar pdf acuse)
        
        ruta_afip = "https://auth.afip.gob.ar/contribuyente_/login.xhtml"

        return ruta_afip