# import thread module
from _thread import *
import threading


# Import socket module
import socket
from random import randint
from random import seed

seed(10)


import time
localTime = [time.time()]

def thread_enviar(host_send, port_send):
	while True:
		time.sleep(randint(5,6))

		temperature = randint(30,100)
		message = "{}\n{}".format(temperature, localTime[0])
		print("Enviar mensagem: {}".format(message))

		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.connect((host_send,port_send))
		s.send(message.encode())
		s.close()
		
def thread_receber(host_recv, port_recv):
	socket_recv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	socket_recv.bind((host_recv, port_recv))
	socket_recv.listen(5)
	print("Escutando processo mestre")
	while True:
		# Estabelecer conexao
		c, addr = socket_recv.accept()
		print('Connected to :', addr[0], ':', addr[1])
		
		# Receber pedido
		data = c.recv(1024).decode()
		print("Mensagem recebida: {}".format(data))
		if str(data) == "REQUEST_TIME":
			# Enviar localTime
			print("Enviando TIME")
			c.send(str(localTime[0]).encode())
			c.close()

			# Receber novo localTime
			c, addr = socket_recv.accept()
			message = c.recv(1024).decode()
			print()
			print(message)
			print()
			newTime = float(message)
			print("New time: {:.2f}".format(newTime))
			localTime[0] = newTime
		
		else:
			print("Um erro inesperado ocorreu! REQUEST_TIME não foi recebido")
		
		c.close()

	socket_recv.close()

def thread_clock():
	count = 0
	hz = 0.5
	while True:
		time.sleep(hz)
		if ((count > 15 and randint(0,1)) or count > 20):
			'''
			if (randint(0,1)):
				localTime[0]-= 1
			else: 
				localTime[0]+= 3
			'''
			print("ANOMALIA!")
			localTime[0]+= 3.0
			count = 0
		else:
			localTime[0]+=hz
			count += hz
		
		

def Main():
	start_new_thread(thread_clock, ())

	# local host IP '127.0.0.1'
	host_send = '10.104.1.131'
	port_send = 8000

	# local host
	host_recv = '10.104.1.151'
	port_recv = 8001

	
	start_new_thread(thread_enviar, (host_send, port_send,))
	start_new_thread(thread_receber, (host_recv, port_recv, ))

	while True:
		time.sleep(1)
		print("Main: ", localTime)

		
 
if __name__ == '__main__':
	Main()
