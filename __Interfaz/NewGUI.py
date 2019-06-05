"""
Ventana de información de los integrantes
"""
#   __________________________
#__/Importación de Bibliotecas
from tkinter import * #labels, canvas, PhotoImage, etc
from tkinter import scrolledtext #Para textos espaciosos
import os  #manejo de rutas
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
#Documentar o eliminar esta función luego de añadir la ventana About al resto del programa.
def cargar_imagen(Nombre):
    ruta = os.path.join("__Interfaz\\imagenes",Nombre)
    Imagen = PhotoImage(file = ruta)
    return Imagen
#   ___________
#__/Ventana Principal
Main = Tk() #Se asigna una función de Tkinter al nombre Main
Main.title("Discardable")
Main.geometry("800x800")
Main.resizable(width=NO, height= NO)

#   __________
#__/Canvas de Main
C_Main = Canvas(Main, width = 800, height = 800, bg = "black")
C_Main.place(x=0,y=0)

def btn_about():
    Main.withdraw()
    about_window()

Abt = Button(C_Main, text = "about", command = btn_about, font = ("Helvetica", 18), bg = "black")
Abt.place(x = 400, y = 400)
#Ventana About

#   ________
#__/About
def about_window(parent = Main):
    About = Toplevel()
    About.title("About")
    About.geometry("1024x576")
    About.resizable(width = NO, height = NO)



    C_About = Canvas(About, width = 1024, height = 576, bg = "FAFAFA") #Cercano al RGB(255) en los 3 aspectos
    C_About.pack(expand = 1, anchor = NW, fill = Y)
    C_About.FondoAbout = FondoAbout = cargar_imagen("FondoInfo.png")
    C_About.create_image(0,0,image = FondoAbout, anchor = NW)
    
    
    
