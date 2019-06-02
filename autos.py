#escoge auto según temporada
#movimiento especial = "dir=1.pwm=1023.dir=-1.pwm=-900.zigzag"

class main_Autos:
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
        txtAuto = open(self.txtfile,"r+")
        filas = txtAuto.readlines()
        self.info = []
        for x in filas:
            fila = x.split(";")
            fila[-1] = fila[-1].replace("\n","")
            fila[-1] = float(fila[-1])
            fila[self.iTEMPO] = int(fila[self.iTEMPO])
            self.info.append(fila)
        txtAuto.close()

    def agregarAuto(self,marca, mod , pai, fot, temp, cntbat, ppb, vpb, est, consu, sense, peso, ef):
        nuevoDatos = [marca, mod, pai, fot, temp, cntbat, ppb, vpb, est, consu, sense, peso, ef]
        self.info.append(nuevoDatos)
        self.actualizarArchivo()
            
    def modificarAuto(self, pos, marca, mod , pai, fot, temp, cntbat, ppb, vpb, est, consu, sense, peso, ef):
        modDatos = [marca, mod , pai, fot, temp, cntbat, ppb, vpb, est, consu, sense, peso, ef]
        self.info.pop(pos)
        self.info.append(modDatos)
        self.actualizarArchivo()

    def actualizarArchivo(self):
        txtAuto = open(self.txtfile,"w")
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

        txtAuto.write(datos)
        txtAuto.close()
        self.refrescar()
        
    def ordenar(self):
        self.info = self.ordenar_aux("")
        self.actualizarArchivo()

    def ordenar_aux(self, matriz = ""):
        param = self.iEFICIENCIA
        
        if matriz == "":
            matriz = self.info
        elif matriz == []:
            return []

        def partir(autos, pivote):
            menores = []
            iguales = []
            mayores = []
            for x in autos:
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

    
                
            
            
        
        
        
        
