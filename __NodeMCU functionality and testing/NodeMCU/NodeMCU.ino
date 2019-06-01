/*
 * Instituto Tecnologico de Costa Rica
 * Computer Engineering
 * Taller de Programacion
 * País de Origen: Costa Rica
 * 
 * Código Servidor
 * Implementación del servidor NodeMCU
 * Proyecto 2, semestre 1
 * 2019
 * 
 * Version 2.0
 * Version de Arduino utilizada: 1.8.9
 * 
 * Profesor: Milton Villegas Lemus
 * Autor: Santiago Gamboa Ramirez
 * Editores: José Fernando Morales Vargas
 *           Alejandro José Quesada Calderón
 * 
 * Restricciónes: Biblioteca ESP8266WiFi instalada
 */

 /*
 Agregadas las funcionalidades de:
 Luces: lf,lb,ll,lr
 Movimiento de motores: pwm[-1023, 1023], dir[-1,0,1]
 sensores: sense
 diagnóstico: diag
 Movimientos partciulares: ZigZag, Infinite, Especial, Circle[-1,1]
 */
 
#include <ESP8266WiFi.h>

//Cantidad maxima de clientes es 1
#define MAX_SRV_CLIENTS 1
//Puerto por el que escucha el servidor
#define PORT 7070

/*
 * ssid: Nombre de la Red a la que se va a conectar el Arduino
 * password: Contraseña de la red
 * 
 * Este servidor no funciona correctamente en las redes del TEC,
 * se recomienda crear un hotspot con el celular
 */
 
const char* ssid = "NodeMCU";
const char* password = "12345678";
 
// servidor con el puerto y variable con la maxima cantidad de 

WiFiServer server(PORT);
WiFiClient serverClients[MAX_SRV_CLIENTS];

/*
 * Intervalo de tiempo que se espera para comprobar que haya un nuevo mensaje
 */
unsigned long previousMillis = 0, temp = 0;
const long interval = 100;

/*
 * Pin donde está conectado el sensor de luz
 * Señal digital, lee 1 si hay luz y 0 si no hay.
 */
#define ldr D8
/**
 * Variables para manejar las luces con el registro de corrimiento.
 * Utilizan una función propia de Arduino llamada shiftOut.
 * shiftOut(ab,clk,LSBFIRST,data), la función recibe 2 pines, el orden de los bits 
 * y un dato de 8 bits.
 * El registro de corrimiento tiene 8 salidas, desde QA a QH. Nosotros usamos 6 de las 8 salidas
 * Ejemplos al enviar data: 
 * data = B00000000 -> todas encendidas
 * data = B11111111 -> todas apagadas
 * data = B00001111 -> depende de LSBFIRST o MSBFIRST la mitad encendida y la otra mitad apagada
 */
#define ab  D6 
#define clk D7
//byte data = 0b11111111;

/*
 * Variables para controlar los motores.
 * EnA y EnB son los que habilitan las salidas del driver.
 * 
 * EnA = 0 o EnB = 0 -> free run (No importa que haya en las entradas el motor no recibe potencia)
 * EnA = 0 -> Controla la potencia (Para regular la velocidad utilizar analogWrite(EnA,valor), 
 * con valor [0-1023])
 * EnB = 0 -> Controla la dirección, poner en 0 para avanzar directo.
 * In1 e In2 son inputs de driver, controlan el giro del motor de potencia
 * In1 = 0 ∧ In2 = 1 -> Moverse hacia adelante
 * In1 = 1 ∧ In2 = 0 -> Moverse en reversa
 * In3 e In4 son inputs de driver, controlan la dirección del carro
 * In3 = 0 ∧ In4 = 1 -> Gira hacia la izquierda
 * In3 = 1 ∧ In4 = 0 -> Gira hacia la derecha
 */
#define EnA D4  
#define In1 D3// D4 en HIGH : retroceder
#define In2 D2 // D3 en HIGH : avanzar
#define In3 D1 // 
#define EnB D5 // 
#define In4 D0 // 0 para ir hacia adelante

byte data = 0b11111111;

/**
 * Función de configuración.
 * Se ejecuta la primera vez que el módulo se enciende.
 * Si no puede conectarse a la red especificada entra en un ciclo infinito 
 * hasta ser reestablecido y volver a llamar a la función de setup.
 * La velocidad de comunicación serial es de 115200 baudios, tenga presente
 * el valor para el monitor serial.
 */
void setup() {
  Serial.begin(115200);
  pinMode(In1,OUTPUT);
  pinMode(In2,OUTPUT);
  pinMode(In3,OUTPUT);
  pinMode(In4,OUTPUT);
  pinMode(EnA,OUTPUT);
  pinMode(EnB,OUTPUT);
  pinMode(clk,OUTPUT);
  pinMode(ab,OUTPUT);
  
  pinMode(ldr,INPUT);

  // ip estática para el servidor
  /*
  IPAddress ip(192,168,43,200);
  IPAddress gateway(192,168,43,1);
  */
  IPAddress ip(192,168,43,200);
  IPAddress gateway(192,168,43,1);
  IPAddress subnet(255,255,255,0);

  WiFi.config(ip, gateway, subnet);

  // Modo para conectarse a la red
  WiFi.mode(WIFI_STA);
  // Intenta conectar a la red
  WiFi.begin(ssid, password);
  
  uint8_t i = 0;
  while (WiFi.status() != WL_CONNECTED && i++ < 20) delay(500);
  if (i == 21) {
    Serial.print("\nCould not connect to: "); Serial.println(ssid);
    while (1) delay(500);
  } else {
    Serial.println("\nIt´s connected");
  }
  server.begin();
  server.setNoDelay(true);

  //Inicialización del carro:
  shiftOut(ab, clk, LSBFIRST, data);
}

/*
 * Función principal que llama a las otras funciones y recibe los mensajes del cliente
 * Esta función comprueba que haya un nuevo mensaje y llama a la función de procesar
 * para interpretar el mensaje recibido.
 */
void loop() {
  
  unsigned long currentMillis = millis();
  uint8_t i;
  //check if there are any new clients
  if (server.hasClient()) {
    for (i = 0; i < MAX_SRV_CLIENTS; i++) {
      //find free/disconnected spot
      if (!serverClients[i] || !serverClients[i].connected()) {
        if (serverClients[i]) serverClients[i].stop();
        serverClients[i] = server.available();
        continue;
      }
    }
    //no free/disconnected spot so reject
    WiFiClient serverClient = server.available();
    serverClient.stop();
  }

  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    for (i = 0; i < MAX_SRV_CLIENTS; i++) {
      // El cliente existe y está conectado
      if (serverClients[i] && serverClients[i].connected()) {
        // El cliente tiene un nuevo mensaje
        if(serverClients[i].available()){
          // Leemos el cliente hasta el caracter '\r'
          String mensaje = serverClients[i].readStringUntil('\r');
          // Eliminamos el mensaje leído.
          serverClients[i].flush();
          
          // Preparamos la respuesta para el cliente
          String respuesta; 
          procesar(mensaje, &respuesta);
          Serial.println(mensaje);
          // Escribimos la respuesta al cliente.
          serverClients[i].println(respuesta);
        }  
        serverClients[i].stop();
      }
    }
  }

}


/*
 * Función para dividir los comandos en pares llave, valor
 * para ser interpretados y ejecutados por el Carro
 * Un mensaje puede tener una lista de comandos separados por ;
 * Se analiza cada comando por separado.
 * Esta función es semejante a string.split(char) de python
 * 
 */
void procesar(String input, String * output){
  //Buscamos el delimitador ;
  Serial.println("Checking input....... ");
  int comienzo = 0, delComa, del2puntos;
  bool result = false;
  delComa = input.indexOf(';',comienzo);
  
  while(delComa>0){
    String comando = input.substring(comienzo, delComa);
    Serial.print("Processing comando: ");
    Serial.println(comando);
    del2puntos = comando.indexOf(':');
    /*
    * Si el comando tiene ':', es decir tiene un valor
    * se llama a la función exe 
    */
    if(del2puntos>0){
        String llave = comando.substring(0,del2puntos);
        String valor = comando.substring(del2puntos+1);

        Serial.print("(llave, valor) = ");
        Serial.print(llave);
        Serial.println(valor);
        //Una vez separado en llave valor 
        *output = implementar(llave,valor); 
    }
    /*
    * Si el comando no recibe sobrecargas, chequea si es alguno de los comandos que no la necesitan
    * a output se le asigna lo que retornen las funciones llamadas, puesto que las mismas indican si hubo un error o no
    */
    else if(comando == "sense"){
      *output = getSense();         
    }
    else if(comando == "ZigZag"){
      *output = ZigZag();         
    }
    else if(comando == "Infinite"){
      *output = infinite();         
    }
    else if(comando == "Especial"){
      *output = especial();         
    }
    else if(comando == "diag"){
      *output = diagnostic();         
    }
    comienzo = delComa+1;
    delComa = input.indexOf(';',comienzo);
  }
}

String implementar(String llave, String valor){
  /**
   * La variable result puede cambiar para beneficio del desarrollador
   * Si desea obtener más información al ejecutar un comando.
   */
  String result="ok;";
  Serial.print("Comparing llave: ");
  Serial.println(llave);
  if(llave == "pwm"){
    Serial.print("Move....: ");
    Serial.println(valor);
    int valorEntero= valor.toInt();
    // esto convierte el valor de str a int para operarlo entre condiciones
    
    if (valorEntero == 0){
      //se inmoviliza el motor de traccion
      digitalWrite(EnA,LOW);
      //se envía un 0 a los pines del motor de dirección, porque deben regresar a su posicion original
      digitalWrite(In3,0);
      digitalWrite(In4,0);
      result="Motor frenado;";
    }
    else if (valorEntero>0 && valorEntero<=1023){
      analogWrite(EnA,valorEntero);
      digitalWrite(In1,1); 
      digitalWrite(In2,0);
      //result="Motor a hacia adelante a potencia: " + valor +";";
    }
    else if (valorEntero<0 && valorEntero>=-1023){
      analogWrite(EnA,abs(valorEntero));
      digitalWrite(In1,0);
      digitalWrite(In2,1);
      //result="Motor a hacia atrás a potencia: " + valor +";";
    }
    else{
      //Se le avisa al usuario que el valor ingresado fue incorrecto
      return "valor invalido. pwm debe ser menor o igual a 1023";
    }
  }
 
  else if(llave == "dir"){
    switch (valor.toInt()){
      case 1:
        Serial.println("Girando derecha");
        //# AGREGAR CÓDIGO PARA GIRAR DERECHA
        //tenemos que decirle a cada case que haga un analogWrite con la potencia máxima para darle tensión a la acción de girar.
        analogWrite(EnB,1023);
        //también va un digitalWrite con los valores respectivos de In3 e In4 que lo hacen girar a la derecha
        digitalWrite(In3,0); //acá se repite el problema de la llave "pwm", en la que Santi dio una instrucción pero el comportamiento esperado no fue el dado, por lo que se invirtió.
        digitalWrite(In4,1);
        result="Girando derecha;";
        
        break;
      case -1:
        Serial.println("Girando izquierda");
        //# AGREGAR CÓDIGO PARA GIRAR IZQUIERDA
        analogWrite(EnB,1023);
        digitalWrite(In3,1);
        digitalWrite(In4,0);
        result="Girando izquierda;";

        break;
        //default lo que hace es decirle al código cuál debería ser el valor en el que se da un else
       default:
       //Código para no girar
        Serial.println("directo");
        analogWrite(EnB,1023);
        digitalWrite(In3,0);
        digitalWrite(In4,0);
        delay(100);
        analogWrite(EnB,0);
        result="Curso directo";
        break;
    }
  }
  else if(llave[0] == 'l'){
    Serial.println("Cambiando Luces");
    Serial.print("valor luz: ");
    Serial.println(valor);
    
    //Recomendación utilizar operadores lógico de bit a bit (bitwise operators)
    switch (llave[1]){
      case 'f':
        Serial.println("Luces frontales");
        if (valor == "1"){
          data = data & 0b11110011;
          Serial.println(data);
          result="Luces frontales encendidas;";
        }
        else if (valor == "0"){
          data = data | 0b00001100;
          Serial.println(data);
          result = "Luces frontales apagadas;";
        }
        //# AGREGAR CÓDIGO PARA ENCENDER LUCES FRONTALES
        break;
      case 'b':
        Serial.println("Luces traseras");
        //# AGREGAR CÓDIGO PARA ENCENDER O APAGAR LUCES TRASERAS
        if (valor == "1"){
          data = data & 0b11001111;
          Serial.println(data);
          result="Luces traseras encendidas;";
        }
        else if (valor == "0"){
          data = data | 0b00110000;
          Serial.println(data);
          result = "Luces traseras apagadas;";
        }
        break;
      case 'l':
        Serial.println("Luces izquierda");
        //# AGREGAR CÓDIGO PARA ENCENDER O APAGAR DIRECCIONAL IZQUIERDA
        if (valor == "1"){
          data = data & 0b01111111;
          Serial.println(data);
          result = "Direccional izquierda encendida;";
        }
        else if (valor == "0"){
          data = data | 0b10000000;
          Serial.println(data);
          result = "Direccional izquierda apagada;";
        }
        break;
      case 'r':
        Serial.println("Luces derechas");
        //# AGREGAR PARA CÓDIGO PARA ENCENDER O APAGAR DIRECCIONAL DERECHA
        if (valor == "1"){
          data = data & 0b10111111;
          Serial.println(data);
          result = "Direccional derecha encendida;";
        }
        else if (valor == "0"){
          data = data | 0b01000000;
          Serial.println(data);
          result = "Direccional derecha apagada;";
        }
        break;
      /**
       * # AGREGAR CASOS CON EL FORMATO l[caracter]:valor;
       * SI SE DESEAN manejar otras salidas del registro de corrimiento
       */
      default:
        Serial.println("Ninguna de las anteriores");
        result = "no hay cambios;";
        break;
    }
    //data VARIABLE QUE DEFINE CUALES LUCES SE ENCIENDEN Y CUALES SE APAGAN
    //Serial.println(data);
    //shiftOut(ab, clk, MSBFIRST, data);
  }
  else if (llave == "Circle"){
    switch (valor.toInt()){
      case 1:
      {
       //En este caso se envían los datos necesarios para hacer que el carro gire a la derecha.
        //enviamos valor alto a "Enable B" para que tenga una tensión suficiente para mover las ruedas delanteras.
        int pot = 1023;
        girarDerecha(pot);
        //enviamos un valor al pin "Enable A" que sea suficiente para que empiece a mover el motor de tracción.
        avanzar(pot);
        //enviamos un delay al node para que cuando pase el tiempo especificado, ejecute una nueva secuencia de comandos.
        delay(12000);
        frenar();
        //detenemos el motor número 2.
        directo();
        result = "Circulo a la derecha;";
        break;
        }
      case -1:
      {
       //En este caso se envían los datos necesarios para hacer que el carro gire a la izquierda.
        int pot = 1023;
        girarIzquierda(pot);
        avanzar(pot);
        delay(12000);
        frenar();
        //detenemos el motor número 2.
        directo();
        result = "Circulo a la izquierda;";
        break;
    }
    default:
    {
            //gira a la derecha segun un valor numérico enviado
          int pot = 1023;
          girarDerecha(pot);
          avanzar(pot);
          int tiempo = valor.toInt();
          delay(tiempo);
          frenar();
          directo();
          result = "se dio vuelta por " +String(tiempo) + " milisegundos";
          break;
    }
    }
  }
  /**
   * El comando tiene el formato correcto pero no tiene sentido para el servidor
   */
  else{
    result = "Undefined key value: " + llave+";";
    Serial.println(result);
  }
  shiftOut(ab, clk, LSBFIRST, data);
  return result;
}

/**
 * Función para obtener los valores de telemetría del auto
 */
//Función que determina el valor de retorno del sensor LDR (específicamente):

/*String light(){
  //evaluamos el valor recibido en el pin ldr por el Node (por si se necesitara revisar en el monitor):
    int valorLDR = digitalRead(ldr);
    Serial.print("nivel de luz");
    Serial.println(valorLDR);
    //con estas líneas, podemos usar el monitor serie para ver la lectura del pin ldr.
    
    //vamos a evaluar los casos posibles del valor encontrado en el pin para definir el retorno de la función, que será usado en sprintf()
    if (valorLDR = 1){
      return "Baja";
    }
    else if (valorLDR = 0){
      return "Alta";
    }
}
*/

String getSense(){
  /*
   * Explicación de la variable batteryLvl:
   * La variable se define a partir del valor máximo obtenido en el PWM al medir baterías de 8.1V (carga/capacidad máxima): 1024.
   * Al definir este valor como el 100% de las baterías, podemos modelar una función lineal que modele el comportamiento de esta relación.
   * La función se define como y = 3.4x + 684
   * Este valor se obtuvo al definir dos puntos de la recta, uno el 100%= (100,1024) donde 100 es el porcentaje aproximado y 1024 es el valor reportado
   * El otro valor es (0,682), el cual se obtiene a partir de una regla de tres.
   * Gracias a estos dos puntos, se modela la función y podemos definir un rango.
   * La mayor lectura, 3.2V corresponde al 100%, la mlectura al estar las baterias en 1.4 es 2.7 (técnicamente descargadas)
   */
  int batteryLvl = round(((analogRead(A0) -682)/3.4));
  
  //definimos light como una función que retornará un string más arriba, pero por motivos de mantener el código más cercano a lo esperado, se cambió.
  
  //declaramos la variable light como dependiente del valor que recibe el pin D8 según la corriente que pasa por el LDR
  int light = digitalRead(ldr);
  Serial.println(light);
  String lightText = "";
  if (light == 0 ){ lightText="Poca luz"; }else{ lightText="Sitio iluminado"; }
  
  /*char sense [16];
  sprintf(sense, "blvl:%d;ldr:%d;", batteryLvl, light);*/
  String sense = "blvl:"+ String(batteryLvl) + " ldr:"+ String(light) + " - " + String(lightText); 
  Serial.print("Sensing: ");
  Serial.println(sense);
  return sense;
}
String ZigZag(){
  //Acá el comportamiento es un poco distinto, haremos que el auto recorra una línea recta por un corto periodo, seguido de un patrón de zigzag leve.
  //debemos darle la potencia a los motores para que tengan un movimiento inicial
  int pot = 1023;
  avanzar(pot);
  directo();
  delay(500);
  //Se utiliza un for para repetir el cambio de dirección 4 veces
  //previamente se confirm[o con el Asistente Santiago Gamboa que estaba permitido usar estas estructuras
  for(int i=0; i<4; i++){
      girarIzquierda(pot);
      delay(500);
      girarDerecha(pot);
      delay(500);
    }
  frenar();
  directo();
  String resul = "Ejecutando un ZigZag;";
  return resul;
}
String infinite(){
 //En este caso se envían los datos necesarios para hacer que el carro gire a la derecha.
 //enviamos valor alto a "Enable B" para que tenga una tensión suficiente para mover las ruedas delanteras.
 int pot = 1023;
 int potdir = 800;
 girarIzquierda(pot);
 delay(100);
 girarDerecha(potdir);
 //enviamos un valor al pin "Enable A" que sea suficiente para que empiece a mover el motor de tracción.
 avanzar(pot);
 //enviamos un delay al node para que cuando pase el tiempo especificado, ejecute una nueva secuencia de comandos.
 delay(12000);
 girarIzquierda(potdir);
 delay(12000);
 frenar();
 //detenemos el motor número 2.
 directo();
 String result;
 result = "Circulo a la derecha;";
 return result;
 }
 
String especial(){
  //en condiciones de energía óptima en los motores,hace que el carro invierta su dirección, es decir, ejecuta un movimiento que le permite ponerse de frente
  //en donde antes se encontraba su parte trasera
  int pot = 1023;
  //diferentes potencias entre direccion y traccion para evitar la interferencia al maximo
  int potdir = 800;
  girarIzquierda(potdir);
  avanzar(pot);
  delay(1500);
  girarDerecha(potdir);
  delay(1000);
  girarIzquierda(potdir);
  retroceder(pot);
  delay(2700);
  avanzar(pot);
  girarDerecha(potdir);
  delay(2800);
  girarIzquierda(potdir);
  delay(200);
  //luego de los movimintos detiene los motores
  frenar();
  directo();
  String resul = "movimiento especial";
  return resul; 
  
}

String diagnostic(){
  //Verifica que todos los sistemas del carro funcionen
  String resul;
  resul = getSense();
  int pot = 900;
  avanzar(pot);
  delay(1000);
  retroceder(pot);
  delay(1000);
  frenar();
  girarDerecha(pot);
  delay(1000);
  girarIzquierda(pot);
  delay(1000);
  directo();
  data = 0b01111111;
  shiftOut(ab, clk, LSBFIRST, data);
  delay(1000);
  data = 0b10111111;
  shiftOut(ab, clk, LSBFIRST, data);
  delay(1000);
  data = 0b11011111;
  shiftOut(ab, clk, LSBFIRST, data);
  delay(1000);
  data = 0b11101111;
  shiftOut(ab, clk, LSBFIRST, data);
  delay(1000);
  data = 0b11110111;
  shiftOut(ab, clk, LSBFIRST, data);
  delay(1000);
  data = 0b11111011;
  shiftOut(ab, clk, LSBFIRST, data);
  delay(1000);
  data = 0b11111111;
  shiftOut(ab, clk, LSBFIRST, data);
  return resul;
 
  
  
  }

/*
 * Funciones Generales v2.0
 * x es una variable que almacena el pwm con el que se va a ejcutar la accion
 * Estas funciones controlan los pines EnA y EnB, más los In 1, 2, 3 y 4 del L298N
 * Los pines EnA y EnB controlan potencia, mientras que los inputs controlan la polaridad.
 * In1 y 2 controlan polaridad del motor de traccion, mientras In3 y 4 controlan polaridad del motor de direccion
*/
void avanzar(int x){
  //mueve el motor de tracci[on hacia adelante
  analogWrite(EnA,x);
  digitalWrite(In1,1);
  digitalWrite(In2,0);
  }
void retroceder(int x){
  //mueve el motor de traccion hacia atras
  analogWrite(EnA,x);
  digitalWrite(In1,0); 
  digitalWrite(In2,1);
  }
void frenar(){
  //detiene el motor de traccion
  analogWrite(EnA,0);
  digitalWrite(In1,0); 
  digitalWrite(In2,0);
  }
void directo(){
  //rectifica y detiene el motor de direccion
  analogWrite(EnB,1023);
  digitalWrite(In3,0);
  digitalWrite(In4,0);
  delay(50);
  analogWrite(EnB,0);
  }
void girarDerecha(int x){
  //mueve el motor de direccion a la derecha
  analogWrite(EnB,1023);
  digitalWrite(In3,0);
  digitalWrite(In4,1);
  }
void girarIzquierda(int x){
  //mueve el motor de direccion a la izquierda
  analogWrite(EnB,1023);
  digitalWrite(In3,1);
  digitalWrite(In4,0);
  }
