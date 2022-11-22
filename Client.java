import java.io.*;
import java.net.*;
import java.util.Random;

// Classe do Client
public class Client {

	// Main
	public static void main(String[] args) {
		// Obtem relogio
		SystemTime time = new SystemTime();

		// Thread do clock
		ClockThread clockThread = new ClockThread(time);
		clockThread.start();

		// Thread de enviar temperatura para responsavel
		SendData sendThread = new SendData(time, "127.0.0.1", 8000);
		sendThread.start();

		// Thread para receber requisicao de sincronizacao e sincronizar
		RecieveDataThread recieveDataThread = new RecieveDataThread(time,"127.0.0.1", 8001);
		recieveDataThread.start();


		while (true){
			// try-catch para aguardar 1 segundo (Precisa do try-catch devido ao InterruptedException)
			try {Thread.sleep(1000);} 
			catch (InterruptedException e){e.printStackTrace();}
		
			// Continuamente imprime o timestamp (Obs.: O numero foi convertido para float para melhorar a aparencia do numero)
			System.out.printf("Timestamp: %.2f\n", time.getTime());
		}
	} 
	
}

class SendData extends Thread {

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
		while (true) {
			try {
				// Aguarda um valor aleatorio até o proximo envio de temperatura
				Thread.sleep(5000);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}

			// Obtem um valor aleatorio de temperatura para ser enviado
			int temp = rand.nextInt(100 - 30) + 30;

			// Prepara uma mensagem String do tipo "string temp + '\n' + string time"
			String message = Integer.toString(temp) + '@' + Double.toString(time.getTime());

			System.out.println("\nTemperatura lida: " + Integer.toString(temp));
			System.out.println("Enviar mensagem: " + message + "\n");
			
			try {
				// Cria um objeto Socket para se conectar com o responsavel
				Socket socket = new Socket(host, port);
				
				// Cria um objeto PrintWriter para envio. Envia a mensagem, limpa o buffer, e fecha
				PrintWriter out = new PrintWriter(socket.getOutputStream(),true);
				out.println(message);
				out.close();

				// Fecha o socket
				socket.close();

			} catch (Exception error) {
				System.out.println(error);
			}

		}
	}

}

class SystemTime {
	private double time;

	// construtor the SystemTime, equivalente ao time.time() do python
	public SystemTime() {
		this.time = System.currentTimeMillis()/1000.0;
		
	}

	// getter e setter para time
	public double getTime() {return time;}
	public void setTime(double time) {this.time = time;}

	// addTime especificado pelo parametro
	public void addTime(double seconds_to_add) {
		this.time += seconds_to_add;
	}
}

class ClockThread extends Thread {
	SystemTime time;
	Double count = 0.0;
	
	Double hz = 0.5; // Segundos da frequencia do clock
	long sleep_time; // Milisegundos para o sleep

	Random rand = new Random();

	// Construtor da classe ClockThread
	ClockThread(SystemTime time) {
		this.time = time;
		this.sleep_time = (long) (hz * 1000.0); // Converte double para long
	}

	// Funcao que sera executada em thread
	public void run() {
		// Loop infinito
		while (true) {
			
			// try-catch para aguardar hz segundos (Precisa do try-catch devido ao InterruptedException)
			try {Thread.sleep(sleep_time);} 			
			catch (InterruptedException e) {e.printStackTrace();}
			
			// Adiciona o tempo do hz ao SystemTime
			time.addTime(hz);
			count += hz;

			// Após 10 segundos, há 33% de chance de ser adicionado ou removido 2 segundos ao invez do padrao 0.5
			if (count > 10.0 && rand.nextInt(3) == 0){
				// Reseta count
				count = 0.0;
				// Decisao de 50% para ser +2 ou -2
				if (rand.nextInt(2) == 0){	
					time.addTime(2.0);
					System.out.println("\nANOMALIA OCORREU! + 2 segundos!\n");
				}else{
					time.addTime(-2.0);
					System.out.println("\nANOMALIA OCORREU! - 2 segundos!\n");
				}
				
				
			}
		}
	}
}

class RecieveDataThread extends Thread {

	SystemTime time;
	String host;
	int port;

	RecieveDataThread(SystemTime time, String host, int port) {
		this.time = time;
		this.host = host;
		this.port = port;
	}

	public void run() {
		
		BufferedReader br;
		String data;

		try {

			ServerSocket server = new ServerSocket(port);
			System.out.println("Esperando pedido de sincronizacao\n");
			
			// Loop infinito
			boolean keep_listening = true;
			while (keep_listening) {
				
				
				Socket client = server.accept();
				System.out.println("\nConectou com endereco: " + client.getLocalSocketAddress());

				br = new BufferedReader(new InputStreamReader(client.getInputStream(), "UTF-8"));
				data = br.readLine().trim();


				System.out.println("Mensagem recebida: " + data);

				if (data.equals("REQUEST_TIME")) {
					String message = Double.toString(time.getTime());

					PrintWriter out = new PrintWriter(client.getOutputStream(),true);
					System.out.println("Enviando time local para processo responsavel");
					out.println(message);
					//out.flush();
					br.close();
					out.close();

					// Encerrar conexào
					client.close();

					// Aguardar novo envio de horario
					client = server.accept();

					br = new BufferedReader(new InputStreamReader(client.getInputStream(), "UTF-8"));
					data = br.readLine().trim();
					br.close();

					System.out.println("Novo time recebido: " + data + "\n");

					time.setTime(Double.parseDouble(data));
				} else {
					System.out.println("Um erro inesperado ocorreu! REQUEST_TIME não foi recebido");
				}

				client.close();
			}
			server.close();

		} catch (IOException error) {
			System.out.println(error);
		}


		
	}
}
