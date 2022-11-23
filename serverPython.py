# import socket programming library
import socket
from _thread import *
import threading
from random import randint
import time

# Armazena relógio (em segundos). Funciona como uma variável global
localTime = [time.time()]

# Lista auxiliar que armazenará todos os relógios.
remoteTimes = []

# Lista que guardará todos os endereços e portas dos clientes.
processos = []

# Lock usado como semáforo para conexões
print_lock = threading.Lock()


# Função que será usada em thread para coletar o relógio de um cliente
def coletarHorario(host, port):
	# Estabelece conexão com o cliente
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.connect((host,port))

	# Envia um requisito REQUEST_TIME
	print("Enviando REQUEST_TIME para " + str(host) + ":" + str(port))
	s.send("REQUEST_TIME\n".encode())

	# Aguarda e recebe o relógio do cliente.
	data = s.recv(1024).decode()

	# Encerra a conexão
	s.close()

	# Adiciona o relógio na lista remoteTimes (Que será usada para calcular média)
	remoteTimes.append(float(data))


# Função que sera usada em thread para enviar o novo relógio
def enviarHorario(host, port, newTime):
	# Estabelece conexão com o cliente
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.connect((host,port))

	# Prepara mensagem ( transforma em string o relógio)
	message = str(newTime) + "\n"
	print("Enviando novo time para " + str(host) + ":" + str(port))

	# Envia mensagem e fecha conexão
	s.send(message.encode())
	s.close()


# Função que será usada para processar o envio de temperatura de um cliente
def threaded(c):
	
	# Obtem a informação, libera o lock e fecha a conexão
	data = c.recv(1024).decode()
	# data = c.recv(1024)
	#data = c.recv(1024)
	print_lock.release()
	c.close()

	print("Recebeu dado bruto: {}".format(data))

	# Prepara a mensagem separando a temperatura do relógio
	# msg = ['TEMPERATURA','RELOGIO']
	msg = data.split("@")

	print("Recebeu temperatura: {}".format(msg[0]))
	print("Recebeu timestamp: {:.2f}".format(float(msg[1])))

	# Obtem a diferença entre o relógio local e o relógio do cliente
	diff = float(localTime[0]) - float(msg[1])
	
	# Se a diferença for maior que 1, iniciar processo de atualização
	if (diff > 1 or diff < -1):
		print("\nDiferença de time: {}".format(diff))
		print("Discrepancia detectada.\n")

		# Limpa a lista remoteTimes que receberá os relógios de todos os processos.
		remoteTimes.clear()

		# Adiciona o relógio local ao remoteTimes
		remoteTimes.append(localTime[0])

		# Declara uma lista vazia my_threads que armazenara threads que serão executadas em breve
		my_threads = []

		# Cria uma thread de requisição de relógio para cada cliente (Não executa ela ainda)
		for processo in processos:
			my_threads.append(threading.Thread(target=coletarHorario, args=(processo[0],processo[1],)))

		# Executa todas as threads
		for thread in my_threads:
			thread.start()
		
		# Cria joins nas threads para que a execução só continue depois que todas as threads concluirem
		for thread in my_threads:
			thread.join()

		# A esse ponto, o remoteTimes deveria ter todos os relógios dos processos

		# Calcular novo horario
		newTime = sum(remoteTimes) / len(remoteTimes)

		# Atualiza relógio local
		localTime[0] = newTime


		print("\nNovo time que sera enviado: {:.2f}\n".format(newTime))
		
		# Enviar novo horario para os clientes
		# Esvazia o my_threads
		my_threads = []

		# Prepara uma thread de envio de relógio para cada cliente (Não executa ela ainda)
		for processo in processos:
			my_threads.append(threading.Thread(target=enviarHorario, args=(processo[0],processo[1], newTime,)))

		# Executa todas as threads
		for thread in my_threads:
			thread.start()
		
		# Cria joins nas threads para que a execução só continue depois que todas as threads concluirem
		for thread in my_threads:
			thread.join()

		# Fim
	else:
		print("\nDiferença de time: {}".format(diff))
		print("Tudo OK.\n")
		
	print()
	

# Thread de clock do processo
def thread_clock():
	count = 0.0
	hz = 0.5

	while True:
		
		# Aguarda 0.5 segundos
		time.sleep(hz)

		# Adiciona 0.5 no relogio local e no counter
		localTime[0]+=hz
		count += hz

		# Após 10 segundos, há 33% de chance de ser adicionado ou removido 2 segundos ao invez do padrao 0.5
		if (count > 10.0 and randint(0,2) == 0):
			
			count = 0.0

			if (randint(0,1) == 0):
				localTime[0]+= 2.0
				print("\nANOMALIA OCORREU! +2 segundos!\n")
			else:
				localTime[0]-= 2.0
				print("\nANOMALIA OCORREU! -2 segundos!\n")

 
def Main():

	# Inicia a thread de clock que atuliza o relogio local
	start_new_thread(thread_clock, ())

	host = ""
	port = 8000

	# Adiciona os endereços e portas de cada cliente à lista processos
	processos.append(['127.0.0.1',8001])
	processos.append(['127.0.0.1',8002])
 
	# Cria um socket para ouvir e receber envios de temperatura dos clientes
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((host, port))
	s.listen(5)
	print("Socket escutando, aguardando envios...\n")

	# Loop sem fim para receber envios de clientes
	while True:
 
		# Estabelece conexao com cliente
		c, addr = s.accept()
		print('Conectou a:', str(addr[0]) + ':' + str(addr[1]))
 
		# Obtem um lock para funcionar como semáforo
		print_lock.acquire()
		
		# Inicia uma nova thread para tratar a conexão
		start_new_thread(threaded, (c,))

	s.close()
 

if __name__ == '__main__':
	Main()
