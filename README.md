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
