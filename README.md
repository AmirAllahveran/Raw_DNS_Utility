# DNS Query Tool

This project is a Python-based DNS query tool that creates and sends DNS query packets to a specified DNS server and decodes the server’s response. It’s a foundational implementation for learning about DNS packet structure and network programming with Python.

## Features

- Constructs DNS query packets based on the input domain name.
- Sends queries to a DNS server using UDP.
- Decodes and displays responses, including IP addresses and other resource data.
- Demonstrates core concepts in network programming and DNS packet handling.

## Requirements

- Python 3.7 or later

## Setup

Clone the repository:

```bash
git clone https://github.com/yourusername/dns-query-tool.git
cd dns-query-tool
```

## Usage

1. Run the script:

   ```bash
   python dns_query.py
   ```

2. Enter a domain name when prompted:

   ```text
   Enter the domain name: example.com
   ```

3. The script will send a DNS query to `8.8.8.8` (Google’s public DNS server) and print the IP address or other information in the response.

### Example Output

```text
Enter the domain name: example.com
Answer 1: 93.184.216.34
```

## Code Structure

- **`create_packet(address: str) -> str`**: Constructs a DNS query packet for the provided address.
- **`decode_packet(packet: str) -> List[str]`**: Decodes a DNS response packet, extracting IP addresses or other data.
- **`parse_parts(message: str, start: int) -> List[str]`**: Helper function to parse DNS packet sections.

## Error Handling

The script includes basic error handling for network issues and encoding errors to ensure stability during execution.

## Customization

- **DNS Server**: By default, the script uses Google’s public DNS server (`8.8.8.8`). You can change this in the code by modifying the `DNS_SERVER` constant.
- **Query ID**: A static ID is used for DNS query packets (`43690`), but this can be randomized for more robust querying in production.

## Learning Resources

If you’re interested in learning more about DNS and network programming, here are a few helpful links:

- [DNS Resource Records](https://en.wikipedia.org/wiki/List_of_DNS_record_types)
- [Python socket module documentation](https://docs.python.org/3/library/socket.html)
- [RFC 1035: DNS Protocol](https://tools.ietf.org/html/rfc1035)

## Contributing

Contributions are welcome! If you have ideas for improvements or find a bug, please open an issue or submit a pull request.
