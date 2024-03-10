import requests
import subprocess

# Set the IP address that you want to limit internet usage for. 
# Code will check activity on this IP

pi_hole_ip = '192.168.2.10'
ip_address = '192.168.2.6'

auth_token = '&auth=3f4fa74468f336df5c4cf1d343d160f8948375732f82ea1a057138ae7d35055c'
#auth_token = '&auth=raspberry'

# Set the Pi-hole API URL and authentication token
#api_url = 'http://192.168.2.10/admin/index.php?login'
api_url = 'http://192.168.2.10/admin/api.php?status'+auth_token

#print (api_url)
# Get the Pi-hole API query for the IP address
api_query = 'http://{}/admin/api.php?getQueryTypes&client={}&summary'.format(pi_hole_ip, ip_address)
#http://192.168.2.10/admin/api.php?getQueryTypes&client=192.168.2.6&summary


# Get the current internet usage duration for the IP address from the Pi-hole API
response = requests.get(api_query+auth_token)

#response = requests.get("http://192.168.2.10/admin/api.php?getQueryTypes&client=192.168.2.6&summary")
dns_queries = int((response.json()['dns_queries_today']).replace(",", ""))

print("DNSs today:", dns_queries)
