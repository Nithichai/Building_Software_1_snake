#include <Adafruit_NeoPixel.h>

int w = 8;
int h = 8;
int wGame = 8;
int hGame = 8;
int data[16][8];
int readState = 0, intoDisplay = 1, showState = 2 ;
int state = showState;
byte firstByte = 255;

int pinStrip = 6;
int numPixel = w * h;

int red = 1;
int green = 2;
int blue = 3;

int colorindex = red;

Adafruit_NeoPixel pixels = Adafruit_NeoPixel(numPixel, pinStrip, NEO_GRB + NEO_KHZ800);

void setup() {
  Serial.begin(115200);
  pixels.begin();
  pixels.show();
}

void loop() {
  if (state == readState) {
    Serial.println("readState");
    readFromGame();
  } else if (state == intoDisplay) {
    Serial.println("intoDisplay");
    showGame();
  } else if (state == showState) {
    Serial.println("showState");
    checkToRead();
  }
  /*byte b = Serial.read();
    if(char(b) == 'a' || char(b) == 's') {
    Serial.println(char(b));
    } else {
    Serial.println(b-65);
    }*/
}

void readFromGame() {
  byte b = Serial.read();
  char c = char(b);
  if (char(firstByte) == 'a') {
    byte by = Serial.read();
    int x = int(b - 65) * w / wGame;
    int y = int(by - 65) * h / hGame;
    data[y][x] = red;
    firstByte = 255;
  } else if (c == 's') {
    byte bx = Serial.read();
    byte by = Serial.read();
    int x = int(bx - 65) * w / wGame;
    int y = int(by - 65) * h / hGame;
    data[y][x] = ++colorindex;
  } else if (b != 255) {
    byte by = Serial.read();
    int x = int(b - 65) * w / wGame;
    int y = int(by - 65) * h / hGame;
    data[y][x] = colorindex;
  } else if (b == 255) {
    state = intoDisplay;
  }
}

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
    if (i % 2 == 0) {
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
        index_led++;
        if (index_led >= numPixel) {
          state = showState;
        }
      }
    } else {
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
        index_led++;
        if (index_led >= numPixel) {
          state = showState;
        }
      }

    }
    pixels.show();
  }
}

void checkToRead() {
  byte b = Serial.read();
  if (char(b) == 'a') {
    state = readState;
    resetData();
    firstByte = b;
    colorindex = red;
  }
}

void resetData() {
  for (int i = 0; i < h; i++) {
    for (int j = 0; j < w; j++) {
      data[i][j] = 0;
    }
  }
}
