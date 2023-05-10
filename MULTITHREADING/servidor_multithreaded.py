import aux
import threading, queue

HOST = aux.HOST
PORT = aux.PORT

send_queues = {}
lock = threading.Lock() 

def handle_client_recv(sock, addr):
	""" Recebe dados do cliente via socket e os espalha a outros clientes """
	rest = bytes()
	while True:
		try:
			(msgs, rest) = aux.recv_msgs(sock, rest) #bloqueia até receber a mensagem completa		
		except (EOFError, ConnectionError):
			handle_disconnect(sock, addr)
			break
		for msg in msgs:
			msg = '{}: {}'.format(addr, msg)
			print(msg)
			broadcast_msg(msg)

def handle_client_send(sock, q, addr):
	""" Monitora a fila de novas mensagens, e as envia para o cliente assim que as mensagens chegam """
	while True:
		msg = q.get()
		if msg == None: break
		try:
			aux.send_msg(sock, msg)
		except (ConnectionError, BrokenPipe):
			handle_disconnect(sock, addr)
			break

def broadcast_msg(msg):
	""" Coloca cada mensagem na fila de saída dos clientes conectados """
	with lock:
		for q in send_queues.values():
			q.put(msg)

def handle_disconnect(sock, addr):
	""" Garante que a fila esteja vazia e o socket fechado quando o cliente disconectar """
	fd = sock.fileno()
	with lock:
		#prepara a fila de saída para o cliente
		q = send_queues.get(fd, None)
	#Se ainda existir a fila, então a função disconecte não foi manipulada.
	if q:
		q.put(None)
		del send_queues[fd]
		addr = sock.getpeername()
		print('Cliente {} desconectado'.format(addr))
		sock.close()

if __name__ == '__main__':
	listen_sock = aux.cria_socket_listen(HOST, PORT)
	addr = listen_sock.getsockname()
	print('Ouvindo em {}'.format(addr))

	while True:
		client_sock, addr = listen_sock.accept()
		q = queue.Queue()
		with lock:
			send_queues[client_sock.fileno()] = q
		# A thread vai rodar a função hanle_client() automaticamente e concorrentemente
		#enquanto estiver no loop
		recv_thread = threading.Thread(target=handle_client_recv, args=[client_sock, addr], daemon=True)
		send_thread = threading.Thread(target=handle_client_send, args=[client_sock, q, addr], daemon=True)
		recv_thread.start()
		send_thread.start()
		print('Conexao de {}'.format(addr))		