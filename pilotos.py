#escoge auto según temporada
#movimiento especial = "dir=1.pwm=1023.dir=-1.pwm=-900.zigzag"

class main_Pilotos:
    #constantes de posicion de datos en la lista pilotoInfo
    iNOM =0
    iEDAD =1
    iPAIS=2
    iTEMPO=3
    iMOV=4
    iPARTICIPA=5
    iPODIO=6
    iVICTO=7
    iABANDO=8
    iREP = 9
    iRGP = 10
    txtfile = "__InfoEscuderías\\EscuderiaInfo.txt"
    CURRENTORDER = "REP"
    

    def __init__(self):
        self.pilotoInfo =[]
        self.IGE = 0
        
        self.refrescar()
        
 

    def refrescar(self):
        txtEscud = open(self.txtfile,"r+")
        filas = txtEscud.readlines()
        self.pilotoInfo = []
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
            self.pilotoInfo.append(fila)
        txtEscud.close()
        self.calcIGE()
        

    def addRGP_REP(self,fila):
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
        for piloto in self.pilotoInfo:
            victorias+= piloto[self.iVICTO]
            participaciones += piloto[self.iPARTICIPA]
        self.IGE = victorias/participaciones

    def agregarPiloto(self,nombre,edad,pais,temp,movimientos, participaciones, podio, victorias, abandonos):
        nuevoDatos = [nombre,edad,pais,temp,movimientos, participaciones, podio, victorias, abandonos]
        self.pilotoInfo.append(nuevoDatos)
        self.ordenar(self.CURRENTORDER)
            
    def modificarPiloto(self, pos, nombre,edad,pais,temp,movimientos, participaciones, podio, victorias, abandonos):
        modDatos = [nombre,edad,pais,temp,movimientos, participaciones, podio, victorias, abandonos]
        self.pilotoInfo.pop(pos)
        self.pilotoInfo.append(modDatos)
        self.ordenar(self.CURRENTORDER)

    def actualizarArchivo(self):
        txtEscud = open(self.txtfile,"w")
        src = self.pilotoInfo
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
        
        
    def ordenar(self, param):
        if type(param) is str:
            if param== "RGP" or param == "REP":
                self.CURRENTORDER = param
                self.actualizarArchivo()
                self.pilotoInfo = self.ordenar_aux("", param)
                self.actualizarArchivo()
            else:
                return "parametro no valido"
        else:
            return "parametro de tipo incorrecto"

    def ordenar_aux(self, matriz = "", paramcd = "RGP"):
        if paramcd == "RGP":
            param = self.iRGP
        elif paramcd == "REP":
            param = self.iREP
        else:
            return "Error, parametro invalido"
        
        if matriz == "":
            matriz = self.pilotoInfo
        elif matriz == []:
            return []

        def partir(pilotos, pivote):
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
        comandos = self.pilotoInfo[posPiloto][self.iMOV]
        comandos = comandos.split(".")
        for cmd in range(0, len(comandos)):
            comandos[cmd] = comandos[cmd].replace("=",":") + ";"
            
        return comandos
        

    
                
            
            
        
        
        
        
