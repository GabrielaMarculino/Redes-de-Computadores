import sys, socket, threading
import aux

HOST = sys.argv[-1] if len(sys.argv) > 1 else '127.0.0.1'
PORT = aux.PORT 

def handle_input(sock):
	"""Digite a mensagem e envie ao servidor..."""
	print("Digite a mensagem, enter para enviar, 's' para sair")
	while True:
		msg = input()
		if msg == 's':
			sock.shutdown(socket.SHUT_RDWR)
			sock.close()
			break
		try:
			aux.send_msg(sock, msg) #bloqueia até o envio terminar.
		except (BrokenPipeError, ConnectionError):
			break

if __name__ == '__main__':
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((HOST, PORT))
	print('Conectado a {}:{}'.format(HOST, PORT))

	#Cria a thread para manipular a entrada do usuário e o envio da mensagem
	thread = threading.Thread(target=handle_input, args=[sock], daemon=True)
	thread.start()
	rest = bytes()
	addr = sock.getsockname()
	#fica em loop infinito até receber as mensagens do servidor

	while True:
		try:
			(msgs, rest) = aux.recv_msgs(sock, rest)
			for msg in msgs:
				print(msg)			
		except ConnectionError:
			print('Conexao com o servidor fechada')
			sock.close()
			break		