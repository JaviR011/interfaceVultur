//// Programa 1 lado Emisor ////


#include <RH_ASK.h>		// incluye libreria RadioHead.h
#include <SPI.h> 		// incluye libreria SPI necesaria por RadioHead.h
 
RH_ASK rf_driver;		// crea objeto para modulacion por ASK

void setup(){
    rf_driver.init();		// inicializa objeto con valores por defecto
    randomSeed(analogRead(0)); // Inicializa el generador de números aleatorios
}
 
void loop(){
    int numeroAleatorio = random(180); // Genera un número aleatorio entre 0 y 179
    float seno = sin(numeroAleatorio * PI / 180.0); // Calcula el seno del ángulo en radianes

    char msg[10];
    dtostrf(seno, 6, 2, msg); // Convierte el float a una cadena
    rf_driver.send((uint8_t *)msg, strlen(msg)); // Función para envío del mensaje
    rf_driver.waitPacketSent(); // Espera al envío correcto
    delay(1000); // Demora de 1 segundo entre envíos
}