#include <arpa/inet.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>
#include <iostream>
#include <chrono>
#include <thread>
using namespace std;
#define PORT 8000

class SendDataThread {
public:
    void operator()(double time){
    string timeText = to_string(time);

    cout << time << '\n';
    cout << timeText << '\n';

    int sock = 0, valread, client_fd;
    struct sockaddr_in serv_addr;
    char message[timeText.length()];
    strncpy(message, to_string(time).c_str(), sizeof(message));

    char buffer[1024] = { 0 };
    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        cout << "Socket creation error" << '\n';
        return;
    }

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);

    // Convert IPv4 and IPv6 addresses from text to binary
    // form
    if (inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr) <= 0) {
      cout << '\n' << "Invalid address/ Address not supported" << '\n';
      return;
    }

    if ((client_fd
        = connect(sock, (struct sockaddr*)&serv_addr,
                  sizeof(serv_addr)))
        < 0) {
        cout << "Connection Failed" << '\n';
        return;
    }
    send(sock, message, strlen(message), 0);
    cout << "Hello message sent" << '\n';
    valread = read(sock, buffer, 1024);
    cout << buffer << '\n';

    // closing the connected socket
    close(client_fd);
  }
};
 
class ClockThread{};

int main(int argc, char const* argv[]) {
  uint64_t timeSinceEpochMilliseconds = std::chrono::duration_cast<std::chrono::milliseconds>(
  std::chrono::system_clock::now().time_since_epoch()).count();

  double time = timeSinceEpochMilliseconds/1000.0;

  thread sendDataThread(SendDataThread(), time);
  sendDataThread.join();

  return 0;
}