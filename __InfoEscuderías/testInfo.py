#escoge auto según temporada

class main_Pilotos():

    def __init__(self, lstInfoPiloto = [], posPiloto = False):
        self.listInfoPiloto = lstInfoPiloto
        self.posPiloto = posPiloto
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
            for i in range(4, len(fila)):
                fila[i] = int(fila[i])
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
