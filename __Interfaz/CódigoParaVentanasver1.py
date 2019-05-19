#Encabezado del Proyecto
"""
______________________________________
Instituto Tecnológico de Costa Rica

Escuela de Ingeniería en Computadores

Curso: Taller de Programación, CE-1102

Project III, Part II
Formula E CE-TEC
Energy Saving and Telemetry Part II

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
#    __________________________
#___/Importación de Bibliotecas
from tkinter import * #Para el uso de labels, canvas, messagebox, etc
import os             #Para manejo de rutas
import threading      #Asignación de hilos
from threading import Thread
import time           #time.sleep() para delays
import random         #En caso que sea necesario generar algún dato en aleatorio
#global

#    ____________________________
#___/Función para cargar imágenes
def cargar_imagen(Nombre):
    ruta = os.path.join("imagenes",Nombre)
    Imagen = PhotoImage(file = ruta)
    return Imagen

#    _____________________________
#___/Creación de Ventana Principal
Main = Tk() #Se asigna una función de Tkinter al nombre Main
Main.title("Home")
Main.minsize(1370,768)
Main.resizable(width=NO,height=NO)

#    _______________________________
#___/Canvas para trabajar la ventana
MainCanv = Canvas(Main,width=1370,height=768,bg="white")
MainCanv.place(x=0,y=0)

#Insertar código que cargue la imagen del fondo en el canvas

def btn_about():
    Main.withdraw()
    about_window()

def btn_test():
    Main.withdraw()
    test_drive_window()

def btn_pilots():
    Main.withdraw()
    pilots_window()


#    _____________
#___/ventana about
def about_window():
    About = Toplevel()
    About.title("About")
    About.minsize(1370,768)
    About.resizable(width= NO, height= NO)
    AboutCanv = Canvas(About, width= 1370, height= 768,bg="white")
    AboutCanv.place(x=0,y=0)
    #Se debe programar la adición de la imagen de los autores y la información del proyecto

    #Se define una función para el botón de atrás a la principal
    def btn_back1():
        About.destroy()
        Main.deiconify() #Recargar la ventana principal
        
    BtnBack1 = Button(AboutCanv, text= "Main", command = btn_back1,fg = "white", bg= "black")
    BtnBack1.place(x = 100, y = 200)

#-----Se termina la venta about y se define la ventana de pruebas
def test_drive_window():
    TestDrive= Toplevel()
    TestDrive.title("Test Drive")
    TestDrive.minsize(width= 1370, height = 768)
    TestDrive.resizable(width= NO, height= NO)
    #Se genera el canvas de la ventana de pruebas
    TestCanv= Canvas(TestDrive, width= 1370, height= 768,bg="white")
    TestCanv.place(x=0, y=0)
    #Se debe programar la adición de las operaciones de la función aparte de generar la ventana

    #Se utiliza el comando del botón atrás para volver a main
    #Para ello se define una función al igual que en la ventana About
    def btn_back2():
        TestDrive.destroy()
        Main.deiconify()
        
    BtnBack2= Button(TestCanv, text = "Main", command = btn_back2, fg= "White", bg= "black")
    BtnBack2.place(x= 200, y =100)

#-----Se termina la ventana de pruebas y se define la de los pilotos
def pilots_window():
    Pilots = Toplevel()
    Pilots.title("Pilots")
    Pilots.minsize(width= 1370, height= 768)
    Pilots.resizable(width= NO, height= NO)
    #Se genera el canvas
    PilotsCanv= Canvas(Pilots, width = 1370, height = 768,bg="white")
    PilotsCanv.place(x=0,y=0)
    #Se debe programar el resto del funcionamiento del módulo antes de declararlo como listo

    #Por ahora se tiene el botón de atras:
    def btn_back3():
        Pilots.destroy()
        Main.deiconify()
        
    BtnBack3= Button(PilotsCanv, text ="Main", command = btn_back3, fg= "white", bg = "black")
    BtnBack3.place(x= 200, y =100)

#------Comandos de los Botones en Main------
BtnAbout= Button(MainCanv, text= "About", command = btn_about,fg= "white",bg ="black") #Para ir a About
BtnAbout.place(x = 100,y = 100)

BtnTest= Button(MainCanv, text= "Test Drive", command = btn_test,fg= "white",bg ="black")  #Para ir a TestDrive
BtnTest.place(x = 200, y = 100)

BtnPilots = Button(MainCanv, text= "Pilots", command = btn_pilots,fg= "white",bg ="black") #Para ir a Pilots
BtnPilots.place(x = 300, y = 100)
    
Main.mainloop()
