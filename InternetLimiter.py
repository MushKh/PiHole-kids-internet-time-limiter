import os
import sys
import requests
import datetime
import time
import subprocess
import logging
from datetime import date 

# Pi-Hole Time Limiter script v1.3
# Check HTTP request is OK to avoid crash after multiple unsuccessfull "get" requests to IP

# Pi-Hole Time Limiter script v1.2
# In v1.2 changed Autorisation according to 
# https://pi-hole.net/blog/2022/11/17/upcoming-changes-authentication-for-more-api-endpoints-required/#page-content

#Usefull Commands
# To keep running script even when ssh teminal will shut down
# sudo nohup python3 script.py &
# To check running processes
# pgrep -af python
#To kill process started with nohup
# sudo kill InternetLimiter
# till 16:00 then from 18:00 to 20:00

# grep "192.168.2.5" /var/log/pihole.log*
# tail -f /var/log/pihole.log | grep 192.168.2.5

# To check log on nohup (in case if app crashed)
# sudo tail -f nohup.out

#Useful Link regarding security
#https://github.com/bee-san/How-I-Hacked-Your-Pi-Hole/blob/master/README.md



today = datetime.datetime.now().strftime("%d, %m, %Y")
log_filename = "/var/www/html/admin/myserver/Limiter_log" + today + ".html"

def restart_script():
    python = sys.executable
    os.execl(python, python, *sys.argv)
    
# Set logging to record all data 
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename=log_filename, filemode="a+", format="%(asctime)-15s %(levelname)-8s %(message)s")
    logging.info("<!DOCTYPE HTML><html><head><title>Usage log</title><link rel='stylesheet' type='text/css' href='home.css'><meta charset='UTF-8'></head><body>")
    
    # Set the maximum internet usage duration in minutes (86400 seconds = 24 hours)
    max_usage_duration = 1 #5 min
    # Address for text file where stored allowed minutes
    FileNameForHours = "/var/www/html/admin/myserver/Parameters.txt"


    # Set the IP address that you want to limit internet usage for. 
    # Code will check activity on this IP
    ip_address = '192.168.2.6'
    
    pi_hole_ip = '192.168.2.10'


    # Set the Pi-hole API URL and authentication token
    #api_url = 'http://192.168.2.10/admin/index.php?login'
    auth_token = '&auth=xxx'
    
    api_url = 'http://192.168.2.10/admin/api.php?status'+auth_token
    #auth_token = 'raspberry'

    # Set the time interval in seconds for checking internet usage duration
    check_interval = 60 # must be dividable to 60
    T_out_interval = 10 # 10 seconds

    #Pi_hole commands
    #Disabling the group will enable the Internet and vice versa
    comm_DisGroup = "sudo /etc/pihole/./setGroupStatus.sh Kids_Group disable"
    comm_EnGroup = "sudo /etc/pihole/./setGroupStatus.sh Kids_Group enable"

    UpdateGravity = "sudo pihole updateGravity"

    # Get the current date and time
    now = datetime.datetime.now()

    # Calculate the end of the day as a datetime object
    end_of_day = now.replace(hour=23, minute=59, second=59)

    # Get the Pi-hole API query for the IP address
    api_query = 'http://{}/admin/api.php?getQueryTypes&client={}&summary'.format(pi_hole_ip, ip_address)

    # Get the start time of the script as a datetime object
    start_time = datetime.datetime.now()
    dns_queries = 0
    usage_duration = 0
    limit_triggered_flag = 0
    usage_minutes = 0
    #At start-up deliberately zero allowed time 
    # Set allowed minutes in text file. This text file can be modified via PHP script externally.
    with open(FileNameForHours, "w") as f:
         f.writelines(str(max_usage_duration))
         print("Allowed min set to:",max_usage_duration)
         logging.info("Allowed min set to: %d <br>", max_usage_duration)
    f.close()
    
    #Then disable group to start counting time
    result = subprocess.run(comm_DisGroup, shell=True, capture_output=True, text=True)
    # Print the output
    #print(result.stdout)
    print("DNS Service Enabled")
    logging.info("DNS Service Enabled <br>")
    result = subprocess.run(UpdateGravity, shell=True, capture_output=True, text=True)
    
    # Number of Attemts  to get responce from IP (PiHole) address
    Atmp = 3 
    
    # Loop until the end of the day
    while datetime.datetime.now() < end_of_day:

        # Get allowed minutes from text file. This text file can be modified via PHP script externally.
        with open(FileNameForHours) as f:
             max_usage_duration = int(f.readline().strip())
        f.close()
        
        Get_Attemts = 0
        # Get the current internet usage duration for the IP address from the Pi-hole API. Atmp = 3 Attemts then timeout for 2 min.
        while Get_Attemts < Atmp:
            response = requests.get(api_query+auth_token)
            Get_Attemts = Get_Attemts+1
            if response.ok:
                #print ('Got responce from pi_hole_ip!')
                break
            else:
                print('Failed to get responce from pi_hole_ip')
                logging.info("Failed to get responce from pi_hole_ip <br>")
                time.sleep(T_out_interval)
            
        
        old_dns_queries = dns_queries
        dns_queries = int((response.json()['dns_queries_today']).replace(",", ""))

        if dns_queries > old_dns_queries:
            #print ("DNSs:", dns_queries)
            #logging.info("DNSs: %d <br>", dns_queries)
            if limit_triggered_flag == 0:
                #usage_duration = #datetime.datetime.now() - start_time
                usage_minutes = usage_minutes + check_interval/60 #int(usage_duration.total_seconds() / 60)

            
            # If the internet usage duration exceeds the maximum, block the IP address
            if usage_minutes >= max_usage_duration:
                # Execute the command and capture the output
                result = subprocess.run(comm_EnGroup, shell=True, capture_output=True, text=True)
                result = subprocess.run(UpdateGravity, shell=True, capture_output=True, text=True)
                # Print the output
                #print(result.stdout)
                if (limit_triggered_flag==0):
                    print("Allowed Min:",max_usage_duration)
                    logging.info("Allowed Min: %d <br>", max_usage_duration)                
                    print ("Used Min:",usage_minutes)
                    logging.info("Used Min: %d <br>", usage_minutes)                
                    print("DNS Service Disabled")
                    logging.info("DNS Service Disabled  <br>")
                limit_triggered_flag = 1
 
                # Print the output
                #print(result.stdout)            
            else :
                #If time was increased after limit time exceeded and internet was blocked
                #then disable the 'block' again
                if (limit_triggered_flag == 1):
                    # Execute the command and capture the output
                    result = subprocess.run(comm_DisGroup, shell=True, capture_output=True, text=True)
                    result = subprocess.run(UpdateGravity, shell=True, capture_output=True, text=True)                    
                    # Print the output
                    #print(result.stdout)
                    print("Allowed Min:",max_usage_duration)
                    logging.info("Allowed Min: %d <br>", max_usage_duration)                     
                    print ("Used Min:",usage_minutes)
                    logging.info("Used Min: %d <br>", usage_minutes)                    
                    print("DNS Service Enabled")
                    logging.info("DNS Service Enabled <br>")
                limit_triggered_flag = 0
                    
        # Wait for the check interval
        time.sleep(check_interval)

    # Unblock the IP address at the end of the day
    # Execute the command and capture the output
    result = subprocess.run(comm_DisGroup, shell=True, capture_output=True, text=True)
    # Print the output
    #print(result.stdout)
    #logging.info("%s  <br>", result.stdout)
    result = subprocess.run(UpdateGravity, shell=True, capture_output=True, text=True)
    # Print the output
    #print(result.stdout)
    #logging.info("%s  <br>", result.stdout) 
    
    restart_script()