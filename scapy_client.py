from scapy.all import IP, UDP, Raw, sr1
import struct
import time

def built_message(tipo_requisicao, identificador):
    # 1 byte req_res e tipo, 2 bytes identificador
    req_res = 0  # 0000 para requisição
    req_res_tipo = (req_res << 4) | tipo_requisicao  # 4 bits para req/res e 4 para tipo
    # !BHB -> network=big endian, 1 byte (tipo e requisicao), 2 Bytes (identificador), 1 byte (tamanho)
    mensagem = struct.pack("!BH", req_res_tipo, identificador)
    return mensagem

# enviar a requisição e receber a resposta
def send_request(server_ip, server_port, tipo_requisicao):
    # gera um id com base no timestamp
    identificador = int(time.time()) & 0xFFF # mantém o id de 2 bytes

    # constrói a mensagem conforme o formato especificado
    mensagem = built_message(tipo_requisicao, identificador)

    # cria o pacote IP e UDP e adiciona a carga útil (mensagem)
    pacote = IP(dst=server_ip) / UDP(dport=server_port) / Raw(load=mensagem)

    # envia o pacote e aguarda a resposta
    resposta = sr1(pacote, timeout=2)

    if resposta and Raw in resposta:
        # extrai e retorna a carga útil da resposta
        return resposta[Raw].load
    else:
        return None

