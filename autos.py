"""
______________________________________
Instituto Tecnológico de Costa Rica

Escuela de Ingeniería en Computadores

Curso: Taller de Programación, CE-1102

Project III, Part II
Formula E CE-TEC
Energy Saving and Telemetry Part II
Módulo de manejo de Autos

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
class main_Autos:
    """
    Clase de manejo de archivos, orden, agregar, modificar y refrescar la lista de autos 
    """
    #constantes de posicion de datos en la lista info
    iMARCA =0
    iMODELO =1
    iPAIS=2
    iFOTO=3
    iTEMPO=4
    iCNTBATERIAS=5
    iPPBATERIA=6
    iVOLTBATERIA=7
    iESTADO=8
    iCONSUMO = 9
    iSENSORES = 10
    iPESO=11
    iEFICIENCIA=12
    txtfile = "__InfoEscuderías\\AutoInfo.txt"
    

    def __init__(self):
        self.info =[]
        self.refrescar()
 

    def refrescar(self):
        """
        Funcionamiento:refresca la lista self.info basado en el archivo __InfoEscuderías\\AutoInfo.txt
        """
        txtAuto = open(self.txtfile,"r+")
        filas = txtAuto.readlines()
        self.info = []
        for x in filas:
            fila = x.split(";")
            fila[-1] = fila[-1].replace("\n","") #elimina salto de línea
            fila[-1] = float(fila[-1]) #convierte eficiencia a float
            fila[self.iTEMPO] = int(fila[self.iTEMPO]) #convierte temporada en int
            self.info.append(fila)
        txtAuto.close()

    def agregarAuto(self,marca, mod , pai, fot, temp, cntbat, ppb, vpb, est, consu, sense, peso, ef):
        """
        Entradas:marca, mod , pai, fot, temp, cntbat, ppb, vpb, est, consu, sense, peso, ef
        Salidas: True si se agregó el auto, False de lo contrario
        Restricciones: temp no puede ser igual al año de temporada de algún otro auto ya existente, todas las entradas deben ser string
        Funcionamiento: agrega un auto a self.info, actualiza el archivo de texto basado en el mismo
        """
        nuevoDatos = [marca, mod, pai, fot, temp, cntbat, ppb, vpb, est, consu, sense, peso, ef]
        for x in self.info:
            if int(temp) == x[self.iTEMPO]: #verifica que no haya un auto de igual temporada
                return False
        self.info.append(nuevoDatos)
        self.actualizarArchivo()
        return True
            
    def modificarAuto(self, pos, marca, mod , pai, fot, temp, cntbat, ppb, vpb, est, consu, sense, peso, ef):
        """
        Entradas: pos, marca, mod , pai, fot, temp, cntbat, ppb, vpb, est, consu, sense, peso, ef
        Salidas: -------------------------
        Restricciones:Todas las entradas deben ser strings
        Funcionamiento: modifica los datos de un auto basado en entradas de valores de reeemplazo
        elimina el auto y agrega su version actualizada
        """
        modDatos = [marca, mod , pai, fot, temp, cntbat, ppb, vpb, est, consu, sense, peso, ef]
        self.info.pop(pos)#elimina version previa de auto
        self.info.append(modDatos) #agrega datos modificados
        self.actualizarArchivo()

    def actualizarArchivo(self):
        """
        Entradas:----------------
        Salidas:---------------
        Restricciones:---------------
        Funcionamiento:Reescribe el archivo de texto base basado en self.info
        """
        txtAuto = open(self.txtfile,"w")
        src = self.info
        datos = ""
        for auto in src:
            line = ""
            for x in auto: #recorre cada elemento de cada auto para formatarlo para escritura
                if type(x) is int or type(x) is float:
                    x = str(x)
                line+= x + ";"
            line = line[0:-1] + '\n' #agrega salto de linea
            datos += line

        txtAuto.write(datos)
        txtAuto.close()
        self.refrescar()
        
    def ordenar(self, Dsc = True):
        """
        Entradas: self, Dsc  - Si la salida debe ser ascendente o descendente
        Salidas: --------------
        Restricciones: Dsc debe ser True o False
        Funcionamiento: Llama al auxiliar, y retorna la matriz ordenada de forma descendente o ascendente basado en Dsc
        Actualiza el archivo según este nuevo orden
        """
        if Dsc:
            self.info = self.ordenar_aux("")[::-1] #devuelve lista descendente
        else:
            self.info = self.ordenar_aux("")
            
        
        self.actualizarArchivo()

    def ordenar_aux(self, matriz = ""):
        """
        Entradas:self, matriz - Matriz que se ordena, inicialmente es self.info, luego se llama a sí misma de forma recursiva
        Salidas: Matriz de autos ordenada por eficiencia
        Restricciones: matriz debe ser tipo lista
        Funcionamiento: usa la función partir para comparar consecutivamente eficiencias de carros usando un algoritmo de quick sort
        """
        param = self.iEFICIENCIA #ordena según eficiencia
        
        if matriz == "":
            matriz = self.info
        elif matriz == []:
            return []

        def partir(autos, pivote):
            """
            Entradas:autos, pivote
            Salidas: lista de menores, mayores e iguales en eficiencia del auto pivote
            Restricciones: autos debe ser una lista, pivote debe ser un elemento de self.info que tenga Eficiencia de valor numérico
            Funcionamiento: compara el pivote contra cada elemento, y separa los distintos elementos de autos en tres
            listas según esto
            """
            menores = []
            iguales = []
            mayores = []
            for x in autos: #recorre cada auto y compara su eficiencia
                if x[param] < pivote:
                    menores.append(x)
                elif x[param] == pivote:
                    iguales.append(x)
                elif x[param] > pivote:
                    mayores.append(x)
            return menores, iguales,  mayores
        
        menores, iguales, mayores = partir(matriz, matriz[0][param])
        ret = self.ordenar_aux(menores)
        ret.extend(iguales)
        ret.extend(self.ordenar_aux(mayores))
        return ret
                
            
            
        
        
        
        
