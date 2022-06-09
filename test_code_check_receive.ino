#include <SPI.h>

#define CAN_2515

const int SPI_CS_PIN = 9;
const int CAN_INT_PIN = 2;

#ifdef CAN_2515
#include "mcp2515_can.h"
mcp2515_can CAN(SPI_CS_PIN); // Set CS pin
#endif                           

void setup()
{
    Serial.begin(115200);

    while (CAN_OK != CAN.begin(CAN_125KBPS)) 
    {
        Serial.println("CAN init fail, retry...");
        delay(100);
    }
    Serial.println("CAN init ok!");
}

void loop()
{
    unsigned char len = 0;
    unsigned char buf[8];
    char bufByte[18] = {0};

    if (CAN_MSGAVAIL == CAN.checkReceive())
    {   
        CAN.readMsgBuf(&len, buf);

        unsigned long canId = CAN.getCanId();
        Serial.print("0x");
        Serial.print(canId, HEX);
        Serial.print(",");
        sprintf(bufByte, "%02X,%02X,%02X,%02X,%02X,%02X,%02X,%02X",buf[0],buf[1],buf[2],buf[3],buf[4],buf[5],buf[6],buf[7]);
        Serial.println(bufByte);
    }
}
