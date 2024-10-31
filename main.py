import binascii
import socket
from typing import List

# Constants for DNS
DNS_SERVER = ("8.8.8.8", 53)
RECURSION_DESIRED = 1
DNS_QUERY_ID = 43690  # Static ID for simplicity; in production, this should be randomized.

def create_flags(recursion_desired: int) -> str:
    """Generate DNS flags for a query packet."""
    return "{:04x}".format(int(f'0000_0000_0000_1_{recursion_desired}000_0000_0000', 2))

def create_packet(address: str) -> str:
    """
    Creates a DNS query packet for the specified address.
    
    :param address: The domain name to query (e.g., "example.com").
    :return: Hexadecimal string of the DNS query packet.
    """
    flags = create_flags(RECURSION_DESIRED)
    addr_parts = [f"{len(part):02x}{binascii.hexlify(part.encode()).decode()}" for part in address.split(".")]
    packet = f"{DNS_QUERY_ID:04x}{flags}000100000000" + "".join(addr_parts) + "0000010001"
    return packet

def decode_packet(packet: str) -> List[str]:
    """
    Decodes a DNS response packet.
    
    :param packet: The DNS response packet in hexadecimal format.
    :return: List of decoded answers from the DNS response.
    """
    res = []
    answer_count = int(packet[12:16], 16)
    answer_start = 32 + len("".join(parse_parts(packet, 24))) * 2 + 2

    for i in range(answer_count):
        atype = packet[answer_start + 4:answer_start + 8]
        rdlength = int(packet[answer_start + 20:answer_start + 24], 16)
        rddata = packet[answer_start + 24:answer_start + 24 + (rdlength * 2)]
        
        # Decode based on type; 0x0001 is for IPv4 addresses
        if atype == "0001":
            data = ".".join(str(int(rddata[j:j + 2], 16)) for j in range(0, len(rddata), 2))
        else:
            data = ".".join(binascii.unhexlify(part).decode('iso8859-1') for part in parse_parts(rddata, 0))
        
        res.append(f"Answer {i + 1}: {data}")
        answer_start += 24 + rdlength * 2

    return res

def parse_parts(message: str, start: int) -> List[str]:
    """
    Parse the parts of a DNS packet message.
    
    :param message: The DNS message in hexadecimal format.
    :param start: The starting index to parse.
    :return: List of hex parts parsed from the message.
    """
    parts = []
    while start < len(message):
        part_length = int(message[start:start + 2], 16)
        if part_length == 0:
            break
        start += 2
        parts.append(message[start:start + part_length * 2])
        start += part_length * 2
    return parts

def main():
    url = input("Enter the domain name:")
    message = create_packet(url)
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.sendto(binascii.unhexlify(message), DNS_SERVER)
            response, _ = sock.recvfrom(4096)
        decoded_response = decode_packet(binascii.hexlify(response).decode("utf-8"))
        for answer in decoded_response:
            print(answer)
    except (socket.error, binascii.Error) as e:
        print(f"Error during DNS query: {e}")

if __name__ == '__main__':
    main()
