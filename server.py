# import socket programming library
import socket
from random import randint
#
import time
localTime = [time.time()]

remoteTimes = []

processos = []
 
# import thread module
from _thread import *
import threading
 
print_lock = threading.Lock()

def coletarHorario(host, port):
	# Coleta horario
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.connect((host,port))
	s.send("REQUEST_TIME".encode())
	data = s.recv(1024).decode()
	s.close()
	# Adiciona horario na lista remoteTimes
	remoteTimes.append(float(data))
	


def enviarHorario(host, port, newTime):
	#Envia horario novo para os outros processos
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.connect((host,port))
	message = str(newTime)
	print("MENSAGEM QUE ESTA SENDO ENVIADA: {}".format(message))
	s.send(message.encode())
	s.close()

# thread function
def threaded(c):
	
	data = c.recv(1024).decode()
	print_lock.release()
	c.close()
	
	print("Recebeu dado: {}".format(data))

	# Verificar se o horário fornecido corresponde com o do sistema.
	msg = data.split("\n")

	diff = float(localTime[0]) - float(msg[1])

	print("Dados: {:.2f} - {:.2f}".format(localTime[0], float(msg[1])))
	print("Diferença: {}".format(diff))
	
	

	if (diff > 1 or diff < -1):
		print("Discrepancia detectada!")

		

		# Limpa a lista para obter novos horarios
		remoteTimes.clear()

		# Enviar pedido de horário (for x threads)
		my_threads = []
		for processo in processos:
			my_threads.append(threading.Thread(target=coletarHorario, args=(processo[0],processo[1],)))

		remoteTimes.append(localTime[0])
		
		for thread in my_threads:
			thread.start()
		
		# For de join
		for thread in my_threads:
			thread.join()


		# Calcular novo horario
		newTime = sum(remoteTimes) / len(remoteTimes)

		localTime[0] = newTime

		print("Enviando dados para subordinados: {:.2f}".format(newTime))
		# Enviar novo horario para outros processos
		my_threads = []
		for processo in processos:
			my_threads.append(threading.Thread(target=enviarHorario, args=(processo[0],processo[1], newTime,)))

		for thread in my_threads:
			thread.start()
		
		# For de join
		for thread in my_threads:
			thread.join()
	
	
	print()

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
			count = 0
			localTime[0]+=hz
		else:
			localTime[0]+=hz
			count += hz

 
def Main():
	start_new_thread(thread_clock, ())

	host = ""

	processos.append(['127.0.0.1',8001])
	#processos.append(['127.0.0.1',8002])
 
	# reserve a port on your computer
	# in our case it is 12345 but it
	# can be anything
	port = 8000
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((host, port))
	print("socket binded to port", port)
 
	# put the socket into listening mode
	s.listen(5)
	print("socket is listening")

 
	# a forever loop until client wants to exit
	while True:
 
		# establish connection with client
		c, addr = s.accept()
 
		# lock acquired by client
		print_lock.acquire()
		print('Connected to :', addr[0], ':', addr[1])
 
		# Start a new thread and return its identifier
		start_new_thread(threaded, (c,))
	s.close()
 
 
if __name__ == '__main__':
	Main()
