#include <Keyboard.h>;

const int swSize = 4;           // Switch's data array size
const int analogDataSize = 2;   // Size array joystick pin array and

const int swPin[swSize] = {3, 2, 4, 5};            // Switch pin
const int joyPin[analogDataSize] = {A0, A1};       // Joystick pin

int prevState[swSize] = {HIGH, HIGH, HIGH, HIGH};    // Previous state of switch
int currState[swSize] = {HIGH, HIGH, HIGH, HIGH};    // Current state of switch
const int keyboardState[swSize] = {'c', 'x', 'x', ' '};   // Switch to Button state array
unsigned long lastDebonceTime[swSize];   // Save time of debounce after pressed
unsigned long debounceDelay = 10;   // Delay debounce


unsigned long analogData[analogDataSize];    // Save joystick value
int minJoyX = 360, maxJoyX = 660;   // Min and max value of x from +5v (10 bit)
int minJoyY = 360, maxJoyY = 640;   // Min and max value of y from +5v (10 bit)
boolean joyUsed = false;            // State of joystick

// Setup
void setup() {
  Keyboard.begin();   // Start keyboard serial
  for (int i = 0; i < swSize; i++) {   // Setup switch pins
    pinMode(swPin[i], INPUT);
  }
}

// Loop
void loop() {
  readSWData(swSize - 1);   // Read switch
  readJoyData(analogDataSize - 1);    // Read joystick
}

// Read data from joystick
void readSWData(int index) {
  if (index < 0 || index >= swSize) return;   // Return when index < 0 or index >= switch array size(4)
  int readSW = digitalRead(swPin[index]);     // Read data from switch
  if (readSW != prevState[index]) {           // Data that is read != data from previous state
    lastDebonceTime[index] = millis();        // Start count debounce time
  }
  if (delayDebounce(index)) {   // Time that is counted is time up
    if (readSW != currState[index]) {   // current state from array != data that is read
      currState[index] = readSW;    // save data to current state
      if (currState[index] == LOW) {  // state is low
        Keyboard.press(keyboardState[index]);   // press key from keyboardState array and released
        Keyboard.releaseAll();
      }
    }
  }
  prevState[index] = readSW;    // save previous state from switch
  readSWData(index - 1);        // next switch
}

// check lastDebonceTime
int delayDebounce(int index) {
  if (millis() - lastDebonceTime[index] >= debounceDelay) // time up return true return false otherwise
    return true;
  return false;
}

// read data from joystick
void readJoyData(int index) {
  if (index < 0 || index >= analogDataSize) return;   // Return when index < 0 or index >= joystick's data array size(2)
  analogData[index] = analogRead(joyPin[index]);      // Read data from joystick
  if (!joyUsed) {   // not used mode
    if (index == 0 && analogData[0] < (minJoyX + maxJoyX) / 2 - (maxJoyX - minJoyX) / 3 &&    // Left
        analogData[1] > (minJoyY + maxJoyY) / 2 - (maxJoyY - minJoyY) / 8 &&
        analogData[1] < (minJoyY + maxJoyY) / 2 + (maxJoyY - minJoyY) / 8 ) {
      Keyboard.press(KEY_LEFT_ARROW);     // Use <-- and released
      Keyboard.releaseAll();
      joyUsed = true;   // Change state
    } else if (index == 0 && analogData[0] > (minJoyX + maxJoyX) / 2 + (maxJoyX - minJoyX) / 3 &&   // Right
               analogData[1] > (minJoyY + maxJoyY) / 2 - (maxJoyY - minJoyY) / 8 &&
               analogData[1] < (minJoyY + maxJoyY) / 2 + (maxJoyY - minJoyY) / 8 ) {
      Keyboard.press(KEY_RIGHT_ARROW);    // Use --> and released
      Keyboard.releaseAll();
      joyUsed = true;   // Change state
    } else if (index == 1 && analogData[1] > (minJoyY + maxJoyY) / 2 + (maxJoyY - minJoyY) / 3 &&   // Up
               analogData[0] > (minJoyX + maxJoyX) / 2 - (maxJoyX - minJoyX) / 8 &&
               analogData[0] < (minJoyX + maxJoyX) / 2 + (maxJoyX - minJoyX) / 8 ) {
      Keyboard.press(KEY_UP_ARROW);   // Use ^ and released
      Keyboard.releaseAll();
      joyUsed = true;   // Change state
    } else if (index == 1 && analogData[1] < (minJoyY + maxJoyY) / 2 - (maxJoyY - minJoyY) / 3 &&   // Down
               analogData[0] > (minJoyX + maxJoyX) / 2 - (maxJoyX - minJoyX) / 8 &&
               analogData[0] < (minJoyX + maxJoyX) / 2 + (maxJoyX - minJoyX) / 8 ) {
      Keyboard.press(KEY_DOWN_ARROW);   // Use v and released
      Keyboard.releaseAll();
      joyUsed = true;   // Change state
    }
  } if (analogData[0] > (minJoyX + maxJoyX) / 2 - (maxJoyX - minJoyX) / 3 &&
        analogData[0] < (minJoyX + maxJoyX) / 2 + (maxJoyX - minJoyX) / 3 &&
        analogData[1] > (minJoyY + maxJoyY) / 2 - (maxJoyY - minJoyY) / 3 &&
        analogData[1] < (minJoyY + maxJoyY) / 2 + (maxJoyY - minJoyY) / 3 &&    // Release joystick and in use
        joyUsed) {
    joyUsed = false;    // Change state joystick
  }
  readJoyData(index - 1);   // Read next coordinate
}
