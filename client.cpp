#include <arpa/inet.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>
#include <iostream>
#include <chrono>
#include <thread>
#include <cstdlib>
#include <algorithm>
using namespace std;
#define PORT 8002
#define PORTSERVER 8000

class SendDataThread {
public:
    void operator()(double* time){
    // string timeText = to_string(time);

    // cout << time << '\n';
    // cout << timeText << '\n';

    // int temp = rand() % 100;

    // string temperatura = to_string(temp);
    
    // string testeVa = temperatura + "@" +  timeText;
    // cout << "testeVa => "<< testeVa << '\n';

    // char* sendMessage = &testeVa[0];

    while (true) {

    int sock = 0, valread, client_fd;
    struct sockaddr_in serv_addr;

    char buffer[1024] = { 0 };
    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        cout << "Socket creation error" << '\n';
        return;
    }

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORTSERVER);
    
    // Convert IPv4 and IPv6 addresses from text to binary
    // form
    if (inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr) <= 0) {
      cout << '\n' << "Invalid address/ Address not supported" << '\n';
      return;
    }

    
      
      int seconds = rand() % 5 + 5;

      this_thread::sleep_for(chrono::milliseconds(seconds*1000));

      string timeText = to_string(*time);
      int temp = rand() % 100;
      string temperatura = to_string(temp);
    
      string testeVa = temperatura + "@" +  timeText;
      cout << "Enviar menssagem => "<< testeVa << '\n';

      char* sendMessage = &testeVa[0];

      if ((client_fd
        = connect(sock, (struct sockaddr*)&serv_addr,
                  sizeof(serv_addr)))
        < 0) {
        cout << "Connection Failed" << '\n';
        return;
      }
      send(sock, sendMessage, strlen(sendMessage), 0);
      cout << "Enviou temperatura e tempo" << '\n';
      

      // closing the connected socket
      close(client_fd);
    }
  }
};
 
class SystemTime{
  uint64_t timeSinceEpochMilliseconds = chrono::duration_cast<chrono::milliseconds>(
  chrono::system_clock::now().time_since_epoch()).count();

  public:
    double time;

    SystemTime() {
      time = timeSinceEpochMilliseconds/1000.0;
    }

    void addTime(double secondsToAdd){
      this->time =0.001;
      
      // this->time += secondsToAdd;
    }

    void print(){
      string timeText = to_string(this->time);
      cout << "Tempo em segundos: " << timeText << '\n';
    }
};

class ClockThread{
  public:
    void operator()(double* time){
      
      double count;

      while (true)  {
        this_thread::sleep_for(chrono::milliseconds(500));
        
        if(count >= 10.0 && rand()%3 == 0){
          count = 0.0;
          if(rand() % 2 == 0) {
            cout << "ANOMALIA +2" << '\n';
            *time += 2.0;
          } else{
            cout << "ANOMALIA -2" << '\n';
            *time += -2.0;
          }
        } else{
          *time += 0.5;
          count += 0.5;
        }
      }
  }
};

class ReceiveDataThread{
  public:
    void operator()(double* time){
    int server_fd, new_socket, valread;
    struct sockaddr_in address;
    int opt = 1;
    int addrlen = sizeof(address);
    char buffer[1024] = { 0 };

    // Creating socket file descriptor
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        perror("socket failed");
        exit(EXIT_FAILURE);
    }

    // Forcefully attaching socket to the port 8080
    if (setsockopt(server_fd, SOL_SOCKET,
                  SO_REUSEADDR | SO_REUSEPORT, &opt,
                  sizeof(opt))) {
        perror("setsockopt");
        exit(EXIT_FAILURE);
    }
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    // Forcefully attaching socket to the port 8080
    if (bind(server_fd, (struct sockaddr*)&address,
            sizeof(address))
        < 0) {
        perror("bind failed");
        exit(EXIT_FAILURE);
    }

    if (listen(server_fd, 3) < 0) {
        perror("listen");
        exit(EXIT_FAILURE);
    }
    while (true) {
      cout << "Aguardando conexao" << '\n';
      if ((new_socket
          = accept(server_fd, (struct sockaddr*)&address,
                    (socklen_t*)&addrlen))
          < 0) {
          perror("accept");
          exit(EXIT_FAILURE);
      }
      
      valread = read(new_socket, buffer, 1024);
      cout << "buffer =================" << buffer << '\n';

      if(strcmp(buffer,"REQUEST_TIME\n") == 0){
        string timeText = to_string(*time);

        char message[100];
        strncpy(message, to_string(*time).c_str(), sizeof(message));

        // cout << "Buffer: " << buffer << '\n'; 
        cout << "Enviar local time ===========" << message <<'\n';

        send(new_socket, message, strlen(message), 0);

        for ( int i = 0; i < sizeof(message);  i++ ) {
          message[i] = (char)0;
        }
      } else{
        // time = (double)
        cout << "recebeu novo horário => " <<  '\n';
        // cout << "buffer => " << buffer <<  '\n';

        for(int i = 0; i < sizeof(buffer); i++){
          if (buffer[i] == '\n') {
            buffer[i] = '\0';
            break;
          }
        }

        *time = atof(buffer);
      }

      for ( int i = 0; i < sizeof(buffer);  i++ ) {
        buffer[i] = (char)0;
      }

      //  cout << "buffer2 =================" << buffer << '\n';
      
      // send(new_socket, hello, strlen(hello), 0);
  
      // closing the connected socket
      close(new_socket);
    }
    // closing the listening socket
    shutdown(server_fd, SHUT_RDWR);
    }
};

int main(int argc, char const* argv[]) {
  uint64_t timeSinceEpochMilliseconds = std::chrono::duration_cast<std::chrono::milliseconds>(
  std::chrono::system_clock::now().time_since_epoch()).count();

  double time = timeSinceEpochMilliseconds/1000.0;

  double* timePointer = &time;
  
  // SystemTime time;

  thread sendDataThread(SendDataThread(), timePointer);

  thread receiveDataThread(ReceiveDataThread(), timePointer);
  
  thread clockThread(ClockThread(), timePointer);
  
   while (true) {
    this_thread::sleep_for(chrono::milliseconds(1000));
    string timeText = to_string(*timePointer);
    cout << "Tempo em segundos: " << timeText << '\n';
  }

  // clockThread.join();

  return 0;
}