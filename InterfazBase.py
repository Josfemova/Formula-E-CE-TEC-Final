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
TTFont = ('Helvetica', 30, 'bold italic')
nnFont = ('Helvetica', 15, 'bold italic') 


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
IGE = MainCanv.create_text(890, 35, text = "Índice Ganador de Escudería: " + str(round(pilotos.IGE, 2)), font = TTFont, fill = '#FAFAFA')
NombreEscud = MainCanv.create_text(200, 35, text = "Loui Vcker 2019", font = TTFont, fill = '#FAFAFA')
MainCarro = 2019

EstadoCarro = MainCanv.create_text(640, 690, text = '', font = ('Helvetica',22,' bold italic'), fill = '#FAFAFA', anchor = CENTER)
def cooords(event):
        print(event.x)
        print(event.y)
MainCanv.bind("<Button-1>",cooords) #Este bind funciona de la misma forma pero opera opuesto al press.
    

Logo = MainCanv.create_image(620, 200, image = MainBG)
logoimg ='logo2.PNG'
logoref=''




newImagen= []
def recargaInfo():
    global newImagen,logoimg,Logo,logoref,EstadoCarro,MainCarro
    newImagen = []
    txtpatro = open("__InfoEscuderías\\patrocinadores.txt")
    l = (txtpatro.readline()).split(":")
    for i in range(0,len(l)):
        newImagen.insert(i,[cargar_imagen(l[i]+'.png')])
        MainCanv.create_image(i*170+200, 600, image = newImagen[i])
    txtpatro.close()
    MainCanv.itemconfig(IGE, text = "Índice Ganador de Escudería: " + str(round(pilotos.IGE, 2)))
    estado=''
    for i in range(0,len(autos.info)):
        if (autos.info[i][autos.iTEMPO] == MainCarro):
            estado = autos.info[i]
            pass
    MainCanv.itemconfig(EstadoCarro,text = ('Auto de temporada: '+estado[autos.iESTADO]))

    txtLOG = open("__InfoEscuderías\\logo.txt")
    logoimg = txtLOG.readline() + '.png'
    logoref = cargar_imagen(logoimg)
    MainCanv.itemconfig(Logo,image =logoref)
    
    
def modificarPatro():
    modPil = Toplevel()
    modPil.geometry('700x150')
    modPil.title('Patrocinadores')
    cmod = Canvas(modPil, width = 700, height = 150)
    cmod.pack()
    mensaje = ('si va a agregar un patrocinador, debe '
               'agregar una imagen con el nombre del patrocinador '
               'en la carpeta Interfaz//imagenes')
    Label(cmod, text = mensaje).grid(row=0, column =1 )
    text = Entry(cmod, justify = CENTER, width = 50, font = nnFont)
    text.grid(row = 1, column = 1)
    txtpatro = open("__InfoEscuderías\\patrocinadores.txt")
    l = txtpatro.readline()
    text.insert(0,l)
    txtpatro.close
    

    def actualizar():
        txtpatro = open("__InfoEscuderías\\patrocinadores.txt",'w')
        txtpatro.write(text.get())
        txtpatro.close()
        recargaInfo()
        modPil.destroy()
        
    Btn = Button(cmod, text = 'Actualizar', font = TTFont, command = actualizar)
    Btn.grid(row = 2, column=1)
    
def modificarLogo():
    modLog = Toplevel()
    modLog.geometry('700x150')
    modLog.title('Logos')
    cmod = Canvas(modLog, width = 700, height = 150)
    cmod.pack()
    mensaje = ('para modificar el Logo debe escribir el '
               'nombre del archivo de imagen sin extensión')
    Label(cmod, text = mensaje).grid(row=0, column =1 )
    text = Entry(cmod, justify = CENTER, width = 50, font = nnFont)
    text.grid(row = 1, column = 1)
    txtLOG = open("__InfoEscuderías\\logo.txt")
    l = txtLOG.readline()
    text.insert(0,l)
    txtLOG.close
    def actualizar():
        txtLOG= open("__InfoEscuderías\\logo.txt",'w')
        txtLOG.write(text.get())
        txtLOG.close()
        recargaInfo()
        modLog.destroy()
    Btn = Button(cmod, text = 'Actualizar', font = TTFont, command = actualizar)
    Btn.grid(row = 2, column=1)
    
recargaInfo()








def btn_about():
    Main.withdraw()
    about_window()

def btn_test():
    Main.withdraw()
    test_drive_window()

def btn_pilots():
    Main.withdraw()
    pilots_window()

def closeX(widgetObj,parent=''):
    widgetObj.destroy()
    if parent !='':
        recargaInfo()
        parent.deiconify()

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
        
    BtnBack1 =  Button(AboutCanv, text= "Main",command =lambda: closeX(About, Main),fg = "cyan", bg= "black")
    BtnBack1.place(x = 600, y = 500)

#-----Se termina la venta about y se define la ventana de pruebas
def test_drive_window(pilotoIndex, parent=Main):
    #Valor inicial de las variables globales para esta ventana
    celebracion = pilotos.getCelebracion(pilotoIndex)
    
    carro = int(pilotos.info[pilotoIndex][pilotos.iTEMPO])
    deEscuderia = False
    for i in range(0,len(autos.info)):
        if (autos.info[i][autos.iTEMPO] == carro):
            carro = i
            deEscuderia = True
            pass
        
    if deEscuderia:
        if autos.info[carro][autos.iESTADO] == 'Disponible':
            pass
        else:
            messagebox.showinfo('Error','AUTO no se encuentra disponible')
            return
    else:
        messagebox.showinfo('Error','AUTO no se encuentra disponible')
        return
    
    parent.withdraw()
    def closeTestDrive():
        nonlocal carro
        nonlocal ActiveWindow
        ActiveWindow = False
        sleep(0.2)
        closeX(TestDrive, parent)
        def getBat():
            try:
                Answer = (send("sense;",True).split(";"))[0]
                if "blvl:" in Answer:
                    battery = int(Answer[5:])
                    if battery < 10:
                        data = autos.info[carro]
                        data[autos.iESTADO]="Descargado"
                        data.insert(0, carro)
                        autos.modificarAuto(*tuple(data))
            except:
                print("error en lectura de bateria")
            myCar.stop()
        Thread(target = getBat, args = ()).start()
            
    Speed = 0
    Moving,WPressed,APressed,SPressed,DPressed,ZPressed,XPressed,CPressed,FPressed,BlinkZ,BlinkC,SentBackON,SentBackOFF = (False,)*13
    FLight = True
    Blight = True
    ActiveWindow = True
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
    TestCanv.create_image(860,240, image = TopWheelL, anchor = NW, tags = "tl", state = HIDDEN)
    TestCanv.create_image(932,242, image = TopWheelL, anchor = NW, tags = "tl", state = HIDDEN)

    TestDrive.Twr = TopWheelR = cargar_imagen("TopWheelRight.png")
    TestCanv.create_image(863,240, image = TopWheelR, anchor = NW, tags = "tr", state = HIDDEN)
    TestCanv.create_image(940,238, image = TopWheelR, anchor = NW, tags = "tr", state = HIDDEN)
    TestDrive.Borde = Borde = cargar_imagen("Car1.png")
    TestCanv.create_image(825,200, image = Borde, anchor = NW,tags = ("fondo","día"))
    TestDrive.fl = FrontLight = cargar_imagen("FrontL.png")
    TestCanv.create_image(865,210, image = FrontLight, anchor = NW, tags = ("lights","front"), state = HIDDEN)
    TestCanv.create_image(930,210, image = FrontLight, anchor = NW, tags = ("lights","front"), state = HIDDEN)
    TestDrive.dirl = DirLight = cargar_imagen("EmL.png")
    TestCanv.create_image(840,250, image = DirLight, anchor = NW, tags = ("lights","left"), state = HIDDEN)
    TestCanv.create_image(930,250, image = DirLight, anchor = NW, tags = ("lights","right"), state = HIDDEN)
    TestDrive.bl = BackLight= cargar_imagen("BackL.png")
    TestCanv.create_image(855,385, image = BackLight, anchor = NW, tags = ("lights", "back"), state = HIDDEN)
    TestCanv.create_image(905,385, image = BackLight, anchor = NW, tags = ("lights", "back"), state = HIDDEN)
    
    #-----------------------------------------
    TestCanv.create_text(120,70, text = "Escudería: Loui Vcker",font = ("Algency FB",18,'bold italic'),fill = "black",tags= "escu", anchor =NW)
    TestCanv.create_text(120,100, text = ("Marca Auto: "+autos.info[carro][0]),font = ("Algency FB",18,'bold italic'),fill = "black",tags= "escu", anchor =NW)
    TestCanv.create_text(120,130, text = ("Modelo Auto: "+autos.info[carro][1]),font = ("Algency FB",18,'bold italic'),fill = "black",tags= "escu", anchor =NW)
    TestCanv.create_text(600,70, text = ("Piloto: " + pilotos.info[pilotoIndex][pilotos.iNOM]),font = ("Algency FB",18,'bold italic'),fill = "black",tags= "escu", anchor =NW)
    TestCanv.create_text(600,100, text = ("Nacionalidad: "+ pilotos.info[pilotoIndex][pilotos.iPAIS]),font = ("Algency FB",18,'bold italic'),fill = "black",tags= "escu", anchor =NW)
    TestCanv.create_text(600,130, text = ("Test Drive 1.0 - Loui Vcker Racing Team"),font = ("Algency FB",18,'bold italic'),fill = "black",tags= "escu", anchor =NW)
    #-----------------------------------------
    
    
    TestCanv.create_text(620,675, text = "PWM:0%", font= ("Algency FB",18,'bold italic'), fill = "black", tags = "pwm", anchor= NW)
    TestCanv.create_text(220,190, text = "%", font = ("Algency FB",18,'bold italic'), fill = "black", tags = "battext", anchor = NW)

    

        #Se debe programar la adición de las operaciones de la función aparte de generar la ventana

    #Se utiliza el comando del botón atrás para volver a main
    #Para ello se define una función al igual que en la ventana About
    myCar = NodeMCU()
    myCar.start()
      
    BtnBack2= Button(TestCanv, text = "Main", command = closeTestDrive, fg= "cyan", bg= "black")
    BtnBack2.place(x= 1100, y =600)

    #Código para trabajar los casos con las teclas de movimiento
    #Se define un evento de mapeo de teclas para la ventana:
    #Función send para enviar los comandos al NodeMCU
    #Esta función es una modificación a la dada en el archivo TelemetryLog por Santiago Gamboa
    def send(Msg, returnAns = False):
        """
        Función send para enviar comandos al Node
        Esta funcion es una modificación a la dada en el archivo TelemetryLog por Santiago Gamboa (Asistente del Curso)
        """
        if(len(Msg)>0 and Msg[-1] == ";"):
            response = myCar.send(Msg)
            if returnAns:
                sleep(4)
                return myCar.readById(response)
    #-----------------------------------------
    def check_sense():
        while ActiveWindow:
            Command = myCar.send("sense;")
            sleep(4);
            response = myCar.readById(Command)
            if ActiveWindow:
                dia_noche(response)
                bateria(response)
            
        
    ThreadSense = Thread(target = check_sense)
    ThreadSense.start()

    def dia_noche(Answer):
        #Validar la posición del caracter en el que la LDR manda la variable light
        
        if Answer[-3] == "0":
            TestCanv.itemconfig("dia", state = HIDDEN)
            TestCanv.itemconfig("noche", state = NORMAL)
        elif Answer[-3] == "1":
            TestCanv.itemconfig("dia", state = NORMAL)
            TestCanv.itemconfig("noche", state = HIDDEN)
        else:
            return

    def bateria(Answer):
        #print("entered")
        #nonlocal Battery
        if len(Answer) == 14:
            Battery = Answer[5]
            TestCanv.itemconfig("battext", text =(Battery) + "%")
        elif len(Answer) == 15:
            Battery = Answer[5:7]
            TestCanv.itemconfig("battext", text =(Battery) + "%")
        elif len(Answer) == 16:
            Battery = Answer[5:8]
            TestCanv.itemconfig("battext", text =(Battery) + "%")
        else:
            return

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
                #código para activar o desactivar las imágenes que dan feedback de giro en la interfaz de usuario.
                TestCanv.itemconfig("tl", state = NORMAL)
            else:
                return
        elif Key == "d":
            if not DPressed and not APressed:
                send("dir:1;")
                DPressed = True
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
                    TestCanv.itemconfig("front",state = NORMAL)
                else:
                    send("lf:0;")
                    FLight = True
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
                Speed += 100
                TestCanv.itemconfig("pwm", text = "PWM:" + str(Speed))
                sleep(0.2)
            else:
                if -500<Speed<=0:
                    send("pwm:" + str(Speed) + ";")
                    Speed += 100
                    TestCanv.itemconfig("pwm", text = "PWM:" + str(Speed))
                    sleep(0.1)
                    
            #en este último caso, la velocidad va a ser mayor que 0, por lo cual se trata normalmente.
                if Speed >= -100:
                    if not SentBackOFF:
                        send("lb:0;")
                        SentBackOFF = True
                        SentBackON = False
                        TestCanv.itemconfig("back", state = HIDDEN)
                Speed += 100
                TestCanv.itemconfig("pwm", text = "PWM:" + str(Speed))
                sleep(1)
                
        TestCanv.itemconfig("pwm", text = "PWM:" + str(Speed))
        #la función entra a este while cuando salga del primero, que es mayor a 500.
        while 1000>= Speed >= 400 and WPressed and not SPressed:
            if Speed==1000:
                Speed += 23
                send("pwm:" + str(Speed) + ";")
                TestCanv.itemconfig("pwm", text = "PWM:" + str(Speed))
                sleep(0.3)
            else:
                Speed += 100
                send("pwm:" + str(Speed) + ";")
                TestCanv.itemconfig("pwm", text = "PWM:" + str(Speed))
                sleep(0.3)
            
        
            
        TestCanv.itemconfig("pwm", text = "PWM:" + str(Speed))
        #---------------------------------------------
    def gradual_back():
        """
        Función que es invocada por el hilo de desaceleración/reversa para generar un movimiento gradual hacia atrás.
        """
        nonlocal Speed,Moving, SPressed, WPressed
        SPressed = True
        while Speed > -400 and SPressed and not WPressed:
            if Speed==1023:
                Speed -= 23
                send("pwm:" + str(Speed) + ";")
                TestCanv.itemconfig("pwm", text = "PWM:" + str(Speed))
                sleep(0.3)
            elif Speed >= 500:
                send("pwm:" + str(Speed) + ";")
                Speed -= 100
                TestCanv.itemconfig("pwm", text = "PWM:" + str(Speed))
                sleep(0.1)
            else:
                Speed -= 100
                send("pwm:" + str(Speed) + ";")
                TestCanv.itemconfig("pwm", text = "PWM:" + str(Speed))
                sleep(0.1)
        TestCanv.itemconfig("pwm", text = "PWM:" + str(Speed))
        #la función entra a este while cuando salga del primero, que es menor a 500.
        while -900<=Speed<=-400 and SPressed and not WPressed:
            Speed -= 100
            send("pwm:" + str(Speed) + ";")
            TestCanv.itemconfig("pwm", text = "PWM:" + str(Speed))
            #print("sent to move backwards by " + str(Speed))
            sleep(0.5)
        
        TestCanv.itemconfig("pwm", text = "PWM:" + str(Speed))
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
            while BlinkZ and ActiveWindow:
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
            while BlinkC and ActiveWindow:
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
        while not SPressed and ActiveWindow:
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

    def ejecutarCelebracion():
        nonlocal celebracion
        for x in celebracion:
            send(x)
            sleep(0.7)
        final = ['pwm:0;','dir:0;','lf:0;','lb:0;','lr:0;','ll:0;']
        for x in final:
            send(x)
            sleep(0.2)


    uBG = '#141414'
    txtBG = '#FAFAFA'

    Button(TestDrive, text="Zigzag",font=nnFont, width=10,bg=uBG,fg = txtBG,bd=0,
           command=lambda: send('ZigZag;')).place(x=1125,y=245, anchor = CENTER)
    Button(TestDrive, text="Círculo D",font=nnFont, width=10,bg=uBG,fg = txtBG,bd=0,
           command=lambda: send('Circle:1;')).place(x=1125,y=285, anchor = CENTER)
    Button(TestDrive, text="Círculo L",font=nnFont, width=10,bg=uBG,fg = txtBG,bd=0,
           command=lambda: send('Circle:-1;')).place(x=1125,y=325, anchor = CENTER)
    Button(TestDrive, text="Inifinito",font=nnFont, width=10,bg=uBG,fg = txtBG,bd=0,
           command=lambda: send('Infinite;')).place(x=1125,y=365, anchor = CENTER)
    Button(TestDrive, text="Especial",font=nnFont, width=10,bg=uBG,fg = txtBG,bd=0,
           command=lambda: send('Especial;')).place(x=1125,y=405, anchor = CENTER)
    Button(TestDrive, text="Celebración",font=nnFont, width=10,bg=uBG,fg = txtBG,bd=0,height =3,
           command=lambda: ejecutarCelebracion()).place(x=1125,y=490, anchor = CENTER)
    Button(TestDrive, text="Cerrar \n Test Drive",font=nnFont, width=10,bg=uBG,fg = txtBG,bd=0,height =3,
           command=lambda: closeTestDrive()).place(x=1125,y=600, anchor = CENTER)
    
    def cooords(event):
        print(event.x)
        print(event.y)
    TestDrive.bind("<Button-1>",cooords) #Este bind funciona de la misma forma pero opera opuesto al press.
    
    TestDrive.bind("<KeyPress>", WASD_Press) #Se le asigna el bind a la función WASD_Press().
    TestDrive.bind("<KeyRelease>",WASD_Release) #Este bind funciona de la misma forma pero opera opuesto al press.
    
    TestDrive.protocol("WM_DELETE_WINDOW", closeTestDrive)

            
    
        
############################################   
############################################
            ############################################
            ############################################
            ############################################
            ############################################
            ############################################
            ############################################
#-----Se termina la ventana de pruebas y se define la de los pilotos
def pilots_window(parent = Main):
    global pilotos,autos, TTFont, nnFont
    DscRGP, DscREP, DscEficiencia = (False,)*3
    
    Pilots = Toplevel()
    Pilots.title("Pilots")
    Pilots.minsize(width= 1200, height= 800)
    Pilots.resizable(width= NO, height= NO)
    
    uFont = ('Helvetica', 14, 'bold italic')
    uBG = 'black'
    txtBG = '#FAFAFA'

    
    C_Pil= Canvas(Pilots,width=1200,height=800,bd=0, highlightthickness=0, bg= uBG)
    #C_Pil.place(relx=0.5,rely=0.5, anchor ='c')
    C_Pil.pack(expand=2, anchor='c', fill=Y)
    C_Pil.fondoPil = fondoPil = cargar_imagen("fondoHistorial.png")
    C_Pil.create_image(0,0, image =fondoPil, anchor = NW)
    sepR = Frame(C_Pil, width = 20)
    sepL = Frame(C_Pil, width = 20)
    sepLow = Frame(C_Pil, height = 10)
    sepR.grid(rowspan = 10, column = 0)
    sepL.grid(rowspan = 10, column = 3)
    sepLow.grid(column = 0, row = 7, columnspan = 3)


    elements = []
    def cargarPilotos(param):
        global pilotos
        nonlocal elements, DscRGP, DscREP
        if param == 'RGP':
            if DscRGP==False:
                DscRGP = True
                pilotos.ordenar(param,True)
            else:
                DscRGP = False
                pilotos.ordenar(param,False)
                
        elif param == 'REP':
            if DscREP==False:
                DscREP = True
                pilotos.ordenar(param,True)
            else:
                DscREP= False
                pilotos.ordenar(param,False)
        #----------------------------------------------        
        for x in elements:
            listBox.delete(x)
        elements = []
        fotos=[]
        C_Pil.fotoPil = []
        for i in range(0, len(pilotos.info)):
            try:
                fotos.insert(i,cargar_imagen(pilotos.info[i][pilotos.iFOTO]))
                C_Pil.fotoPil.insert(i,fotos[i])
            except Exception as e:
                print(e)
            data = [i+1]+pilotos.info[i][pilotos.iNOM:pilotos.iMOV] + pilotos.info[i][pilotos.iPARTICIPA:]
            data = tuple(data)
            elements.append(listBox.insert("", "end", values=data,image = fotos[i], tags = ('elemento',)))
            
    elementsA = []
    def cargarAutos():
        global autos
        nonlocal elementsA, DscEficiencia
        if DscEficiencia:
            autos.ordenar(False)
            DscEficiencia = False
        else:
            autos.ordenar(True)
            DscEficiencia = True
        #---------------------------------------------
        for x in elementsA:
            listBoxAut.delete(x)
        elementsA= []
        fotos=[]
        C_Pil.fotoAutos=[]
        for i in range(0, len(autos.info)):
            try:
                fotos.insert(i,cargar_imagen(autos.info[i][autos.iFOTO]))
                C_Pil.fotoAutos.insert(i,fotos[i])
            except Exception as e:
                print(e)
            data = autos.info[i][:autos.iFOTO] + autos.info[i][autos.iTEMPO:]
            data = tuple(data)
            elementsA.append(listBoxAut.insert("", "end", values=data,image = fotos[i], tags = ('elemento',)))



    style = ttk.Style(C_Pil)
    style.configure('Treeview', rowheight=70, font = ('Helvetica',13,'bold italic'))
    style.configure('Treeview.Heading', font = ('Helvetica',13,'bold italic'))
    #Organizacion del TreeView de Pilotos
    #-------------------------------------------------------------------------
    Frame(C_Pil, height = 70).grid(row=0, columnspan =4)
    C_Pil.create_text(550, 20, text = 'Pilotos', fill = txtBG, font = TTFont, anchor = NW)
    #labelPil = Label(C_Pil, text="Pilotos",bg=txtBG,fg = uBG, font=TTFont).grid(row=0, columnspan=4)
    cols = ('Pos','Nombre Completo',"Edad","Nacionalidad","Tempo","Eventos","Podio","Victorias","Abandonos","REP","RGP")
    listBox = ttk.Treeview(C_Pil,columns=cols,height = 6)
    for col in cols:
        listBox.heading(col, text=col)
    listBox.heading('REP', command =lambda : cargarPilotos("REP"))
    listBox.heading('RGP', command =lambda : cargarPilotos("RGP"))
    listBox.column('#0', width = 150, anchor = 'c')
    listBox.column(cols[0], width = 40, anchor = 'c')
    listBox.column(cols[1], width = 200, anchor = 'c')
    listBox.column(cols[2], width = 60, anchor = 'c')
    listBox.column(cols[3], width = 120, anchor = 'c')
    for i in range(4, len(cols)):
        listBox.column(cols[i], width = 80, anchor = 'c')
    listBox.grid(row=1, column=1, columnspan=2)
    #--------------------------------------------------------------------------

    #Organización del TreeView de Autos
    #-------------------------------------------------------------------------
    Frame(C_Pil, height = 20).grid(row=4, columnspan =4)
    C_Pil.create_text(550, 565, text = 'Autos', fill = txtBG, font = TTFont, anchor = NW)
    #labelAutos = Label(C_Pil, text="Autos",bg=txtBG,fg = uBG, font=TTFont).grid(row=4, columnspan=3)
    colsAut = ('Marca','Modelo','Origen','Temporada','Baterias','CPB','VoltPB','Estado','Consumo','sensores','Peso','Eficiencia')
    listBoxAut = ttk.Treeview(C_Pil,columns=colsAut,height = 5)
    for col in colsAut:
        listBoxAut.heading(col, text=col)
    listBoxAut.heading('Eficiencia', command =lambda : cargarAutos())
    for i in range(0, len(colsAut)):
        listBoxAut.column(colsAut[i], width =90, anchor ='c')
    listBoxAut.column('#0', width = 150, anchor = 'c')
    listBoxAut.column(colsAut[5], width = 50, anchor = 'c')
    listBoxAut.column(colsAut[6], width = 50, anchor = 'c')
    listBoxAut.grid(row=5, column=1, columnspan=2)
    #-------------------------------------------------------------------------


   



    def agregarPiloto(parent = Pilots):
        nonlocal cols
        parent.withdraw()
        AP=Toplevel()
        AP.title("Agregar Piloto")
        AP.minsize(320,270)
        AP.resizable(width=NO,height=NO)
        CAP = Canvas(AP, width = 320, height = 270)
        CAP.place(x=0, y=0, anchor =NW)
        
        def closeAP():
            parent.deiconify()
            AP.destroy()
            cargarPilotos(pilotos.CURRENTORDER)
            
        hojaTec= []
        for i in range(1,len(cols)-2):
            Label(CAP, text = cols[i]).place(x=5,y=(20*i)+20)
            entryText=Entry(CAP,width=30, justify = CENTER)
            entryText.place(x=120, y=(20*i)+20)
            hojaTec.append(entryText)

        Label(CAP, text = 'Ruta de foto').place(x=5,y=(20*(len(cols)-2))+20)
        entryText=Entry(CAP,width=30, justify = CENTER)
        entryText.place(x=120, y=(20*(len(cols)-2)+20))
        hojaTec.insert(0, entryText)
        
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
                if i!= 0 and i!=1 and i!= 3 :
                    try:
                        float(newData[i])
                    except:
                        print(newData[i])
                        i= len(newData)
                        print(newData)
                        print("error")
            newData.insert(pilotos.iMOV, createCeleb())
            tuple(newData)
            pilotos.agregarPiloto(*newData)
            closeAP()

            
            
        Btn_cerrar = Button(CAP, width=25,text="Cerrar",command=closeAP).place(x = 10, y=5)
        Btn_agregar = Button(CAP, width=25,text="Agregar",command=enviar).place(x = 10, y = 220)



    def modificarPiloto(piloto, parent = Pilots):
        if piloto == []:
            return
        nonlocal cols
        parent.withdraw()
        AP=Toplevel()
        AP.title("Modificar Piloto")
        AP.minsize(320,270)
        AP.resizable(width=NO,height=NO)
        CAP = Canvas(AP, width = 320, height = 270)
        CAP.place(x=0, y=0, anchor =NW)
        
        def closeAP():
            global pilotos
            nonlocal cargarPilotos
            parent.deiconify()
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
        Label(CAP, text = 'Ruta de foto').place(x=5,y=(20*(len(cols)-2))+20)
        entryText=Entry(CAP,width=30, justify = CENTER)
        entryText.place(x=120, y=(20*(len(cols)-2)+20))
        entryText.insert(0,pilotos.info[pos][pilotos.iFOTO])
        hojaTec.insert(0, entryText)
        
            
        def enviar():
            global pilotos
            nonlocal hojaTec, pos, closeAP
            newData = []
            for x in hojaTec:
                newData.append(x.get())
            newData.insert(pilotos.iMOV,pilotos.info[pos][pilotos.iMOV])                    
            newData.insert(0,pos)
            for i in range(0, len(newData)):
                if i!=1 and i!= 2 and i!= 4 and i!=6:
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


    def agregarAuto(parent = Pilots):
        nonlocal colsAut
        parent.withdraw()
        Aa=Toplevel()
        Aa.title("Agregar Auto")
        Aa.minsize(320,340)
        Aa.resizable(width=NO,height=NO)
        CAP = Canvas(Aa, width = 320, height = 340)
        CAP.place(x=0, y=0, anchor =NW)
        
        def closeAP():
            parent.deiconify()
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
            agregado = autos.agregarAuto(*newData)
            if not agregado:
                messagebox.showinfo('error','Ya existe un auto para esta temporada')
            closeAP()

            
            
        Btn_cerrar = Button(CAP, width=25,text="Cerrar",command=closeAP).place(x = 10, y=5)
        Btn_agregar = Button(CAP, width=25,text="Agregar",command=enviar).place(x = 10, y = 310)


        

    def modificarAuto(Auto,pos, parent = Pilots):
        if Auto == []:
            return
        nonlocal colsAut
        parent.withdraw()
        Aa=Toplevel()
        Aa.title("Modificar Auto")
        Aa.minsize(320,330)
        Aa.resizable(width=NO,height=NO)
        CAP = Canvas(Aa, width = 320, height = 330)
        CAP.place(x=0, y=0, anchor =NW)
        
        def closeAP():
            global autos
            nonlocal cargarAutos
            parent.deiconify()
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
        

    Btn_modificar = Button(C_Pil, text = "modificar información",font=nnFont, width = 25,bg=uBG,fg = txtBG,bd=0,
                           command = lambda: modificarPiloto(list(listBox.item(listBox.selection(),'values')))).grid(row= 2, column =2)
    
    Btn_agregar = Button(C_Pil, text="agregar piloto",font=nnFont, width=25,bg=uBG,fg = txtBG,bd=0,
                         command=lambda: agregarPiloto()).grid(row = 2, column = 1 )
    
    Btn_TestDrive = Button(C_Pil, text="TestDrive",font=nnFont, width=25,bg=uBG,fg = txtBG,bd=0,
                           command=lambda: test_drive_window(listBox.index(listBox.selection()),Pilots)).grid(row=3, column=2)


    Btn_modificarA = Button(C_Pil, text = "modificar información",font=nnFont, width =25,bg=uBG,fg = txtBG,bd=0,
                            command = lambda: modificarAuto(list(listBoxAut.item(listBoxAut.selection(),'values')),
                                                            listBoxAut.index(listBoxAut.selection()))).grid(row= 6, column =2)
    
    Btn_agregarA = Button(C_Pil, text="agregar auto",font=nnFont, width=25,bg=uBG,fg = txtBG,bd=0,
                          command=lambda: agregarAuto()).grid(row = 6, column = 1 )

    Btn_Atras = Button(C_Pil, text="Atrás",font=nnFont, width=25,bg=uBG,fg = txtBG,
                          command=lambda: closeX(Pilots, Main)).place(x=10,y=10)
    
    cargarPilotos(pilotos.CURRENTORDER)
    cargarAutos()

    Pilots.protocol("WM_DELETE_WINDOW", lambda : closeX(Pilots, Main))


    
  
#------Comandos de los Botones en Main------
BtnAbout= Button(MainCanv, text= "Información",font = TTFont, command = btn_about,fg= "#FAFAFA",bg ="black") #Para ir a About
BtnAbout.place(x = 100,y = 100)

BtnPilots = Button(MainCanv, text= "Autos y Pilotos",font = TTFont, command = btn_pilots,fg= "#FAFAFA",bg ="black") #Para ir a Pilots
BtnPilots.place(x = 800, y = 100)

BtnPilots = Button(MainCanv, text= "Modificar Patrocinadores",font = nnFont, command = modificarPatro,fg= "#FAFAFA",bg ="black") #para editar patrocinadores
BtnPilots.place(x = 1000, y = 670)

BtnPilots = Button(MainCanv, text= "Modificar Logo",font = nnFont, command = modificarLogo,fg= "#FAFAFA",bg ="black") #para editar patrocinadores
BtnPilots.place(x = 10, y = 670)

Main.protocol("WM_DELETE_WINDOW", lambda : closeX(Main))
    
Main.mainloop()
