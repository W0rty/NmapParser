# NmapParser
This tool allows you to scan range of IPs, store them into files, and them parse result in a database.

Many features are included :

- Recover version of a service running on a certain ip/port from the database.
- Export results to CSV
- Add your configuration (specific port, specific state(open,filtered), specific country)
- Parse result in the terminal
- ...


The file nmap_on_ip.py will nmap on ranges randomly and on random ports, to avoid being spotted.
Choosen ports are most common one on a server (ssh,ftp,http,https,vpn,...)

# How to use it ?
- Read INSTALL.txt and follow instructions.
- Create a file ip_to_scan.txt with ips you have to scan! (with a \n between ips)
- Launch script nmap_on_ip.py
- Launch script parserResult.py (even if the script nmap_on_ip.py is still running, you will have your first results!)
- ENJOY :)

