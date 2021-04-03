import binascii
import socket


def build_message(address=""):
    params = "{:04x}".format(
        int(str(0) + str(0).zfill(4) + str(0) + str(0) + str(1) + str(0) + str(0).zfill(3) + str(0).zfill(4), 2))

    packet = ""
    packet += "{:04x}".format(43690)
    packet += params
    packet += "{:04x}".format(1)
    packet += "{:04x}".format(0)
    packet += "{:04x}".format(0)
    packet += "{:04x}".format(0)

    addr_parts = address.split(".")
    for part in addr_parts:
        addr_len = "{:02x}".format(len(part))
        addr_part = binascii.hexlify(part.encode())
        packet += addr_len
        packet += addr_part.decode()

    packet += "00"
    packet += "{:04x}".format(1)
    packet += "{:04x}".format(1)

    return packet


def decode_message(packet):
    res = []
    question = parse_parts(packet, 24, [])

    Answer = 34 + (len("".join(question))) + (len(question) * 2)

    NUM_ANSWERS = max([int(packet[12:16], 16), int(packet[16:20], 16), int(packet[20:24], 16)])
    if NUM_ANSWERS > 0:
        for ANSWER_COUNT in range(NUM_ANSWERS):
            if Answer < len(packet):
                ATYPE = packet[Answer + 4:Answer + 8]
                RDLENGTH = int(packet[Answer + 20:Answer + 24], 16)
                RDDATA = packet[Answer + 24:Answer + 24 + (RDLENGTH * 2)]

                if ATYPE == "{:04x}".format(1):
                    octets = [RDDATA[i:i + 2] for i in range(0, len(RDDATA), 2)]
                    data = ".".join(list(map(lambda x: str(int(x, 16)), octets)))
                else:
                    data = ".".join(
                        map(lambda p: binascii.unhexlify(p).decode('iso8859-1'), parse_parts(RDDATA, 0, [])))

                Answer = Answer + 24 + (RDLENGTH * 2)

            try:
                ATYPE
            except NameError:
                None
            else:
                res.append(data)
    else:
        print("No Answer")

    return "\n".join(res)


def parse_parts(packet, start, parts):
    part_start = start + 2
    part_len = packet[start:part_start]

    if len(part_len) == 0:
        return parts

    part_end = part_start + (int(part_len, 16) * 2)
    parts.append(packet[part_start:part_end])

    if packet[part_end:part_end + 2] == "00" or part_end > len(packet):
        return parts
    else:
        return parse_parts(packet, part_end, parts)


if __name__ == '__main__':
    url = input('Enter your name address:')
    message = build_message(url)
    message = message.replace(" ", "").replace("\n", "")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        sock.sendto(binascii.unhexlify(message), ("8.8.8.8", 53))
        response, _ = sock.recvfrom(4096)
    finally:
        sock.close()

    print("Response:\n" + decode_message(binascii.hexlify(response).decode("utf-8")))
