import sys
import re

def validate_ip(ip):
    octets = ip.split('.')
    binary_octets = []
    message = ""
    
    # Check if there are 4 octets
    if len(octets) != 4:
        return "INVALID", "Invalid IP: IP address must consist of four octets separated by periods."
    
    for octet in octets:
        # Check if each octet is a number between 0 and 255
        if not octet.isdigit() or not (0 <= int(octet) <= 255):
            binary_octets.append("INVALID")
        else:
            # Convert octet to binary and ensure it's 8 bits long
            binary_octet = bin(int(octet))[2:].zfill(8)
            binary_octets.append(binary_octet)
    
    binary_ip = '.'.join(binary_octets)
    return "INVALID" if "INVALID" in binary_octets else "VALID", f"{binary_ip}"

def validate_subnet_mask(mask):
    octets = mask.split('.')
    binary_octets = []

    # Check if there are 4 octets
    if len(octets) != 4:
        return "INVALID", "Invalid subnet mask: Subnet mask must consist of four octets separated by periods."

    for octet in octets:
        # Check if each octet is a number between 0 and 255
        if not octet.isdigit() or not (0 <= int(octet) <= 255):
            binary_octets.append("INVALID")
        else:
            # Convert octet to binary and ensure it's 8 bits long
            binary_octet = bin(int(octet))[2:].zfill(8)
            binary_octets.append(binary_octet)

    binary_mask = ''.join(binary_octets)

    # Ensure it's a valid subnet mask
    if re.match(r'^(1+)(0+)$', binary_mask):
        return "VALID", '.'.join([binary_octet for binary_octet in binary_octets])
    else:
        # Construct the message for invalid subnet mask
        invalid_message = '.'.join([binary_octet if octet.isdigit() and (0 <= int(octet) <= 255) else 'INVALID' for octet, binary_octet in zip(octets, binary_octets)])
        return "INVALID", invalid_message


def interactive_mode():
    # Prompt for IP address
    ip = input("Enter IP address: ")
    ip_status, ip_message = validate_ip(ip)
    print(f"{ip}\n   {ip_message}.   {ip_status}")
    
    # Prompt for subnet mask
    subnet_mask = input("Enter subnet mask: ")
    subnet_status, subnet_message = validate_subnet_mask(subnet_mask)
    print(f"{subnet_mask}\n   {subnet_message}.   {subnet_status}")


def batch_mode_ip(input_file, output_file):
    try:
        with open(input_file, 'r') as f:
            ips = f.readlines()
        
        with open(output_file, 'w') as f:
            for ip in ips:
                status, message = validate_ip(ip.strip())
                f.write(f"{ip.strip()}\n   {message}.   {status}\n")
    except FileNotFoundError:
        pass


def batch_mode_subnet_mask(input_file, output_file):
    try:
        with open(input_file, 'r') as f:
            masks = f.readlines()
        
        with open(output_file, 'w') as f:
            for mask in masks:
                status, message = validate_subnet_mask(mask.strip())
                f.write(f"{mask.strip()}\n   {message}.   {status}\n")
    except FileNotFoundError:
        pass


# Parse command-line arguments
if len(sys.argv) > 1:
    mode = sys.argv[1]
    if mode == 'interactive':
        interactive_mode()
    elif mode == 'batch_ips':
        batch_mode_ip('batch_ips.txt', 'batch_ip_validation_output.txt')
    elif mode == 'batch_subnet_masks':
        batch_mode_subnet_mask('batch_subnet_masks.txt', 'batch_subnet_mask_validation_output.txt')
else:
    print("Usage: python script_name.py <mode>")
    print("Available modes:")
    print("  interactive: Run in interactive mode")
    print("  batch_ips: Run batch mode for IP addresses")
    print("  batch_subnet_masks: Run batch mode for subnet masks")
