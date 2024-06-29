import socket
import struct
import threading

def parse_dns_request(data):
    try:
        header = struct.unpack('!HHHHHH', data[:12])
        transaction_id = header[0]
        questions = header[2]
        
        query_parts = []
        idx = 12
        while True:
            length = data[idx]
            if length == 0:
                break
            part = data[idx+1:idx+1+length].decode('utf-8')
            query_parts.append(part)
            idx += 1 + length
        query_name = '.'.join(query_parts)
        
        query_type, query_class = struct.unpack('!HH', data[idx+1:idx+5])
        
        return {
            'transaction_id': transaction_id,
            'questions': questions,
            'query_name': query_name,
            'query_type': query_type,
            'query_class': query_class
        }
    except Exception as e:
        return {'error': str(e)}

def create_dns_response(request):
    transaction_id = request['transaction_id']
    flags = 0x8180  # Standard query response, No error
    questions = request['questions']
    answer_rrs = 1
    authority_rrs = 0
    additional_rrs = 0

    header = struct.pack('!HHHHHH', transaction_id, flags, questions, answer_rrs, authority_rrs, additional_rrs)

    # Query section
    query = b''
    for part in request['query_name'].encode('ascii').split(b'.'):
        query += struct.pack('B', len(part)) + part
    query += b'\x00'  # End of domain name
    query += struct.pack('!HH', request['query_type'], request['query_class'])

    # Answer section
    answer = b'\xc0\x0c'  # Pointer to domain name
    answer += struct.pack('!HHIH', 1, 1, 300, 4)  # TYPE A, CLASS IN, TTL 300, Data length 4
    answer += socket.inet_aton('137.137.137.137')

    return header + query + answer

def handle_dns_request(data, addr, socket):
    request = parse_dns_request(data)
    if 'error' not in request:
        response = create_dns_response(request)
        socket.sendto(response, addr)
        print(f"Responded to query for {request['query_name']} from {addr[0]}:{addr[1]}")
    else:
        print(f"Error parsing request from {addr[0]}:{addr[1]}: {request['error']}")

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = ('0.0.0.0', 53)
    print(f"Starting fake DNS server on UDP port 53")
    sock.bind(server_address)
    
    while True:
        try:
            data, addr = sock.recvfrom(512)  # DNS typically uses 512 byte messages
            threading.Thread(target=handle_dns_request, args=(data, addr, sock)).start()
        except KeyboardInterrupt:
            print("\nShutting down the server...")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
    
    sock.close()

if __name__ == "__main__":
    main()
