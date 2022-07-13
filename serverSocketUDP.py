# coding: utf-8
#!/usr/bin/python3

from requires import *

def solveHostnameServer(servername):

    '''
        Utilizando a lib socket, a função solveHostnameServer recebe como parâmetro
    um dos subdomínios disponíveis em *.ntp.br da função getNTPServerInformations()
    e utiliza-se a função gethostbyname disponível em socket para tentar resolver esse
    subdomínio e obter seu endereço público.

    '''
    
    hostname= socket.gethostname()
    IPAddr= socket.gethostbyname(servername)

    return IPAddr

def getNTPServerInformations():

    '''

        Utiliza-se a lib NTPTimeNow para consultar os diversos subdomínios disponíveis
    em ntp.br para tentar obter a hora atual. A função percorre a lista poolservers e
    quando um dos endereços disponíveis retornar uma resposta válida, a iteração do laço
    será interrompida e retornará um dicionário/objeto contendo o nome do subdomínio,
    o IP público do subdomínio e a hora atual disponibilizada pela consulta ao serviço
    disponível em *.ntp.br. Caso um endereço esteja incorreto ou indisponível, existe um
    tratamento genérico a exceção que retornará o valor como None, que servirá como base
    em uma condicional(if) de validação.
        O trecho do código ntp_now": "%s" % now.ntp_now()" existente no dicionário "dictData",
    converte a data/hora atual de datetime para string.

    '''

    poolservers = [
    'a.st1.ntp.br',
    'b.st1.ntp.br',
    'c.st1.ntp.br',
    'd.st1.ntp.br',
    'a.ntp.br',
    'b.ntp.br',
    'c.ntp.br',
    'gps.ntp.br',
    ]

    for servername in poolservers:

        try:

            now = NTPTimeNow(poolservers= servername)

            serverAddress = solveHostnameServer(servername)

            dictData = {
            "servername": servername,
            "serverAddress": serverAddress,
            "ntp_now": "%s" % now.ntp_now(),
            }

            return dictData

        except Exception as Error:

            print(Error)

            return None

def socketIPV4_UDP(): # Construtor/Parametrização do Socket

    '''

        - AF_INET especifica que o socket existirá sob o protocolo IPV4;
        - SOCK_DGRAM especifica que o socket será construído sob o protocolo UDP;

    '''

    socketConstructor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    return socketConstructor

def addressingSocketServer(): # Construtor do Serviço/Servidor

    '''

        - socketConstructor chama a função que constrói o socket.
        - localhost é equivalente ao endereço IPV4 127.0.0.1, portanto, esse serviço só poderá receber requisições
        internas, ou seja, dentro da máquina que aloca este serviço. Para que este serviço possa receber
        requisições externas, deverá utilizar o IP 0.0.0.0 ou o endereço atual da sua interface de rede IPV4.
        - listeningPort é a variável que armazena o endereço da porta reservada para o serviço do servidor UDP
        - listeningPort deve ser do tipo inteiro, o que é uma exigência da função bind().
        - Importante considerar que as portas equivalente e abaixo de 1024 são reservadas ao sistema operacional,
        portanto a escolha da porta considera essa premissa.

    '''

    socketConstructor = socketIPV4_UDP()

    socketConstructor.bind((addressIPV4, listeningPort))

    return socketConstructor

def dataReceiver(): # Construtor da "escuta" que receberá a requisição/solicitação do Client


    '''

        recvfrom() é uma função utilizada para receber os dados do socket. O 1024 passado
    como parâmetro nessa função, é o tamanho do buffer em bytes aceito pela função determinado por você, 
    pode utilizar valores maiores tanto quanto menores que este.
        bytesAddressPair irá gerar uma tupla, contendo a mensagem recebida do Client e o endereço de origem da requisição.
        Ao aplicar o método encode (aplicado na variável bytesToSend) sobre a mensagem a ser enviada pelo server, convertemos
    a mensagem do tipo string para bytes, sendo esta uma exigência para que a função sendto possa ser capaz em enviar o socket
    para a origem.
    '''

    socketConstructor = addressingSocketServer()
    
    bytesAddressPair = socketConstructor.recvfrom(1024)

    message = bytesAddressPair[0]

    address = bytesAddressPair[1]

    return socketConstructor, bytesAddressPair

def ReplySender(): # Construtor do recurso que responderá a requisição do Cliente
    
    socketConstructor, bytesAddressPair = dataReceiver()

    getTimeNow = getNTPServerInformations()

    responseData = f"{getTimeNow['serverAddress']} {addressIPV4} {getTimeNow['ntp_now']}"

    bytesToSend = str.encode(responseData, "utf-8")

    socketConstructor.sendto(bytesToSend, bytesAddressPair[1])

def exitServer(): # Função de Interrupção do Script.

    '''

        A instrução sys.exit() ordena que o processo seja encerrado pelo sistema.

    '''

    sys.exit()

def main(): # Função Principal do Script.

    '''

        A função main() chama a função ReplySender().


    '''

    ReplySender()

if __name__ == '__main__': # Condicional que verifica se o arquivo fora invocado diretamente para que as instruções abaixo sejam executadas.

    '''

        essa condicional (if __name__ == '__main__':) implica em como o seu script é invocado, 
    por exemplo: se você rodar esse arquivo diretamente (python serverSocketUDP.py) em um terminal, 
    tudo que está após esse if, será executado. Caso você importe o arquivo serverSocketUDP.py 
    em um outro arquivo .py, nada acontecerá, pois nenhuma função está sendo chamada antes 
    dessa condicional. Se quiser simplificar, você pode tirar essas próximas linhas abaixo,
    remover a indentação após o if e apagar a linha inteira de if __name__ == '__main__':.

        Criado um loop infinito (while True:) para simular um serviço em execução constante, aguardando por requisições (inputs)
    socket UDP de um host(Client) qualquer. Note que após a chamada a função main() que é a função principal
    do serviço, incluiu-se a chamada a função exitServer() para encerrar a execução do serviço.
        Caso opte para deixar o serviço em loop constante, basta remover ou comentar a chamada a função exitServer() com um # no início da linha.
        Se precisar que o seu serviço seja alcançado em uma rede local, altere o valor da variável
    addressIPV4 para 0.0.0.0 ou o seu IPv4 (pode obter seu IP abrindo o CMD e digitar o comando ipconfig no Windows, ou ifconfig no Linux),
    que geralmente será algo como 192.168.0.*.

        Note que algumas strings começam como f"um texto qualquer {variavel}".
    Esse "f" ao início de uma string é uma espécie de formatador para que possa incluir o valor 
    das variáveis diretamente na string, utilizando {} e o nome da variável dentro do {}.
    Outro caso de formatador que utilizei em string foi o "%s" % variavel. Ambos tem o mesmo objetivo,
    incluir o valor da variável no meio de uma string, transformando qualquer valor em texto.
        

        Funções Construídas:

            - Nome: solveHostnameServer, Parâmetros: servername, Funcionalidade: resolver o endereço passado por parâmetro.
            - Nome: getNTPServerInformations, Parâmetros: Nenhum, Funcionalidade: consulta *.ntp.br para obter a data/hora atual.
            - Nome: socketIPV4_UDP, Parâmetros: Nenhum, Funcionalidade: Construtor/Parametrização do Socket.
            - Nome: addressingSocketServer, Parâmetros: Nenhum, Funcionalidade: # Construtor do Serviço/Servidor.
            - Nome: dataReceiver, Parâmetros: Nenhum, Funcionalidade: Construtor da "escuta" que receberá a requisição/solicitação do Client.
            - Nome: ReplySender, Parâmetros: Nenhum, Funcionalidade: Construtor do recurso que responderá a requisição do Cliente
            - Nome: exitServer, Parâmetros: Nenhum, Funcionalidade: Função que encerra o Script se invocado.
            - Nome: main, Parâmetros: Nenhum, Funcionalidade: Função que chama a função ReplySender()
    '''

    print(f"Socket Server Inicializado para o endereço {addressIPV4}:{listeningPort}")

    while True:

        main()
        #exitServer()