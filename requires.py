# coding: utf-8
#!/usr/bin/python3

'''
	Arquivo criado para armazenar as bibliotecas utilizadas em clientSocketUDP e serverSocketUDP.
	O endereço e porta do Servidor estão armazenados neste arquivo.
	Instruções:

	- Rodar primeiro o arquivo serverSocketServer.py
	- Depois rodar o arquivo clienteSocketServer.py

'''

import socket, sys
from ntptimenow import NTPTimeNow

addressIPV4 = "localhost"
listeningPort = 5555