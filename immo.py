from subprocess import call
#import submit
import json
from pprint import pprint
import os.path
import time
from datetime import datetime
from json import JSONDecodeError
import traceback
import smtplib
from email.mime.text import MIMEText
import requests
import urllib.request
import bs4 as bs
import pandas as pd
#from email.message import EmailMessage
fname="href.json"
while True:
    try:
        if os.path.isfile(fname):
            call(["mv", fname, "href_old.json"])
            if not os.path.isfile("submit_expose.json"):
                call(["cp", fname, "submit_expose.json"])
            call(["scrapy", "crawl", "immoscout", "-o", "href.json", "-s", "LOG_ENABLED=false"])
            with open('href.json') as data_file:
                    data = json.load(data_file)
            data=list(set([i[u'href'] for i in data]))
            with open('href_old.json') as data_old_file:
                    data_old = json.load(data_old_file)
            data_old=list(set([i[u'href'] for i in data_old]))
            with open('submit_expose.json') as data_submit_file:
                    data_submit = json.load(data_submit_file)
            data_submit=list(set([i[u'href'] for i in data_submit]))
        else:
            call(["scrapy", "crawl", "immoscout", "-o", "href.json", "-s", "LOG_ENABLED=false"])
            with open('href.json') as data_file:
                    data = json.load(data_file)
            data=list(set([i[u'href'] for i in data]))
            print(data)
            ini=raw_input("No href.json file found. Sending messages to all offers found above?(y/n)\n")
            #ini=input("No href.json file found. Sending messages to all offers found above?(y/n)\n")
            if ini.lower() == "y":
                data_old = []
                data_submit = []
            elif ini.lower() == "n":
                call(["cp", fname, "href_old.json"])
                call(["cp", fname, "submit_expose.json"])
                with open('href_old.json') as data_old_file:
                        data_old = json.load(data_old_file)
                data_old=list(set([i[u'href'] for i in data_old]))
                with open('submit_expose.json') as data_submit_file:
                        data_submit = json.load(data_submit_file)
                data_submit=list(set([i[u'href'] for i in data_submit]))
        #with open('href.json', 'w') as data_file:
        #    json.dump(data,data_file)
        #print(data)
        #black list
        if os.path.isfile('blacklist.json'):
            with open('blacklist.json') as blacklist:
                blacklist = json.load(blacklist)
            blacklist = list(set([i[u'href'] for i in blacklist]))
        else:
            blacklist = []
        print("Blacklist: ", blacklist)

        #with open('href_old.json', 'w') as data_old_file:
        #    json.dump(data_old,data_old_file)
        #print(data_old)
        #diff_id=list(set(data)-set(data_old)-set(blacklist))
        diff_id=list(set(data)-set(data_old)-set(blacklist)-set(data_submit))
        #print(diff_id)
        if len(diff_id) != 0:
            text_file = open("sent_request.dat", "a")
            text_file1 = open("diff.dat", "a")
            print(len(diff_id), "new offers found")
            print("New offers id: ", diff_id)
            betreff = '''Subject: Neue Wohnungsanzeige(n)\n\n'''
            sender = 'immobot@immoscout24.de'
            receivers = ['wohnung@bulgar.club']
            #Initiiere einen leeren DataFrame, ein Tabellenobjekt aehnlich einer Matrix.
            df = pd.DataFrame()
            for new in diff_id:
                print("Sending message to: ", new)
                #submit.submit_app(new)
                text_file.write("ID: %s \n" % new)
                text_file.write(str(datetime.now())+'\n')
                text_file1.write(str(new)+'\n')
                fsubmit = "submit_expose.json"
                new_el = [
                            {
                             "href": new
                            }
                         ]
                if os.path.isfile(fsubmit):
                    # File exists
                    with open(fsubmit, 'r') as json_file:
                            inhalt = json.load(json_file)
                            #print("Print data from json:", inhalt)
                            inhalt_new = inhalt + new_el
                            #print("Data_new:" , inhalt_new)
                    with open(fsubmit, 'w') as output_file:
                            json.dump(inhalt_new, output_file)
                else:
                    # Create file - !!! submit_expose.json muss existieren und mind. den Inhalt [] haben !!!!
                    with open(fsubmit, 'w') as outfile:
                            array= []
                            array.append(new_el)
                            json.dump(array, outfile)
                #data_submit.insert(0,{'href': new })
                try:
                    # Definiere ein BeautifulSoup-Objekt innerhalb eines try-Blocks. 'soup' enthaelt jetzt den gesamten Quellcode der angegebenen URL.
                    soup = bs.BeautifulSoup(urllib.request.urlopen('https://www.immobilienscout24.de'+str(new)).read(),'lxml')
                    
                    # Der Quellcode wird nach <script>-Tags durchsucht. Innerhalb dieser Tags sucht der Scraper nach dem Wort 'keyValues'. Hier befinden sich naemlich alle relevanten Daten zur Wohnung.
                    data = pd.DataFrame(json.loads(str(soup.find_all("script")).split("keyValues = ")[1].split("}")[0]+str("}")),index=[str(datetime.now())])
                    
                    # Zum Dataframe wird ein weiteres Merkmal, naemlich die URL der Wohnung, hinzugefuegt.
                    #data["URL"] = "https://www.immobilienscout24.de" + str(new)
                    
                    # Der DataFrame df wird um den DataFrame "data" ergaenzt.
                    df = df.append(data)
                    
                    # Berechne Preis pro Quadratmeter
                    #miete = str(df["obj_baseRent"])
                    #flaeche = int(df["obj_livingSpace"])
                    #suche = "."
                    
                    #print (flaeche)
                    #flaeche_neu = flaeche.replace(".","")
                    #print (flaeche_neu)
                    #flaeche_int = int(flaeche_neu)
                    #print (flaeche_int)
                    
                    #print (flaeche)
                    #print (flaeche_neu)
                    
                    #if miete.find(suche) < 0:
                    #    miete = miete + ".00"
                    
                    #if flaeche.find(suche) < 0:
                    #    flaeche = flaeche + ".00"
                    
                    #preis_pro_qm = 'Preis pro m2: ' + str(float[miete]/float[flaeche])
                    #print (preis_pro_qm)
                    
                    # Setze Mailbetreff zusammen
                    betreff = betreff + "https://www.immobilienscout24.de" + str(new) + "\n\n"
                    
                    # Leere Dataframe
                    df.drop(df.loc[:,:].columns,axis=1)
                    
                except Exception as e:
                    print("Fehler bei " + str(new) + " " +  str(datetime.now())+": " + str(e))
            try:
                smtpObj = smtplib.SMTP('192.168.11.217')
                smtpObj.sendmail(sender, receivers, betreff)
                smtpObj.quit()
                print ("Successfully sent email")
            except SMTPException:
                print ("Error: unable to send email")
            text_file.close()
            text_file1.close()
        else:
            print("No new offers.")

    except JSONDecodeError as e:
        print("There was a problem with reading a json formatted object")
        print("".join(traceback.TracebackException.from_exception(e).format()))
    finally:
        print("Time: ", datetime.now())
        time.sleep(150)
