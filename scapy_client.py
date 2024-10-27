from scapy.all import *
import struct
import time

# Função para construir a mensagem do cliente
def construir_mensagem(tipo_requisicao, identificador):
    # Exemplo de payload com tipo de requisição e identificador
    payload = struct.pack("!BH", tipo_requisicao, identificador)
    return payload

# Função principal do cliente
def cliente_scapy():
    src_ip = "192.168.0.104"  # IP de origem
    dst_ip = "15.228.191.109"  # IP do servidor
    src_port = 49455
    dst_port = 50000

    while True:
        print("\n1. Solicitar data e hora")
        print("2. Solicitar mensagem motivacional")
        print("3. Solicitar quantidade de respostas emitidas")
        print("4. Sair")

        escolha = input("Escolha uma opção (1-4): ")

        if escolha == "4":
            print("Encerrando o cliente...")
            break

        tipo_requisicao = int(escolha) - 1
        identificador = 1236  # Exemplo de identificador para o pedido
        payload = construir_mensagem(tipo_requisicao, identificador)

        # Cria o pacote UDP com campos manualmente definidos
        udp_header = UDP(sport=src_port, dport=dst_port, len=8 + len(payload), chksum=0)
        
        # Calcula o checksum UDP com um cabeçalho UDP zerado
        pseudo_header = struct.pack('!4s4sBBH', 
                                    socket.inet_aton(src_ip), 
                                    socket.inet_aton(dst_ip), 
                                    0, 
                                    socket.IPPROTO_UDP, 
                                    udp_header.len)
        checksum_data = pseudo_header + bytes(udp_header) + payload
        
        # Se o comprimento for ímpar, adicione um byte de padding
        if len(checksum_data) % 2 != 0:
            checksum_data += b'\x00'

        checksum = 0
        for i in range(0, len(checksum_data), 2):
            word = (checksum_data[i] << 8) + checksum_data[i + 1]
            checksum += word
        checksum = (checksum >> 16) + (checksum & 0xFFFF)
        checksum += (checksum >> 16)
        udp_header.chksum = ~checksum & 0xFFFF

        # Monta o pacote IP/UDP completo com o payload
        pacote = IP(src=src_ip, dst=dst_ip) / udp_header / Raw(load=payload)

        # Envia o pacote e aguarda a resposta
        resposta = sr1(pacote, timeout=2)

        if resposta:
            if escolha == "3":
                # Interpreta a resposta como um número (unsigned short de 2 bytes, por exemplo)
                quantidade_requisicoes = struct.unpack("!H", resposta[Raw].load[:2])[0]
                print("Quantidade de requisições ao servidor:", quantidade_requisicoes)
            else:
            # Exibe a resposta de forma legível
            # Exemplo de como pular os primeiros 4 bytes, ajuste conforme necessário
                mensagem = resposta[Raw].load[4:].decode('latin-1')
                print(mensagem)

        else:
            print("Sem resposta do servidor.")

# Executa o cliente
cliente_scapy()

