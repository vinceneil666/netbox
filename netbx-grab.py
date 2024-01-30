#
# Will search for devices with specific role and serialnumber. Then produce a csv file with misc values. For use towards fortimanger ztp
#

import requests
import csv

api_url = "https://netbox-url/api/dcim/devices/"

params = {
    'role': 'firewall',
    'serial__ic': 'fg'
}

api_key = 'YOUR KEY IN HERE'

headers = {
    'Authorization': f'Token {api_key}'
}

response = requests.get(api_url, params=params, headers=headers)

if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

    
    if data['count'] > 0:
        devices = data['results']

        
        csv_filename = 'FILENAME.csv'

        
        with open(csv_filename, 'w', newline='') as csvfile:
            fieldnames = ['name', 'serial', 'role', 'primary_ip', 'tags']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            
            writer.writeheader()

           
            for device in devices:
                # Get primary IP information
                primary_ip_info = device.get('primary_ip4', {})
                primary_ip_address = primary_ip_info.get('address', 'N/A')

                # Get tags for the device
                device_tags = ', '.join(tag['name'] for tag in device.get('tags', [])) if 'tags' in device else 'N/A'

                writer.writerow({
                    'name': device['name'],
                    'serial': device['serial'],
                    'role': device['device_role']['name'],
                    'primary_ip': primary_ip_address,
                    'tags': device_tags
                })

        print(f'Data has been saved to {csv_filename}')
    else:
        print('No devices found.')
else:
    print(f'Error: {response.status_code}')
    print(response.text)
