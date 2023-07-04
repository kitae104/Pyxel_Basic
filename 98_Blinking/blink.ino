void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
  while (!Serial) {
    ;
  }
}

int blk_on = 0;

void loop() {
  if (Serial.available() > 0)
  {
    String cmmd = Serial.readStringUntil('\n');
    Serial.println(cmmd);
    if (cmmd == "on")
    {
      blk_on = 1;
    }
    else if (cmmd == "off")
    {
      blk_on = 0;
    }    
  }
  if (blk_on ==1){
    digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
    delay(500);                       // wait for a second
    digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
    delay(500);     
  }
}