import socket

HOST = ''
PORT = 4040

def cria_socket_listen(host, port):
	"""Configura o socket para o servidor receber os pedidos de conexão """
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1);
	sock.bind((host, port))
	sock.listen(100)
	return sock

def recv_msgs(sock, data=bytes()):
	"""Recebe dados e os quebra em mensagens completas com um delimitador de byte nulo """
	msgs = []
	#Lê repetidamente 4.096 bytes do soquete, armazenando os bytes em dados até vermos um delimitador
	while not msgs:
		recvd = sock.recv(4096)
		if not recvd:
			#o socket foi fechado prematuramente
			raise ConnectionError()
		data = data + recvd
		(msgs, rest) = parse_recvd_data(data)		
	msgs = [msg.decode('utf-8') for msg in msgs]
	return (msgs, rest) 

def prep_msg(msg):
	""" Prepara a string para ser enviada como mensagem """
	msg += '\0'
	return msg.encode('utf-8')

def send_msg(sock, msg):
	""" Envia a string pelo socket """
	dados = prep_msg(msg)
	sock.sendall(dados)

def parse_recvd_data(data):
	"""Quebra os dados brutos da rede em mensagens delimitadas por um byte nulo """
	parts = data.split(b'\0')
	msgs = parts[:-1]
	rest = parts[-1]
	return (msgs, rest)