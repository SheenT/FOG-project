#include <Wire.h>
int mpu = 0x68;
int16_t AcX, AcY, AcZ, Tmp, GyX, GyY, GyZ;
int16_t peaks[5];
int16_t incoming[3];
  
  int sizePeaks = 0;
  int sizeIncoming = 0;
  int index = 0;
  int fogCount = 0;
  int normalCount = 0;

const int motorPin = 3;
const int speakerPin = 8;

bool isStart = true;
 
  
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Wire.begin();
  Wire.beginTransmission(mpu);
  Wire.write(0x6B);
  Wire.write(0);
  Wire.endTransmission(true);
  pinMode(motorPin, OUTPUT);
  

  
  
}

void loop() {
  // put your main code here, to run repeatedly:
  Wire.beginTransmission(mpu);
  Wire.write(0x3B);
  Wire.endTransmission(false);
  Wire.requestFrom(mpu,14,true);
  AcX = Wire.read()<<8|Wire.read();
  AcY = Wire.read()<<8|Wire.read();
  AcZ = Wire.read()<<8|Wire.read();
  Tmp = Wire.read()<<8|Wire.read();
  GyX = Wire.read()<<8|Wire.read();
  GyY = Wire.read()<<8|Wire.read();
  GyZ = Wire.read()<<8|Wire.read();

double nowTime = millis();
//  Serial.print(nowTime); Serial.print(","); Serial.print( " " );
//  Serial.print("AcX = "); Serial.print(AcX); Serial.print( " " );
//  Serial.print("AcY = "); Serial.print(AcY );Serial.print( " " );
//  Serial.print("AcZ = "); Serial.print(AcZ );Serial.print( " " );
//  Serial.print("Tmp = "); Serial.print(Tmp );Serial.print( " " );
//  Serial.print("GyX = "); Serial.print(GyX );Serial.print( " " );
//  Serial.print("GyY = "); Serial.print(GyY );Serial.print( " " );
//  Serial.print("GyZ = "); Serial.print(GyZ );Serial.print( " " );
//  Serial.println();

if(isStart == true){
  delay(2000);
  isStart = false;
}

UpdateIncoming(AcY);
FindandUpdatePeaks();
if(sizeIncoming > 1){
  int16_t diff = DifferenceFromLocalMax(incoming[1]); 
  if((-0.90*(incoming[1]) + 18000) < diff ){
    normalCount++;
    fogCount = 0;
    if(normalCount > 1){
     //do normal stuff (nothing)
     Serial.print("This is normal");
     Serial.print(incoming[0]);
    }
  }
  else{
    normalCount = 0;
    fogCount++;
    if(fogCount > 1){
      int currentTime = 0;
      while( currentTime < 1200){
         digitalWrite(motorPin, HIGH);
         tone(speakerPin, 900, 40);
  
         delay(600);
  
         digitalWrite(motorPin, LOW);
         tone(speakerPin, 900, 40);
         delay(600);
         Serial.print("This is FOG");
         Serial.print(fogCount);

        currentTime = currentTime + 1200;
      }
    }
  }
}


delay(50);
 
}

void UpdateIncoming(int16_t currentAccel){
  if(sizeIncoming < 3){
    incoming[sizeIncoming] = currentAccel;
    sizeIncoming++;
   }
   else{
    incoming[0] = incoming[1];
    incoming[1] = incoming[2];
    incoming[2] = currentAccel;
   }
}
void FindandUpdatePeaks(){
  if(sizeIncoming < 3){
    return;
  }
  else if(incoming[1] > incoming[2] && incoming[1] > incoming[0]){
    if(sizePeaks < 5){
      peaks[sizePeaks] = incoming[1];
      sizePeaks++;
    }
    else{

      for(int i = 0; i < sizePeaks-1; i++){
        peaks[i] = peaks[i+1];
        }
      peaks[sizePeaks - 1] = incoming[1];
     }
      
   }
}
int16_t DifferenceFromLocalMax(int16_t currentAccel){
  if(sizePeaks == 0)
  {
    return 0;
  }
  else{
    int16_t localMax = 0;
    for(int i = 0; i < sizePeaks; i++){
       if(peaks[i] > localMax){
        localMax = peaks[i];
       }
    }
    return localMax - currentAccel;
   
  }
}
