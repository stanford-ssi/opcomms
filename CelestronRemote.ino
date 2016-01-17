#define RX 2 // Receive pin
#define TX 3 // Transmit pin
#define EN_PIN 4
#define LED 13
#define BITTIME 45
#define POS '%' //37
#define NEG '$' //36
#define AZM 16
#define ALT 17
#define RIGHT NEG + (2*AZM) //68
#define LEFT POS + (2*AZM) //69
#define UP NEG + (2*ALT) //70
#define DOWN POS + (2*ALT) //71
#define BUFLEN 64
#define CHARBUFLEN 10
char msgBuf[BUFLEN];
unsigned char charBuf[CHARBUFLEN];


void setup(){
  Serial.begin(250000); // sets the baud rate

  // Set the mode of various pins (whether they read or write)
  pinMode(EN_PIN, OUTPUT);
  pinMode(TX, OUTPUT);
  pinMode(RX, INPUT_PULLUP);
  pinMode(LED, OUTPUT);

  digitalWrite(EN_PIN, HIGH);
  digitalWrite(TX, HIGH);
  digitalWrite(LED, LOW);

  delay(1000);

  // Move up for 2 seconds at speed 9
  celestronMoveCmd(UP,9);
  delay(2000);
  celestronStopCmd();
}

void loop(){ // run over and over
  // Move right for one second at speed 9.
  celestronMoveCmd(RIGHT,9);
  delay(1000);
  celestronStopCmd();


  celestronPosCmd(AZM);
  celestronPosCmd(AZM);
  celestronPosCmd(AZM);
  celestronPosCmd(AZM);
  celestronPosCmd(AZM);
  delay(3000);

  /*celestronMoveCmd(LEFT,9);
  delay(2000);
  celestronMoveCmd(LEFT,0);
  delay(1000);
  celestronMoveCmd(DOWN,9);
  delay(2000);
  celestronMoveCmd(DOWN,0);
  delay(1000);
  celestronMoveCmd(RIGHT,9);
  delay(2000);
  celestronMoveCmd(RIGHT,0);
  delay(1000);*/
}
void beginCmd(){
  pinMode(EN_PIN, OUTPUT);
  pinMode(TX, OUTPUT);
  digitalWrite(EN_PIN,LOW);
  digitalWrite(TX, HIGH);
}
void endCmd(){
  pinMode(EN_PIN, INPUT_PULLUP); //Hi-Z pin, but pull up
  pinMode(TX, INPUT_PULLUP); //Hi-Z pin, but pull up
}
void celestronWrite(char c){
  digitalWrite(TX, LOW);
  delayMicroseconds(BITTIME);
  for(int i = 0; i < 8; i++){
    digitalWrite(TX,c & 0b1); //Mask to set pin to value of LSB
    c = c >> 1; //Move to next LSB
    delayMicroseconds(BITTIME);
  }
  digitalWrite(TX, HIGH);
  delayMicroseconds(BITTIME);
}
void celestronMoveCmd(char dir, int spd){
  char axis = (dir - NEG) / 2; //convert direction to axis variable
  char realdir = dir - (2 *axis); //convert "direction" constant to actual value needed by Celestron
  unsigned char lastChar = 239 - (realdir + axis + spd);
  beginCmd();
  celestronWrite(';');
  celestronWrite(4);
  celestronWrite('\r');
  celestronWrite(axis);
  celestronWrite(realdir);
  celestronWrite(spd);
  celestronWrite(lastChar);
  endCmd();
}
void celestronPosCmd(char axis){
  unsigned char lastChar = 239 - axis;

  beginCmd();
  celestronWrite(';');
  celestronWrite(3);
  celestronWrite('\r');
  celestronWrite(axis);
  celestronWrite(1);
  celestronWrite(lastChar);
  endCmd();
  delayWhileReading(20);
}
void celestronStopCmd(){
  celestronMoveCmd(LEFT,0);
  celestronMoveCmd(UP,0);
  delay(500);
}
void delayWhileReading(long msToDelay){
  int bufIndex = 0;

  digitalWrite(LED, HIGH);
  unsigned long startTime = micros();

  bool incomingMsg = 0;
  bool lastState = 0;

  while(micros() - startTime < msToDelay * 1000){ //While time elapsed since start of function is less than prescribed time
    if(digitalRead(EN_PIN) == LOW){
      //digitalWrite(LED, LOW);
      incomingMsg = 1;
    }else{
      //digitalWrite(LED, HIGH);
      incomingMsg = 0;
    }
    if(incomingMsg){

    ////////////////////////////////////
      if(digitalRead(RX) != lastState){
        lastState = !lastState;
        bufIndex++;
      }
      if(bufIndex < BUFLEN){
        if(lastState) msgBuf[bufIndex] ++;
        else msgBuf[bufIndex] --;
        if((lastState && msgBuf[bufIndex] >= 100) || (msgBuf[bufIndex] <= -100)) bufIndex++;
      }
      ////////////////////////////////////
    }
    delayMicroseconds(11); //7 uSec with LEDs, 11 uSec without works pretty well
  }
  digitalWrite(LED, LOW);
  int N = -1;
  int c = 0;
  bool isActive = 0;
  unsigned char workingChar = 0;
  for(int i = 0; i < BUFLEN; i++){
    msgBuf[i] = msgBuf[i]/2;

    if(msgBuf[i] < 0){
      for(int j = msgBuf[i]; j < 0; j++){
        //Serial.print('0');
        if(!isActive){
          isActive = 1;
          //Serial.print('|');
        }
        N++;
        workingChar = workingChar >> 1;
        if(N == 8){ //Done building a character
          N = -1;
          charBuf[c] = workingChar;
          c++;
          isActive = 0;
        }
      }
    }else if(msgBuf[i] > 0){
      for(int j = 0; j < msgBuf[i]; j++){
        //Serial.print('1');
        if(isActive){
          N++;
          workingChar = (workingChar >> 1) | 0b10000000;
          if(N == 8){
            //Serial.println();
            N = -1;
            charBuf[c] = workingChar;
            c++;
            isActive = 0;
          }
        }
      }
    }
    //Serial.print('|');
    //Serial.print(msgBuf[i], DEC);
    //Serial.print(' ');
  }

  for(int i = 0; i < BUFLEN; i++){
    //Serial.print(msgBuf[i], DEC);
    //Serial.print(' ');
    msgBuf[i]=0; //Clear buffer
  }

  Serial.println();
  delay(5);
}

/* Function: celestronFindPosition()                                                        *
 * ---------------------------------------------------------------------------------------- *
 * Reads in the position data several times, and takes the most commonly occuring value for *
 * each character as the accurate value, and creates a long from the three of them.         *
 * ---------------------------------------------------------------------------------------- */
void celestronFindPosition(){

  // Ideally, we would use a Map to store the number of times a given value appears in position n,
  // but C does not have default support for this, and the code for a Map is long and complicated.
  // Instead, we use three 255-char arrays as a poor-man's Map, using the index of a cell as the
  // key, and the character stored as the value. 
  
  // C/C++ arrays also don't automatically 0 the memory addresses contained within thte array,
  // so we also need to call memset to 0 the values stored inside.
  
  unsigned char pos5[255];
  memset(pos5, 0, 255);
  unsigned char pos6[255];
  memset(pos6, 0, 255);
  unsigned char pos7[255];
  memset(pos7, 0, 255);

  // These three boolean variables track whether or not the given position has returned three consistent values;
  bool pos5Done = false;
  bool pos6Done = false;
  bool pos7Done = false;

  // Until all positions have been consistent three times, call celestronPosCmd to refill the
  // charBuf, and updates the map/boolean variables. 
  while(!pos5Done || !pos6Done || !pos7Done){
  	celestronPosCmd(AZM);

	unsigned char pos5Value = charBuf[5];
	unsigned char pos6Value = charBuf[6];
	unsigned char pos7Value = charBuf[7];

	pos5[pos5Value] += 1;
	pos6[pos6Value] += 1;
	pos7[pos7Value] += 1;

	if(!pos5Done) pos5Done = checkFoundEnough(pos5);
	if(!pos6Done) pos6Done = checkFoundEnough(pos6);
	if(!pos7Done) pos7Done = checkFoundEnough(pos7);

	printAndClearCharBuf();
  }

  // Pull out the most frequently occuring values from each position
  pos5Value = getMostFrequentValue(pos5);
  pos6Value = getMostFrequentValue(pos6);
  pos7Value = getMostFrequentValue(pos7);

  // Turn the three chars into a single long (4 byte integral type)
  long actualValue = 0 | (pos5 << 2*sizeof(char)) | (pos6 << sizeof(char)) | pos7;
  Serial.println(actualValue);
}

bool checkFoundEnough(unsigned char[] arr){
	for(int i = 0; i < 255; i++){
		if(arr[i] >= 3){
			return true;
		}
	}

	return false;
}

unsigned char getMostFrequentValue(unsigned char[] arr){
	unsigned char freq = 0;
	unsigned char value = 0;

	for(int i = 0; i < 255; i++){
		if(arr[i] > freq){
			freq = arr[i];
			value = i;
		}
	}

	return value;
}

void printAndClearCharBuf(){
  ///// Print and clear charBuf

  for(int i = 0; i < CHARBUFLEN; i++){
    Serial.print(charBuf[i], DEC);
    Serial.print('\t');
    charBuf[i] = 0; //Clear buffer
  }
  /////
}
