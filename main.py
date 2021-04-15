import binascii
import socket


def create_packet(address=""):
    RD = 0
    params = "{:04x}".format(
        int(str(0) + str(0).zfill(4) + str(0) + str(0) + str(RD) + str(0) + str(0).zfill(3) + str(0).zfill(4), 2))

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


def decode_packet(message):
    res = []

    QDCOUNT = message[8:12]
    ANCOUNT = message[12:16]
    NSCOUNT = message[16:20]
    ARCOUNT = message[20:24]

    # Question section
    QUESTION_SECTION_STARTS = 24
    question_parts = parse_parts(message, QUESTION_SECTION_STARTS, [])

    QTYPE_STARTS = QUESTION_SECTION_STARTS + (len("".join(question_parts))) + (len(question_parts) * 2) + 2
    QCLASS_STARTS = QTYPE_STARTS + 4

    # Answer section
    ANSWER_SECTION_STARTS = QCLASS_STARTS + 4

    NUM_ANSWERS = max([int(ANCOUNT, 16), int(NSCOUNT, 16), int(ARCOUNT, 16)])
    if NUM_ANSWERS > 0:
        for ANSWER_COUNT in range(NUM_ANSWERS):
            if ANSWER_SECTION_STARTS < len(message):
                ATYPE = message[ANSWER_SECTION_STARTS + 4:ANSWER_SECTION_STARTS + 8]
                RDLENGTH = int(message[ANSWER_SECTION_STARTS + 20:ANSWER_SECTION_STARTS + 24], 16)
                RDDATA = message[ANSWER_SECTION_STARTS + 24:ANSWER_SECTION_STARTS + 24 + (RDLENGTH * 2)]

                if ATYPE == "{:04x}".format(1):
                    octets = [RDDATA[i:i + 2] for i in range(0, len(RDDATA), 2)]
                    RDDATA_decoded = ".".join(list(map(lambda x: str(int(x, 16)), octets)))
                else:
                    RDDATA_decoded = ".".join(
                        map(lambda p: binascii.unhexlify(p).decode('iso8859-1'), parse_parts(RDDATA, 0, [])))

                ANSWER_SECTION_STARTS = ANSWER_SECTION_STARTS + 24 + (RDLENGTH * 2)

            try:
                ATYPE
            except NameError:
                None
            else:
                res.append("# ANSWER " + str(ANSWER_COUNT + 1) + ":" + RDDATA_decoded)

    return "\n".join(res)




def parse_parts(message, start, parts):
    part_start = start + 2
    part_len = message[start:part_start]

    if len(part_len) == 0:
        return parts

    part_end = part_start + (int(part_len, 16) * 2)
    parts.append(message[part_start:part_end])

    if message[part_end:part_end + 2] == "00" or part_end > len(message):
        return parts
    else:
        return parse_parts(message, part_end, parts)


if __name__ == '__main__':
    url = input("Enter your name address:")
    message = create_packet(url)
    message = message.replace(" ", "").replace("\n", "")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.sendto(binascii.unhexlify(message), ("198.41.0.4", 53))
        response, _ = sock.recvfrom(4096)
    finally:
        sock.close()

    print("Response:\n" + decode_packet(binascii.hexlify(response).decode("utf-8")))
