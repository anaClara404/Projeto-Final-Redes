import socket
import struct

def criar_payload(tipo_requisicao, identificador):
    req_res = 0  # 0000 para requisicao
    req_res_and_tipo = req_res | tipo_requisicao  # combina os campos
    payload = struct.pack(">BH", req_res_and_tipo, identificador)  # big-endian
    return payload

def calcular_checksum(
    cabecalho_ip,
    porta_origem,
    porta_destino,
    comprimento,
    checksum_provisorio,
    payload,
):
    
def criar_cabecalho_ip():

def criar_cabecalho_udp():

def criente_raw():

def main():
    ip_servidor = "15.228.191.109"
    porta_servidor = "5000"
    cliente_raw(ip_servidor, porta_servidor)