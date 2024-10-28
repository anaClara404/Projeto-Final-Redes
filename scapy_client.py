# Ana Clara Ferreira Epaminondas, Danylo Rodrigues Nunes, Giovanni Mendes Costa

from scapy.all import *
import struct

# construir a mensagem do cliente
def construir_mensagem(req_res, tipo_requisicao, identificador, tamanho):
    # 4 bits para req/res e 4 bits para tipo de requisição
    req_res_tipo = (req_res << 4) | tipo_requisicao
    # montando os 4 bits req/res e 4 bits tipo em um byte, e empacotando os dados
    payload = struct.pack('!BHB', req_res_tipo, identificador, tamanho)
    # !BHB -> network=big endian, 1 byte (req/res e tipo), 2 bytes (identificador), 1 byte (tamanho)
    return payload

# Função principal do cliente
def cliente_scapy():
    # obtém o IP do host
    src_ip = socket.gethostbyname(socket.gethostname())  # IP de origem dinâmico
    dst_ip = "15.228.191.109"  # IP do servidor
    src_port = 59155  # porta de origem do cliente
    dst_port = 50000   # porta de destino do servidor

    while True:
        # menu de opções para o usuário
        print("\n1. Solicitar data e hora")
        print("2. Solicitar mensagem motivacional")
        print("3. Solicitar quantidade de respostas emitidas")
        print("4. Sair")

        escolha = input("Escolha uma opção (1-4): ")

        if escolha == "4":
            print("Encerrando o cliente...")
            break

        # determina se é uma requisição (0) ou resposta (1) e tipo de requisição
        req_res = 1 if escolha == "3" else 0 
        tipo_requisicao = int(escolha) - 1  # converte a escolha do usuário em tipo de requisição
        identificador = 1236 
        tamanho = 10  # ex de tamanho do payload

        # monta o payload
        payload = construir_mensagem(req_res, tipo_requisicao, identificador, tamanho)

        # monta o pacote udp com os campos do cabeçalho
        udp_header = UDP(sport=src_port, dport=dst_port, len=8 + len(payload), chksum=0)
        
        # calcula o checksum UDP com um cabeçalho UDP zerado
        pseudo_header = struct.pack('!4s4sBBH', 
                                    socket.inet_aton(src_ip),  # IP de origem
                                    socket.inet_aton(dst_ip),  # IP de destino
                                    0,
                                    socket.IPPROTO_UDP,  # protocolo UDP
                                    udp_header.len)  # comprimento do cabeçalho
        checksum_data = pseudo_header + bytes(udp_header) + payload  # combina todos os dados para calcular o checksum
        
        # se o comprimento for ímpar, adiciona um byte de padding
        if len(checksum_data) % 2 != 0:
            checksum_data += b'\x00'  # adiciona padding se necessário

        checksum = 0
        for i in range(0, len(checksum_data), 2):
            # monta palavras de 16 bits para calcular o checksum
            word = (checksum_data[i] << 8) + checksum_data[i + 1]
            checksum += word
        checksum = (checksum >> 16) + (checksum & 0xFFFF)  # reduz para 16 bits
        checksum += (checksum >> 16)  # adiciona o carry
        udp_header.chksum = ~checksum & 0xFFFF  # complemento de um

        # monta o pacote IP/UDP completo
        pacote = IP(src=src_ip, dst=dst_ip) / udp_header / Raw(load=payload)

        # envia o pacote e aguarda a resposta
        resposta = sr1(pacote, timeout=2)  # espera uma resposta por 2 seg

        if resposta:
            if escolha == "3":
                quantidade_requisicoes = struct.unpack("!H", resposta[Raw].load[:2])[0]
                print("Quantidade de requisições ao servidor:", quantidade_requisicoes)
            else:
                # exibe a resposta de forma legível
                # pula os primeiros 4 bytes 
                mensagem = resposta[Raw].load[4:].decode('latin-1')  # decodifica a resposta recebida
                print(mensagem)
        else:
            print("Sem resposta do servidor.")

# chama a função p/ executar o cliente
cliente_scapy()   