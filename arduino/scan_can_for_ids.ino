#include <SPI.h>

#define CAN_2515

const int SPI_CS_PIN = 10;
const int CAN_INT_PIN = 2;

#ifdef CAN_2515
#include "mcp2515_can.h"
mcp2515_can CAN(SPI_CS_PIN); // Set CS pin
#endif                           

void setup()
{
    SERIAL_PORT_MONITOR.begin(115200);

    while (CAN_OK != CAN.begin(CAN_125KBPS))//Setting the CAN bus speed
    {
        SERIAL_PORT_MONITOR.println("CAN initialization failed, retrying...");
        delay(100);
    }
    SERIAL_PORT_MONITOR.println("CAN initialization successful!");
}
void loop()
{
    unsigned char len = 0;
    unsigned char buf[8];
    static unsigned long ids[100] = {0};
    bool newID = true;
    static int idAmount = 0;

    if (CAN_MSGAVAIL == CAN.checkReceive())
    {
        CAN.readMsgBuf(&len, buf);
        unsigned long canId;
        if(idAmount==0)
        {
          ids[0] = CAN.getCanId();
          idAmount=1;
        }
        for(int i = 0;i < idAmount;i++)
        {
          if(CAN.getCanId() == ids[i])
          {
            newID = false;
            break;
          }
        }
        if(newID)
        {
          ids[idAmount] = CAN.getCanId();
          idAmount++;
          
          SERIAL_PORT_MONITOR.print("New ID found, ID list now: ");

          for (int j = 0; j < idAmount; j++)
          {
            SERIAL_PORT_MONITOR.print(ids[j], HEX);
            SERIAL_PORT_MONITOR.print(", ");
          }
          SERIAL_PORT_MONITOR.println("");
          SERIAL_PORT_MONITOR.print("Total amount of ids: ");
          SERIAL_PORT_MONITOR.print(idAmount);
          SERIAL_PORT_MONITOR.println("");
          SERIAL_PORT_MONITOR.println("-----------------------------");
        }
    }
}
