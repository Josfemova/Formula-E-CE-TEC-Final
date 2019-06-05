"""
Ventana de información de los integrantes
"""
#   __________________________
#__/Importación de Bibliotecas
from tkinter import * #labels, canvas, PhotoImage, etc
#from tkinter import scrolledtext #Para textos espaciosos
from tkinter.scrolledtext import ScrolledText as ST
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

def closeX(widgetObj,parent=''):
    widgetObj.destroy()
    if parent !='':
        parent.deiconify()

Abt = Button(C_Main, text = "about", command = btn_about, font = ("Helvetica", 18), bg = "white")
Abt.place(x = 400, y = 400)
#Ventana About

#   ________
#__/About
def about_window(parent = Main):
    AboutText = \
    """
Instituto Tecnológico de Costa Rica

Escuela de Ingeniería en Computadores

Curso: Taller de Programación, CE-1102
Grupo 2

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
"""
    HelpText = \
"""
Hints:

Al abandonar esta ventana puede modificar los
patrocinadores o el logo de la escudería

Para proceder con el Test Drive, debe abandonar
esta ventana, presionar el botón de Pilotos
y seleccionar alguno de los pilotos disponibles,
o bien crear un nuevo piloto.


Verifique que tanto el computador como el auto
estén conectados a la misma red WiFi.


Dentro del Test Drive, para controlar el auto
utilice WASD para el movimiento, Z para la
dirección izquierda, C para la derecha, y
X para apagar las direccionales.


Las luces frontales se encienden con F, las traseras son automáticas.
"""
    About = Toplevel()
    About.title("About")
    About.geometry("1280x720")
    About.resizable(width = NO, height = NO)


    C_About = Canvas(About, width = 1280, height = 720, bg = "#FAFAFA") #Cercano al RGB(255) en los 3 aspectos
    C_About.pack(anchor = NW, fill = Y)
    C_About.FondoAbout = FondoAbout = cargar_imagen("FondoAbout.png")
    C_About.create_image(0,0,image = FondoAbout, anchor = NW)
    C_About.Alejandro = FotoAlejandro = cargar_imagen("Alejandro.png")
    C_About.create_image(825,25, image = FotoAlejandro, anchor = NW)
    C_About.Morales = FotoMorales = cargar_imagen("Morales.png")
    C_About.create_image(1105, 25, image = FotoMorales, anchor = NW)
    C_About.Creditos = AboutText
    C_About.create_text(10,10,anchor = NW, text = AboutText, font = ("Helvetica", 10, "bold italic"),
                        fill = "#FAFAFA", justify = CENTER)
    
    C_About.Hints = Hints = ST(C_About, width = 45, height = 10, bg = "Black", font = ("Helvetica", 10, "bold italic"), fg = "white")
    C_About.Hints.insert(INSERT,HelpText)
    C_About.Hints.place(x = 20, y= 540)


    
    Btn_CerrarAb= Button(C_About, command =lambda: closeX(About, Main),  text = "Volver", bg = "black", fg = "#FAFAFA", font = ("Helvetica", 14, "bold italic"))
    Btn_CerrarAb.place(x = 640,y = 690, anchor = CENTER)


Main.mainloop()
    
    
    
    
