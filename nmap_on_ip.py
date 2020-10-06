import time
import os
import random
import datetime
import configparser
import sys

#recover conf
cfg = configparser.ConfigParser(allow_no_value=True)
cfg.read('./conf.cfg')
hour_start = int(cfg.get('nmapscan','hour_start'))
hour_stop = int(cfg.get('nmapscan','hour_stop'))
user_agent = cfg.get('nmapscan','user_agent')

#Return current hour
#if 10am, return true else false
def getCurrentHour():
    now = datetime.datetime.now()
    if(now == hour_start):
        return True
    else:
        return False

#This method will sleep x hours before continuing the script
def sleepForTheNight():
    res = str(datetime.datetime.strptime(str(hour_start),'%H')-datetime.datetime.strptime(str(hour_stop),'%H'))
    res = res.split(",")[1].replace(" ","").split(":")[0]
    time.sleep(int(res)*60*60)
    return 0
    
#This method will call nmap with an ip and a port
#ips and ports are chosen randomly in arrays
#also, the script will wait a randomly amount of seconds between each request and each ips
#furthermore, if the hour is 5pm, the script will sleep until 9am.
def nmap(allRanges):
    i=0
    totalNbPorts = 14
    openPorts = []
    nmapResults = []
    totalIps = len(allRanges)
    while(i<totalIps):
        try:
            j=0
            ipToScan = []
            portsByIp = dict()
            removed = ""
            #Getting 5 random IPs in the array to make confused the SOC
            for i in range(5):
                ipToScan.append(allRanges[random.randint(0,len(allRanges)-1)])
                portsByIp["string%s"%i] = [443,8080,80,22,21,20,3389,1723,1701,50,51,500,1521,23]
            while(j<totalNbPorts*5): #In fact we will scan randomly 5 ip on 14 ports
                
                #######################################################################################
                #Puting them here to flush automaticly in a file if the script has to be stopped      
                #File to recover IP to scan                                                           

                #File to store nmap results
                fNmapResults = open("nmap_results.txt","a")

                #File to store IP:PORT opened
                fOpenPort = open("ip_port_open.txt","a")
                ########################################################################################

                randomIpToScan = random.randint(0,4)
                while(str(randomIpToScan) in removed):
                    randomIpToScan = random.randint(0,4)
                if(len(portsByIp["string%s"%str(randomIpToScan)])==0):
                    fIpToScan = open("ip_to_scan.txt","w")
                    print("Deleting ip %s"%ipToScan[randomIpToScan])
                    allRanges.remove(ipToScan[randomIpToScan])
                    for ip in allRanges:
                        fIpToScan.write(ip)
                    fIpToScan.close()
                    removed += str(randomIpToScan)
                    portsByIp.pop("string%s"%str(randomIpToScan))
                    j -= 1
                else:
                    port = portsByIp["string%s"%str(randomIpToScan)][random.randint(0,len(portsByIp["string%s"%str(randomIpToScan)])-1)]
                    ip = ipToScan[randomIpToScan].strip()
                    portsByIp["string%s"%str(randomIpToScan)].remove(port)
                    print("Nmap on "+str(ip).strip()+":"+str(port))
                    if(port==80 or port==8080 or port==443):
                        res = os.popen('nmap -p' + str(port) + " --script http-methods --script-args http.useragent='Firefox(41.0)' " + str(ip)).read()
                    else:
                        res = os.popen('nmap -p' + str(port) +" "+ str(ip)).read()
                    if("closed" not in res and "down" not in res):
                        openPorts.append(str(ip)+":"+str(port))
                        fOpenPort.write(str(ip)+":"+str(port)+"\n")
                        nmapResults.append(res)
                        fNmapResults.write(res+"\n\n\n")
                    fOpenPort.close()
                    fNmapResults.close()
                if(getCurrentHour() == True):
                    sleepForTheNight()
                waitingFor = random.randint(5,10)
                time.sleep(waitingFor)
                j += 1
            waitingFor = random.randint(60,100)
            time.sleep(waitingFor)
            i += 1
        except Exception as e:
            if("Keyboard" not in e):
                continue
            else:
                sys.exit(-1)

#This method will be used to recover ips from a file and write 
#result of nmap method in a file
def main():
    print("NOTE: Use this tool at your own risk and in the legality of your country, I will clear myself of any illegal act carried out with this tool.")
    allIps = []
    with open('ip_to_scan.txt','r') as lines:
        for line in lines:
            allIps.append(line)
    nmap(allIps)

if __name__ == "__main__":
    main()
