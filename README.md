# Fake DNS Server

This project implements a simple fake DNS server in Python. It responds to all DNS queries by resolving them to the IP address 137.137.137.137, regardless of the domain name requested.

## Features

- Listens for DNS queries on UDP port 53
- Parses incoming DNS requests
- Responds to all queries with a fixed IP address (137.137.137.137)
- Handles multiple requests simultaneously using threading
- Logs queries and responses

## Requirements

- Python 3.6+
- Administrator/root privileges (to bind to port 53)

## Installation

1. Clone this repository:
2. No additional Python packages are required as this script uses only built-in modules.

## Usage

1. Run the script with administrator/root privileges:

On Linux/macOS:

sudo python3 fakedns.py

2. The server will start and listen for DNS queries on UDP port 53.

3. Test the server using nslookup or dig:
   
nslookup www.example.com 127.0.0.1

dig @127.0.0.1 www.example.com

Replace `127.0.0.1` with the IP address of the machine running the script if different.

## Configuration

The IP address that all queries resolve to (currently set to 137.137.137.137) can be changed by modifying the `create_dns_response` function in the script.

## Limitations

- This is a simplified DNS server and doesn't handle all types of DNS queries or follow all DNS protocols.
- It's meant for educational and testing purposes only.
- Using this in a production environment or on a network you don't control could cause issues with normal DNS resolution.

## Contributing

Contributions, issues, and feature requests are welcome.


## Disclaimer

This tool is for educational purposes only. Use responsibly and only on networks and systems you own or have permission to test.
