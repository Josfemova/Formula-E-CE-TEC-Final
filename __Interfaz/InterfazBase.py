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

def btn_back(Window):
    Window.destroy()
    Main.deiconify()

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
        
    BtnBack1 =  Button(AboutCanv, text= "Main",command =lambda: btn_back(About),fg = "cyan", bg= "black")
    BtnBack1.place(x = 600, y = 500)
    About.mainloop()

#-----Se termina la venta about y se define la ventana de pruebas
def test_drive_window():
    #Variables globales para el funcionamiento de la ventana
    global Pot, NotMoving,Pressed,DirR,DirL, BlinkC, BlinkZ, PressW, PressS, PressF, Front, lbr
    Pot = 0
    NotMoving = True
    Pressed = False
    DirR = False
    DirL = False
    BlinkC = False
    BlinkZ = False
    PressW = False
    PressS = False
    PressF = False
    Front = True
    lbr = True
    TestDrive= Toplevel()
    TestDrive.title("Test Drive")
    TestDrive.geometry("1280x720")
    TestDrive.resizable(width= NO, height= NO)
    #Se genera el canvas de la ventana de pruebas
    TestCanv= Canvas(TestDrive, width= 1280, height= 720,bg="black")
    TestCanv.place(x=0, y=0)
    FondoTest = cargar_imagen("POV.png")
    TestCanv.create_image(0,0,image=FondoTest, anchor = NW,state = NORMAL)
    Borde = cargar_imagen("Car1.png")
    TestCanv.create_image(925,200, image = Borde, anchor = NW,tags = ("fondo","día"))
    Escudería = TestCanv.create_text(60,300, text = "Escudería",font = ("Consolas",15),fill = "White")
    NombreCarro = TestCanv.create_text(600,15, text = "NombreCarro", font = ("Consolas",15),fill = "White")
    Potencia = TestCanv.create_text(603,657, text = "PWM:0%", font= ("Consolas",18), fill = "White", tags = "pwm")
    #Se debe programar la adición de las operaciones de la función aparte de generar la ventana

    #Se utiliza el comando del botón atrás para volver a main
    #Para ello se define una función al igual que en la ventana About
    myCar = NodeMCU()
    myCar.start()
      
    BtnBack2= Button(TestCanv, text = "Main", command = lambda: btn_back(TestDrive), fg= "cyan", bg= "black")
    BtnBack2.place(x= 1100, y =600)

    #Código para trabajar los casos con las teclas de movimiento
    #Se define un evento de mapeo de teclas para la ventana:
    
    #Función send para enviar los comandos al NodeMCU
    #Esta función es una modificación a la dada en el archivo TelemetryLog por Santiago Gamboa
    def send(Msg):
        """
        Función send para enviar comandos al Node
        Esta funcion es una modificación a la dada en el archivo TelemetryLog por Santiago Gamboa (Asistente del Curso)
        """
        if(len(Msg)>0 and Msg[-1] == ";"):
            myCar.send(Msg)
        else:
            return
    send("lb:1;")    
    def WASD_Press(event):
        global Pressed, Pot, NotMoving, DirR, DirL, BlinkZ, BlinkC, PressS, PressW, PressF, Front
        Key = event.char #Estoy asigna la presión de una tecla a la variable Key.
        Pressed = True
        if Key == "w": #Se debe manejar con strings pues es el argumento que maneja "char".
            #Hacer una aceleración gradual, para esto se utiliza una función aparte.
            if Pressed and not(PressW):
                ThreadAccel = Thread(target = gradual_accel)
                ThreadAccel.start()
            else:
                return
        elif Key == "s":
            if Pressed and not(NotMoving) and not(PressS):
                ThreadDecel = Thread(target = gradual_decel)
                ThreadDecel.start()
            elif Pressed and NotMoving and not(PressS):
                ThreadBack = Thread(target = gradual_reverse)
                ThreadBack.start()
            else:
                return
        elif Key == "a":
            DirL = True
            if DirR:
                return
            else:
                if Pressed:
                    send("dir:-1;")
            #Se tiene que meter lo de cambiar las imágenes
                else:
                    return
        elif Key == "d":
            DirR = True
            if DirL:
                return
            else:
                if Pressed:
                    send("dir:1;")
                else:
                    return
        elif Key == "z":
            if Pressed and not(BlinkZ):
                BlinkZ = True
                BlinkC = False
                thread_blink(-1)
            else:
                return
                
        elif Key == "c":
            if Pressed and not(BlinkC):
                BlinkC = True
                BlinkZ = False
                thread_blink(1)
            else:
                return
        elif Key == "x":
            if Pressed and (BlinkC or BlinkZ):
                BlinkC = False
                BlinkZ = False
            else:
                return
        elif Key == "f": #Front para luces, PressF para la tecla
            if PressF:
                return
            else:
                PressF = True
                if Front:
                    send("lf:1;")
                    Front = False
                    print("on")
                else:
                    send("lf:0;")
                    Front = True
                    print("off")
        else:
            return #Se llega a esta línea cuando hay algún evento de caracteres en el teclado, pero es insignificante para el comportamiento del carro (ejemplo, la H)
    #-------------------------------------------
    def thread_blink(Dir):
        global BlinkZ, BlinkC
        if BlinkZ:
            BlinkC = False
            ThreadBlink = Thread(target =blink_lights, args = [Dir, 1])
            ThreadBlink.start()
        elif BlinkC:
            BlinkZ = False
            ThreadBlink = Thread(target =blink_lights, args = [Dir,1])
            ThreadBlink.start()
        else:
            return
    def blink_lights(Direction,Timer):
        LedStatus = Timer%2
        if Direction == -1:
            while Timer < 101 and BlinkZ:
                send("ll:" + str(LedStatus) + ";")
                Timer += 1
                time.sleep(0.5)
                print("Left")
            send("ll:" + str(LedStatus) + ";")
        elif Direction == 1:
            while Timer < 101 and BlinkC:
                send("lr:" + str(LedStatus) + ";")
                Timer += 1
                time.sleep(0.5)
                print("Right")
            send("lr:" + str(LedStatus) + ";")
        else:
            return
    def gradual_accel():
        """
    Función gradual_accel que es invocada por el Thread con el objetivo de generar una aceleración gradual
    """
        global Pot, NotMoving, Pressed, PressW,lbr
        NotMoving = False
        PressW = True
        if lbr:
            lbr = False
            send("lb:0;")
            
        while Pot <= 900 and Pressed:
            Pot += 100
            send("pwm:" + str(Pot) +";")
            time.sleep(0.5)
            TestCanv.itemconfig(Potencia, text = ("PWM:" + str(Pot//10) +"%"))
        send("pwm:" + str(Pot) + ";")
        TestCanv.itemconfig(Potencia, text = ("PWM:" + str(round(Pot//10)) + "%"))
    #---------------------------------------

        
    def gradual_decel():
        global Pot, NotMoving,PressS
        NotMoving = False
        PressS = True
        while Pot > 0 and Pressed:
            Pot -= 100
            send("pwm:" + str(Pot) + ";")
            TestCanv.itemconfig(Potencia, text = ("PWM:" + str(round(Pot//10)) + "%"))
            time.sleep(0.5)
        Pot = 0
        send("pwm:" + str(Pot) + ";") #para dejar el carro en 0 una vez que se alcanza ese valor y luego empezar a dar reversa.
        TestCanv.itemconfig(Potencia, text = ("PWM:" + str(round(Pot//10)) + "%"))
        NotMoving = True
        PressS = False
    #-----------------------------------------
    def gradual_reverse():
        global Pot, NotMoving, Pressed, PressS
        NotMoving = False
        PressS = True
        while -900<Pot<=0 and Pressed:
            Pot -= 100
            send("pwm:" + str(Pot) + ";")
            TestCanv.itemconfig(Potencia, text = ("PWM:" + str(round(Pot//10)) + "%"))
            time.sleep(0.5)
        send("pwm:" + str(Pot) + ";")
        TestCanv.itemconfig(Potencia, text = ("PWM:" + str(round(Pot//10)) + "%"))
        
        
    def WASD_Release(event):
        global Pot, pwmBack, DirL, DirR, Pressed, NotMoving, PressW, PressS, PressF
        Key = event.char
        Pressed = False
        if (Key == "w") or (Key == "s"):
            PressW = False
            PressS = False
            if NotMoving:
                return
            else:
                ThreadStop = Thread(target = gradual_pullover)
                ThreadStop.start()
        elif (Key == "a") or (Key == "d"):
            DirL = False
            DirR = False
            #Código para detener el parpadeo
            send("dir:0;")
        elif Key == "f":
            PressF = False
    #------------------------------------------------

        
    def gradual_pullover():
        """
        Función para detener el auto cuando se sueltan las teclas de movimientos acc/reversa
        """
        global Pot, NotMoving, Pressed, lbr
        if not lbr:
            lbr = True
            send("lb:1;")
            
        if Pot > 0:
            while Pot > 0 and not(Pressed):
                Pot -= 100
                send("pwm:" + str(Pot) + ";")
                TestCanv.itemconfig(Potencia, text = ("PWM:" + str(round(Pot//10)) + "%"))
                time.sleep(0.5)
            Pot = 0
            send("pwm:" + str(Pot) + ";")
            TestCanv.itemconfig(Potencia, text = ("PWM:" + str(round(Pot//10)) + "%"))
            NotMoving = True
            
        else:
            while Pot < 0 and not(Pressed):
                Pot += 100
                send("pwm:" + str(Pot) + ";")
                TestCanv.itemconfig(Potencia, text = ("PWM:" + str(round(Pot//10)) + "%"))
                time.sleep(0.25)
            Pot = 0
            send("pwm:" + str(Pot) + ";")
            TestCanv.itemconfig(Potencia, text = ("PWM:" + str(round(Pot//10)) + "%"))
            NotMoving = True
    #----------------------------------------------------------

            
    TestDrive.bind("<KeyPress>", WASD_Press) #Se le asigna el bind a la función WASD_Press().
    TestDrive.bind("<KeyRelease>",WASD_Release) #Este bind funciona de la misma forma pero opera opuesto al press.
    
    
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
        
    BtnBack3= Button(PilotsCanv, text ="Main",command = lambda: btn_back(Pilots), fg= "cyan", bg = "black")
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
