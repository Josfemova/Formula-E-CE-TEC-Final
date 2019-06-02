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
from tkinter import ttk
from WiFiClient import NodeMCU #Comunicación WIFI con el carro.
import os             #Para manejo de rutas
from random import randint
from autos import main_Autos
from pilotos import main_Pilotos
from threading import Thread
from time import sleep


#    ____________________________
#___/Obejtos globales
pilotos = main_Pilotos()
autos = main_Autos() 



def cargar_imagen(Nombre):
    ruta = os.path.join("__Interfaz\\imagenes",Nombre)
    Imagen = PhotoImage(file = ruta)
    return Imagen

#    _____________________________
#___/Creación de Ventana Principal
Main = Tk() #Se asigna una función de Tkinter al nombre Main
Main.title("Home")
Main.geometry('1280x720')
Main.resizable(width=NO,height=NO)

#    _______________________________
#___/Canvas para trabajar la ventana
MainCanv = Canvas(Main,width=1280,height=720,bg="grey")
MainCanv.place(x=0,y=0)

MainBG = cargar_imagen("MainFondo.png")
MainCanv.create_image(0,0,image= MainBG, anchor = NW)

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

#-----Se termina la venta about y se define la ventana de pruebas
def test_drive_window(pilotoIndex = 0):
    #Valor inicial de las variables globales para esta ventana
    celebracion = pilotos.getCelebracion(pilotoIndex)
    carro = int(pilotos.info[pilotoIndex][pilotos.iTEMPO])
    for i in range(0,len(autos.info)):
        if (autos.info[i][autos.iTEMPO] == carro):
            carro = i
            i=len(autos.info)
            print(carro)
            
    
    Speed = 0
    Moving,WPressed,APressed,SPressed,DPressed,ZPressed,XPressed,CPressed,FPressed,BlinkZ,BlinkC,SentBackON,SentBackOFF = (False,)*13
    FLight = True
    Blight = True
    BlightCount = 0
    
    #Valor inicial del auto al entrar a la ventana
    #send("lb:1;")

    #*****************
    TestDrive= Toplevel()
    TestDrive.title("Test Drive")
    TestDrive.geometry("1280x720")
    TestDrive.resizable(width= NO, height= NO)
    #Se genera el canvas de la ventana de pruebas
    TestCanv= Canvas(TestDrive, width= 1280, height= 720,bg="black")
    TestCanv.place(x=0, y=0)

    TestDrive.FondoDia = FondoDia = cargar_imagen("DAY.png")
    TestCanv.create_image(0,0,image=FondoDia, anchor = NW,tags = "dia", state = NORMAL)
    TestDrive.FondoNoche =FondoNoche = cargar_imagen("NIGHT.png")
    TestCanv.create_image(0,0,image= FondoNoche, anchor = NW, tags = "noche", state = HIDDEN)

    TestDrive.Twl = TopWheelL = cargar_imagen("TLWheel.png")
    TestCanv.create_image(960,240, image = TopWheelL, anchor = NW, tags = "tl", state = HIDDEN)
    TestCanv.create_image(1032,242, image = TopWheelL, anchor = NW, tags = "tl", state = HIDDEN)

    TestDrive.Twr = TopWheelR = cargar_imagen("TopWheelRight.png")
    TestCanv.create_image(963,240, image = TopWheelR, anchor = NW, tags = "tr", state = HIDDEN)
    TestCanv.create_image(1040,238, image = TopWheelR, anchor = NW, tags = "tr", state = HIDDEN)


    TestDrive.Borde = Borde = cargar_imagen("Car1.png")
    TestCanv.create_image(925,200, image = Borde, anchor = NW,tags = ("fondo","día"))

    TestCanv.create_text(60,300, text = "Escudería",font = ("Consolas",15),fill = "White",tags= "escu")
    TestCanv.create_text(600,15, text = (autos.info[carro][0] +autos.info[carro][1]) , font = ("Consolas",15),fill = "White",tags = "name")
    TestCanv.create_text(640,360, text = "PWM:0%", font= ("Consolas",18), fill = "White", tags = "pwm", anchor= CENTER)
    TestCanv.create_text(1100,500, text = "Charge: %", font = ("Consolas", 18), fill = "white", tags = "battext", anchor = NW)

    TestDrive.fl = FrontLight = cargar_imagen("FrontL.png")
    TestCanv.create_image(965,210, image = FrontLight, anchor = NW, tags = ("lights","front"), state = HIDDEN)
    TestCanv.create_image(1030,210, image = FrontLight, anchor = NW, tags = ("lights","front"), state = HIDDEN)

    TestDrive.dirl = DirLight = cargar_imagen("EmL.png")
    TestCanv.create_image(940,250, image = DirLight, anchor = NW, tags = ("lights","left"), state = HIDDEN)
    TestCanv.create_image(1030,250, image = DirLight, anchor = NW, tags = ("lights","right"), state = HIDDEN)

    TestDrive.bl = BackLight= cargar_imagen("BackL.png")
    TestCanv.create_image(955,385, image = BackLight, anchor = NW, tags = ("lights", "back"), state = HIDDEN)
    TestCanv.create_image(1005,385, image = BackLight, anchor = NW, tags = ("lights", "back"), state = HIDDEN)

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
    #--------------------
    def check_sense():
        while True:
            Command = myCar.send("sense;")
            sleep(9);
        
    ThreadSense = Thread(target = check_sense)
    ThreadSense.start()

    def get_log():
        """
        Hilo que actualiza los Text cada vez que se agrega un nuevo mensaje al log de myCar
        """
        indice = 0
        while(myCar.loop):
            while(indice < len(myCar.log)):
                mnsSend = "[{0}] cmd: {1}\n".format(indice,myCar.log[indice][0])

                mnsRecv = "{1}\n".format(indice,myCar.log[indice][1])
                Answer = mnsRecv #Se almacena la variable de retorno en el comando.
                #print(Answer)
                #print(len(Answer))
                if len(Answer) >= 15:
                    LDR = Thread(target = dia_noche, args = [Answer])
                    LDR.start()
                    Bat = Thread(target = bateria, args = [Answer])
                    Bat.start()
                indice+=1
            sleep(0.200)

    def dia_noche(Answer):
        #Validar la posición del caracter en el que la LDR manda la variable light
        if Answer[-4] == "0":
            TestCanv.itemconfig("dia", state = HIDDEN)
            TestCanv.itemconfig("noche", state = NORMAL)
        elif Answer[-4] == "1":
            TestCanv.itemconfig("dia", state = NORMAL)
            TestCanv.itemconfig("noche", state = HIDDEN)
        else:
            return

    def bateria(Answer):
        #print("entered")
        #nonlocal Battery
        if len(Answer) == 15:
            Battery = Answer[5]
            TestCanv.itemconfig("battext", text ="Charge: "+ (Battery) + "%")
        elif len(Answer) == 16:
            Battery = Answer[5:7]
            TestCanv.itemconfig("battext", text ="Charge: "+ (Battery) + "%")
        elif len(Answer) == 17:
            Battery = Answer[5:8]
            TestCanv.itemconfig("battext", text ="Charge: "+ (Battery) + "%")
        else:
            return


    p = Thread(target=get_log)
    p.start()
    #------------------
    def WASD_Press(event):
        """
        Función que controla los eventos que se activarán al presionar teclas definidas
        """
        nonlocal WPressed, APressed, SPressed, DPressed, ZPressed, XPressed, CPressed, FPressed, FLight, Blight, BlinkZ, BlinkC
        Key = event.char
        if Key == "w":
            if not WPressed and not SPressed:
                WPressed = True
                ThreadForwards = Thread(target = gradual_front)
                sleep(0.2)
                ThreadForwards.start()
                #Hilo que controla la aceleración delantera del carro.
            else:
                return #do nothing
        elif Key == "s":
            if not SPressed and not WPressed:
                SPressed = True
                ThreadBackwards = Thread(target = gradual_back)
                ThreadBackwards.start()
                sleep(0.3)
                ThreadBacklightsP = Thread(target = back_light_control_press)
                ThreadBacklightsP.start()
            else:
                return
        elif Key == "a":
            if not APressed and not DPressed:
                send("dir:-1;")
                APressed = True
                #print("sent to turn L")
                #código para activar o desactivar las imágenes que dan feedback de giro en la interfaz de usuario.
                TestCanv.itemconfig("tl", state = NORMAL)
            else:
                return
        elif Key == "d":
            if not DPressed and not APressed:
                send("dir:1;")
                DPressed = True
                #print("sent to turn R")
                TestCanv.itemconfig("tr", state = NORMAL)
            else:
                return
        elif Key == "z":
            if not ZPressed and not CPressed:
                ZPressed = True
                if BlinkZ:
                    return
                else:
                    thread_blink("L")
            else:
                return
        elif Key == "x":
            if not XPressed and not(ZPressed or CPressed):
                XPressed = True
                BlinkZ = False
                BlinkC = False
                TestCanv.itemconfig("left", state = HIDDEN)
                TestCanv.itemconfig("right", state = HIDDEN)
                #print("stopped blinking")
            else:
                return
        elif Key == "c":
            if not CPressed and not ZPressed:
                CPressed = True
                if BlinkC:
                    return
                else:
                    thread_blink("R")
            else:
                return
        elif Key == "f":
            if not FPressed:
                FPressed = True
                if FLight:
                    send("lf:1;")
                    FLight = False
                    #print("sent to turn front on")
                    TestCanv.itemconfig("front",state = NORMAL)
                else:
                    send("lf:0;")
                    FLight = True
                    #print("sent to turn front off")
                    TestCanv.itemconfig("front",state = HIDDEN)
            else:
                return
        elif Key =="j":
            
            return
        elif key == "k":
            return
        else:
            return #cuando suceda un evento pero no coincida con las teclas determinadas en este módulo
        #--------------------------------------
    #Definición de las funciones objetivo de los hilos llamados en el módulo anterior.
    def gradual_front():
        """
        Función que es invocada por el hilo de aceleración para generar un avance gradual
        """
        nonlocal Speed, Moving, WPressed, SPressed, SentBackOFF,SentBackON
        WPressed = True
        Moving = True
        while Speed < 400 and WPressed and not SPressed:
            if Speed <= -500:
            #En este caso se trabaja con un aumento de velocidad, en un caso esp. en que esta es menor que -500
                send("pwm:" + str(Speed) + ";")
                #print("speed was lower than or at -500 so it was sent before incrementing")
                Speed += 100
                TestCanv.itemconfig("pwm", text = "PWM:" + str(Speed//10) +"%")
                #print("incremented speed to " + str(Speed))
                sleep(1)
            else:
            #en este último caso, la velocidad va a ser mayor que 0, por lo cual se trata normalmente.
                if Speed >= -100:
                    if not SentBackOFF:
                        send("lb:0;")
                        #print("SentBackOFF")
                        SentBackOFF = True
                        SentBackON = False
                        TestCanv.itemconfig("back", state = HIDDEN)
                Speed += 100
                TestCanv.itemconfig("pwm", text = "PWM:" + str(Speed//10) +"%")
                #print("incremented speed to " + str(Speed))
                sleep(1)
                
        TestCanv.itemconfig("pwm", text = "PWM:" + str(Speed//10) + "%")
        #print("incremented speed to " + str(Speed) + " and exited first while")
        sleep(1)
        #la función entra a este while cuando salga del primero, que es mayor a 500.
        while 900>= Speed >= 400 and WPressed and not SPressed:
            Speed += 100
            send("pwm:" + str(Speed) + ";")
            TestCanv.itemconfig("pwm", text = "PWM:" + str(Speed//10) +"%")
            #print("sent to move forward by " + str(Speed))
            sleep(1)
        #send("pwm:" + str(Speed) + ";")
        #print("sent to move forward by " + str(Speed) + " and exited second while")
        TestCanv.itemconfig("pwm", text = "PWM:" + str(Speed//10) +"%")
        sleep(1)
        #---------------------------------------------
    def gradual_back():
        """
        Función que es invocada por el hilo de desaceleración/reversa para generar un movimiento gradual hacia atrás.
        """
        nonlocal Speed,Moving, SPressed, WPressed
        SPressed = True
        while Speed > -400 and SPressed and not WPressed:
            if Speed >= 500:
                send("pwm:" + str(Speed) + ";")
                #print("Speed was higher than or at 500, so it was sent before decrementing")
                Speed -= 100
                TestCanv.itemconfig("pwm", text = "PWM:" + str(Speed//10) +"%")
                #print("decremented speed to " + str(Speed))
                sleep(1)
            else:
                Speed -= 100
                TestCanv.itemconfig("pwm", text = "PWM:" + str(Speed//10) +"%")
                #print("decremented speed to " + str(Speed))
                sleep(1)
        TestCanv.itemconfig("pwm", text = "PWM:" + str(Speed//10) +"%")
        #print("decremented speed to " + str(Speed) + " and exited first while")
        sleep(1)
        #la función entra a este while cuando salga del primero, que es menor a 500.
        while -900<=Speed<=-400 and SPressed and not WPressed:
            Speed -= 100
            send("pwm:" + str(Speed) + ";")
            TestCanv.itemconfig("pwm", text = "PWM:" + str(Speed//10) +"%")
            #print("sent to move backwards by " + str(Speed))
            sleep(1)
        #send("pwm:" + str(Speed) + ";")
        TestCanv.itemconfig("pwm", text = "PWM:" + str(Speed//10) +"%")
        #print("sent to move backwards by " + str(Speed) + " and exited second while")
        #-------------------------------------------
    def thread_blink(Direction):
        """
        Función que recibe la dirección a la que se desea activar el hilo de parpadeo para las direccionales.
        """
        nonlocal ZPressed, CPressed, BlinkZ, BlinkC
        if ZPressed and not (CPressed or XPressed):
            BlinkZ = True
            ThreadBlink = Thread(target = blink_lights, args = [Direction, 0])
            ThreadBlink.start()
        elif CPressed and not (ZPressed or XPressed):
            BlinkC = True
            ThreadBlink = Thread(target = blink_lights, args = [Direction, 0])
            ThreadBlink.start()
        else:
            return
    #--------------------
    def blink_lights(Direction, Counter):
        nonlocal ZPressed, CPressed, XPressed, BlinkC, BlinkZ
        if Direction == "L":
            while BlinkZ:
                LED = Counter%2
                send("ll:" + str(LED) + ";")
                if LED == 1:
                    TestCanv.itemconfig("left", state = NORMAL)
                    #print("Left light is ON")
                    Counter += 1
                else:
                    TestCanv.itemconfig("left", state = HIDDEN)
                    #print("Left light is OFF")
                    Counter += 1
                sleep(1)
            send("ll:0;")
            TestCanv.itemconfig("left", state = HIDDEN)
            #print("Left light is OFF and exited while")
        elif Direction == "R":
            while BlinkC:
                LED = Counter%2
                send("lr:" + str(LED) + ";")
                if LED == 1:
                    TestCanv.itemconfig("right", state = NORMAL)
                    #print("Right light is ON")
                    Counter += 1
                else:
                    TestCanv.itemconfig("right", state = HIDDEN)
                    #print("Right light is OFF")
                    Counter += 1
                sleep(1)
            send("lr:0;")
            TestCanv.itemconfig("right", state = HIDDEN)
            #print("Right light is OFF and exited while")
        else:
            return
        #---------------------------------

    def back_light_control_press():
        nonlocal Speed, SentBackON, SentBackOFF, SPressed
        while SPressed:
            if SentBackON:
                return
            else:
                send("lb:1;")
                #print("SentBackON")
                TestCanv.itemconfig("back",state = NORMAL)
                SentBackON = True
                SentBackOFF = False
        #print("S released, exit press while")
    #-----------------------------------------                
    #Función WASD_Release que se activa con los eventos en los que se suelta una de las teclas especificadas:
    def WASD_Release(event):
        """
        Función que controla los eventos que se activarán al soltar teclas definidas
        """
        nonlocal WPressed, APressed, SPressed, DPressed, ZPressed, XPressed, CPressed, FPressed
        Key = event.char
        #print(Key)
        if Key == "w":
            WPressed = False
        elif Key == "s":
            SPressed = False
            ThreadBacklightsR = Thread(target = back_light_control_release)
            ThreadBacklightsR.start()
        elif Key == "a":
            APressed = False
            send("dir:0;")
            TestCanv.itemconfig("tl", state = HIDDEN)
        elif Key == "d":
            DPressed = False
            send("dir:0;")
            TestCanv.itemconfig("tr", state = HIDDEN)
        elif Key == "z":
            ZPressed = False
        elif Key == "x":
            XPressed = False
        elif Key == "c":
            CPressed = False
        elif Key == "f":
            FPressed = False

    def back_light_control_release():
        nonlocal SPressed, SentBackON, SentBackOFF, Speed, WPressed
        #print(SPressed)
        while not SPressed:
            while Speed >= 0:
                if SentBackOFF:
                    return
                else:
                    send("lb:0;")
                    #print("SentBackOFF")
                    TestCanv.itemconfig("back", state = HIDDEN)
                    SentBackOFF = True
                    SentBackON = False
            else:
                if SentBackON:
                    return
                else:
                    send("lb:1;")
                    #print("SentBackON")
                    TestCanv.itemconfig("back", state = NORMAL)
                    SentBackON = True
                    SentBackOFF = False
        #print("S was pressed and exit release while")


    TestDrive.bind("<KeyPress>", WASD_Press) #Se le asigna el bind a la función WASD_Press().
    TestDrive.bind("<KeyRelease>",WASD_Release) #Este bind funciona de la misma forma pero opera opuesto al press.
    
    TestDrive.protocol("WM_DELETE_WINDOW", lambda : closeX(TestDrive))
    def ejecutarCelebracion():
        nonlocal celebracion
        for x in celebracion:
            send(x)
        
    

#-----Se termina la ventana de pruebas y se define la de los pilotos
def pilots_window():
    
    Pilots = Toplevel()
    Pilots.title("Pilots")
    Pilots.minsize(width= 800, height= 1000)
    Pilots.resizable(width= NO, height= NO)
    #Se genera el canvas
    PilotsCanv= Canvas(Pilots, width = 800, height = 1000)
    PilotsCanv.place(relx = 0.5,rely=0.5)
    #Se debe programar el resto del funcionamiento del módulo antes de declararlo como listo
    
    #Por ahora se tiene el botón de atras:
        
    BtnBack3= Button(PilotsCanv, text ="Main",command = lambda: btn_back(Pilots), fg= "cyan", bg = "black")
    BtnBack3.place(x= 200, y =100)
    Pilots.protocol("WM_DELETE_WINDOW", lambda : closeX(Pilots))








def closeX(widgetObj):
    widgetObj.destroy()

    
btnFont = ('Helvetica', 30, 'bold italic')   
#------Comandos de los Botones en Main------
BtnAbout= Button(MainCanv, text= "About",font = btnFont, command = btn_about,fg= "#FAFAFA",bg ="black") #Para ir a About
BtnAbout.place(x = 100,y = 100)

BtnTest= Button(MainCanv, text= "Test Drive", font = btnFont,command = btn_test,fg= "#FAFAFA",bg ="black")  #Para ir a TestDrive
BtnTest.place(x = 400, y = 100)

BtnPilots = Button(MainCanv, text= "Pilots",font = btnFont, command = btn_pilots,fg= "#FAFAFA",bg ="black") #Para ir a Pilots
BtnPilots.place(x = 800, y = 100)
Main.protocol("WM_DELETE_WINDOW", lambda : closeX(Main))
    
Main.mainloop()
