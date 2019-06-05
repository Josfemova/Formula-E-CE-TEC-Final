"""
______________________________________
Instituto Tecnológico de Costa Rica

Escuela de Ingeniería en Computadores

Curso: Taller de Programación, CE-1102

Project III, Part II
Formula E CE-TEC
Energy Saving and Telemetry Part II
Módulo de manejo de Pilotos

Profesor:
Milton Villegas Lemus
Asistente:
Santiago Gamboa

Desarrolladores/Autores:
Alejandro José Quesada Calderón
Carné: 2019150208
José Fernando Morales Vargas
Carné: 2019024270

Año: 2019

País de Producción: Costa Rica

Versión del programa: 1.0.0

Versión de Python: 3.7.2
____________________________________
"""
class main_Pilotos:
    """
    Clase de manejo de archivos, orden, agregar, modificar y refrescar la lista de pilotos
    """
    #constantes de posicion de datos en la lista info
    iFOTO= 0
    iNOM =1
    iEDAD =2
    iPAIS=3
    iTEMPO=4
    iMOV=5
    iPARTICIPA=6
    iPODIO=7
    iVICTO=8
    iABANDO=9
    iREP = 10
    iRGP = 11
    
    txtfile = "__InfoEscuderías\\EscuderiaInfo.txt"
    CURRENTORDER = "REP"
    

    def __init__(self):
        self.info =[]
        self.IGE = 0
        
        self.refrescar()
        
 

    def refrescar(self):
        """
        Funcionamiento:refresca la lista self.info basado en el archivo __InfoEscuderías\\EscuderiaInfo.txt
        """
        txtEscud = open(self.txtfile,"r+")
        filas = txtEscud.readlines()
        self.info = []
        for x in filas:
            fila = x.split(";")
            fila[-1] = fila[-1].replace("\n","")
            for i in range(self.iPARTICIPA, self.iREP):
                fila[i] = int(fila[i])
                #print(i)
                
            if len(fila) == self.iRGP+1:
                fila[self.iREP] = float(fila[self.iREP])
                fila[self.iRGP] = float(fila[self.iRGP])
                
            fila = self.addRGP_REP(fila)
            self.info.append(fila)
        txtEscud.close()
        self.calcIGE()
        

    def addRGP_REP(self,fila):
        """
        Entradas:fila  - un piloto de la matriz self.info
        Salidas:fila con el RGP y el REP agregados\recalculado
        Restricciones:los datos de victorias, particiapciones, abandonos y podios deben ser
        tipo int
        Funcionamiento:aplica las operaciones provistas en el docuemnto
        de requerimentos a los datos de los pilotos
        """
        podio = fila[self.iPODIO]
        partEfectiva  = fila[self.iPARTICIPA]-fila[self.iABANDO] #totales - abandonos
        primerLugar = fila[self.iVICTO]
        
        #Redimiento global (general) 
        #RGP= ((Victorias + SegYTerLugar)*100)/(Participaciones - Abandonos)
        #Rendimiento especifico (victorias)
        #REP = (Victorias *100)/(Participaciones - Abandonos)

        RGP = (podio*100)/partEfectiva
        RGP = round(RGP, 2)
        REP = (primerLugar*100)/partEfectiva
        REP = round(REP, 2)
        
        try:
            fila[self.iRGP] = RGP
            try:
                fila[self.iREP] =REP
            except:
                fila.append(REP)
        except:
            fila.append(RGP)
            fila.append(REP)

        return fila
    
    def calcIGE(self):
        participaciones = 0
        victorias = 0
        for piloto in self.info:
            victorias+= piloto[self.iVICTO]
            participaciones += piloto[self.iPARTICIPA]
        self.IGE = victorias/participaciones

    def agregarPiloto(self,foto,nombre,edad,pais,temp,movimientos, participaciones, podio, victorias, abandonos):
        """
        Entradas:foto,nombre,edad,pais,temp,movimientos, participaciones, podio, victorias, abandonos
        Salidas: --------------------------------
        Funcionamiento: agrega un piloto a self.info, actualiza el archivo de texto basado en el mismo
        """
        nuevoDatos = [foto,nombre,edad,pais,temp,movimientos, participaciones, podio, victorias, abandonos]
        self.info.append(nuevoDatos)
        self.ordenar(self.CURRENTORDER)
            
    def modificarPiloto(self, pos, foto,nombre,edad,pais,temp,movimientos, participaciones, podio, victorias, abandonos):
        """
        Entradas:foto,nombre,edad,pais,temp,movimientos, participaciones, podio, victorias, abandonos
        Salidas: --------------------------------
        Restricciones:Todas las entradas deben ser strings
        Funcionamiento: modifica los datos de un piloto basado en entradas de valores de reeemplazo
        elimina el piloto y agrega su version actualizada
        """
        modDatos = [foto,nombre,edad,pais,temp,movimientos, participaciones, podio, victorias, abandonos]
        self.info.pop(pos)
        self.info.append(modDatos)
        self.ordenar(self.CURRENTORDER)

    def actualizarArchivo(self):
        """
        Entradas:----------------
        Salidas:---------------
        Restricciones:---------------
        Funcionamiento:Reescribe el archivo de texto base basado en self.info
        """
        txtEscud = open(self.txtfile,"w")
        src = self.info
        datos = ""
        for piloto in src:
            line = ""
            for x in piloto:
                if type(x) is int or type(x) is float:
                    x = str(x)
                line+= x + ";"
            line = line[0:-1] + '\n'
            datos += line

        txtEscud.write(datos)
        txtEscud.close()
        
        self.refrescar()
        
        
    def ordenar(self, param, Desc = True):
        """
        Entradas: self,param - REP o RGP, Dsc  - Si la salida debe ser ascendente o descendente
        Salidas: si el parametro no es correcto, lo indica
        Restricciones: Dsc debe ser True o False, param debe ser REP o RGP
        Funcionamiento: Llama al auxiliar, y retorna la matriz de  pilotos ordenada de forma descendente o ascendente basado en Dsc
        Actualiza el archivo según este nuevo orden
        """
        if type(param) is str:
            if param== "RGP" or param == "REP":
                self.CURRENTORDER = param
                self.actualizarArchivo()
                if Desc:
                    self.info = self.ordenar_aux("", param)[::-1]
                else:
                    self.info = self.ordenar_aux("", param)
                self.actualizarArchivo()
            else:
                return "parametro no valido"
        else:
            return "parametro de tipo incorrecto"

    def ordenar_aux(self, matriz = "", paramcd = "RGP"):
        """
        Entradas:self, matriz - Matriz que se ordena, inicialmente es self.info, luego se llama a sí misma de forma recursiva, paramcd - Si se ordena por REP o RGP
        Salidas: Matriz de autos ordenada por eficiencia
        Restricciones: matriz debe ser tipo lista, paramcd debe ser REP o RGP
        Funcionamiento: usa la función partir para comparar consecutivamente REP o RGP de pilotos usando un algoritmo de quick sort
        """
        if paramcd == "RGP":
            param = self.iRGP
        elif paramcd == "REP":
            param = self.iREP
        else:
            return "Error, parametro invalido"
        
        if matriz == "":
            matriz = self.info
        elif matriz == []:
            return []

        def partir(pilotos, pivote):
            """
            Entradas:pilotos, pivote
            Salidas: lista de menores, mayores e iguales en param de pilotos
            Restricciones: pilotos debe ser una lista, pivote debe ser un elemento de self.info que tenga el param de valor numérico
            Funcionamiento: compara el pivote contra cada elemento, y separa los distintos elementos de autos en tres
            listas según esto
            """
            menores = []
            iguales = []
            mayores = []
            for x in pilotos:
                if x[param] < pivote:
                    menores.append(x)
                elif x[param] == pivote:
                    iguales.append(x)
                elif x[param] > pivote:
                    mayores.append(x)
            return menores, iguales,  mayores
        
        menores, iguales, mayores = partir(matriz, matriz[0][param])
        ret = self.ordenar_aux(menores,paramcd)
        ret.extend(iguales)
        ret.extend(self.ordenar_aux(mayores,paramcd))
        return ret

    def getCelebracion(self, posPiloto):
        """
        Entradas:self, posPiloto - posicion de piloto en la matriz
        Salidas: lista de movimientos formateados para ejecutar en el modulo de test drive
        Restricciones: posPiloto debe ser una posición válida de piloto
        """
        comandos = self.info[posPiloto][self.iMOV]
        comandos = comandos.split(".")
        for cmd in range(0, len(comandos)):
            comandos[cmd] = comandos[cmd].replace("=",":") + ";"
            
        return comandos
        

    
                
            
            
        
        
        
        
