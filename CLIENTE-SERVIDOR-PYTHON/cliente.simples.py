import socket

MAQ = 'localhost'
PORTA = 12345
TAM_BUFFER = 256

if __name__ == '__main__':
	cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	maq = input("Digite o nome da máquina: [%s]: " %MAQ) or MAQ
	porta = input("Digite a porta [%s]: " %PORTA) or PORTA

	sock_addr = (maq, int(porta))
	cliente_socket.connect(sock_addr)

	payload = 'GET TIME'
	try:
		while True:
			cliente_socket.send(payload.encode('utf-8'))
			dados = cliente_socket.recv(TAM_BUFFER)
			print(repr(dados))
			conteudo = input("Deseja enviar mais dados ao servidor[s/n]:")
			if conteudo.lower() == 'y':
				payload = input("Digite o payload: ")
			else:
				break
	except KeyboardInterrupt:
		print("Finalizado pelo usuário")
	cliente_socket.close()

	#Rodar: Digite o nome da maquina: [localhost]: localhost
	#       Digite a porta [12345]: 12345
	