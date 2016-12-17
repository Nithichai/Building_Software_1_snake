#include <Adafruit_NeoPixel.h>

int w = 8;      // width of led
int h = 8;      // height of led
int wGame = 8;  // width of game
int hGame = 8;  // height of game
int data[16][8];// data table
int readState = 0, intoDisplay = 1, showState = 2 ; // state number
int state = showState;  // state
byte firstByte = 255;  // get firstByte data

int pinStrip = 6; // pin control led
int numPixel = w * h;  // number of pixel of led

int red = 1;  // color code
int green = 2;
int blue = 3;

int colorindex = red; // color index

Adafruit_NeoPixel pixels = Adafruit_NeoPixel(numPixel, pinStrip, NEO_GRB + NEO_KHZ800); // led setting

void setup() {
  Serial.begin(115200); // set baudrate of arduino
  pixels.begin();       // start led
  pixels.show();        // reset all pixel
}

void loop() {
  if (state == readState) {   // State that read data from serial
    Serial.println("readState");
    readFromGame();
  } else if (state == intoDisplay) {  // State that send data to led
    Serial.println("intoDisplay");
    showGame();
  } else if (state == showState) {  // State that show led and wait to received data
    Serial.println("showState");
    checkToRead();
  }

void readFromGame() {
  byte b = Serial.read();   // Read data
  char c = char(b);         // Set to char
  if (char(firstByte) == 'a') {   // Get apple data
    byte by = Serial.read();    // Read to get y data
    int x = int(b - 65) * w / wGame;  // set x from game to x of led
    int y = int(by - 65) * h / hGame; // set y from game to y of led
    data[y][x] = red;   // Set to red
    firstByte = 255;
  } else if (c == 's') {    // Get Snake
    byte bx = Serial.read();  // Get x
    byte by = Serial.read();  // Get y
    int x = int(bx - 65) * w / wGame;   // set x from game to x of led
    int y = int(by - 65) * h / hGame;   // set x from game to x of led
    data[y][x] = ++colorindex;  // Chnage color's index
  } else if (b != 255) {    // continue read snake pos
    byte by = Serial.read();    // get y
    int x = int(b - 65) * w / wGame;    // set x from game to x of led
    int y = int(by - 65) * h / hGame;   // set y from game to y of led
    data[y][x] = colorindex;    // Set color
  } else if (b == 255) {    // No data to recv => change state
    state = intoDisplay; 
  }
}

// Show data into led
void showGame() {
  for (int i = 0; i < h; i++) {
    for (int j = 0; j < w; j++) {
      Serial.print(data[i][j]);
      Serial.print(" ");
    }
    Serial.println();
  }
  Serial.println("---------");
  int index_led = 0;
  for (int i = 0; i < h; i++) {
    if (i % 2 == 0) {   // Even row
      for (int j = 0; j < w; j++) {
        if (data[i][w - j - 1] == red) {
          pixels.setPixelColor(index_led, pixels.Color(100, 0, 0));
        } else if (data[i][w - j - 1] == green) {
          pixels.setPixelColor(index_led, pixels.Color(0, 100, 0));
        } else if (data[i][w - j - 1] == blue) {
          pixels.setPixelColor(index_led, pixels.Color(0, 0, 100));
        } else {
          pixels.setPixelColor(index_led, pixels.Color(0, 0, 0));
        }
        index_led++;    // Go to next led
        if (index_led >= numPixel) {
          state = showState;  // Show complete => next state
        }
      }
    } else {    // Odd row
      for (int j = 0; j < w; j++) {
        if (data[i][j] == red) {
          pixels.setPixelColor(index_led, pixels.Color(100, 0, 0));
        } else if (data[i][j] == green) {
          pixels.setPixelColor(index_led, pixels.Color(0, 100, 0));
        } else if (data[i][j] == blue) {
          pixels.setPixelColor(index_led, pixels.Color(0, 0, 100));
        } else {
          pixels.setPixelColor(index_led, pixels.Color(0, 0, 0));
        }
        index_led++;    // Go to next led
        if (index_led >= numPixel) {
          state = showState;    // Show complete => next state
        }
      }

    }
    pixels.show();  // Show led
  }
}

// Wait to see 'a' (apple)
void checkToRead() {
  byte b = Serial.read();
  if (char(b) == 'a') {   
    state = readState;
    resetData();
    firstByte = b;
    colorindex = red;
  }
}

// Reset table
void resetData() {
  for (int i = 0; i < h; i++) {
    for (int j = 0; j < w; j++) {
      data[i][j] = 0;
    }
  }
}
