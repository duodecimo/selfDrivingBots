#include <ESP8266WiFi.h>

// headers
void foward();
void back();
void left();
void right();
void stop();

const char* ssid = "PKVIR12AB";
const char* password = "5852696300";
int value;
 
WiFiServer server(80);

// conexoes ponte H
// 12v -> fonte externa 5v corrente
// gnd -> wemos gnd
// 5v  -> wemos 5v

// wemos
// gnd -> fonte externa 5v gnd

//Definicoes pinos Arduino ligados a entrada da Ponte H
int enA = D3;
int IN1 = D4;
int IN2 = D5;
int IN3 = D6;
int IN4 = D7;
int enB = D8;

// definições de velocidade
// obs.: oportunidade de igualar motores
const int speedA = 312;
const int speedB = 400;

void setup()
{
  //Define os pinos como saida
  pinMode(enA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(enB, OUTPUT);

  Serial.begin(115200);
  delay(5000);
 
 
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
 
  // Connect to WiFi network
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
 
  WiFi.begin(ssid, password);
 
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
 
  // Start the server
  server.begin();
  Serial.println("Server started");
 
  // Print the IP address
  Serial.print("Use this URL : ");
  Serial.print("http://");
  Serial.print(WiFi.localIP());
  Serial.println("/");
 
}
 
void loop() {
  // Check if a client has connected
  WiFiClient client = server.available();
  if (!client) {
    return;
  }
 
  // Wait until the client sends some data
  Serial.println("new client");
  while(!client.available()){
    delay(1);
  }
 
  // Read the first line of the request
  String request = client.readStringUntil('\r');
  Serial.println(request);
  client.flush();
 
  // Match the request
 
  if (request.indexOf("/FOWARD") != -1) {
    value = 0;
    foward();
  } 
  if (request.indexOf("/BACK") != -1) {
    value = 1;
    back();
  } 
  if (request.indexOf("/LEFT") != -1) {
    value = 2;
    left();
  }
  if (request.indexOf("/RIGHT") != -1){
    value = 3;
    right();
  }
  if (request.indexOf("/STOP") != -1){
    value = 4;
    stop();
  }
 
 
 
  // Return the response
  client.println("HTTP/1.1 200 OK");
  client.println("Content-Type: text/html");
  client.println(""); //  do not forget this one
  client.println("<!DOCTYPE HTML>");
  client.println("<html>");
 
  client.print("Led pin is now: ");
 
  if(value == 0) {
    client.print("go Foward");  
  } else if(value == 1) {
    client.print("go Back");  
  } else if(value == 2) {
    client.print("go Left");  
  } else if(value == 3) {
    client.print("go Right");  
  } else if(value == 4) {
    client.print("stop");  
  }
  client.println("<br><br>");
  client.println("Click <a href=\"/FOWARD\">here</a> to go foward<br>");
  client.println("Click <a href=\"/BACK\">here</a> to go back<br>");
  client.println("Click <a href=\"/LEFT\">here</a> to go left<br>");
  client.println("Click <a href=\"/RIGHT\">here</a> to go right<br>");
  client.println("Click <a href=\"/STOP\">here</a> to stop<br>");
  client.println("</html>");
 
  delay(1);
  Serial.println("Client disconnected");
  Serial.println("");
 
}


// motor control

void foward() {
  //Gira o Motor A no sentido horario
  analogWrite(enA, speedA);// PWM possible range 0~900
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  //Gira o Motor B no sentido anti-horario
  analogWrite(enB, speedB);// PWM possible range 0~900
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  delay(50);
}

void back() {
  //Gira o Motor A no sentido anti-horario
  analogWrite(enA, speedA);// PWM possible range 0~900
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  //Gira o Motor B no sentido horario
  analogWrite(enB, speedB);// PWM possible range 0~900
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  delay(50);
}

void right() {
  //Gira o Motor A no sentido anti-horario
  analogWrite(enA, speedA);// PWM possible range 0~900
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  //Gira o Motor B no sentido anti-horario
  analogWrite(enB, speedB);// PWM possible range 0~900
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  delay(50);
}

void left() {
  //Gira o Motor A no sentido horario
  analogWrite(enA, speedA);// PWM possible range 0~900
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  //Gira o Motor B no sentido horario
  analogWrite(enB, speedB);// PWM possible range 0~900
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  delay(50);
}

void stop() {
  //para o Motor A
  analogWrite(enA, speedA);// PWM possible range 0~900
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, HIGH);
  //para o Motor B
  analogWrite(enB, speedB);// PWM possible range 0~900
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, HIGH);
  delay(50);
}

