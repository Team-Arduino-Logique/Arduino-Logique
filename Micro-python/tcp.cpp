// TCP C++ client which sends a data structure  to a ESP32 server
//
// open ports in firewall to allow TCP communication

#include <inttypes.h>
#include <windows.h>

#include <time.h> // clock_t, clock, CLOCKS_PER_SEC

// test structure
struct __attribute__((packed)) Data {
  int16_t seq;  // sequence number
  int32_t distance;
  float voltage;
  char text[50];
} data = { 0, 56, 3.14159, "hello test" };  // sample data

#ifdef __WIN32
  #include <winsock.h>          // for windows
  #define socklen_t int
#else
  #include <arpa/inet.h>        // for UNIX
  #include <netdb.h>
  #include <netinet/in.h>
  #define errno h_errno
#endif
#include <stdio.h>
#include <unistd.h>
#include <iostream>
#include <fstream>

void delay(unsigned int milliseconds){
    clock_t start = clock();
    while((clock() - start) * 1000 / CLOCKS_PER_SEC < milliseconds);
}

using namespace std;

int main()
{
      struct sockaddr_in socketinfo;
  #ifdef __WIN32                // windows WINSOCK startup
      WSAData wsaData;
      if (WSAStartup(MAKEWORD(1, 1), &wsaData) != 0) {
          return 255;
      }
  #endif
        // attempt to connect to server
        socketinfo.sin_family = AF_INET;
        socketinfo.sin_port = htons(10000);                         // remote server port
        //socketinfo.sin_addr.s_addr = inet_addr("127.0.0.1");
        socketinfo.sin_addr.s_addr = inet_addr("192.168.1.211");    // remote server IP address
        // create socket
        int socket1 = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
        if(socket1 < 0)
            { cout << "error in socket1 creation. aborting." << endl; return -1; }
        cout << "socket created OK\n";
        // attempt to connect to server
        if (connect(socket1, (sockaddr*)&socketinfo, sizeof(socketinfo)) < 0)
            { cout << "unable to connect to server. aborting." << endl; return -1; }
         cout << "connected to server OK \n";
         // loop transmitting data to server every second
         while(1) {
            // connected to server, send message
            cout << "data.seq = " << data.seq << " voltage " << data.voltage << endl;
            // int status2=send(socket1, "Hello server from C++ client", 28, 0);
            int status2=send(socket1, (char *) &data, (int) sizeof(data), 0);
            if(status2 == -1)
                {    cout << "error in sending" << endl; return -1;  }
            cout << "status transmitted " << status2 << "bytes " << endl;
            data.seq++;
            data.distance+=25;
            data.voltage+=3.14159;
            data.text[9]++;
            delay(2000);
         }
        close(socket1);
}