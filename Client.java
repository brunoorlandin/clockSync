import java.io.*;  
import java.net.*;
import java.time.*;
// import java.time.temporal.*;
import java.util.Random;

public class Client {
  public static void main(String[] args){
    SystemTime time = new SystemTime();
    
    System.out.println("First time: " + time.getTime());

    ClockThread clockThread = new ClockThread(time);
    clockThread.start();

    SendData sendThread = new SendData(time, "127.0.0.1", 8000);
    sendThread.start();

    // RecieveDataThread recieveDataThread = new RecieveDataThread(time, "127.0.0.1", 8000);
    // recieveDataThread.start();

    while (true){
      try {
      Thread.sleep(5000);
      } catch (InterruptedException e) {
        e.printStackTrace();
      }
      System.out.println("Teste: " + time.getTime());
    }

    

    // time.addTime();
    // System.out.println("Teste: " + time.getTime());

    // System.out.println("Time after thread: " + time.getTime());
  
    // try {
    //   Socket socket = new Socket("localhost",8000);  
      
    //   InetAddress address = socket.getInetAddress();

    //   System.out.println(address);

    //   socket.close();

    // } catch (Exception e) {
    //     System.out.println(e);
    // }
  }
}

class SendData extends Thread{

  SystemTime time;
  String host;
  int port;
  Random rand = new Random();

  SendData(SystemTime time, String host, int port) {
    this.time = time;
    this.host = host;
    this.port = port;
  }

  public void run() {
    while (true){
      try {
        Thread.sleep(rand.nextInt(6-5) + 5);
      } catch (InterruptedException e) {
        e.printStackTrace();
      }
  
      int temp = rand.nextInt(100-30) + 30;
      String message = Integer.toString(temp) + '\n' + Long.toString(time.getTime());
  
      try {
        Socket socket = new Socket(host,port);
  
        DataOutputStream dout = new DataOutputStream(socket.getOutputStream());  
        dout.writeUTF(message);  
        dout.flush();  
        dout.close();  
  
        socket.close();
  
      } catch (Exception error) {
        System.out.println(error);
      }
    }
  }

}

class SystemTime{

  private Instant instant = Instant.now();
  private long time = instant.getEpochSecond();

  public SystemTime() {}

  public long getTime() {
    return time;
  }

  public void setTime(long time) {
    this.time = time;
  }

  public void addTime(){
    long time = getTime();
    
    setTime(time + 10);
  }
}

class ClockThread extends Thread {
  SystemTime time;
  Double count = 0.0;
  Double hz = 0.5;
  Random rand = new Random();

  ClockThread(SystemTime time) {
    this.time = time;
  }

  public void run() {

    while (true){
      try {
      Thread.sleep(Double.valueOf(hz * 1000).longValue());
      } catch (InterruptedException e) {
        e.printStackTrace();
      }
      time.addTime();
      // if ((count > 15 && rand.nextInt(1)) || count > 20){

      // }

    }
    
    
  }
}

class RecieveDataThread extends Thread{

  SystemTime time;
  String host;
  int port;

  RecieveDataThread(SystemTime time, String host, int port) {
    this.time = time;
    this.host = host;
    this.port = port;
  }
  
  public void run() {
      while (true){
        try {
          Socket socket = new Socket(host, port, null, 8001);
          // socket.accept();

          SocketAddress addrress = socket.getLocalSocketAddress();
          System.out.println("Java client address = " + addrress);
        
          DataInputStream din = new DataInputStream(socket.getInputStream());
          DataOutputStream dout = new DataOutputStream(socket.getOutputStream());

          String data = din.readUTF();

          if(data == "REQUEST_TIME"){
            dout.writeUTF(Long.toString(time.getTime()));

            String timeRecieved = din.readUTF();

            System.out.println("New time: " + timeRecieved);

            time.setTime(Long.parseLong(timeRecieved));
          } else {
            System.out.println("Um erro inesperado ocorreu! REQUEST_TIME não foi recebido");
          }
          
          socket.close();
        } catch (Exception error) {
          System.out.println(error);
        }
      }
  }
}


