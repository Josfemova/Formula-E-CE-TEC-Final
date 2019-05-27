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
root.minsize(800,600)
root.resizable(width=NO,height=NO)

c_Main= Canvas(root,width=800,height=600)
c_Main.place(relx=0.50,y=150, anchor ='c')



elements = []
def cargar(param):
    pilotos.ordenar(param)
    global elements
    for x in elements:
        listBox.delete(x)
    elements = []
    for i in range(0, len(pilotos.pilotoInfo)):
        data = [i+1]+pilotos.pilotoInfo[i][:4] + pilotos.pilotoInfo[i][5:]
        data = tuple(data)
        elements.append(listBox.insert("", "end",tag='el', values=data))


label = Label(c_Main, text="High Scores", font=("Arial",30)).grid(row=0, columnspan=3)
cols = ('Pos','Nombre Completo',"Edad","Nacionalidad","Tempo","Eventos","Podio","Victorias","Abandonos","REP","RGP")
listBox = ttk.Treeview(c_Main,columns=cols, show='headings')
for col in cols:
    listBox.heading(col, text=col)
listBox.heading('REP', command =lambda : cargar("REP"))
listBox.heading('RGP', command =lambda : cargar("RGP"))
listBox.tag_bind('el', sequence= '<Button-1>',callback = lambda x: print('lol'))

listBox.column(cols[0], width = 30, anchor = 'c')
listBox.column(cols[1], width = 120, anchor = 'c')
listBox.column(cols[2], width = 40, anchor = 'c')
listBox.column(cols[3], width = 90, anchor = 'c')
for i in range(3, len(cols)):
    listBox.column(cols[i], width = 70, anchor = 'c')
listBox.grid(row=1, column=0, columnspan=2)


    
Btn_agregar = Button(c_Main, text="agregar piloto", width=50, command=lambda: cargar("REP")).grid(row = 2, column = 0 )
cargar("RGP")
