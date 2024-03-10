Installation procedure.

1. Assuming that you have Ph-Hole installed on Raspberry Pi and have access to it thru SSH.
For easy access to all Ph-Hole folders and files it's best to have WinSCP installed. It need to connect to Rpi with SSH (Enable SSH from Rpi). 
Also Pi-Hole IP need to be configured in local Modem/Router as primary DNS server. I also disable secondary DNS server in router to avoid bypassing Pi-Hole.

2. In Pi-Hole under /var/www/html/admin/  modify  index.php page. Remove original page and put index.php modified file from repo. 
This will add "Allowed time" and "Times Log" additional fields to Pi-Hole Dashboard.
By doing this we realize that in case of Pi-Hole updates related to this page these fileds will be removed.

3. Create folder /var/www/html/admin/myserver. Copy home.css, ListLogs.php, Parameters.txt, ReadPar.php, WritePar.php to that folder.

4. In InternetLimiter.py  script you need to add Pi-Hole IP address and an IP address on which you want activity/time to be monitored and calculated. Find below rows in script file and replace x.x with your kid local IP address and yy with Pi-Hole local IP.
    ip_address = '192.168.x.x'    
    pi_hole_ip = '192.168.y.y'
5. In Pi-Hole open  /etc/pihole/setupVars.conf (WEBPASSWORD) and get the token from (WEBPASSWORD) filed then copy/replace it to 
	auth_token = xxx 
	line in InternetLimiter.py file. This will allow script to make changes in your Pi-Hole.

6. Create /var/www/html/myserver folder in Pi-Hole and copy InternetLimiter.py to it.

7. Configring Pi-Hole
	A) Using Pi-Hole web interface open Groups page and create "Kids_Group" in it.
	B) Using Pi-Hole web interface open Clients page then in field "Add a new client" add your kid phone and/or PC MAC 		addresses. Using MAC address identification here seems to work more reliable that using IP address.
	C) After seeing kids MAC addresses in "List of configured clients" on same page add them to both "Default" and 	"Kids_Group". For other IP that must not be affected by this scripts leave to just "Default" group.
	D) Go to Domains page.
	Add in "RegEx:"  .* then click Add to Blacklist. This will blacklist all web-pages for kid except following pages.
	Add in "RegEx:" field all web pages that must not be affected by this script for the kid. 
	For example .*outlook.* Add to Whitelist.
	E) Under "List of domains" on same page for appropriate pages choose "Kids_Group".
	
	These Whitelist and Blacklist paged will be working only when "Kids_Group" in Groups will be enabled. Enabling or 	Disabling this group is happening from InternetLimiter.py script. But is also can be tested/verified manually from Pi-	Hole interface.

	F) For Pi-Hole reliable IP/MACs identification in Logs its better to have Pi-Hole also configured as DHCP server. 
	Go to Settings->DHCP page and set "Enable DHCP" tickbox. Also do not forget to disable DHCP server functionality in 	your Modem/Router to avoid collisions.

8. Do not forget to change default Pi-Hole password from "Raspberry" to something else. Some kids are smarter that we think.



	
	
	
