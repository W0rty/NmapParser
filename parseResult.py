#!/usr/bin/python3
import os
import sys
import csv
import re
import time
import platform
import mysql.connector
import requests
import random
import subprocess
password = ''
user = 'root'
#Used to parse arrays to sort data according to the configuration of the user
def parseArrays(ips,nmaps,port,state,country,hasToBeExported):
    if(hasToBeExported == True):
        newNmaps = []
        newIps = []
        if(port == -1 and state == "None"):
            newNmaps = nmaps
            newIps = ips
        else:
            if(port == -1):
                if(state == "open"):
                    for n in nmaps:
                        if("open" in n):
                            newNmaps.append(n)
                            if(n.split("\n")[0] == ''):
                                if('(' in n.split("\n")[2].split("for ")[1]):
                                    ip = n.split("\n")[2].split("for ")[1].split("(")[1].split(")")[0]
                                else:
                                    ip = n.split("\n")[2].split("for ")[1]
                                newIps.append(ip+":"+n.split("\n")[6].split(" ")[0].split("/")[0])
                            else:
                                if('(' in n.split("\n")[1].split("for ")[1]):
                                    ip = n.split("\n")[1].split("for ")[1].split("(")[1].split(")")[0]
                                else:
                                    ip = n.split("\n")[1].split("for ")[1]
                                newIps.append(ip+":"+n.split("\n")[5].split(" ")[0].split("/")[0])
                else:
                    newNmaps = []
                    for n in nmaps:
                        if("filtered" in n):
                            newNmaps.append(n)
                            if(n.split("\n")[0] == ''):
                                if('(' in n.split("\n")[2].split("for ")[1]):
                                    ip = n.split("\n")[2].split("for ")[1].split("(")[1].split(")")[0]
                                else:
                                    ip = n.split("\n")[2].split("for ")[1]
                                newIps.append(ip+":"+n.split("\n")[6].split(" ")[0].split("/")[0])
                            else:
                                if('(' in n.split("\n")[1].split("for ")[1]):
                                    ip = n.split("\n")[1].split("for ")[1].split("(")[1].split(")")[0]
                                else:
                                    ip = n.split("\n")[1].split("for ")[1]
                                newIps.append(ip+":"+n.split("\n")[5].split(" ")[0].split("/")[0])
            else:
                if(state == "None"):
                    for n in nmaps:
                        try:
                            if(n.split("\n")[5].split(" ")[0].split("/")[0] == str(port) or n.split("\n")[6].split(" ")[0].split("/")[0] == str(port)):
                                newNmaps.append(n)
                                if(n.split("\n")[0] == ''):
                                    if('(' in n.split("\n")[2].split("for ")[1]):
                                        ip = n.split("\n")[2].split("for ")[1].split("(")[1].split(")")[0]
                                    else:
                                        ip = n.split("\n")[2].split("for ")[1]
                                    newIps.append(ip+":"+n.split("\n")[6].split(" ")[0].split("/")[0])
                                else:
                                    if('(' in n.split("\n")[1].split("for ")[1]):
                                        ip = n.split("\n")[1].split("for ")[1].split("(")[1].split(")")[0]
                                    else:
                                        ip = n.split("\n")[1].split("for ")[1]
                                    newIps.append(ip+":"+n.split("\n")[5].split(" ")[0].split("/")[0])
                        except:
                            continue
                else:
                    if(state == "open"):
                        for n in nmaps:
                            try:
                                if(n.split("\n")[5].split(" ")[0].split("/")[0] == str(port) or n.split("\n")[6].split(" ")[0].split("/")[0] == str(port) and "open" in n):
                                    newNmaps.append(n)
                                    if(n.split("\n")[0] == ''):
                                        if('(' in n.split("\n")[2].split("for ")[1]):
                                            ip = n.split("\n")[2].split("for ")[1].split("(")[1].split(")")[0]
                                        else:
                                            ip = n.split("\n")[2].split("for ")[1]
                                        newIps.append(ip+":"+n.split("\n")[6].split(" ")[0].split("/")[0])
                                    else:
                                        if('(' in n.split("\n")[1].split("for ")[1]):
                                            ip = n.split("\n")[1].split("for ")[1].split("(")[1].split(")")[0]
                                        else:
                                            ip = n.split("\n")[1].split("for ")[1]
                                        newIps.append(ip+":"+n.split("\n")[5].split(" ")[0].split("/")[0])
                            except:
                                continue
                    else:
                        for n in nmaps:
                            try:
                                if(n.split("\n")[5].split(" ")[0].split("/")[0] == str(port) or n.split("\n")[6].split(" ")[0].split("/")[0] == str(port) and "filtered" in n):
                                    newNmaps.append(n)
                                    if(n.split("\n")[0] == ''):
                                        if('(' in n.split("\n")[2].split("for ")[1]):
                                            ip = n.split("\n")[2].split("for ")[1].split("(")[1].split(")")[0]
                                        else:
                                            ip = n.split("\n")[2].split("for ")[1]
                                        newIps.append(ip+":"+n.split("\n")[6].split(" ")[0].split("/")[0])
                                    else:
                                        if('(' in n.split("\n")[1].split("for ")[1]):
                                            ip = n.split("\n")[1].split("for ")[1].split("(")[1].split(")")[0]
                                        else:
                                            ip = n.split("\n")[1].split("for ")[1]
                                        newIps.append(ip+":"+n.split("\n")[5].split(" ")[0].split("/")[0])
                            except:
                                continue
        return [newNmaps,newIps]
    else:
        try:
            connection = mysql.connector.connect(host='localhost',database='nmap',user=user,password=password)
            if(connection.is_connected()):
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM resultats") #WHERE VERSION != NULL
                records = cursor.fetchall()
        except:
            pass
        finally:
            if(connection.is_connected()):
                connection.close()
                cursor.close()
        toReturn = []
        if(int(port) != -1 and state.lower() != "none" and country.lower() != "none"):
            for r in records:
                if(r[1] == int(port) and r[2].lower() == state.lower() and r[8].lower() == country.lower()):
                    toReturn.append(r)
        else:
            if(int(port) != -1 and state.lower() == "none" and country.lower() == "none"):
                for r in records:
                    if(r[1] == int(port)):
                        toReturn.append(r)
            else:
                if(int(port) == -1 and state.lower() != "none" and country.lower() == "none"):
                    for r in records:
                        if(r[2].lower() == state.lower()):
                            toReturn.append(r)
                else:
                    if(int(port) == -1 and state.lower() == "none" and country.lower() != "none"):
                        for r in records:
                            if(r[8].lower() == country.lower()):
                                toReturn.append(r)
                    else:
                        if(int(port) != -1 and state.lower() == "none" and country.lower() != "none"):
                            for r in records:
                                if(r[8].lower() == country.lower() and r[1] == int(port)):
                                    toReturn.append(r)
                        else:
                            if(int(port) == -1 and state.lower() != "none" and country.lower() != "none"):
                                for r in records:
                                    if(r[8].lower() == country.lower() and r[2].lower() == state.lower()):
                                        toReturn.append(r)
                            else:
                                if(int(port) != -1 and state.lower() != "none" and country.lower() == "none"):
                                    for r in records:
                                        if(r[1] == int(port) and r[2].lower() == state.lower()):
                                            toReturn.append(r)
                                else:
                                    for r in records:
                                        toReturn.append(r)
        return toReturn
            
#save datas in db
def saveInDb(ips,nmaps,port,state,country):
    data = parseArrays(ips,nmaps,port,state,country,True)
    dataNmaps = data[0]
    dataIps = data[1]
    toWrite = []
    try:
        connection = mysql.connector.connect(host='localhost',database='nmap',user=user,password=password)
        if(connection.is_connected()):
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM resultats")
            records = cursor.fetchall()
    except:
        pass
    finally:
        if(connection.is_connected()):
            connection.close()
            cursor.close()

    for i in range(len(dataNmaps)):
        alreadyInDb = False
        for r in records:
            if(r[0] == dataIps[i].split(":")[0] and r[1] == int(dataIps[i].split(":")[1])):
                alreadyInDb = True
        if(alreadyInDb == False):
            try:
                whois = os.popen("whois "+dataIps[i].split(":")[0]).read()
                pays = requests.post("https://iplocation.com/",data={'ip':dataIps[i].split(":")[0]}).json()['country_name']
                rangeOfIp = whois.split("inetnum")[1].split(":")[1].split("netname")[0].replace(" ",'').strip()
                if("linux" in platform.system().lower()):
                    hostname = subprocess.Popen("host "+dataIps[i].split(":")[0],shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    hostname = str(hostname.stdout.read())
                    if("not found" in hostname or "Invalid argument" in hostname or "timed out" in hostname):
                        hostname = "NONE"
                    else:   
                        hostname = hostname.split("pointer ")[1].split("\n")[0]
                else:
                    hostname = os.popen("ping -a "+dataIps[i].split(":")[0]).read()
                    if("demande dépassé" in hostname):
                        hostname = ""
                    else:
                        hostname = hostname.split("\n")[1].split(" ")[5]
                verification = "HAVE TO BE DONE"
                service = ''
                if("PORT" not in dataNmaps[i].split("\n")[5]):
                    service = nmaps[i].split("\n")[5].split(" ")[2]
                else:
                    service = nmaps[i].split("\n")[6].split(" ")[2]
                if(service == ''):
                    service = nmaps[i].split("\n")[6].split(" ")[3]
                if("open" in dataNmaps[i]):
                    toWrite.append(dataIps[i].split(":")[0]+","+dataIps[i].split(":")[1].strip()+","+"OPEN"+","+service+","+rangeOfIp+","+hostname+","+"https://apps.db.ripe.net/db-web-ui/query?bflag=false&dflag=false&rflag=true&searchtext="+dataIps[i].split(":")[0]+"&source=RIPE"+","+verification+","+pays)
                else:
                    toWrite.append(dataIps[i].split(":")[0]+","+dataIps[i].split(":")[1].strip()+","+"FILTERED"+","+service+","+rangeOfIp+","+hostname+","+"https://apps.db.ripe.net/db-web-ui/query?bflag=false&dflag=false&rflag=true&searchtext="+dataIps[i].split(":")[0]+"&source=RIPE"+","+verification+","+pays)        
            except Exception as e:
                print(e)
                continue
    try:
        connection = mysql.connector.connect(host='localhost',
                                        database='nmap',
                                        user=user,
                                        password=password)
        if(connection.is_connected()):
            for info in toWrite:
                cursor = connection.cursor()
                info = info.split(",")
                cursor.execute("""INSERT INTO resultats(IP,PORT,ETAT,SERVICE,RANGE_IP,DNS,URL_RIPE,VERIFICATION,PAYS,VERSION) VALUES ('"""+info[0]+"""',"""+info[1]+""",'"""+info[2]+"""','"""+info[3]+"""','"""+info[4]+"""','"""+info[5]+"""','"""+info[6]+"""','"""+info[7]+"""','"""+info[8]+"""','NULL')""")
                connection.commit()
    except Exception as e:
        print("INFOS ARE:")
        print(info)
        print(e)
    finally:
        if(connection.is_connected()):
            connection.close()
            cursor.close()
            

#Export all results to a .csv file for analyse
def exportToCSV(port,state,country):
    name = input("Which name do you want to give to the file? (Filename must end with .csv):\n")
    regex = ".*.csv"
    pattern = re.compile(regex)
    while(pattern.match(name) == None):
        name = input("Error : filename must end with .csv\n\nWhich name do you want to give to the file?:\n")
    if(os.path.exists(name)):
        choix = input(name+" is already in use, do you want to overwrite it?(y/n): ")
        while(choix.lower() != "y" and choix.lower() != "n"):
            choix = input(name+" is already in use, do you want to overwrite it?(y/n): ")
        if(choix == "n"):
            print("\n")
            exportToCSV(port,state,country)

    try:
        connection = mysql.connector.connect(host='localhost',database='nmap',user=user,password=password)
        if(connection.is_connected()):
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM resultats")
            records = cursor.fetchall()
    except:
        pass
    finally:
        if(connection.is_connected()):
            connection.close()
            cursor.close()
    
    with open(name,'w',newline='') as outcsv:
        writer = csv.writer(outcsv, delimiter=';')
        writer.writerow(['IP','PORT','ETAT','SERVICE','RANGE_IP','DOMAIN NAME','URL RIPE','VERIFICATION','PAYS','VERSION'])
        if(int(port) != -1 and state.lower() != "none" and country.lower() != "none"):
            for r in records:
                if(r[1] == int(port) and r[2].lower() == state.lower() and r[8].lower() == country.lower()):
                    writer.writerow(r)
        else:
            if(int(port) != -1 and state.lower() == "none" and country.lower() == "none"):
                for r in records:
                    if(r[1] == int(port)):
                        writer.writerow(r)
            else:
                if(int(port) == -1 and state.lower() != "none" and country.lower() == "none"):
                    for r in records:
                        if(r[2].lower() == state.lower()):
                            writer.writerow(r)
                else:
                    if(int(port) == -1 and state.lower() == "none" and country.lower() != "none"):
                        for r in records:
                            if(r[8].lower() == country.lower()):
                                writer.writerow(r)
                    else:
                        if(int(port) != -1 and state.lower() == "none" and country.lower() != "none"):
                            for r in records:
                                if(r[8].lower() == country.lower() and r[1] == int(port)):
                                    writer.writerow(r)
                        else:
                            if(int(port) == -1 and state.lower() != "none" and country.lower() != "none"):
                                for r in records:
                                    if(r[8].lower() == country.lower() and r[2].lower() == state.lower()):
                                        writer.writerow(r)
                            else:
                                if(int(port) != -1 and state.lower() != "none" and country.lower() == "none"):
                                    for r in records:
                                        if(r[1] == int(port) and r[2] == state.lower()):
                                            writer.writerow(r)
                                else:
                                    for r in records:
                                        writer.writerow(r)
        outcsv.close()
    print("All results have been exported to "+name+" !")

#This method will use the -v option of nmap to scan the version of a specific service on an ip
def version(ips,nmaps,port,state,country):
    data = parseArrays(ips,nmaps,port,state,country,False) #Recovering IP according to the configuration of user
    for d in data:
        if(d[9] != "NULL"):
            data.remove(d)
    show(data,True,False)
    index = input("Which index do you want to use? (0 -> "+str(len(data)-1)+")\n")
    while(index.isdigit() == False or int(index) < 0 and int(index) > len(data)-1):
        print("Invalid index.")
        index = input("Which index do you want to use? (0 -> "+str(len(data)-1)+")\n")
    if("FILTERED" in data[int(index)]):
        choice = input("It is not recommended to nmap on a filtered port for discretion.\nDo you want to continue?(y/n): ")
        while(choice.lower() != "y" and choice.lower() != "n"):
            print("Invalid entry.")
            choice = input("It is not recommended to nmap on a filtered port for discretion.\nDo you want to continue?(y/n): ")
        if(choice == "n"):
            return 0
    IP = data[int(index)][0]
    PORT = data[int(index)][1]
    print("Recovering version of "+data[int(index)][3]+" on "+IP+":"+str(PORT))
    res = os.popen("nmap -p "+str(PORT)+" -sV "+IP).read()
    unknown = False    
    if("down" not in res.lower()):
        if(len(res.split("\n")[6].split(" ")) < 4):
            version = "UNKNOWN"
        else:
            version = res.split("\n")[6].split(" ")[3]
    else:
        unknown = True

    if(unknown == False):
        try:
            connection = mysql.connector.connect(host='localhost',database='nmap',user=user,password=password)
            if(connection.is_connected()):
                cursor = connection.cursor()
                cursor.execute("""UPDATE resultats SET VERSION='"""+version+"""', VERIFICATION='POSITIVE' WHERE IP='"""+IP+"""' AND PORT="""+str(PORT))
                connection.commit()
        except Exception as e:
            print(e)
            pass
        finally:
            if(connection.is_connected()):
                connection.close()
                cursor.close()
    else:
        try:
            connection = mysql.connector.connect(host='localhost',database='nmap',user=user,password=password)
            if(connection.is_connected()):
                cursor = connection.cursor()
                cursor.execute("""UPDATE resultats SET VERIFICATION='FALSE POSITIVE' WHERE IP='"""+IP+"""' AND PORT="""+str(PORT))
                connection.commit()
        except Exception as e:
            print(e)
            pass
        finally:
            if(connection.is_connected()):
                connection.close()
                cursor.close()
    return 1

#Print on the terminal the nmap results according to the configuration
def show(data,hasToPrintIndex,printOnlyVersion):
    if(hasToPrintIndex == False and printOnlyVersion == False):
        print('-----------------------------------------------------------------------------------------------------------------------------------------------------')
        print('|          IP          |     PORT     |          SERVICE          |          STATE          |          COUNTRY          |          VERSION          |')
        print('-----------------------------------------------------------------------------------------------------------------------------------------------------')
        for d in data:
            try:
                toDisplay = '|     '+d[0]
                while(len(toDisplay) < 22):
                    toDisplay += ' '
                toDisplay += ' |'
                toDisplay += '     '+str(d[1])
                while(len(toDisplay) < 38):
                    toDisplay += ' '
                toDisplay += '|'
                toDisplay += '         '
                toDisplay += d[3]
                while(len(toDisplay) < 66):
                    toDisplay += ' '
                toDisplay += '|'
                toDisplay += '         '
                toDisplay += d[2]
                while(len(toDisplay) < 92):
                    toDisplay += ' '
                if(len(d[8]) > 6):
                    toDisplay += '|       '
                    toDisplay += d[8]
                else:
                    toDisplay += '|          '
                    toDisplay += d[8]
                while(len(toDisplay) < 120):
                    toDisplay += " "
                if("NULL" in d[9]):
                    toDisplay += "|        "
                    version = "NOT ANALYSE"
                else:
                    toDisplay += "|          "
                    version = d[9]
                toDisplay += version
                while(len(toDisplay) < 148):
                    toDisplay += " "
                toDisplay += "|"
                toDisplay += "\n-----------------------------------------------------------------------------------------------------------------------------------------------------"
                print(toDisplay)
            except Exception as e:
                print(e)
                continue
    else:
        hasBeenPrinted = 0
        if(hasToPrintIndex == False and printOnlyVersion == True):
            print('-----------------------------------------------------------------------------------------------------------------------------------------------------')
            print('|          IP          |     PORT     |          SERVICE          |          STATE          |          COUNTRY          |          VERSION          |')
            print('-----------------------------------------------------------------------------------------------------------------------------------------------------')
            for d in data:
                if(d[9] != "NULL"):
                    hasBeenPrinted += 1
                    try:
                        toDisplay = '|     '+d[0]
                        while(len(toDisplay) < 22):
                            toDisplay += ' '
                        toDisplay += ' |'
                        toDisplay += '     '+str(d[1])
                        while(len(toDisplay) < 38):
                            toDisplay += ' '
                        toDisplay += '|'
                        toDisplay += '         '
                        toDisplay += d[3]
                        while(len(toDisplay) < 66):
                            toDisplay += ' '
                        toDisplay += '|'
                        toDisplay += '         '
                        toDisplay += d[2]
                        while(len(toDisplay) < 92):
                            toDisplay += ' '
                        if(len(d[8]) > 6):
                            toDisplay += '|       '
                            toDisplay += d[8]
                        else:
                            toDisplay += '|          '
                            toDisplay += d[8]
                        while(len(toDisplay) < 120):
                            toDisplay += " "
                        toDisplay += "|          "
                        version = d[9]
                        toDisplay += version
                        while(len(toDisplay) < 148):
                            toDisplay += " "
                        toDisplay += "|"
                        toDisplay += "\n-----------------------------------------------------------------------------------------------------------------------------------------------------"
                        print(toDisplay)
                    except Exception as e:
                        print(e)
                        continue
            if(hasBeenPrinted == 0):
                print("\033[1;31m"+"No results for the current configuration."+"\033[0;0m")
        else:
            if(hasToPrintIndex == True):
                i = 0
                print('-------------------------------------------------------------------------------------------------------------------------------')
                print('|INDEX|          IP          |     PORT     |          SERVICE          |          STATE          |          COUNTRY          |')
                print('-------------------------------------------------------------------------------------------------------------------------------')
                for d in data:
                    if(d[9] == "NULL"):
                        try:
                            if(len(str(i)) == 1):
                                toDisplay = '|  '+str(i)
                            else:
                                if(len(str(i)) == 2 or len(str(i)) == 3):
                                    toDisplay = '| '+str(i)
                                else:
                                    if(len(str(i)) == 4):
                                        toDisplay = '|'+str(i)
                            while(len(toDisplay) < 6):
                                toDisplay += ' '
                            toDisplay += '|     '+d[0]
                            while(len(toDisplay) < 28):
                                toDisplay += ' '
                            toDisplay += ' |'
                            toDisplay += '     '+str(d[1])
                            while(len(toDisplay) < 44):
                                toDisplay += ' '
                            toDisplay += '|'
                            toDisplay += '         '
                            toDisplay += d[3]
                            while(len(toDisplay) < 72):
                                toDisplay += ' '
                            toDisplay += '|'
                            toDisplay += '         '
                            toDisplay += d[2]
                            while(len(toDisplay) < 98):
                                toDisplay += ' '
                            if(len(d[8]) > 6):
                                toDisplay += '|       '
                                toDisplay += d[8]
                            else:
                                toDisplay += '|          '
                                toDisplay += d[8]
                            while(len(toDisplay) < 126):
                                toDisplay += " "
                            toDisplay += "|"
                            toDisplay += "\n-------------------------------------------------------------------------------------------------------------------------------"
                            print(toDisplay)
                            i += 1
                        except Exception as e:
                            print(e)
                            continue           
            if(i == 0):
                print("\033[1;31m"+"No results for the current configuration."+"\033[0;0m") 
#Set the variable state to open or filtered   
def setState(port,country):
    records = []
    try:
        connection = mysql.connector.connect(host='localhost',database='nmap',user=user,password=password)
        if(connection.is_connected()):
            cursor = connection.cursor()
            if(port != -1 and country.lower() != "none"):
                cursor.execute("SELECT DISTINCT ETAT FROM resultats WHERE PORT="+str(port)+" AND PAYS='"+country+"'")
                records = cursor.fetchall()
            else:
                if(port == -1 and country.lower() != "none"):
                    cursor.execute("SELECT DISTINCT ETAT FROM resultats WHERE PAYS='"+country+"'")
                    records = cursor.fetchall()
                else:
                    if(port != -1 and country.lower() == "none"):
                        cursor.execute("SELECT DISTINCT ETAT FROM resultats WHERE PORT="+str(port))
                        records = cursor.fetchall()
                    else:
                        cursor.execute("SELECT DISTINCT ETAT FROM resultats")
                        records = cursor.fetchall()
    except Exception as e:
        print(e)
        pass
    finally:
        if(connection.is_connected()):
            connection.close()
            cursor.close()
    if(len(records) != 0):
        print("Available state are ",end='')
        for r in records:
            print("'"+r[0].lower()+"', ",end='')
        print("'none' (to reset)")
        s = input("setState: ")
        while(any(s.upper() in i for i in records) == False and s.lower() != 'none'):
            print("state can only take as values ",end='')
            for r in records:
                print("'"+r[0].lower()+"', ",end='')
            print("'none' (to reset), please retry.\n")
            s = input("setState: ")
        return s
    else:
        print("No states are available with this configuration.")
        return "none"

#Set the variable port to an available port
def setPort(country,state):
    records = []
    try:
        connection = mysql.connector.connect(host='localhost',database='nmap',user=user,password=password)
        if(connection.is_connected()):
            cursor = connection.cursor()
            if(country.lower() != "none" and state.lower() != "none"):
                cursor.execute("SELECT DISTINCT PORT FROM resultats WHERE PAYS='"+country+"' AND ETAT='"+state+"'")
                records = cursor.fetchall()
            else:
                if(country.lower() != "none" and state.lower() == "none"):
                    cursor.execute("SELECT DISTINCT PORT FROM resultats WHERE PAYS='"+country+"'")
                    records = cursor.fetchall()
                else:
                    if(country.lower() == "none" and state.lower() != "none"):
                        cursor.execute("SELECT DISTINCT PORT FROM resultats WHERE ETAT='"+state+"'")
                        records = cursor.fetchall()
                    else:
                        cursor.execute("SELECT DISTINCT PORT FROM resultats")
                        records = cursor.fetchall()
    except Exception as e:
        print(e)
        pass
    finally:
        if(connection.is_connected()):
            connection.close()
            cursor.close()
    if(len(records) != 0):
        print("Available port are: ",end='')
        for r in records:
            print(str(r[0])+",",end='')
        print("-1 (to reset)")
        p = input("setPort: ")
        if(p!="-1"):
            while(p.isdigit() == False or any(int(p) in i for i in records) == False):
                print("Invalid port.\n\nAvailable port are: ",end='')
                for r in records:
                    print(str(r[0])+",",end='')
                print("-1 (to reset), please retry.")
                p = input("setPort: ")
        return int(p)
    else:
        print("No ports are available with this configuration.")
        return -1

#Set the variable country as an available country
def setCountry(port,state):
    records = []
    try:
        connection = mysql.connector.connect(host='localhost',database='nmap',user=user,password=password)
        if(connection.is_connected()):
            cursor = connection.cursor()
            if(port != -1 and state.lower() != "none"):
                cursor.execute("SELECT DISTINCT PAYS FROM resultats WHERE PORT="+str(port)+" AND ETAT='"+state+"'")
                records = cursor.fetchall()
            else:
                if(port == -1 and state.lower() != "none"):
                    cursor.execute("SELECT DISTINCT PAYS FROM resultats WHERE ETAT='"+state+"'")
                    records = cursor.fetchall()
                else:
                    if(port != -1 and state.lower() == "none"):
                        cursor.execute("SELECT DISTINCT PAYS FROM resultats WHERE PORT="+str(port))
                        records = cursor.fetchall()
                    else:
                        cursor.execute("SELECT DISTINCT PAYS FROM resultats")
                        records = cursor.fetchall()
    except Exception as e:
        print(e)
        pass
    finally:
        if(connection.is_connected()):
            connection.close()
            cursor.close()
    if(len(records) != 0):
        print("Available country are ",end='')
        for r in records:
            print("'"+r[0]+"', ",end='')
        print("'none' (to reset)")
        s = input("setCountry: ")
        while(any(s in i for i in records) == False and s.lower() != 'none'):
            print("country can only take as values ",end='')
            for r in records:
                print("'"+r[0]+"', ",end='')
            print("'none' (to reset) please retry.\n")
            s = input("setCountry: ")
        return s
    else:
        print("No countries are available with this configuration.")
        return "none"

def help():
    print("\033[92m"+'''clear : clear the console
country : Change current country
display : Display current configuration
export : Export all outputs to a CSV file (depending your configuration)
help : Display help menu
port : Change current port 
save : Save all results in database
show : Show results of nmap depending your configuration (use -v option to only print nmaps results which have a correct version for a specific service)
state : Change current state to display (filtered or open)
version : Scan version of a specific service on an IP (depending your configuration)
quit : Exit the program'''+"\033[0;0m")

def main():
    port = -1
    country = "None"
    state = "None"
    ipsPorts = []
    forClear = ''
    if(os.path.isfile("./ip_port_open.txt") == False):
        print("\033[1;31m"+"Missing file ip_port_open.txt, exiting script.")
        sys.exit(-1)
    if(os.path.isfile("./nmap_results.txt") == False):
        print("\033[1;31m"+"Missing file nmap_results.txt, exiting script.")
        sys.exit(-1)
    whois = subprocess.Popen("whois localhost",shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    whois = str(whois.stdout.read())
    if("linux" in platform.system().lower()):
        host = os.popen("host localhost").read()
        if("command not found" in whois):
            print("\033[1;31m"+"Missing whois command, run: sudo apt install whois -y to fix it.")
            sys.exit(-1)
        if("command not found" in host):
            print("\033[1;31m"+"Missing host command, run: sudo apt install dnsutils -y to fix it.")
            sys.exit(-1)
    '''else:
        if("n'est pas reconnu" in whois):
            print("\033[1;31m"+"Missing whois command, you can download it from here: https://docs.microsoft.com/en-us/sysinternals/downloads/whois"+"\033[0;0m")
            sys.exit(-1)
    '''
    with open("ip_port_open.txt",'r', errors='ignore') as lines:
        for line in lines:  
            ipsPorts.append(line)
    nmapResults = open("nmap_results.txt",'r', errors='ignore').read()
    nmaps = nmapResults.split("\n\n\n")
    if("linux" in platform.system().lower()):
        forClear = "clear"
        os.system(forClear)
    else:
        forClear = "cls"
        os.system(forClear)
    print("NOTE: Use this tool at your own risk and in the legality of your country, I will clear myself of any illegal act carried out with this tool.")    
    print("Hi! Welcome on the nmap results parser!  \nTo see which commands are available, enter 'help'.")
    while True:
        choice = input(">> ")
        if(choice.lower() == "help"):
            help()
        else:
            if(choice.lower() == "clear"):
                os.system(forClear)
            else:
                if(choice.lower() == "export"):
                    exportToCSV(port,state,country)
                else:
                    if(choice.lower() == "display"):
                        print("\033[92m"+'''Current configuration: 
port = '''+str(port)+'''
state = '''+state+'''
country = '''+country+"\033[0;0m")
                    else:
                        if(choice.lower() == "state"):
                            state = setState(port,country).lower()
                        else:
                            if("show" in choice.lower()):
                                if(choice.lower() == "show -v"):
                                    ret = parseArrays(ipsPorts,nmaps,port,state,country,False)
                                    show(ret,False,True)
                                else:
                                    ret = parseArrays(ipsPorts,nmaps,port,state,country,False)
                                    show(ret,False,False)
                            else:
                                if(choice.lower() == "quit"):
                                    print("\033[92m"+"Bye!"+"\033[0;0m")
                                    sys.exit(-1)
                                else:
                                    if(choice.lower() == "port"):
                                        port = setPort(country,state)
                                    else:
                                        if(choice.lower() == "version"):
                                            res = version(ipsPorts,nmaps,port,state,country)
                                            while(res == 0):
                                                res = version(ipsPorts,nmaps,port,state,country)
                                        else:
                                            if(choice.lower() == "save"):
                                                saveInDb(ipsPorts,nmaps,port,state,country)
                                            else:
                                                if(choice.lower() == "country"):
                                                    country = setCountry(port,state)
                                                else:
                                                    print("\033[1;31m"+choice.lower()+" : unknown command.\nType 'help' to see all commands."+"\033[0;0m")

if __name__ == "__main__":
    main()
