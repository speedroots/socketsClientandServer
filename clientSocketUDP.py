# coding: utf-8
#!/usr/bin/python3

from requires import *

def socketIPV4_UDP():
    
    '''

        - AF_INET especifica que o socket existirá sob o protocolo IPV4;
        - SOCK_DGRAM especifica que o socket será construído sob o protocolo UDP;

    '''

    socketConstructor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    return socketConstructor

def createMessage():

    userMessage = input("Digite uma mensagem qualquer para enviar ao Socket Server: ")

    bytesToSend = str.encode(userMessage, "utf-8")

    return bytesToSend

def senderAndReceiverMessage(): # Construtor do Serviço/Servidor

    '''

        - socketConstructor é a variável que armazena o endereço IPV4 ao qual o serviço será instanciado
        - localhost é equivalente ao endereço IPV4 127.0.0.1, portanto, esse serviço só poderá receber requisições
        internas, ou seja, dentro da máquina que aloca este serviço. Para que este serviço possa receber
        requisições externas, deverá utilizar o IP 0.0.0.0 ou o endereço atual da sua interface de rede IPV4.
        - listeningPort é a variável que armazena o endereço da porta reservada para o serviço do servidor UDP
        - listeningPort deve ser do tipo inteiro, o que é uma exigência da função bind() durante a construção do serviço
        - Importante considerar que as portas equivalente e abaixo de 1024 são reservadas ao sistema operacional,
        portanto a escolha da porta considera essa premissa.
            Ao aplicar o método decode sobre a resposta obtida pelo Socket Server em bytes, para string.

            recvfrom() é uma função utilizada para receber os dados do socket. O 1024 passado
    como parâmetro nessa função, é o tamanho do buffer em bytes aceito pela função determinado por você, 
    pode utilizar valores maiores tanto quanto menores que este.

    '''

    socketConstructor = socketIPV4_UDP()

    bytesToSend = createMessage()

    socketConstructor.sendto(bytesToSend, (addressIPV4, listeningPort))

    responseFromServer = socketConstructor.recvfrom(1024)

    print(responseFromServer[0].decode("utf-8"))

def main():
    
    senderAndReceiverMessage()

if __name__ == '__main__':

    main()