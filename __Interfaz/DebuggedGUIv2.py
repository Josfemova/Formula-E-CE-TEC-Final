"""
Prueba de modificación para el proyecto III
Ventana de Pruebas.
"""
from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
from WiFiClient import NodeMCU
import os
import threading
from threading import Thread
import time
#import random
#Variables globales para el funcionamiento de la ventana
#global Pot, NotMoving,Pressed,DirR,DirL, BlinkC, BlinkZ, PressW, PressS, PressF, Front, BackON
global Speed, Moving, WPressed, APressed, SPressed, DPressed, ZPressed, XPressed, CPressed, FLight, Blight, BlinkZ,BlinkC, SentBackON
#Valor inicial de las variables globales para esta ventana
Speed = 0
Moving = False
WPressed = False
APressed = False
SPressed = False
DPressed = False
ZPressed = False
XPressed = False
CPressed = False
FPressed = False
FLight = True
Blight = True
BlinkZ = False
BlinkC = False
BlightCount = 0
SentBackON = False
SentBackOFF = False
#Valor inicial del auto al entrar a la ventana
#send("lb:1;")
def cargar_imagen(Nombre):
    ruta = os.path.join("imagenes",Nombre)
    Imagen = PhotoImage(file = ruta)
    return Imagen
#*****************
TestDrive= Tk()
TestDrive.title("Test Drive")
TestDrive.geometry("1280x720")
TestDrive.resizable(width= NO, height= NO)
#Se genera el canvas de la ventana de pruebas
TestCanv= Canvas(TestDrive, width= 1280, height= 720,bg="black")
TestCanv.place(x=0, y=0)

FondoDia = cargar_imagen("DAY.png")
TestCanv.create_image(0,0,image=FondoDia, anchor = NW,tags = "dia", state = NORMAL)
FondoNoche = cargar_imagen("NIGHT.png")
TestCanv.create_image(0,0,image= FondoNoche, anchor = NW, tags = "noche", state = HIDDEN)

TopWheelL = cargar_imagen("TLWheel.png")
TestCanv.create_image(960,240, image = TopWheelL, anchor = NW, tags = "tl", state = HIDDEN)
TestCanv.create_image(1032,242, image = TopWheelL, anchor = NW, tags = "tl", state = HIDDEN)

TopWheelR = cargar_imagen("TopWheelRight.png")
TestCanv.create_image(963,240, image = TopWheelR, anchor = NW, tags = "tr", state = HIDDEN)
TestCanv.create_image(1040,238, image = TopWheelR, anchor = NW, tags = "tr", state = HIDDEN)

Borde = cargar_imagen("Car1.png")
TestCanv.create_image(925,200, image = Borde, anchor = NW,tags = ("fondo","día"))

TestCanv.create_text(60,300, text = "Escudería",font = ("Consolas",15),fill = "White",tags= "escu")
TestCanv.create_text(600,15, text = "NombreCarro", font = ("Consolas",15),fill = "White",tags = "name")
TestCanv.create_text(640,360, text = "PWM:0%", font= ("Consolas",18), fill = "White", tags = "pwm", anchor= CENTER)
TestCanv.create_text(1100,500, text = "Charge: %", font = ("Consolas", 18), fill = "white", tags = "battext", anchor = NW)

FrontLight = cargar_imagen("FrontL.png")
TestCanv.create_image(965,210, image = FrontLight, anchor = NW, tags = ("lights","front"), state = HIDDEN)
TestCanv.create_image(1030,210, image = FrontLight, anchor = NW, tags = ("lights","front"), state = HIDDEN)

DirLight = cargar_imagen("EmL.png")
TestCanv.create_image(940,250, image = DirLight, anchor = NW, tags = ("lights","left"), state = HIDDEN)
TestCanv.create_image(1030,250, image = DirLight, anchor = NW, tags = ("lights","right"), state = HIDDEN)

BackLight= cargar_imagen("BackL.png")
TestCanv.create_image(955,385, image = BackLight, anchor = NW, tags = ("lights", "back"), state = HIDDEN)
TestCanv.create_image(1005,385, image = BackLight, anchor = NW, tags = ("lights", "back"), state = HIDDEN)

    #Se debe programar la adición de las operaciones de la función aparte de generar la ventana

#Se utiliza el comando del botón atrás para volver a main
#Para ello se define una función al igual que en la ventana About
myCar = NodeMCU()
myCar.start()
  
#BtnBack2= Button(TestCanv, text = "Main", command = lambda: btn_back(TestDrive), fg= "cyan", bg= "black")
#BtnBack2.place(x= 1100, y =600)

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
        print("heehee")
        return

#--------------------
def check_sense():
    while True:
        Command = myCar.send("sense;")
        time.sleep(9);
    
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
            print(Answer)
            print(len(Answer))
            if len(Answer) >= 15:
                LDR = Thread(target = dia_noche, args = [Answer])
                LDR.start()
                Bat = Thread(target = bateria, args = [Answer])
                Bat.start()
            indice+=1
        time.sleep(0.200)

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
    global Battery
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
    global Speed, Moving, WPressed, APressed, SPressed, DPressed, ZPressed, XPressed, CPressed, FPressed, FLight, Blight, SentBack, BlinkZ, BlinkC
    Key = event.char
    if Key == "w":
        if not WPressed and not SPressed:
            WPressed = True
            ThreadForwards = Thread(target = gradual_front)
            time.sleep(0.2)
            ThreadForwards.start()
            #Hilo que controla la aceleración delantera del carro.
        else:
            return #do nothing
    elif Key == "s":
        if not SPressed and not WPressed:
            SPressed = True
            ThreadBackwards = Thread(target = gradual_back)
            ThreadBackwards.start()
            time.sleep(0.3)
            ThreadBacklightsP = Thread(target = back_light_control_press)
            ThreadBacklightsP.start()
        else:
            return
    elif Key == "a":
        if not APressed and not DPressed:
            send("dir:-1;")
            APressed = True
            print("sent to turn L")
            #código para activar o desactivar las imágenes que dan feedback de giro en la interfaz de usuario.
            TestCanv.itemconfig("tl", state = NORMAL)
        else:
            return
    elif Key == "d":
        if not DPressed and not APressed:
            send("dir:1;")
            DPressed = True
            print("sent to turn R")
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
            print("stopped blinking")
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
                print("sent to turn front on")
                TestCanv.itemconfig("front",state = NORMAL)
            else:
                send("lf:0;")
                FLight = True
                print("sent to turn front off")
                TestCanv.itemconfig("front",state = HIDDEN)
        else:
            return
    else:
        return #cuando suceda un evento pero no coincida con las teclas determinadas en este módulo
    #--------------------------------------
#Definición de las funciones objetivo de los hilos llamados en el módulo anterior.
def gradual_front():
    """
    Función que es invocada por el hilo de aceleración para generar un avance gradual
    """
    global Speed, Moving, WPressed, SPressed, SentBackOFF,SentBackON
    WPressed = True
    Moving = True
    while Speed < 400 and WPressed and not SPressed:
        if Speed <= -500:
        #En este caso se trabaja con un aumento de velocidad, en un caso esp. en que esta es menor que -500
            send("pwm:" + str(Speed) + ";")
            print("speed was lower than or at -500 so it was sent before incrementing")
            Speed += 100
            TestCanv.itemconfig("pwm", text = "PWM:" + str(Speed//10) +"%")
            print("incremented speed to " + str(Speed))
            time.sleep(1)
        else:
        #en este último caso, la velocidad va a ser mayor que 0, por lo cual se trata normalmente.
            if Speed >= -100:
                if not SentBackOFF:
                    send("lb:0;")
                    print("SentBackOFF")
                    SentBackOFF = True
                    SentBackON = False
                    TestCanv.itemconfig("back", state = HIDDEN)
            Speed += 100
            TestCanv.itemconfig("pwm", text = "PWM:" + str(Speed//10) +"%")
            print("incremented speed to " + str(Speed))
            time.sleep(1)
            
    TestCanv.itemconfig("pwm", text = "PWM:" + str(Speed//10) + "%")
    print("incremented speed to " + str(Speed) + " and exited first while")
    time.sleep(1)
    #la función entra a este while cuando salga del primero, que es mayor a 500.
    while 900>= Speed >= 400 and WPressed and not SPressed:
        Speed += 100
        send("pwm:" + str(Speed) + ";")
        TestCanv.itemconfig("pwm", text = "PWM:" + str(Speed//10) +"%")
        print("sent to move forward by " + str(Speed))
        time.sleep(1)
    send("pwm:" + str(Speed) + ";")
    print("sent to move forward by " + str(Speed) + " and exited second while")
    time.sleep(1)
    #---------------------------------------------
def gradual_back():
    """
    Función que es invocada por el hilo de desaceleración/reversa para generar un movimiento gradual hacia atrás.
    """
    global Speed,Moving, SPressed, WPressed
    SPressed = True
    while Speed > -400 and SPressed and not WPressed:
        if Speed >= 500:
            send("pwm:" + str(Speed) + ";")
            print("Speed was higher than or at 500, so it was sent before decrementing")
            Speed -= 100
            TestCanv.itemconfig("pwm", text = "PWM:" + str(Speed//10) +"%")
            print("decremented speed to " + str(Speed))
            time.sleep(1)
        else:
            Speed -= 100
            TestCanv.itemconfig("pwm", text = "PWM:" + str(Speed//10) +"%")
            print("decremented speed to " + str(Speed))
            time.sleep(1)
    TestCanv.itemconfig("pwm", text = "PWM:" + str(Speed//10) +"%")
    print("decremented speed to " + str(Speed) + " and exited first while")
    time.sleep(1)
    #la función entra a este while cuando salga del primero, que es menor a 500.
    while -900<=Speed<=-400 and SPressed and not WPressed:
        Speed -= 100
        send("pwm:" + str(Speed) + ";")
        TestCanv.itemconfig("pwm", text = "PWM:" + str(Speed//10) +"%")
        print("sent to move backwards by " + str(Speed))
        time.sleep(1)
    send("pwm:" + str(Speed) + ";")
    TestCanv.itemconfig("pwm", text = "PWM:" + str(Speed//10) +"%")
    print("sent to move backwards by " + str(Speed) + " and exited second while")
    #-------------------------------------------
def thread_blink(Direction):
    """
    Función que recibe la dirección a la que se desea activar el hilo de parpadeo para las direccionales.
    """
    global ZPressed, CPressed, BlinkZ, BlinkC
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
    global ZPressed, CPressed, XPressed, BlinkC, BlinkZ
    if Direction == "L":
        while BlinkZ:
            LED = Counter%2
            send("ll:" + str(LED) + ";")
            if LED == 1:
                TestCanv.itemconfig("left", state = NORMAL)
                print("Left light is ON")
                Counter += 1
            else:
                TestCanv.itemconfig("left", state = HIDDEN)
                print("Left light is OFF")
                Counter += 1
            time.sleep(1)
        send("ll:0;")
        TestCanv.itemconfig("left", state = HIDDEN)
        print("Left light is OFF and exited while")
    elif Direction == "R":
        while BlinkC:
            LED = Counter%2
            send("lr:" + str(LED) + ";")
            if LED == 1:
                TestCanv.itemconfig("right", state = NORMAL)
                print("Right light is ON")
                Counter += 1
            else:
                TestCanv.itemconfig("right", state = HIDDEN)
                print("Right light is OFF")
                Counter += 1
            time.sleep(1)
        send("lr:0;")
        TestCanv.itemconfig("right", state = HIDDEN)
        print("Right light is OFF and exited while")
    else:
        return
    #---------------------------------

def back_light_control_press():
    global Speed, SentBackON, SentBackOFF, SPressed
    while SPressed:
        if SentBackON:
            return
        else:
            send("lb:1;")
            print("SentBackON")
            TestCanv.itemconfig("back",state = NORMAL)
            SentBackON = True
            SentBackOFF = False
    print("S released, exit press while")
#-----------------------------------------                
#Función WASD_Release que se activa con los eventos en los que se suelta una de las teclas especificadas:
def WASD_Release(event):
    """
    Función que controla los eventos que se activarán al soltar teclas definidas
    """
    global Speed, Moving, WPressed, APressed, SPressed, DPressed, ZPressed, XPressed, CPressed, FPressed, FLight, Blight, Blink, SentBack
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
    global SPressed, SentBackON, SentBackOFF, Speed, WPressed
    print(SPressed)
    while not SPressed:
        while Speed >= 0:
            if SentBackOFF:
                return
            else:
                send("lb:0;")
                print("SentBackOFF")
                TestCanv.itemconfig("back", state = HIDDEN)
                SentBackOFF = True
                SentBackON = False
        else:
            if SentBackON:
                return
            else:
                send("lb:1;")
                print("SentBackON")
                TestCanv.itemconfig("back", state = NORMAL)
                SentBackON = True
                SentBackOFF = False
    print("S was pressed and exit release while")


TestDrive.bind("<KeyPress>", WASD_Press) #Se le asigna el bind a la función WASD_Press().
TestDrive.bind("<KeyRelease>",WASD_Release) #Este bind funciona de la misma forma pero opera opuesto al press.
    
    
TestDrive.mainloop()
