#define sensorUmidade 8
#define leitura A0
#define rele 12
#define ledVM 5
#define ledAM 6
#define ledVD 7

bool leituraSensor;
bool leituraAnterior;

void setup() {

  //Inicia comunicação serial
  Serial.begin(9600);
  
  //Sensor
  pinMode(sensorUmidade, INPUT);

  //Atuador
  pinMode(rele, OUTPUT);
  
  //LEDs
  pinMode(ledVM, OUTPUT);
  pinMode(ledAM, OUTPUT);
  pinMode(ledVD, OUTPUT);
}

void loop() {

  leituraSensor = digitalRead(sensorUmidade);

  //Linha que envia os sinais do sensor via Serial para gravar no BD
  if (leituraSensor == HIGH) {
     //No estado seco
     digitalWrite(ledVM, HIGH);
     digitalWrite(ledVD, LOW);
  } else {
     //No estado úmido
     digitalWrite(ledVM, LOW);
     digitalWrite(ledVD, HIGH);
  }

  //Estado seco  
  if (leituraSensor && !leituraAnterior) {
     delay(5000);
     digitalWrite(ledVM, LOW);
     digitalWrite(ledAM, HIGH);

     while (digitalRead(sensorUmidade)) {
        //Linha que envia os sinais do sensor via Serial para gravar no BD
        Serial.println(analogRead(leitura)); 
        digitalWrite(rele, HIGH);
        delay(500);
        digitalWrite(rele, LOW);
        delay(10000);          
     }
     digitalWrite(ledAM, LOW);
  }
  leituraAnterior = leituraSensor;
}
