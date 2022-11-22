# Import thread module
from _thread import *
import threading

# Import socket module
import socket
from random import randint

import time

# Armazena relógio (em segundos). Funciona como uma variável global
localTime = [time.time()]

# Função que será usada em thread para enviar "temperatura \n relogio" para o servidor responsável
def thread_enviar(host_send, port_send):
	# Loop infinito
	while True:
		# Pausar por um tempo, de 5 a 10 segundos
		time.sleep(randint(5,10))

		# Obter uma temperatura para ser enviada
		temperature = randint(30,100)

		# Prepara mensagem no formato "temperatura \n relogio"
		message = "{}@{}".format(temperature, localTime[0])
		print("\nTemperatura lida: {}".format(temperature))
		print("Enviar mensagem: {}\n".format(message))

		# Estabelece uma conexão com o servidor responsável
		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.connect((host_send,port_send))
		
		# Envia mensagem e fecha a conexão
		s.send(message.encode())
		s.close()
		
# Função que será usada em thread para receber requisição do servidor responsável
def thread_receber(host_recv, port_recv):
	
	# Cria um socket para ouvir e receber requisição de atualização de horário do servidor responsável
	socket_recv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	socket_recv.bind((host_recv, port_recv))
	socket_recv.listen(5)
	print("Esperando pedido de sincronizacao")
	
	# Loop infinito
	while True:
		
		# Aceita uma nova conexão do processo responsável
		c, addr = socket_recv.accept()
		print('\nConectou com endereco: ', addr[0], ':', addr[1])
		
		# Receber mensagem e armazena em data
		data = c.recv(1024).decode().strip()
		print("Mensagem recebida: {}".format(data))
		
		# Verifica se a requisição é REQUEST_TIME
		if str(data) == "REQUEST_TIME":
			
			# Envia relógio local para servidor responsável e fecha a conexão
			print("Enviando time local para processo responsável")
			c.send(str(localTime[0]).encode())
			c.close()

			# Aguarda e aceita uma nova conexão do processo responsável
			c, addr = socket_recv.accept()
			
			# Recebe o novo relogio do processo responsável
			message = c.recv(1024).decode().strip()

			# Obtem novo relogio e o atualiza para o relogio local
			newTime = float(message)
			print("Novo time recebido: {:.2f}\n".format(newTime))
			localTime[0] = newTime
		
		else:
			print("Um erro inesperado ocorreu! REQUEST_TIME não foi recebido\n")
		
		c.close()

	socket_recv.close()

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

	''''
	# Estabelece o endereço e porta do servidor responsável
	host_send = '10.104.1.131'
	port_send = 8000

	# Estabelece o endereço e porta do servidor local (Este aqui)
	host_recv = '10.104.1.150'
	port_recv = 8002
	'''

	# Estabelece o endereço e porta do servidor responsável
	host_send = '127.0.0.1'
	port_send = 8000

	# Estabelece o endereço e porta do servidor local (Este aqui)
	host_recv = '127.0.0.1'
	port_recv = 8002

	# Inicia thread_enviar. Essa thread serve para enviar temperatura para o servidor responsável
	start_new_thread(thread_enviar, (host_send, port_send,))

	# Inicia thread_receber. Essa thread serve para receber requisição de atualização de relógio, enviar o relógio local, e receber o novo relógio a ser usado.
	start_new_thread(thread_receber, (host_recv, port_recv, ))

	while True:
		# Loop infinito que continuamente imprime o relógio local.
		time.sleep(1)
		print("Timestamp: {:.2f}".format(localTime[0]))

if __name__ == '__main__':
	Main()
