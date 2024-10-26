import socket
import struct

# porta e ip do servidor
server_address = ('15.228.191.109', 50000)

# construir a mensagem
def build_message(req_res, tipo, identificador, tamanho=0):
    # 4 bits req/res, 4 bits tipo, 16 bits identificador
    # montando os 4 bits req/res e 4 bits tipo em um byte
    req_res_tipo = (req_res << 4) | tipo
    payload = struct.pack('!BHB', req_res_tipo, identificador, tamanho)
    # >BHB -> network=big endian, 1 byte (tipo e requisicao), 2 Bytes (identificador), 1 byte (tamanho)
    return payload

# enviar a requisição e receber a resposta
def send_request(server_address, payload):
    # socket UDP
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(payload, server_address)
        response, _ = sock.recvfrom(1024)
        return response
    
# interpretar a resposta recebida
def interpret_response(response):
    req_res_tipo, identificador, tamanho = struct.unpack('!BHB', response[:4])
    req_res = (req_res_tipo >> 4) & 0x0F  # extraindo os 4 bits de req/res
    tipo = req_res_tipo & 0x0F            # extraindo os 4 bits de tipo

    # print(f"Resposta do Servidor:")
    # print(f"Req/Res: {req_res}")
    # print(f"Tipo: {tipo}")
    # print(f"Identificador: {identificador}")
    # print(f"Tamanho da resposta: {tamanho}")

# menu para o cliente
while True:
    print("\n1. Solicitar data e hora")
    print("2. Solicitar frase motivacional")
    print("3. Solicitar quantidade de respostas emitidas")
    print("4. Sair")
    
    choice = int(input("Escolha uma opção: "))

    if choice == 1:
        # requisição de data e hora (req/res = 0000, tipo = 0000)
        message = build_message(req_res=0, tipo=0, identificador=1234)
        response = send_request(server_address, message)
        interpret_response(response)
        date_time = response[4:].decode('utf-8').strip()
        print(date_time)
        
    elif choice == 2:
        # requisição de frase motivacional (req/res = 0000, Tipo = 0001)
        message = build_message(req_res=0, tipo=1, identificador=1235)
        response = send_request(server_address, message)
        interpret_response(response)
        motivational_message = response[4:].decode('utf-8').strip()
        print(motivational_message)
        
    elif choice == 3:
        # requisição de quantidade de respostas (req/res = 0000, tipo = 0010)
        message = build_message(req_res=0, tipo=2, identificador=1236)
        response = send_request(server_address, message)
        interpret_response(response)
        
        request_number_bytes = response[4:]
        request_number = int.from_bytes(request_number_bytes[:4], byteorder='big')
        print(f"Quantidade de requisições ao servidor: {request_number}") 
        
    elif choice == 4:
        print("Encerrando o cliente...")
        break
    
    else:
        print("Opção inválida. Tente novamente.")