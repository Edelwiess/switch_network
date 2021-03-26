import socket


class DNSQuery:
    def __init__(self, data):
        self.data = data
        self.dominio = ''

        tipo = ((data[2]) >> 3) & 15  # Opcode bits
        print('tipo: ',tipo)
        if tipo == 0:  # Standard query
            ini = 12
            lon = (data[ini])
            print('lon: ',lon)
            while lon != 0:
                self.dominio += (data[ini + 1:ini + lon + 1]).decode('utf8') + '.'
                ini += lon + 1
                lon = (data[ini])

    def respuesta(self, ip):
        packet = b''
        if self.dominio:
            #print(type(self.data[:2]))
            #print(self.data[:2])
            packet += self.data[:2] + b"\x81\x80"
            packet += self.data[4:6] + self.data[4:6] + b'\x00\x00\x00\x00'  # Questions and Answers Counts
            packet += self.data[12:]  # Original Domain Name Question
            packet += b'\xc0\x0c'  # Pointer to domain name
            packet += b'\x00\x01\x00\x01\x00\x00\x00\x3c\x00\x04'  # Response type, ttl and resource data length -> 4 bytes
            #packet += (str.join('', map(lambda x: chr(int(x)), ip.split('.')))).encode('utf8')  # 4bytes of IP
            packet += bytes(map(int, ip.split('.')))


        return packet


if __name__ == '__main__':
    ip = input('input the ip and all queries all be solved to it')
    print('pyminifakeDNS:: dom.query. 60 IN A %s' % ip)


    udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udps.bind(('', 53))

    try:
        while 1:
            data, addr = udps.recvfrom(1024)
            print(data)
            p = DNSQuery(data)
            udps.sendto(p.respuesta(ip), addr)
            print('Respuesta: %s -> %s' % (p.dominio, ip))
    except KeyboardInterrupt:
        print('Finalizando')
        udps.close()
