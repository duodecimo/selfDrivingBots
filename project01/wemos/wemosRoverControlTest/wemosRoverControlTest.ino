// headers
void foward();
void back();
void left();
void right();
void stopMove();
int value;

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
// obs.: oportunidade de igualar motore
int speedA = 500;
int speedB = 500;

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
 

}
 
void loop() {
 if(speedA < 1500) {
  speedA+=50;
  speedB+=50;
 }
 Serial.print("speedA : ");
 Serial.println(speedA);
 Serial.print("speedB : ");
 Serial.println(speedB);
 Serial.println("foward");
 foward();
 delay(5000);
 Serial.println("back");
 back();
 delay(5000);
 Serial.println("left");
 left();
 delay(5000);
 Serial.println("right");
 right();
 delay(5000);
 Serial.println("stop");
 stopMove();
 delay(5000);
}


// motor control

void foward() {
  //Gira o Motor A no sentido horario
  analogWrite(enA, speedA);// PWM possible range 0~900
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  //Gira o Motor B no sentido anti-horario
  analogWrite(enB, speedB);// PWM possible range 0~900
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  delay(50);
}

void back() {
  //Gira o Motor A no sentido anti-horario
  analogWrite(enA, speedA);// PWM possible range 0~900
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  //Gira o Motor B no sentido horario
  analogWrite(enB, speedB);// PWM possible range 0~900
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  delay(50);
}

void left() {
  //Gira o Motor A no sentido anti-horario
  analogWrite(enA, speedA);// PWM possible range 0~900
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  //Gira o Motor B no sentido anti-horario
  analogWrite(enB, speedB);// PWM possible range 0~900
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  delay(50);
}

void right() {
  //Gira o Motor A no sentido horario
  analogWrite(enA, speedA);// PWM possible range 0~900
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  //Gira o Motor B no sentido horario
  analogWrite(enB, speedB);// PWM possible range 0~900
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  delay(50);
}

void stopMove() {
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

