import binascii
import socket

def create_packet(address=""):
    """
    Create a DNS query packet.
    """
    RECURSION_DESIRED = 1
    FLAGS = "{:04x}".format(int(f'00{"0"*4}0{"0"*4}{RECURSION_DESIRED}0{"0"*3}{"0"*4}', 2))

    addr_parts = [f"{len(part):02x}{binascii.hexlify(part.encode()).decode()}" for part in address.split(".")]

    packet = (f"{43690:04x}{FLAGS}000100000000" + "".join(addr_parts) + "0000010001")
    return packet

def decode_packet(packet):
    """
    Decode a DNS response packet.
    """
    res = []
    answer_start = 32 + len("".join(parse_parts(packet, 24))) * 2 + 2
    answer_count = max([int(packet[i:i+4], 16) for i in (12, 16, 20)])

    for _ in range(answer_count):
        ATYPE = packet[answer_start + 4:answer_start + 8]
        RDLENGTH = int(packet[answer_start + 20:answer_start + 24], 16)
        RDDATA = packet[answer_start + 24:answer_start + 24 + (RDLENGTH * 2)]

        if ATYPE == "{:04x}".format(1):
            fetchedBytes = [RDDATA[i:i + 2] for i in range(0, len(RDDATA), 2)]
            data = ".".join(str(int(byte, 16)) for byte in fetchedBytes)
        else:
            data = ".".join(binascii.unhexlify(part).decode('iso8859-1') for part in parse_parts(RDDATA, 0))

        res.append(f"# {_ + 1} : {data}")
        answer_start += 24 + RDLENGTH * 2

    return res

def parse_parts(message, start):
    """
    Parse parts of the DNS packet.
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

if __name__ == '__main__':
    url = input("Enter your name address:")
    message = create_packet(url)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(binascii.unhexlify(message), ("8.8.8.8", 53))
        response, _ = sock.recvfrom(4096)

    print(decode_packet(binascii.hexlify(response).decode("utf-8")))
