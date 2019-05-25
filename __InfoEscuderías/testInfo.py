#escoge auto según temporada

class main_Pilotos():

    def __init__(self):
        self.pilotoInfo =[]
        self.IGE = 0
        self.refrescar()
        self.calcIGE()

    #[4] = participaciones \\[5] = podio \\[6] = 1er lugar\\[7] = abandonos

    def refrescar(self):
        txtEscud = open("EscuderiaInfo.txt","r+")
        filas = txtEscud.readlines()
        for x in filas:
            fila = x.split(";")
            fila[len(fila)-1] = fila[len(fila)-1].replace("\n","")
            for i in range(4, 8):
                fila[i] = int(fila[i])
            for i in range(8,len(fila)):
                fila[i] = float(fila[i])
                
            fila = self.addRGP_REP(fila)
            self.pilotoInfo.append(fila)
        txtEscud.close()

    def addRGP_REP(self,fila):
        podio = fila[5]
        partEfectiva  = fila[4]-fila[7] #totales - abandonos
        primerLugar = fila[6]
        
        #Redimiento global (general) 
        #RGP= ((Victorias + SegYTerLugar)*100)/(Participaciones - Abandonos)
        #Rendimiento especifico (victorias)
        #REP = (Victorias *100)/(Participaciones - Abandonos)

        RGP = (podio*100)/partEfectiva
        RGP = round(RGP, 2)
        REP = (primerLugar*100)/partEfectiva
        REP = round(REP, 2)
        
        try:
            fila[8] = RGP
            try:
                fila[9] =REP
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
            victorias+= piloto[6]
            participaciones += piloto[4]
        self.IGE = victorias/participaciones

    def agregarPiloto(self,infoPiloto):
        return

    def actualizarArchivo(self):
        txtEscud = open("EscuderiaInfo.txt","w")
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
        self.refrescar()


    def ordenar(self, matriz = "", param = "RGP"):
        if param == "RGP":
            param = 8
        elif param == "REP":
            param = 9
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
        ret = self.ordenar(menores)
        ret.extend(iguales)
        ret.extend(self.ordenar(mayores))
        return ret
    
        
                
            
            
        
        
        
        
