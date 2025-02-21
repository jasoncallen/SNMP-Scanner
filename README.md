# SNMP Scanner

## Overview
This Python script performs SNMP GET requests on a list of IP addresses to retrieve information based on specified OIDs. The results are saved in a JSON file.

## Features
- Asynchronous SNMP GET requests using `pysnmp`
- Reads IPs and OIDs from text files
- Outputs results to a JSON file
- Error handling for SNMP communication failures

## Prerequisites
Before running this script, ensure you have the following:

- Python 3.7 or higher
- Required dependencies installed (see Installation section below)

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/jasoncallen/snmp-scanner.git
   cd snmp-scanner
   ```

2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
   The `requirements.txt` file should contain:
   ```
   pysnmp
   asyncio
   ```

## Usage

### 1. Prepare Input Files
- *Input file:** A text file (`input.txt`) containing IP addresses, one per line.
- **OID list file:** A text file (`oids.txt`) containing OIDs, one per line.

### 2. Run the Script
```sh
python snmp_scanner.py
```

### 3. Output
- The script will generate a JSON file (`output.json`) containing SNMP data for each IP.
- If an error occurs for an IP, it will be recorded in the JSON output.

## Example JSON Output
```json
[
    {
        "IP": "192.168.1.1",
        "OIDs": {
            "1.3.6.1.2.1.1.5.0": "Router-1",
            "1.3.6.1.2.1.2.2.1.2.1": "eth0"
        }
    },
    {
        "IP": "192.168.1.2",
        "Error": "Request timed out"
    }
]
```

## Configuration
- Modify `community` in `snmp_scanner.py` to change the SNMP community string (default: `public`).
- Update `input.txt` and `oids.txt` for different targets and queries.

## License
This project is licensed under the GNU V2.0 License.

