#Encabezado del Proyecto
"""
______________________________________
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
____________________________________
"""
#    __________________________
#___/Importación de Bibliotecas
from tkinter import * #Para el uso de labels, canvas, Photo, etc
#from tkinter import scrolledtext #para utilizar en la ventana about
from tkinter.scrolledtext import ScrolledText as ST
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
    """
    Entradas:Nombre
    Salidas:referencia a photoImage Creada
    Restricciones:Nombre debe referenciar una imagen exitente, esta debe encontrarse en la carpeta imagenes dentro de _Interfaz
    Funcionamiento: Carga una photoimage según el nombre de imagen que se ingresa
    """
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
IGE = MainCanv.create_text(940, 35, text = "Índice Ganador de Escudería: " + str(round(pilotos.IGE, 2)), font = TTFont, fill = '#FAFAFA')
NombreEscud = MainCanv.create_text(290, 35, text = "Loui Vcker - Costa Rica - 2019", font = TTFont, fill = '#FAFAFA')
MainCarro = 2019
EstadoCarro = MainCanv.create_text(640, 690, text = '', font = ('Helvetica',22,' bold italic'), fill = '#FAFAFA', anchor = CENTER)  
Logo = MainCanv.create_image(620, 200, image = MainBG)
logoimg =''
logoref=''



newImagen= []
def recargaInfo():
    """
    Funcionamiento: Recarga los patrocinadores, información de escudería y logos en la pantalla principal
    """
    global newImagen,logoimg,Logo,logoref,EstadoCarro,MainCarro
    newImagen = []
    txtpatro = open("__InfoEscuderías\\patrocinadores.txt")
    l = (txtpatro.readline()).split(":")
    #carga las imágenes de los patrocinadores basados en un txt cargado por medio de iteracion
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
    """
    Funcionamiento: Muestra una ventana que permite ingresar los nombres de los patrocinadores
    """
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
        """
        Funcionamiento: actualiza archivo de texto que guarda patrocinadores
        """
        txtpatro = open("__InfoEscuderías\\patrocinadores.txt",'w')
        txtpatro.write(text.get())
        txtpatro.close()
        recargaInfo()
        modPil.destroy()
        
    Btn = Button(cmod, text = 'Actualizar', font = TTFont, command = actualizar)
    Btn.grid(row = 2, column=1)
    
def modificarLogo():
    """
    Funcionamiento: Muestra una ventana que permite ingresar los el nombre del logo a mostrar (nombre de imagen sin extensión)
    """
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


#    _____________________________________________________________
#___/Funciones para uso de botones definidos al final del programa

def btn_about():
    """
    Comando del botón para iniciar la ventana de about/información
    """
    Main.withdraw() #Guarda la ventana principal
    about_window() #Invoca la funcion de la ventana de información

def btn_test():
    """
    Comando del botón para iniciar la ventana de Test Drive
    Nota: esta sólo puede accederse por medio de la ventana de pilotos.
    """
    Main.withdraw() #Guarda la ventana principal
    test_drive_window() #Invoca la función de la ventana de pruebas/ Test Drive

def btn_pilots():
    """
    Comando del botón para iniciar la ventana de pilotos/autos
    """
    Main.withdraw()
    pilots_window()

def closeX(widgetObj,parent=''):
    """
    Función general que puede utilizarse para cerrar cualquier ventana.
    Restricciones: para invocar este módulo debe utilizarse la exprexión lambda a la hora de asignarla como comando.
    """
    widgetObj.destroy() #Destruye la ventana del primer parámetro
    if parent !='': #Si el parent invocado es una ventana y no se deja como una cadena vacía:
        recargaInfo()
        parent.deiconify() #Se reabre la ventana "parent" del widget a cerrar.

#    _____________
#___/ventana about
def about_window():
    """
    Funcionamiento: Ventana que muestra información de autores
    """
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
    About.geometry("700x690")
    About.resizable(width = NO, height = NO)

    #    ___________________________________
    #___/ Definicion de elementos de ventana
    C_About = Canvas(About, width = 1280, height = 720, bg = "#FAFAFA") #Cercano al RGB(255) en los 3 aspectos
    C_About.pack(anchor = NW, fill = Y)
    C_About.FondoAbout = FondoAbout = cargar_imagen("FondoAbout.png")
    C_About.create_image(-200,0,image = FondoAbout, anchor = NW)
    C_About.Alejandro = FotoAlejandro = cargar_imagen("Alejandro.png")
    C_About.create_image(10,500, image = FotoAlejandro, anchor = NW)
    C_About.Morales = FotoMorales = cargar_imagen("Morales.png")
    C_About.create_image(170, 500, image = FotoMorales, anchor = NW)
    C_About.Creditos = AboutText
    C_About.create_text(10,10,anchor = NW, text = AboutText, font = ("Helvetica", 10, "bold italic"),
                        fill = "#FAFAFA", justify = CENTER)
    
    C_About.Hints = Hints = ST(C_About, width = 50, height = 15, bg = "Black", font = ("Helvetica", 10, "bold italic"), fg = "white",bd = 0)
    C_About.Hints.insert(INSERT,HelpText)
    C_About.Hints.place(x = 320, y= 20)


    
    Btn_CerrarAb= Button(C_About, command =lambda: closeX(About, Main),  text = "Volver", bg = "black", fg = "#FAFAFA",
                         font = ("Helvetica", 14, "bold italic"), height = 3, width = 27,bd=3)
    Btn_CerrarAb.place(x = 340,y = 570, anchor = NW)






#############################################################################################################################################################################
    
#############################################################################################################################################################################
    
#############################################################################################################################################################################




#_______________________________________________________       Sección de Ventana de Test Drive              ________________________________________________________________



#############################################################################################################################################################################
    
#############################################################################################################################################################################
    
#############################################################################################################################################################################
    
#-----Se termina la venta about y se define la ventana de pruebas
def test_drive_window(pilotoIndex, parent=Main):
    """
    Entradas: pilotoIndex  - posición de piloto en lista de pilotos.info, parent - ventana que lama a test drive
    Salidas: pilotoIndex debe ser un piloto con un auto asignado el cual esté disponible
    Funcionamiento: Ventana encargada de controlar lo que respecta al control de carro, y el gurdado de eficiencia, nivel de batería y sensores
    """
    #Valor inicial de las variables globales para esta ventana

    #toma los datos de piloto y auto a ser utilizados en el test drive
    celebracion = pilotos.getCelebracion(pilotoIndex)
    carro = int(pilotos.info[pilotoIndex][pilotos.iTEMPO])

    #    _______________________________
    #___/ Chequeo de que el carro este disponible
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
        """
        Funcionamiento: Calcula el nivel de bateria del carro, calcula si el mismo está descargado
        Cierra la ventana del test drive luego del cálculo y retorna a la ventana de autos y pilotoso
        """
        nonlocal carro
        nonlocal ActiveWindow
        ActiveWindow = False
        sleep(0.2)
        parent.withdraw()
        mensaje = Toplevel(TestDrive)
        mensaje.title('Espere')
        mensaje.geometry('200x100')
        Label(mensaje, text = 'Espere, \n actualizando datos', font = nnFont).pack()
        def getBat():
            try:
                #    _____________________________________________
                #___/Calculo de bater[ia antes de cerra test drive
                response = (send("sense;",True))
                Answer = (response.split(';'))[0]
                if "blvl:" in Answer:
                    battery = int(Answer[5:])
                    data = autos.info[carro]
                    if battery < 10:
                        data[autos.iESTADO]="Descargado"
                    data[autos.iSENSORES] = response.split(';')[0]+","+response.split(';')[1]    
                    data.insert(0, carro)
                    autos.modificarAuto(*tuple(data))
                    
            except:
                print("error en lectura de bateria")
            mensaje.destroy()
            closeX(TestDrive, parent)
            myCar.stop()
        Thread(target=getBat).start()
        
        
    #    ______________________________________________________________________________________________________
    #___/ Variables y flags a ser utilizadas en el funcionamiento del test drive y coordinación de comandos      
    Speed = 0
    Moving,WPressed,APressed,SPressed,DPressed,ZPressed,XPressed,CPressed,FPressed,BlinkZ,BlinkC,SentBackON,SentBackOFF = (False,)*13
    FLight = True
    Blight = True
    ActiveWindow = True
    BlightCount = 0
    
    #    _______________________________________________
    #___/Definicion de elementos graficos de la ventana
    TestDrive= Toplevel()
    TestDrive.title("Test Drive")
    TestDrive.geometry("1280x720")
    TestDrive.resizable(width= NO, height= NO)
    #Se genera el canvas de la ventana de pruebas
    TestCanv= Canvas(TestDrive, width= 1280, height= 720,bg="black")
    TestCanv.place(x=0, y=0)
    #    _______________________________
    #___/Definición de fondos
    TestDrive.FondoDia = FondoDia = cargar_imagen("DAY.png")
    TestCanv.create_image(0,0,image=FondoDia, anchor = NW,tags = "dia", state = NORMAL)
    TestDrive.FondoNoche =FondoNoche = cargar_imagen("NIGHT.png")
    TestCanv.create_image(0,0,image= FondoNoche, anchor = NW, tags = "noche", state = HIDDEN)
    #    _______________________________
    #___/Definición de Llantas
    TestDrive.Twl = TopWheelL = cargar_imagen("TLWheel.png")
    TestCanv.create_image(860,240, image = TopWheelL, anchor = NW, tags = "tl", state = HIDDEN)
    TestCanv.create_image(932,242, image = TopWheelL, anchor = NW, tags = "tl", state = HIDDEN)

    TestDrive.Twr = TopWheelR = cargar_imagen("TopWheelRight.png")
    TestCanv.create_image(863,240, image = TopWheelR, anchor = NW, tags = "tr", state = HIDDEN)
    TestCanv.create_image(940,238, image = TopWheelR, anchor = NW, tags = "tr", state = HIDDEN)
    #    _______________________________
    #___/Imagen del carro
    TestDrive.Borde = Borde = cargar_imagen("Car1.png")
    TestCanv.create_image(825,200, image = Borde, anchor = NW,tags = ("fondo","día"))

    #    _______________________________
    #___/Definición de direccionales y luces frontales
    TestDrive.fl = FrontLight = cargar_imagen("FrontL.png")
    TestCanv.create_image(865,210, image = FrontLight, anchor = NW, tags = ("lights","front"), state = HIDDEN)
    TestCanv.create_image(930,210, image = FrontLight, anchor = NW, tags = ("lights","front"), state = HIDDEN)
    TestDrive.dirl = DirLight = cargar_imagen("EmL.png")
    TestCanv.create_image(840,250, image = DirLight, anchor = NW, tags = ("lights","left"), state = HIDDEN)
    TestCanv.create_image(930,250, image = DirLight, anchor = NW, tags = ("lights","right"), state = HIDDEN)

    #    _______________________________
    #___/Definición de indicadores de dirección
    TestCanv.dir0  = dir0 = cargar_imagen("Directo.png")
    TestCanv.create_image(635,180, image = dir0, anchor = NE, state = NORMAL)
    TestCanv.create_image(645,180, image = dir0, anchor = NW, state = NORMAL)
    TestCanv.dirI  = dirI = cargar_imagen("Izquierda.png")
    TestCanv.dirD  = dirD = cargar_imagen("Derecha.png")
    TestCanv.create_image(635,180, image = dirI, anchor = NE,tags = ("tl"), state = HIDDEN)
    TestCanv.create_image(645,180, image = dirD, anchor = NW,tags = ("tr"), state = HIDDEN)

    #    _______________________________
    #___/Definición de luz trasera
    TestDrive.bl = BackLight= cargar_imagen("BackL.png")
    TestCanv.create_image(855,385, image = BackLight, anchor = NW, tags = ("lights", "back"), state = HIDDEN)
    TestCanv.create_image(905,385, image = BackLight, anchor = NW, tags = ("lights", "back"), state = HIDDEN)
    #    _______________________________
    #___/Indicador de frenado y reversa
    TestDrive.revON = revON= cargar_imagen("Reversa.png")
    TestDrive.revOff = revOff= cargar_imagen("ReversaOff.png")
    TestCanv.create_image(925,600, image = revOff)
    TestCanv.create_image(925,600, image = revON, tags = ("lights", "back"), state = HIDDEN)
    
    #----------------------------------------- Información escuderia ---------------------------------------------------------------------------------
    TestCanv.create_text(120,70, text = "Escudería: Loui Vcker",font = ("Algency FB",18,'bold italic'),fill = "black",tags= "escu", anchor =NW)
    TestCanv.create_text(120,100, text = ("Marca Auto: "+autos.info[carro][0]),font = ("Algency FB",18,'bold italic'),fill = "black",tags= "escu", anchor =NW)
    TestCanv.create_text(120,130, text = ("Modelo Auto: "+autos.info[carro][1]),font = ("Algency FB",18,'bold italic'),fill = "black",tags= "escu", anchor =NW)
    TestCanv.create_text(600,70, text = ("Piloto: " + pilotos.info[pilotoIndex][pilotos.iNOM]),font = ("Algency FB",18,'bold italic'),fill = "black",tags= "escu", anchor =NW)
    TestCanv.create_text(600,100, text = ("Nacionalidad: "+ pilotos.info[pilotoIndex][pilotos.iPAIS]),font = ("Algency FB",18,'bold italic'),fill = "black",tags= "escu", anchor =NW)
    TestCanv.create_text(600,130, text = ("Test Drive 1.0 - Loui Vcker Racing Team"),font = ("Algency FB",18,'bold italic'),fill = "black",tags= "escu", anchor =NW)
    #-----------------------------------------
    
    #    _______________________________
    #___/Definición de indicador de PWM
    TestCanv.create_text(620,675, text = "PWM:0%", font= ("Algency FB",18,'bold italic'), fill = "black", tags = "pwm", anchor= NW)
    TestCanv.create_text(220,190, text = "%", font = ("Algency FB",18,'bold italic'), fill = "black", tags = "battext", anchor = NW)

    #carga de imagenes de acelerometro
    TestCanv.AOff = AOff = cargar_imagen('AOff.png')
    TestCanv.GrON = GrON = cargar_imagen('GrON.png')
    TestCanv.ReON = ReON = cargar_imagen('ReOn.png')

    #    ______________________________________
    #___/ Creacion de imágenes del acelerómetro
    for i in range(0, 6):
        TestCanv.create_image((520+i*57), 580, image = AOff)
    
    for i in range(0,3):
        #460, 590
        TestCanv.create_image((520+i*57), 580, image = ReON, tag =('Red'+str(2-i), 'redAcc'), state = HIDDEN)
        #Se debe programar la adición de las operaciones de la función aparte de generar la ventana
    for i in range(0,3):
        #460, 590
        TestCanv.create_image((691+i*57), 580, image = GrON, tag =('Green'+str(i), 'greenAcc'), state = HIDDEN)
        #Se debe programar la adición de las operaciones de la función aparte de generar la ventana
    def gradualOff(light):
        """
        Funcionamiento: apaga gradualmente luces rojas y verdes
        """
        nonlocal cntGreen, cntRed,SPressed, WPressed, Speed,ActiveWindow
        if light == 'GR':
            cntGreen = 0
            light = 'Green'
        elif light == 'RE':
            cntRed = 0
            light = 'Red'
   
        for i in range(0, 3):
            if not (SPressed or WPressed) and Speed!=0:
                sleep(1.7)
            else:
                sleep(0.07)
            if ActiveWindow:
                TestCanv.itemconfig((light+str(2-i)), state = HIDDEN)
                
    cntGreen = 0
    def gradualAccGreen():
        """
        Funcionamiento: Prende luces verdes de acelerómetro conforme se aplica pwm a avanzar
        """
        nonlocal WPressed,cntGreen
        while WPressed:
            cntGreen+=1
            sleep(0.004)
            if cntGreen == 100:
                TestCanv.itemconfig(('Green0'), state = NORMAL)
            elif cntGreen == 200:
                TestCanv.itemconfig(('Green0'), state = NORMAL)
                TestCanv.itemconfig(('Green1'), state = NORMAL)
            elif cntGreen == 300:
                TestCanv.itemconfig(('Green0'), state = NORMAL)
                TestCanv.itemconfig(('Green1'), state = NORMAL)
                TestCanv.itemconfig(('Green2'), state = NORMAL)

    cntRed = 0
    def gradualAccRed():
        """
        Funcionamiento: Prende luces rojas de acelerómetro conforme se aplica pwm a frenar o reversa
        """
        nonlocal SPressed,cntRed
        while SPressed:
            cntRed+=1
            sleep(0.004)
            if cntRed == 100:
                TestCanv.itemconfig(('Red0'), state = NORMAL)
            elif cntRed == 200:
                TestCanv.itemconfig(('Red0'), state = NORMAL)
                TestCanv.itemconfig(('Red1'), state = NORMAL)
            elif cntRed == 300:
                TestCanv.itemconfig(('Red0'), state = NORMAL)
                TestCanv.itemconfig(('Red1'), state = NORMAL)   
                TestCanv.itemconfig(('Red2'), state = NORMAL)
            
    #    _______________________________
    #___/Final de codigo de acelerometro        


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
        Entradas: el mensaje a enviarle al auto para que este lo procese como comando.
        Salidas: el comando a enviar por medio de la clase NodeMCU.
        Restricciones: Debe ser un comando válido de los que se incorporaron en la primera parte del proyecto.
        Funcionamiento: SE comunica con el hardware a través de la clase NodeMCU, utiliza el método send para hacerle llegar este comando,
            luego el método readById para obtener la respuesta del mismo.
        """
        if(len(Msg)>0 and Msg[-1] == ";"):
            response = myCar.send(Msg)
            if returnAns:
                sleep(4)
                return myCar.readById(response)
    #-----------------------------------------
    def check_sense():
        """
        Funcionamiento: envia repetidas veces el comando sense para tomar los datos de sensores del auto
        """
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
        """
        Entradas: La respuesta obtenida por el WiFiClient al enviar el comando sense;
        Salidas: un cambio en la interfaz gráfica para cuando la luz del ambiente cambie de intensidad.
        Restricciones: La entrada debe haber pasado por otras funciones que las procesen para trabajar con los índices correctamente
        Funcionamiento: Trabaja la cadena de entrada por medio de índices, valida el caracter que está en la posición -3, si este es un 0
        o un 1, cambia el fondo dependiendo de cual sea para dar alusión a la iluminación.
        """
        #Validar la posición del caracter en el que la LDR manda la variable light
        
        if Answer[-3] == "0":
            TestCanv.itemconfig("dia", state = HIDDEN) #Oculta los elementos con la etiqueta de día y muestra los de noche
            TestCanv.itemconfig("noche", state = NORMAL) #En estos casos son sólo los fondos.
        elif Answer[-3] == "1":
            TestCanv.itemconfig("dia", state = NORMAL)
            TestCanv.itemconfig("noche", state = HIDDEN)
        else:
            return

    def bateria(Answer):
        """
        Entradas:La respuesta obtenida por el WiFiClient al enviar el comando sense;
        Salidas: una configuración en pantalla de la lectura del sensor de batería, guardando este en una variable.
        Restricciones: La entrada (respuesta) debe haber sido tratada con otras funciones para que este comportamiento se lleve a cabo exitosamente.
        Funcionamiento: Valida el largo de la respuesta, ya que esta puede cambiar dependiendo de la cantidad de dígitos que se lean en el sensor, para
        cada caso válido, se configura un elemento con la etiqueta battext a que contenga el nuevo valor de la batería.
        """
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

        Entradas: el evento enviado por el binding asignado dentro de la ventana TEst Drive
        Salidas: variadas para cada evento, dependiendo de cada tecla.
        Restricciones: la entrada sólo puede ser un evento.
        """
        #Se solicita el valor de estas variables previamente asignados en la ventana Test Drive, para que todos los eventos se manejen
        #en sincronía  y se pueda utilizar estas variables para validar condiciones/ detener hilos de ejecución.
        nonlocal WPressed, APressed, SPressed, DPressed, ZPressed, XPressed, CPressed, FPressed, FLight, Blight, BlinkZ, BlinkC
        #Asigna los eventos a letras en el teclado
        Key = event.char
        if Key == "w":
            if not WPressed and not SPressed:
                WPressed = True
                ThreadForwards = Thread(target = gradual_front)
                sleep(0.2)
                ThreadForwards.start()
                Thread(target=gradualAccGreen, args=()).start()
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
                Thread(target=gradualAccRed, args=()).start()
                #Hilo que controla la reversa/ detención del auto
            else:
                return
        elif Key == "a":
            if not APressed and not DPressed:
                send("dir:-1;")
                APressed = True
                #código para activar o desactivar las imágenes que dan feedback de giro en la interfaz de usuario.
                TestCanv.itemconfig("tl", state = NORMAL)
                #tl representa los elementos que se crearon para el caso "turn left".
            else:
                return
        elif Key == "d":
            if not DPressed and not APressed:
                send("dir:1;")
                DPressed = True
                #Se configuran los elementos que deben activarse al girar a la derecha para que se muestren en pantalla.
                TestCanv.itemconfig("tr", state = NORMAL)
            else:
                return
        elif Key == "z":
            if not ZPressed and not CPressed:
                ZPressed = True
                if BlinkZ:
                    return
                else:
                    thread_blink("L") #Se invoca una función que utiliza este argumento para condicionar el inicio de un hilo.
            else:
                return
        elif Key == "x":
            if not XPressed and not(ZPressed or CPressed):
                XPressed = True
                BlinkZ = False
                BlinkC = False
                #Se pasan las variables de parpadeo en ambas direcciones a falso, pues esta tecla se utiliza para detener estos procesos
                TestCanv.itemconfig("left", state = HIDDEN)
                TestCanv.itemconfig("right", state = HIDDEN)
                #Se ocultan las imágenes de las direccionales en la interfaz.
            else:
                return
        elif Key == "c":
            if not CPressed and not ZPressed:
                CPressed = True
                if BlinkC:
                    return
                else:
                    thread_blink("R") #Se invoca una función que utiliza este argumento para condicionar el inicio de un hilo.
            else:
                return
        elif Key == "f":
            if not FPressed:
                #Inmediatamente se cambia la variable a True en el primer evento, para asi evitar que el sistema envíe todas las presiones de la tecla
                #Como eventos a la función, esta variable retorna a su estado de falso (abriendo la posibilidad de un nuevo evento) hasta que es liberada
                #Por el usuario.
                FPressed = True
                if FLight:
                    #Se utiliza esta variable y sus cambios con el objetivo de poder encender y apagar las frontales con la misma tecla. 
                    send("lf:1;")
                    FLight = False
                    TestCanv.itemconfig("front",state = NORMAL)
                else:
                    send("lf:0;")
                    FLight = True
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
        Restricciones: Es para iniciar un proceso, debe ser invocada sin argumentos, pues dentro de ella se solicitan las variables que
        necesita para operar normalmente.
        """
        #Nuevamente se invocan las variables declaradas al inicio de la ventana para controlar todos los eventos com más facilidad y al mismo tiempo.
        nonlocal Speed, Moving, WPressed, SPressed, SentBackOFF,SentBackON
        #Las últimas dos variables son para controlar el estado de las luces traseras.
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
                sleep(0.2)
                
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
        Restricciones: esta, al igual que la que controla el hilo de aceleración, debe ser invocada sin argumentos.
        """
        nonlocal Speed,Moving, SPressed, WPressed
        #Se invocan las variables fuera del espectro local de la función con el objetivo de ser capaz de detener su ejecución /validar que no se repita la función
        #Durante el mismo evento.
        SPressed = True
        while Speed > -400 and SPressed and not WPressed:
            if Speed==1023:
                Speed -= 23
                send("pwm:" + str(Speed) + ";")
                TestCanv.itemconfig("pwm", text = "PWM:" + str(Speed))
                sleep(0.01)
            elif Speed >= 500:
                send("pwm:" + str(Speed) + ";")
                Speed -= 100
                TestCanv.itemconfig("pwm", text = "PWM:" + str(Speed))
                sleep(0.3)
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
            sleep(0.4)
        
        TestCanv.itemconfig("pwm", text = "PWM:" + str(Speed))
        #-------------------------------------------
        
    def thread_blink(Direction):
        """
        Función que controla el parpadeo de las direccionales
        Entradas: la dirección en la que se quiere iniciar el parpadeo
        Restricciones: esta dirección sólo puede ser una L o una R mayúsculas dadas en string.
        """
        nonlocal ZPressed, CPressed, BlinkZ, BlinkC
        if ZPressed and not (CPressed or XPressed):
            BlinkZ = True
            #Se activa la variable de parpadeo a la izquierda (con tecla Z) y se activa el hilo
            ThreadBlink = Thread(target = blink_lights, args = [Direction, 0])
            ThreadBlink.start()
        elif CPressed and not (ZPressed or XPressed):
            BlinkC = True
            #se activa la variable de parpadeo a la derecha (con tecla C) y se activa el hilo.
            ThreadBlink = Thread(target = blink_lights, args = [Direction, 0])
            ThreadBlink.start()
        else:
            return
    #--------------------
        
    def blink_lights(Direction, Counter):
        """
        Función que automatiza el proceso de parpadeo en las luces direccionales.
        Entrdas: La dirección en la que se desea activar el parpadeo, y el contador que se utilizará como valor inicial
            para condicionar el comando que se envía al auto.
        Salidas: Configuracion de objetos en el canvas, y mensajes a la clase myCar o NodeMCU de WiFiClient.
        Restricciones: Sólo puede ser invocada por el hilo, de lo contrario esta funcionará sólo para un ciclo y no se podrá ejecutar otro
        proceso paralelamente a este.
        """
        nonlocal ZPressed, CPressed, XPressed, BlinkC, BlinkZ
        #En esta función el contador se utiliza para generar un residuo con 2 (dado que el módulo de dos sólo retorna dos elementos, 0 o 1.
        #Gracias a esto, es fácil controlar la activación y desactivacion de las luces.
        if Direction == "L":
            while BlinkZ and ActiveWindow:
                #Se define la variable LED como el módulo 2 del contador.
                LED = Counter%2
                send("ll:" + str(LED) + ";")
                #Se le envía al NodeMCU el comando de control para la direccional, el valor que determina si debe
                #Apagarlas o encenderlas se determina por el valor actual del contador en esta ejecución.
                if LED == 1:
                    #Se configuran los objetos en pantalla.
                    TestCanv.itemconfig("left", state = NORMAL)
                    #print("Left light is ON")
                    Counter += 1
                else:
                    #Se configuran los objetos en pantalla.
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
        """
        Función que controla el estado de las luces traseras a medida que se presiona la tecla S
        """
        #Se utilizan las variables de la ventana, fuera de tanto el puntero local de la función, como el global del programa.
        nonlocal Speed, SentBackON, SentBackOFF, SPressed
        #Este proceso se ejecutará siempre que la tecla S se esté presionando (ya que su variable cambia a falso sólo cuando esta se libera)
        while SPressed:
            if SentBackON: #Utiliza la variable para verificar si ya le envió a las luces traseras que debían encenderse, si ya lo hizo, se mantiene en espera.
                return
            else:
                send("lb:1;") #Si no le ha enviado a las luces que se enciendan, les envía el comando de encendido
                #print("SentBackON")
                TestCanv.itemconfig("back",state = NORMAL) #Configura los objetos en pantalla con la etiqueta dada para que se muestre el estado de las luces.
                SentBackON = True #Cambia la variable a verdadero porque acaba de encenderlas y sólo debe enviarse una vez por presion de la tecla.
                SentBackOFF = False
        #print("S released, exit press while")
    #-----------------------------------------                
    #Función WASD_Release que se activa con los eventos en los que se suelta una de las teclas especificadas:
    def WASD_Release(event):

        """
        Función que controla los eventos que se activarán al soltar teclas definidas
        """
        #Al igual que a la función que controla la presion de teclas, esta trabaja con eventos del teclado específicos (validados dentro de la funcion)
        nonlocal WPressed, APressed, SPressed, DPressed, ZPressed, XPressed, CPressed, FPressed
        Key = event.char
        #Se asigna el evento a una variable local Key
        #print(Key)

        #Cambiará cada variable a falso (para las que funcionan como indicador de que la tecla se está presionando)
        if Key == "w":
            WPressed = False
            Thread(target=gradualOff,args = ('GR',)).start() #Se invoca al hilo para retornar las luces de indicador aceleración a apagadas a medida que se desacelera
        elif Key == "s":
            SPressed = False
            ThreadBacklightsR = Thread(target = back_light_control_release)
            #Si se suelta la S, invoca a la funcion que controla el estado de las luces traseras si esta
            #Tecla no se está presionando
            ThreadBacklightsR.start()
            Thread(target=gradualOff,args = ('RE',)).start() #Invoca al hilo para retornar las luces de indicador de frenado a apagadas a medida que se acelera
        elif Key == "a":
            APressed = False
            send("dir:0;") #Se envía al carro que retorne a la dirección central
            TestCanv.itemconfig("tl", state = HIDDEN) #Se ocultan las ruedas delanteras en pantalla.
        elif Key == "d":
            DPressed = False
            send("dir:0;") #Se envía al carro que retorne a la dirección central
            TestCanv.itemconfig("tr", state = HIDDEN) #SE ocultan las ruedas delanteras en pantalla.
        elif Key == "z":
            ZPressed = False
        elif Key == "x":
            XPressed = False
        elif Key == "c":
            CPressed = False
        elif Key == "f":
            FPressed = False

    def back_light_control_release():
        """
        Funcionamiento: Controla el estado de las luces traseras cuando la S no se esté presionando (y la ventana siga activa)
        """
        #Se trabaja con las variables no-locales
        nonlocal SPressed, SentBackON, SentBackOFF, Speed, WPressed
        #print(SPressed)
        while not SPressed and ActiveWindow:
            while Speed >= 0: #Entra a esta condición si la potencia es positiva o igual que 0, pues aquí, si se libera la tecla S, debe apagar las lb.
                if SentBackOFF: #Verifica si ya envió las luces a un estado de apagado, esto con el objetivo de que el comando se envíe una vez cada repetición.
                    return
                else:
                    send("lb:0;") #Si no se había enviado el comando, envía que se apaguen las luces
                    #print("SentBackOFF")
                    TestCanv.itemconfig("back", state = HIDDEN) #Oculta los elementos en pantalla que corresponden a las luces
                    SentBackOFF = True #Cambia la variable a verdadero pues acaba de retornarlas a apagado.
                    SentBackON = False
            else:
                #Se entra a esta condición si la tecla no se está presionando, pero la potencia/pwm está en un valor negativo( en este caso debe permanecer encendida)
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
        """
        Funcionamiento: Ejcuta los comandos de la celebración del piloto
        """
        nonlocal celebracion
        for x in celebracion:
            send(x)
            sleep(0.7)
        final = ['pwm:0;','dir:0;','lf:0;','lb:0;','lr:0;','ll:0;']
        for x in final:
            send(x)
            sleep(0.2)
            
    def calcEficiencia():
        """
        Funcionamiento: envía dos comandos circle al carro, calcula la bateria antes y después, saca la diferencia, y la guarda como la eficiencia
        del auto
        """
        mensaje = Toplevel(TestDrive)
        mensaje.title('Espere')
        mensaje.geometry('200x100')
        Label(mensaje, text = 'Espere, \n actualizando datos', font = nnFont).pack()
        resultado = ""
        def calcBat():
            nonlocal resultado
            try:
                #    _______________________________
                #___/ Comandos y calculos de eficiencia
                #
                #Si alguna respuesta es un timeout, cancela el proceso
                response = (send("sense;",True))
                Answer = (response.split(';'))[0]
                BateriaInicial = 0
                if "blvl:" in Answer:
                    BateriaInicial= int(Answer[5:])
                else:
                    resultado = "error en recuperar información de batería, intente de nuevo"
                    endCalc()
                    return
                
                send("Circle:1;")
                Sleep(10)
                send("Circle:1;")
                Sleep(10)
                response = (send("sense;",True))
                Answer = (response.split(';'))[0]
                BateriaFinal= 0
                if "blvl:" in Answer:
                    BaterialFinal = int(Answer[5:])
                else:
                    resultado = "error en recuperar información de batería, intente de nuevo"
                    endCalc()
                    return
                
                data = autos.info[carro]
                nuevaEficiencia = BateriaInicial - BateriaFinal
                if (nuevaEficiencia) >=0: 
                    data[autos.iEFICIENCIA]=nuevaEficiencia 
                    data.insert(0, carro)
                    autos.modificarAuto(*tuple(data))
                    resultado = "Eficiencia guardad de: "+ str(nuevaEficiencia)
                    endCalc()
                    return
                else:
                    resultado = "error en recuperar información de batería, intente de nuevo"
                    endCalc()
                    return
            except:
                resultado = "error en recuperar información de batería, intente de nuevo"
                endCalc()
                return
            
        def endCalc():
            mensaje.destroy()
            messagebox.showinfo('Resultado', resultado)
            
        Thread(target = calcBat, args = ()).start()
        
        

    uBG = '#141414'
    txtBG = '#FAFAFA'
    #    _______________________________
    #___/Definición de botones

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
    Button(TestDrive, text="Celebración",font=nnFont, width=10,bg=uBG,fg = txtBG,bd=0,height =1,
           command=lambda: ejecutarCelebracion()).place(x=1125,y=445, anchor = CENTER)
    Button(TestDrive, text="Eficiencia",font=nnFont, width=10,bg=uBG,fg = txtBG,bd=0,height =1,
           command=lambda: calcEficiencia()).place(x=1125,y=485, anchor = CENTER)
    Button(TestDrive, text="Cerrar \n Test Drive",font=nnFont, width=10,bg=uBG,fg = txtBG,bd=0,height =3,
           command=lambda: closeTestDrive()).place(x=1125,y=600, anchor = CENTER)
##    
##    def cooords(event):
##        print('x',event.x,'y',event.y)
##    TestDrive.bind("<Button-1>",cooords)

    TestDrive.bind("<KeyPress>", WASD_Press) #Se le asigna el bind a la función WASD_Press().
    TestDrive.bind("<KeyRelease>",WASD_Release) #Este bind funciona de la misma forma pero opera opuesto al press.
    
    TestDrive.protocol("WM_DELETE_WINDOW", closeTestDrive)

            
#############################################################################################################################################################################
    
#############################################################################################################################################################################
    
#############################################################################################################################################################################





#__________________________________________               Sección de la tabla de posiciones            _____________________________________________________________________





        
#############################################################################################################################################################################
    
#############################################################################################################################################################################
    
#############################################################################################################################################################################


#-----Se termina la ventana de pruebas y se define la de los pilotos
def pilots_window(parent = Main):
    """
    Entradas:parent - ventana que la llama
    Funcionamiento: Ventana de muestra de datos de pilotos
    """
    global pilotos,autos, TTFont, nnFont
    DscRGP, DscREP, DscEficiencia = (False,)*3
    
    Pilots = Toplevel()
    Pilots.title("Pilots")
    Pilots.minsize(width= 1200, height= 800)
    Pilots.resizable(width= NO, height= NO)
    
    uFont = ('Helvetica', 14, 'bold italic')
    uBG = 'black'
    txtBG = '#FAFAFA'

    #    _________________________________________
    #___/Carga de elementos gráficos principales

    #otros elementos depende de las funciones definidas posteriormente
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
        """
        Entradas:param - indica el parámetro de orden de los pilotos
        Salidas: recarga la ventana con los pilotos reordenados
        Funcionamiento: Encuentra el orden actual de los pilotos, los ordena en orden contrario
        """
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
            #intenta cargar la foto del piloto, en caso de falla, evita crasheo usando un try except
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
        """
        Salidas: recarga la ventana con los autos ordenados por eficiencia
        Funcionamiento: Encuentra el orden actual de los autos, los ordena en orden contrario
        """
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
            #intenta cargar la imagen de un auto, si falla la ruta de la imagen, previene el crasheo usando un try except
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
    #-------------------------------------------------------------------------
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
    #definicion de columnas del treeview
    colsAut = ('Marca','Modelo','Origen','Tempo','Baterias','CPB','VoltPB','Estado','Consumo','Sensores','Peso','Eficiencia')
    listBoxAut = ttk.Treeview(C_Pil,columns=colsAut,height = 5)
    for col in colsAut:
        listBoxAut.heading(col, text=col)
    listBoxAut.heading('Eficiencia', command =lambda : cargarAutos())
    #define al ancho de los diferentes espacios en el treeview de autos
    for i in range(0, len(colsAut)):
        listBoxAut.column(colsAut[i], width =90, anchor ='c')
    listBoxAut.column('#0', width = 150, anchor = 'c')
    listBoxAut.column(colsAut[5], width = 50, anchor = 'c')
    listBoxAut.column(colsAut[6], width = 50, anchor = 'c')
    listBoxAut.column('Sensores', width = 110, anchor = 'c')
    listBoxAut.column('Estado', width = 100, anchor = 'c')
    
    listBoxAut.grid(row=5, column=1, columnspan=2)
    #-------------------------------------------------------------------------


   



    def agregarPiloto(parent = Pilots):
        """
        Entradas: parent  - ventana pariente
        Funcionamiento: Recibe los nuevos datos de un piloto a agregar, crea una celebración random, y lo integra dentro de la lista de pilotos
        cierra la ventana creada al enviar los datos
        """
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
            """
            Funcionamiento: Guarda los datos extraídos de la ventana creada por agregarPiloto
            """
            global pilotos
            nonlocal hojaTec, closeAP
            
            def createCeleb():
                #crea una celebración random
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
        """
        Entradas: piloto  - Información del item de treeview que conserva la información de un piloto, con su posición en la primer posición de la lista
        parent- ventana padre
        Funcionamiento: toma los datos del treeview de un piloto, permite modificarlos, los guarda al presionar el boton de guardado
        y se cierra al finalizar
        """
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
        #    ______________________________________________
        #___/obtiene los datos de los entries usando un for
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
        """
        Entradas: parent - ventana que lo llama
        Salidas: agregar auto a la lista autos.info
        Restricciones: datos deben ser permitidos segun las reglas de autos.info
        Funcionamiento: crea una ventana para ingresar los datos, al presionar agregar, agrega el auto y cierra la ventana
        para volver a la ventana padre
        """
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
        #    _______________________________
        #___/obtiene los datos de los entries usando un for
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
            global autos
            nonlocal hojaTec, closeAP
            
            newData = []
            for x in hojaTec:
                newData.append(x.get())
            #cambia la posicion de ruta de foto del final de la lista a la posicion definida segun las reglas de auto.info
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
        """
        Entradas: auto - lista de informacion de auto a modificar, pos  - posicion de auto en autos.info
        parent  - ventana padre
        Salidas: guardado de los datos modificados de un carro en autos.info
        Restricciones: Los datos de modificación deben ser validos según las reglas de autos.info
        Funcionamiento: Toma los datos del treeview del auto seleccionado, los muestra en entries
        de tkinter, permite modificarlos, y al preisonar guardar permite guardarlos
        """
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
        
    #    _________________________________________
    #___/ Definiciones de botones de Pilots window
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
    
    
    def refresh(event):
        cargarPilotos(pilotos.CURRENTORDER)
        cargarAutos()
        
    listBoxAut.bind("<Map>", refresh)
    Pilots.protocol("WM_DELETE_WINDOW", lambda : closeX(Pilots, Main))

#############################################################################################################################################################################
    
#############################################################################################################################################################################
    
#############################################################################################################################################################################






#    _______________________________
#___/definicion de botones de main    
  
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
