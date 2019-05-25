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
AboutText ="""
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
Hints: Verifique que el auto encendió
correctamente.
Verifique que tanto el equipo de telemetría
como el auto estén
conectados a la misma red inalámbrica.
Utilice las teclas WASD para mover el auto.
seleccione un piloto e inicie su Test Drive.
"""
#    __________________________
#___/Importación de Bibliotecas
from tkinter import * #Para el uso de labels, canvas, Photo, etc
from tkinter import scrolledtext #para utilizar en la ventana about
from tkinter import messagebox #Pop-up de mensajes
from WiFiClient import NodeMCU #Comunicación WIFI con el carro.
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
Main.geometry('800x600')
Main.resizable(width=NO,height=NO)

#    _______________________________
#___/Canvas para trabajar la ventana
MainCanv = Canvas(Main,width=1370,height=768,bg="grey")
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
    About.minsize(800,600)
    About.resizable(width= NO, height= NO)
    AboutCanv = Canvas(About, width= 800, height= 600,bg="grey")
    AboutCanv.place(x=0,y=0)
    Info = scrolledtext.ScrolledText(About,width= 40, height= 10,bg= "black", fg= "cyan") #no es una medida en pixeles
    Info.insert(INSERT,AboutText) #Se añade el texto del comentario multilínea perteneciente a la variable, dentro del scrolledtext.
    Info.place(x = 400, y = 10)
    FotoAle = cargar_imagen("AlejandroPrueba.png")
    AboutCanv.create_image(1,1,image=FotoAle,anchor = NW)
    #Se define una función para el botón de atrás a la principal
    def btn_back1():
        About.destroy()
        Main.deiconify() #Recargar la ventana principal
        
    BtnBack1 = Button(AboutCanv, text= "Main", command = btn_back1,fg = "cyan", bg= "black")
    BtnBack1.place(x = 600, y = 500)
    About.mainloop()

#-----Se termina la venta about y se define la ventana de pruebas
def test_drive_window():
    TestDrive= Toplevel()
    TestDrive.title("Test Drive")
    TestDrive.geometry("1280x720")
    TestDrive.resizable(width= NO, height= NO)
    #Se genera el canvas de la ventana de pruebas
    TestCanv= Canvas(TestDrive, width= 1280, height= 720,bg="black")
    TestCanv.place(x=0, y=0)
    FondoTest = cargar_imagen("POV.png")
    TestCanv.create_image(0,0,image=FondoTest, anchor = NW,state = NORMAL)
    Borde = cargar_imagen("Outline1.png")
    TestCanv.create_image(800,300, image = Borde, anchor = NW,state = NORMAL)
    #Se debe programar la adición de las operaciones de la función aparte de generar la ventana

    #Se utiliza el comando del botón atrás para volver a main
    #Para ello se define una función al igual que en la ventana About
    #myCar = NodeMCU()
    #myCar.start()
    def btn_back2():
        TestDrive.destroy()
        Main.deiconify()
        
    BtnBack2= Button(TestCanv, text = "Main", command = btn_back2, fg= "cyan", bg= "black")
    BtnBack2.place(x= 1100, y =600)
    TestDrive.mainloop()

#-----Se termina la ventana de pruebas y se define la de los pilotos
def pilots_window():
    Pilots = Toplevel()
    Pilots.title("Pilots")
    Pilots.minsize(width= 800, height= 600)
    Pilots.resizable(width= NO, height= NO)
    #Se genera el canvas
    PilotsCanv= Canvas(Pilots, width = 800, height = 600,bg="grey")
    PilotsCanv.place(x=0,y=0)
    #Se debe programar el resto del funcionamiento del módulo antes de declararlo como listo

    #Por ahora se tiene el botón de atras:
    def btn_back3():
        Pilots.destroy()
        Main.deiconify()
        
    BtnBack3= Button(PilotsCanv, text ="Main", command = btn_back3, fg= "cyan", bg = "black")
    BtnBack3.place(x= 200, y =100)
    Pilots.mainloop()

#------Comandos de los Botones en Main------
BtnAbout= Button(MainCanv, text= "About", command = btn_about,fg= "cyan",bg ="black") #Para ir a About
BtnAbout.place(x = 100,y = 100)

BtnTest= Button(MainCanv, text= "Test Drive", command = btn_test,fg= "cyan",bg ="black")  #Para ir a TestDrive
BtnTest.place(x = 200, y = 100)

BtnPilots = Button(MainCanv, text= "Pilots", command = btn_pilots,fg= "cyan",bg ="black") #Para ir a Pilots
BtnPilots.place(x = 300, y = 100)
    
Main.mainloop()
