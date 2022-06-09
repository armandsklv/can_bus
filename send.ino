#include <SPI.h>
#define CAN_2515
//Arduino parametri darbam ar CAN Bus Shield V2.0
const int SPI_CS_PIN = 9;
const int CAN_INT_PIN = 2;

#ifdef CAN_2515
#include "mcp2515_can.h"
mcp2515_can CAN(SPI_CS_PIN);
#endif
void setup()
  { //Virknes kopnes datu parraides atrums, bitos
    SERIAL_PORT_MONITOR.begin(115200);
    while(!Serial){};
    //Tiek uzstadits CAN kopnes datu parraides atrums
    // CAN_250KBPS - liela atruma CAN kopnei
    // CAN_125KBPS - Zema atruma CAN kopnei
    while (CAN_OK != CAN.begin(CAN_125KBPS))
    {
        SERIAL_PORT_MONITOR.println("Couldn't initialize CAN connection. Trying again...");
        delay(100);
    }
    SERIAL_PORT_MONITOR.println("CAN connection initialized!");
}
//masivs ar vertibam, kas tiks nosutitas CAN zina
unsigned char data_buf[8] = {0x80, 0x10, 0x00, 0x40, 0x35, 0x00, 0x00, 0x00};
void loop()
{   //sendMsgBuf parametri: CAN ID hex formata, 1 zinas veids - extended
    //8 - baitu daudzums zina, masivs ar CAN zinas vertibam
    CAN.sendMsgBuf(0x280142A, 1, 8, data_buf);
    delay(5000);
}
