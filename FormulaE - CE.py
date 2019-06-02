import sys
import os
from random import randint
from autos import main_Autos
from pilotos import main_Pilotos
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from threading import Thread
from time import sleep

def cargar_imagen(Nombre):
    ruta = os.path.join("__Interfaz\\imagenes",Nombre)
    Imagen = PhotoImage(file = ruta)
    return Imagen

pilotos = main_Pilotos()
autos = main_Autos() 

root = Tk()
root.title('Prueba de carga')
root.minsize(830,700)
root.resizable(width=NO,height=NO)

uFont = ('Arial', 14)
uBG = '#FAFAFA'
c_Main= Canvas(root,width=830,height=700,bd=0, highlightthickness=0, bg= uBG)
#c_Main.place(relx=0.5,rely=0.5, anchor ='c')
c_Main.pack(expand=2, anchor='c', fill=Y)


elements = []
def cargarPilotos(param):
    global ordenActual
    pilotos.ordenar(param)
    global elements
    for x in elements:
        listBox.delete(x)
    elements = []
    for i in range(0, len(pilotos.info)):
        data = [i+1]+pilotos.info[i][:4] + pilotos.info[i][5:]
        data = tuple(data)
        elements.append(listBox.insert("", "end", values=data))
        
elementsA = []
def cargarAutos():
    autos.ordenar()
    global elementsA
    for x in elementsA:
        listBoxAut.delete(x)
    elementsA= []
    for i in range(0, len(autos.info)):
        data = autos.info[i][:autos.iFOTO] + autos.info[i][autos.iTEMPO:]
        data = tuple(data)
        elementsA.append(listBoxAut.insert("", "end", values=data))

#Organizacion del TreeView de Pilotos
labelPil = Label(c_Main, text="Pilotos",bg=uBG, font=("Arial",30)).grid(row=0, columnspan=3)
cols = ('Pos','Nombre Completo',"Edad","Nacionalidad","Tempo","Eventos","Podio","Victorias","Abandonos","REP","RGP")
listBox = ttk.Treeview(c_Main,columns=cols, show='headings')
for col in cols:
    listBox.heading(col, text=col)
listBox.heading('REP', command =lambda : cargarPilotos("REP"))
listBox.heading('RGP', command =lambda : cargarPilotos("RGP"))

listBox.column(cols[0], width = 30, anchor = 'c')
listBox.column(cols[1], width = 120, anchor = 'c')
listBox.column(cols[2], width = 40, anchor = 'c')
listBox.column(cols[3], width = 90, anchor = 'c')
for i in range(3, len(cols)):
    listBox.column(cols[i], width = 80, anchor = 'c')
listBox.grid(row=1, column=0, columnspan=2)

#Organización del TreeView de Autos

labelAutos = Label(c_Main, text="Autos",bg=uBG, font=("Arial",30)).grid(row=4, columnspan=3)
colsAut = ('Marca','Modelo','Origen','Temporada','Baterias','CPB','VoltPB','Estado','Consumo','sensores','Peso','Eficiencia')
listBoxAut = ttk.Treeview(c_Main,columns=colsAut, show='headings')
for col in colsAut:
    listBoxAut.heading(col, text=col)
for i in range(0, len(colsAut)):
    listBoxAut.column(colsAut[i], width =70, anchor ='c')
listBoxAut.grid(row=5, column=0, columnspan=2)



def agregarPiloto():
    global cols
    root.withdraw()
    AP=Toplevel()
    AP.title("Agregar Piloto")
    AP.minsize(320,270)
    AP.resizable(width=NO,height=NO)
    CAP = Canvas(AP, width = 320, height = 270)
    CAP.place(x=0, y=0, anchor =NW)
    
    def closeAP():
        root.deiconify()
        AP.destroy()
        cargarPilotos(pilotos.CURRENTORDER)
        
    hojaTec= []
    for i in range(1,len(cols)-2):
        Label(CAP, text = cols[i]).place(x=5,y=(20*i)+20)
        entryText=Entry(CAP,width=30, justify = CENTER)
        entryText.place(x=120, y=(20*i)+20)
        hojaTec.append(entryText)
    
    def enviar():
        global pilotos
        nonlocal hojaTec, closeAP
        
        def createCeleb():
            newCeleb = "pwm=0"
            for x in range(0,5):
                mov = randint(0, 5)
                if mov == 0:
                    newCeleb += ".dir=1"
                elif mov == 1:
                    newCeleb += ".dir=-1"
                elif mov == 2:
                    newCeleb += ".dir=0"
                elif mov == 3:
                    newCeleb += ".pwm=" + str(randint(700, 1023))
                elif mov == 4:
                    newCeleb += ".pwm="+ str(randint(-1023, -700))
                elif mov == 5:
                    newCeleb += ".zigzag"
            return newCeleb
        
        newData = []
        for x in hojaTec:
            newData.append(x.get())                   
        for i in range(0, len(newData)):
            if i!= 0 and i!= 2 :
                try:
                    float(newData[i])
                except:
                    print(newData[i])
                    i= len(newData)
                    print(newData)
                    print("error")
        newData.insert(4, createCeleb())
        tuple(newData)
        pilotos.agregarPiloto(*newData)
        closeAP()

        
        
    Btn_cerrar = Button(CAP, width=25,text="Cerrar",command=closeAP).place(x = 10, y=5)
    Btn_agregar = Button(CAP, width=25,text="Agregar",command=enviar).place(x = 10, y = 220)



def modificarPiloto(piloto):
    if piloto == []:
        return
    global cols
    root.withdraw()
    AP=Toplevel()
    AP.title("Modificar Piloto")
    AP.minsize(320,270)
    AP.resizable(width=NO,height=NO)
    CAP = Canvas(AP, width = 320, height = 270)
    CAP.place(x=0, y=0, anchor =NW)
    
    def closeAP():
        global cargarPilotos, ordenActual,pilotos
        root.deiconify()
        AP.destroy()
        cargarPilotos(pilotos.CURRENTORDER)
        
    hojaTec= []
    for i in range(1,len(cols)-2):
        Label(CAP, text = cols[i]).place(x=5,y=(20*i)+20)
        entryText=Entry(CAP,width=30, justify = CENTER)
        entryText.place(x=120, y=(20*i)+20)
        entryText.insert(0,piloto[i])
        hojaTec.append(entryText)
    pos = int(piloto[0])-1
        
    def enviar():
        global pilotos
        nonlocal hojaTec, pos, closeAP
        newData = []
        for x in hojaTec:
            newData.append(x.get())
        newData.insert(4,pilotos.info[pos][4])                    
        newData.insert(0,pos)
        for i in range(0, len(newData)):
            if i!= 1 and i!= 3 and i!=5:
                try:
                    float(newData[i])
                except:
                    print(newData[i])
                    i= len(newData)
                    print(newData)
                    print("error")
        tuple(newData)
        pilotos.modificarPiloto(*newData)
        closeAP()
        
    Btn_cerrar = Button(CAP, width=25,text="Cerrar",command=closeAP).place(x = 10, y=5)
    Btn_agregar = Button(CAP, width=25,text="Guardar",command=enviar).place(x = 10, y = 220)


def agregarAuto():
    global colsAut
    root.withdraw()
    Aa=Toplevel()
    Aa.title("Agregar Auto")
    Aa.minsize(320,340)
    Aa.resizable(width=NO,height=NO)
    CAP = Canvas(Aa, width = 320, height = 340)
    CAP.place(x=0, y=0, anchor =NW)
    
    def closeAP():
        root.deiconify()
        Aa.destroy()
        cargarAutos()
        
    hojaTec= []
    for i in range(0,len(colsAut)):
        Label(CAP, text = colsAut[i]).place(x=5,y=(20*(i+1))+20)
        entryText=Entry(CAP,width=30, justify = CENTER)
        entryText.place(x=120, y=(20*(i+1))+20)
        hojaTec.append(entryText)
        
    Label(CAP, text = 'Archivo Foto').place(x=5,y=(20*(len(colsAut)+1))+20)
    entryText=Entry(CAP,width=30, justify = CENTER)
    entryText.place(x=120, y=(20*(len(colsAut)+1))+20)
    hojaTec.append(entryText)   
    
    def enviar():
        global pilotos
        nonlocal hojaTec, closeAP
        
        newData = []
        for x in hojaTec:
            newData.append(x.get())
        newData.insert(autos.iFOTO, newData[-1])
        newData.pop(-1)
        tuple(newData)
        autos.agregarAuto(*newData)
        closeAP()

        
        
    Btn_cerrar = Button(CAP, width=25,text="Cerrar",command=closeAP).place(x = 10, y=5)
    Btn_agregar = Button(CAP, width=25,text="Agregar",command=enviar).place(x = 10, y = 310)


    

def modificarAuto(Auto,pos):
    if Auto == []:
        return
    global colsAut
    root.withdraw()
    Aa=Toplevel()
    Aa.title("Modificar Auto")
    Aa.minsize(320,330)
    Aa.resizable(width=NO,height=NO)
    CAP = Canvas(Aa, width = 320, height = 330)
    CAP.place(x=0, y=0, anchor =NW)
    
    def closeAP():
        global cargarAutos, autos
        root.deiconify()
        Aa.destroy()
        cargarAutos()
        
    hojaTec= []
    for i in range(0,len(colsAut)-1):
        Label(CAP, text = colsAut[i]).place(x=5,y=(20*(i+1))+20)
        entryText=Entry(CAP,width=30, justify = CENTER)
        entryText.place(x=120, y=(20*(i+1))+20)
        entryText.insert(0,Auto[i])
        hojaTec.append(entryText)
        
    Label(CAP, text = "Archivo Foto").place(x=5,y=(20*(len(colsAut)+1))+20)
    entryText=Entry(CAP,width=30, justify = CENTER)
    entryText.place(x=120, y=(20*(len(colsAut)+1))+20)
    entryText.insert(0,autos.info[pos][autos.iFOTO])
    hojaTec.append(entryText)
        
    def enviar():
        global autos
        nonlocal hojaTec, closeAP,pos
        newData = []
        for x in hojaTec:
            newData.append(x.get())
            
        newData.insert(autos.iFOTO,newData[-1])
        newData.pop(-1)
        newData.insert(autos.iEFICIENCIA,autos.info[pos][autos.iEFICIENCIA])   
        newData.insert(0,pos)
        tuple(newData)
        autos.modificarAuto(*newData)
        closeAP()
        
    Btn_cerrar = Button(CAP, width=25,text="Cerrar",command=closeAP).place(x = 10, y=5)
    Btn_agregar = Button(CAP, width=25,text="Guardar",command=enviar).place(x = 10, y = 300)

def verFoto(indAuto):
    global autos
    TkFoto = Toplevel()
    TkFoto.title("Foto")
    TkFoto.minsize(600,400)
    TkFoto.resizable(width=NO,height=NO)
    CAP = Canvas(TkFoto, width = 600, height = 400)
    CAP.place(x=0, y=0, anchor =NW)
    try:
        foto = cargar_imagen(autos.info[indAuto][autos.iFOTO])
    except:
        messagebox.showinfo('Error','ruta de imagen no valida')
        TkFoto.destroy()
        return
    CAP.create_image(0,0, image=foto, anchor = NW)
    CAP.fotoAuto = foto
    TkFoto.protocol("WM_DELETE_WINDOW", lambda : TkFoto.destroy())
    




Btn_modificar = Button(c_Main, text = "modificar información", width = 50, command = lambda: modificarPiloto(list(listBox.item(listBox.selection(),'values')))).grid(row= 2, column =1)
Btn_agregar = Button(c_Main, text="agregar piloto", width=50, command=lambda: agregarPiloto()).grid(row = 2, column = 0 )
Btn_TestDrive = Button(c_Main, text="TestDrive", width=50, command=lambda: cargarPilotos("REP")).grid(row=3, columnspan = 3 )

Btn_modificarA = Button(c_Main, text = "modificar información", width = 50, command = lambda: modificarAuto(list(listBoxAut.item(listBoxAut.selection(),'values')), listBoxAut.index(listBoxAut.selection()))).grid(row= 6, column =1)
Btn_agregarA = Button(c_Main, text="agregar auto", width=50, command=lambda: agregarAuto()).grid(row = 6, column = 0 )
Btn_VerFoto = Button(c_Main, text="Ver foto", width=50, command=lambda: verFoto(listBoxAut.index(listBoxAut.selection()))).grid(row=7, columnspan = 3 )

cargarPilotos(pilotos.CURRENTORDER)
cargarAutos()
#root.mainloop()
