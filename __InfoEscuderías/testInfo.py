def main_Pilotos(lstInfoPiloto = []):
    IGE = 0
    #[4] = participaciones \\[5] = podio \\[6] = 1er lugar\\[7] = abandonos
    pilotoInfo = []

    def refrescar():
        txtEscud = open("EscuderiaInfo.txt","r+")
        filas = txtEscud.readlines()
        nonlocal pilotoInfo
        for x in filas:
            fila = x.split(";")
            fila[len(fila)-1] = fila[len(fila)-1].replace("\n","")
            for i in range(4, len(fila)):
                fila[i] = int(fila[i])
            pilotoInfo.append(fila)
            fila = addRGP_REP(fila)
        txtEscud.close()

    def addRGP_REP(fila):
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

            
    refrescar()
    print(pilotoInfo)
        




def main_Puntajes(puntaje, jugador):
    """
    Entradas: puntaje - puntaje del jugador a comparar, nombre - nombre del jugador a ser guardado en caso de que gane un puesto mayor
    Salidas: nom - listas de nombres de mayor puntaje, score - lista de mayores puntajes
    Restricciones: 
    Funcionamiento: recibe un puntaje y jugador a comparar. Si el puntaje es vacio, solo devuelve las listas de mayores puestos y texto nulo,
    si se ingresa nombre y puntaje, retornar[a la lista de mayores puntajes y un mensaje que diga si el puntaje es mayor a alguno anterior
    """
    comparar = []
    nom = []
    score = []
    mensaje = ""
    
    def refresh():
        nonlocal comparar
        a=open("__mpnt\\puntajes.txt","r+")
        comparar = a.readlines()
        a.close()
    

    def cargar_Lista(cad,i, name):
        if cad[i] == '#':
            nonlocal nom, score
            numero = cad[i+1: (len(cad)-1)]
            nom += [name[2:]]
            score+= [numero]
            
        else:
            name = name + cad[i]
            cargar_Lista(cad,i+1,name)
            
    def refresco_Puntajes(i):
        #llena los datos de las listas locales
        if i<5:
            nonlocal comparar
            x= comparar[i]
            cargar_Lista(x,0,"")
            refresco_Puntajes(i+1)
        

    def new_Score(puntaje,jugador,cnt):
        #compara si un puntaje fue mayor a los ya existentes
        nonlocal nom,score,mensaje
        if cnt>4:
            mensaje= "no supero los puntajes anteriores"
        else:
            if puntaje > int(score[cnt]):
                nom= nom[:cnt]+[jugador]+ nom[cnt:4]
                score= score[:cnt]+[ str(puntaje) ] + score[cnt:4]
                if cnt==0:
                    rocola(4)
                mensaje ="Felicidades, su puntaje es el número " + str(cnt+1)
            else:
                new_Score(puntaje,jugador,cnt+1)
                
            
    def write_New_Scores(cnt, line):
        nonlocal nom, score
        writer= open("__mpnt\\puntajes.txt","w")

        if cnt>4:
            writer.write(line)
            return
        else:
            line = line + str(cnt+1)+"."+nom[cnt] + "#" + score[cnt]
            line = line + '\n'
        write_New_Scores(cnt+1, line)
        writer.close()
    
    refresh()        
    refresco_Puntajes(0)
    
    
    if puntaje != "" and jugador!="":
        new_Score(puntaje,jugador, 0)
        write_New_Scores(0, "")

    return nom,score,mensaje
        
