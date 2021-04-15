# import binascii
# import socket
#
#
# def create_packet(address=""):
#     RD = 1
#     params = "{:04x}".format(
#         int(str(0) + str(0).zfill(4) + str(0) + str(0) + str(RD) + str(0) + str(0).zfill(3) + str(0).zfill(4), 2))
#
#     packet = ""
#     packet += "{:04x}".format(43690)
#     packet += params
#     packet += "{:04x}".format(1)
#     packet += "{:04x}".format(0)
#     packet += "{:04x}".format(0)
#     packet += "{:04x}".format(0)
#
#     addr_parts = address.split(".")
#     for part in addr_parts:
#         addr_len = "{:02x}".format(len(part))
#         addr_part = binascii.hexlify(part.encode())
#         packet += addr_len
#         packet += addr_part.decode()
#
#     packet += "00"
#     packet += "{:04x}".format(1)
#     packet += "{:04x}".format(1)
#
#     return packet
#
#
# def decode_packet(packet):
#     res = []
#
#     ANCOUNT = packet[12:16]
#     NSCOUNT = packet[16:20]
#     ARCOUNT = packet[20:24]
#
#     answer = 32 + (len("".join(parse_parts(packet, 24, [])))) + (len(parse_parts(packet, 24, [])) * 2) + 2
#
#     answer_number = max([int(ANCOUNT, 16), int(NSCOUNT, 16), int(ARCOUNT, 16)])
#     if answer_number > 0:
#         for i in range(answer_number):
#             if answer < len(packet):
#                 ATYPE = packet[answer + 4:answer + 8]
#                 RDLENGTH = int(packet[answer + 20:answer + 24], 16)
#                 RDDATA = packet[answer + 24:answer + 24 + (RDLENGTH * 2)]
#
#                 if ATYPE == "{:04x}".format(1):
#                     fetchedBytes = [RDDATA[i:i + 2] for i in range(0, len(RDDATA), 2)]
#                     data = ".".join(list(map(lambda x: str(int(x, 16)), fetchedBytes)))
#                 else:
#                     data = ".".join(
#                         map(lambda p: binascii.unhexlify(p).decode('iso8859-1'), parse_parts(RDDATA, 0, [])))
#
#                 answer = answer + 24 + (RDLENGTH * 2)
#
#             try:
#                 ATYPE
#             except NameError:
#                 None
#             else:
#                 res.append("# " + str(i + 1) + " : " + data)
#
#     return res
#
#
# def parse_parts(message, start, parts):
#     part_start = start + 2
#     part_len = message[start:part_start]
#
#     if len(part_len) == 0:
#         return parts
#
#     part_end = part_start + (int(part_len, 16) * 2)
#     parts.append(message[part_start:part_end])
#
#     if message[part_end:part_end + 2] == "00" or part_end > len(message):
#         return parts
#     else:
#         return parse_parts(message, part_end, parts)
#
#
# if __name__ == '__main__':
#     url = input("Enter your name address:")
#     message = create_packet(url)
#     message = message.replace(" ", "").replace("\n", "")
#
#     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     try:
#         sock.sendto(binascii.unhexlify(message), ("8.8.8.8", 53))
#         response, _ = sock.recvfrom(4096)
#     finally:
#         sock.close()
#
#     print(decode_packet(binascii.hexlify(response).decode("utf-8")))
