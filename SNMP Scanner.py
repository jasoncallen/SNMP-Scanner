import asyncio
import json
from pysnmp.hlapi.v3arch.asyncio import *

async def snmp_get(ip, community_string, oids):
    """
    Perform an SNMP GET request on the given OIDs for a single IP.

    Args:
        ip (str): The IP address of the SNMP-enabled device.
        community_string (str): The SNMP community string for authentication.
        oids (list): A list of OID strings to query.

    Returns:
        dict: A dictionary containing the IP address and retrieved OID values.
              If an error occurs, the dictionary includes an error message.
    """
    snmpEngine = SnmpEngine()
    
    iterator = get_cmd(
        snmpEngine,
        CommunityData(community_string, mpModel=0),
        await UdpTransportTarget.create((ip, 161)),
        ContextData(),
        *[ObjectType(ObjectIdentity(oid)) for oid in oids]
    )

    errorIndication, errorStatus, errorIndex, varBinds = await iterator

    result = {"IP": ip, "OIDs": {}}
    if errorIndication:
        result["Error"] = str(errorIndication)
    elif errorStatus:
        result["Error"] = f"{errorStatus.prettyPrint()} at {errorIndex and varBinds[int(errorIndex) - 1][0] or '?'}"
    else:
        for varBind in varBinds:
            key, value = [x.prettyPrint() for x in varBind]
            result["OIDs"][key] = value
    
    snmpEngine.close_dispatcher()
    return result

async def scan_snmp(ip_list_file, oid_list_file, output_file, community_string="public"):
    """
    Scan a list of IPs for SNMP information based on OIDs from a file and write results to a JSON file.

    Args:
        ip_list_file (str): Path to the file containing a list of IP addresses.
        oid_list_file (str): Path to the file containing a list of OIDs.
        output_file (str): Path to the JSON file where results will be stored.
        community_string (str, optional): The SNMP community string. Defaults to "public".

    Returns:
        None: The function writes the results to a JSON file.
    """
    with open(ip_list_file, 'r') as ip_file, open(oid_list_file, 'r') as oid_file:
        ips = [line.strip() for line in ip_file if line.strip()]
        oids = [line.strip() for line in oid_file if line.strip()]
    
    tasks = [snmp_get(ip, community_string, oids) for ip in ips]
    results = await asyncio.gather(*tasks)
    
    with open(output_file, 'w') as json_file:
        json.dump(results, json_file, indent=4)

if __name__ == "__main__":

    input_ips = "input.txt"  # File containing list of IPs
    input_oids = "oids.txt"  # File containing list of OIDs
    output_json = "output.json"  # Output JSON file
    community = "public"
    
    asyncio.run(scan_snmp(input_ips, input_oids, output_json, community))
