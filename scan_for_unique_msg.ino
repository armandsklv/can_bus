#include <SPI.h>
#define CAN_2515
//Arduino parametri darbam ar CAN Bus Shield V2.0
const int SPI_CS_PIN = 10;
const int CAN_INT_PIN = 2;

#ifdef CAN_2515
#include "mcp2515_can.h"
mcp2515_can CAN(SPI_CS_PIN);
#endif                           
void setup()
{   //Virknes kopnes datu parraides atrums, bitos
    SERIAL_PORT_MONITOR.begin(115200);
    //Tiek uzstadits CAN kopnes datu parraides atrums
    // CAN_250KBPS - liela atruma CAN kopnei
    // CAN_125KBPS - Zema atruma CAN kopnei
    while (CAN_OK != CAN.begin(CAN_250KBPS))
    {
        SERIAL_PORT_MONITOR.println("Couldn't initialize CAN connection. Trying again...");
        delay(100);
    }
    SERIAL_PORT_MONITOR.println("CAN connection initialized!");
}
void loop()
{
    unsigned char len = 0; //Datu bufera garums
    unsigned char buf[8]; //Datu buferis, max izmers 8 baiti
    static unsigned char messages[50][8]; //Masivs unikalajam CAN zinam
    static int messageAmount=0;
    bool newMessage = true;
    char bufByte[18] = {0};
    if (CAN_MSGAVAIL == CAN.checkReceive())
    {
        CAN.readMsgBuf(&len, buf);
        //CAN kopnes ID decimalaja forma, kuras zinas tiek atfiltretas
        unsigned long canId = 1228836;
        //Katru reizi ka tiek nolasīta CAN ziņa izveletajai CAN ID tiek parbaudits vai zina ir unikala
        // ja ziņa ir unikala, tad ieraksta masiva, ja nav, tad turpina ar nakamo CAN zinu
        if(canId == CAN.getCanId())
        {
          if(messageAmount == 0)
          {
            for(int j = 0;j<len;j++)
            {
              messages[messageAmount][j] = buf[j];
            }
          }
          int equalBytes;
          if(messageAmount != 0)
          {
            for(int m = 0;m < messageAmount;m++)
            {
              equalBytes = 0;
              for(int b = 0;b < len;b++)
              {
                if(messages[m][b] == buf[b])
                {
                  equalBytes++;
                }
              }
              if(equalBytes == len)
              {
                newMessage = false;
                break;
              }
            }
            if(newMessage)
            {
              for(int k = 0;k < len;k++)
              {
                messages[messageAmount][k] = buf[k];
              }
              messageAmount++; 
            }
          }
          else
          {
            messageAmount++;
          }
          // Atrodot jaunu unikalu zinu izvada visu unikalo zinu sarakstu
          if(newMessage)
          {
            SERIAL_PORT_MONITOR.println("New unique message found, message list now: ");
            for(int i = 0;i < messageAmount;i++)
            {
              sprintf(bufByte, "%02X %02X %02X %02X %02X %02X %02X %02X",
              messages[i][0],messages[i][1],messages[i][2],
              messages[i][3],messages[i][4],messages[i][5],
              messages[i][6],messages[i][7]);
              SERIAL_PORT_MONITOR.println(bufByte);
            }
            SERIAL_PORT_MONITOR.println("");
            SERIAL_PORT_MONITOR.print("Total amount of messages: ");
            SERIAL_PORT_MONITOR.print(messageAmount);
            SERIAL_PORT_MONITOR.println("");
            SERIAL_PORT_MONITOR.println("--------------------------");
            SERIAL_PORT_MONITOR.println("");
          }
          newMessage = false;
        }
    }   
}
