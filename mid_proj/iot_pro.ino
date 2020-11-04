#include <LiquidCrystal.h>

Here we have used Hitachi-compatible LCDs HD44780 which can be controlled in two 
modes: 
4-bit or 8-bit. 
For displaying text on the screen, we can do most everything in 4-bit mode
 //The HD44780 

// lcd(rs, en, d4, d5, d6, d7);

LiquidCrystal lcd(12, 11, 5, 4, 3, 2);
#define t1 10
#define t2 9
#define t3 8
#define green 7
#define red 6
#define buzzer 13

/*
 The circuit:
 * LCD RS pin to digital pin 12
 * LCD Enable pin to digital pin 11
 * LCD D4 pin to digital pin 5
 * LCD D5 pin to digital pin 4
 * LCD D6 pin to digital pin 3
 * LCD D7 pin to digital pin 2
 * LCD R/W pin to ground
 * LCD VSS pin to ground
 * LCD VCC pin to 5V
 * 250K resistor:
 * ends to +5V and ground
 * wiper to LCD VO pin (pin 3)

This is what each of the 16 pins stand for:

1. Ground- This is the ground of the LCD.
2. VCC- It is for powring the LCD.
3. VO - Contrast adjustment Pin, Connecting a potentiometer to 
this can dim the lights to the adjusted level that we want it.

4. Register Select Pin(RS)- If RS=0, this is Command Mode. If RS=1, this is Data 
Mode
5. R/W Pin- If R/W=0, this is Write Mode.(Default) If R/W=1, this is Read Mode.Here we are using for diaplay purpose that's why it is set to GND port
6. Clock (Enable) Pin. If it enabled then the data will be pass through data ports.. The HD44780 is falling edge triggered.
7. Bit 0 (Not used in 4-bit operation)
8. Bit 1 (Not used in 4-bit operation)
9. Bit 2 (Not used in 4-bit operation)
10. Bit 3 (Not used in 4-bit operation)
For displaying text on the screen, we can do most everything in 4-bit mode
11. Bit 4
12. Bit 5
13. Bit 6
14. Bit 7
15. Backlight Anode (+)- This is where you place the positive DC voltage if you want the backlight to be powered. The nominal operating voltage for LED backlights is 5V at full brightness.
16. Backlight Cathode- This is where you connect the ground of the DC voltage for the LCD backlights.(-)


 The 4-bit mode requires seven I/O pins(4 data + 3 control RS+RW+EN) from the Arduino,

*/

/*
 PING sensor --> ultrasonic rangefinder and returns the
 distance to the closest object in range. To do this, it sends a pulse
 to the sensor to initiate a reading, then listens for a pulse
 to return.  The length of the returning pulse is proportional to
 the distance of the object from the sensor.
*/


/*
Serial.begin() - > This starts serial communication, so that the Arduino can send out commands through the USB connection.
				    Sets the data rate in bits per second (baud) for serial data transmission.
*/

int distanceThreshold = 300; // It is the threshhold from which we can estimate whether the car is available in parking slot or not 

void setup() 
{	
	lcd.begin(16,2); //LCD screen set for 16 cols and 2 rows
 	lcd.setCursor(0,0); // default cursor set
	// we have done usual setup for LEDs and Buzzer
	pinMode(green,OUTPUT);
	pinMode(red,OUTPUT);
	pinMode(buzzer,OUTPUT);
	Serial.begin(9600); //data transmission rate
}

long readDistance(int triggerPin, int echoPin)
{
	// This function will return duration from the sending of the ping
  	 // to the reception of its echo off of an object.
	   pinMode(triggerPin, OUTPUT); 
  // The sensor is actually triggered by a HIGH pulse of 2 or more microseconds.
  // but before that we have first Given a short LOW pulse beforehand to ensure a 
  // clean HIGH pulse:
	
	digitalWrite(triggerPin, LOW);
	delayMicroseconds(2);
	// Then we have given actual HIGH pulse 
	digitalWrite(triggerPin, HIGH);
	delayMicroseconds(10);
	digitalWrite(triggerPin, LOW);
	 // The same pin is used to read the signal from the 
	pinMode(echoPin, INPUT);
	return pulseIn(echoPin, HIGH);
}

void loop()
{
    // measure the ping time in cm
	float d1 = microsecondsToCentimeters(readDistance(t1, t1));
	float d2 = microsecondsToCentimeters(readDistance(t2, t2));
	float d3 = microsecondsToCentimeters(readDistance(t3, t3));
	// It is just for debugging purpose
	Serial.println("d1 = " + String(d1) + "cm");
	Serial.println("d2 = " + String(d2) + "cm");
	Serial.println("d3 = " + String(d3) + "cm");
  	// as we have seen above distance threshhold is set to 300 cm 
    // 3 slot comparison If all the slots will be free then all the distance would be greater than 300 
      if (d1>300 & d2>300 & d3>300)
      {
          lcd.setCursor(0,0);
          lcd.print("3 Slots Free");
          lcd.setCursor(0,1);
          lcd.print("Slot 1 2 3 Free");
          delay(1000);
      }
	// 2 slots comparison --> here any 2 of the slot will be free , we are just checking through all possible combinations
	else if((d1>300 & d2>300)|(d2>300 & d3>300)|(d3>300 & d1>300))
	{
		lcd.setCursor(0,0);
		lcd.print("2 Slots Free");
		lcd.setCursor(0,1);
		// More specific for display purpose 
		if(d1>300 & d2>300)
			lcd.print("Slot 1 & 2 Free");
		else if(d1>300 & d3>300)
			lcd.print("Slot 1 & 3 Free");
		else
			lcd.print("Slot 2 & 3 Free");
    
		delay(1000);
	}
    // No slots available here all will be occupied so, all the distances will be less than 300
	else if(d1<300 & d2<300 & d3<300)
	{
		lcd.setCursor(0,0);
		lcd.print("No Slot Free");
		lcd.setCursor(0,1);
		lcd.print("Parking is Full");
		
		delay(1000);
	}
   // single slot comparison If it won't gone to any of the above conditions then it will go to else part
   else 
	{
		lcd.setCursor(0,0);
		lcd.print("1 Slot Free");
		lcd.setCursor(0,1);
		// Individual checking 
		if(d1>300)
			lcd.print("Slot 1 is Free");
		else if (d2>300)
			lcd.print("Slot 2 is Free");
		else
			lcd.print("Slot 3 is Free");
  
		delay(1000);
	}

	// Second Objectice
	// Here we are checking if any of the car is placed less than 50 cm to the wall/ any object, then we are checking 
	// for which one the above conditions hold
	if(d1<50 || d2<50 || d3<50)
	{ 
        digitalWrite(green,LOW);
        lcd.clear();
        lcd.setCursor(0,0);
        // Turn on the RED LED if the car is too close:
		lcd.print("Do Park Proper");
		digitalWrite(red,HIGH);
		digitalWrite(buzzer,HIGH);
		delay(500);
        digitalWrite(red,LOW);
		digitalWrite(buzzer,LOW);
		delay(500);
      if(d1<50){
            lcd.setCursor(0,1); 
			lcd.print("Park Proper in 1");
        	Serial.println("In Slot 1");
       	    delay(500);
      }
      if (d2<50){
        	lcd.setCursor(0,1);
			lcd.print("Park Proper in 2");
        	Serial.println("In Slot 2");
        	delay(500);
      }
      if (d3<50){
        	lcd.setCursor(0,1);
			lcd.print("Park Proper in 3");
        	Serial.println("In Slot 3");
        	delay(500);
      }
	}  
	// and in else part we just turn on the GREEN LED if all goes Good 
	else
	{
      // Turn on the GREEN LED if all the cars are parked properly:
        lcd.clear();
		lcd.print("Parked Properly");
        delay(1000);
		digitalWrite(green,HIGH);
	} 
 	
  delay(500);
  lcd.clear();
  delay(200);
}

// Now Rahin will takeover for Scalabilty and future scope of this project.Thank you.

long microsecondsToCentimeters(long microseconds) {
  // The speed of sound is 340 m/s or 29 microseconds per centimeter.
  // The ping travels out and back, so to find the distance of the
  // object we take half of the distance travelled.
  // It is just distance speed formula
  return microseconds / 29 / 2;
}
