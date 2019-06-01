"""import tkinter as tk
from tkinter import ttk
elements = []
def show():

    tempList = [['Jim', '0.33'], ['Dave', '0.67'], ['James', '0.67'], ['Eden', '0.5']]
    tempList.sort(key=lambda e: e[1], reverse=True)

    for i in range(0,len(tempList)):
        data = [i+1] + tempList[i]
        data = tuple(data)
        elements.append(listBox.insert("", "end", values=data))
def erase():
    global elements
    for x in elements:
        listBox.delete(x)
    elements = []

scores = tk.Tk() 
label = tk.Label(scores, text="High Scores", font=("Arial",30)).grid(row=0, columnspan=3)
# create Treeview with 3 columns
cols = ('Position', 'Name', 'Score')
listBox = ttk.Treeview(scores, columns=cols, show='headings')
# set column headings
for col in cols:
    listBox.heading(col, text=col)    
listBox.grid(row=1, column=0, columnspan=2)

showScores = tk.Button(scores, text="Show scores", width=15, command=show).grid(row=4, column=0)
closeButton = tk.Button(scores, text="Close", width=15, command=erase).grid(row=4, column=1)

scores.mainloop()
"""
import sys
import os
from random import randint
from autos import main_Autos
from pilotos import main_Pilotos
from tkinter import *
from tkinter import ttk
from threading import Thread
from time import sleep


pilotos = main_Pilotos()
autos = main_Autos() 

root = Tk()
root.title('Prueba de carga')
root.minsize(800,400)
root.resizable(width=NO,height=NO)

c_Main= Canvas(root,width=800,height=600)
c_Main.place(relx=0.50,rely=0.5, anchor ='c')


elements = []
def cargar(param):
    global ordenActual
    pilotos.ordenar(param)
    global elements
    for x in elements:
        listBox.delete(x)
    elements = []
    for i in range(0, len(pilotos.pilotoInfo)):
        data = [i+1]+pilotos.pilotoInfo[i][:4] + pilotos.pilotoInfo[i][5:]
        data = tuple(data)
        elements.append(listBox.insert("", "end", values=data))


label = Label(c_Main, text="Pilotos", font=("Arial",30)).grid(row=0, columnspan=3)
cols = ('Pos','Nombre Completo',"Edad","Nacionalidad","Tempo","Eventos","Podio","Victorias","Abandonos","REP","RGP")
listBox = ttk.Treeview(c_Main,columns=cols, show='headings')
for col in cols:
    listBox.heading(col, text=col)
listBox.heading('REP', command =lambda : cargar("REP"))
listBox.heading('RGP', command =lambda : cargar("RGP"))

listBox.column(cols[0], width = 30, anchor = 'c')
listBox.column(cols[1], width = 120, anchor = 'c')
listBox.column(cols[2], width = 40, anchor = 'c')
listBox.column(cols[3], width = 90, anchor = 'c')
for i in range(3, len(cols)):
    listBox.column(cols[i], width = 70, anchor = 'c')
listBox.grid(row=1, column=0, columnspan=2)



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
        cargar(pilotos.CURRENTORDER)
        
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



def modificarPiloto(piloto = ""):
    global cols
    root.withdraw()
    AP=Toplevel()
    AP.title("Agregar Piloto")
    AP.minsize(320,270)
    AP.resizable(width=NO,height=NO)
    CAP = Canvas(AP, width = 320, height = 270)
    CAP.place(x=0, y=0, anchor =NW)
    
    def closeAP():
        global cargar, ordenActual,pilotos
        root.deiconify()
        AP.destroy()
        cargar(pilotos.CURRENTORDER)


        
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
        newData.insert(4,pilotos.pilotoInfo[pos][4])                    
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

    




Btn_modificar = Button(c_Main, text = "modificar información", width = 50, command = lambda: modificarPiloto(list(listBox.item(listBox.selection(),'values')))).grid(row= 2, column =1)
Btn_agregar = Button(c_Main, text="agregar piloto", width=50, command=lambda: agregarPiloto()).grid(row = 2, column = 0 )
Btn_TestDrive = Button(c_Main, text="TestDrive", width=50, command=lambda: cargar("REP")).grid(rowspan = 3, columnspan = 3 )
cargar(pilotos.CURRENTORDER)
#root.mainloop()
