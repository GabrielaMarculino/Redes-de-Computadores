import socket
from time import ctime
MAQ = 'localhost'
PORTA = 12345
TAM_BUFFER = 1024
ADDR = (MAQ, PORTA)

if __name__ == '__main__':
	servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	servidor_socket.bind(ADDR)
	servidor_socket.listen(5)
	servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	while True:
		print('Servidor aguardando conexoes...')
		cliente_socket, addr = servidor_socket.accept()
		print('Cliente conectado de: ', addr)

		while True:
			dados = cliente_socket.recv(TAM_BUFFER)
			if not dados or dados.decode('utf-8') == 'END':
				break
			print("Recebidos do cliente: %s" %dados.decode('utf-8'))
			print("Envidando a hora do servidor ao cliente: %s" %ctime())
			try:
				cliente_socket.send(bytes(ctime(), 'utf-8'))
			except KeyboardInterrupt:
				print("Finalizado pelo usuario")
		cliente_socket.close()
	servidor_socket.close()

	#Rodar: python3 servidor_simples.py