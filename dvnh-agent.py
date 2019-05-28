import os
import sys
import subprocess
import json
import requests

filename = '/var/log/suricata/eve.json'
dvnh_api_url = 'http://192.168.100.111:9000/handle_attack'
f = subprocess.Popen(['tail','-F',filename],\
        stdout=subprocess.PIPE,stderr=subprocess.PIPE)



def run():
    if not os.path.exists(filename):
        print("{} is not found".format(filename))
        sys.exit(1)
    print("Started listen to suricata IDS log file {}".format(filename))
    while True:
        event = f.stdout.readline()
    
        event = json.loads(event)
        if event['event_type'] == 'alert':
            print("Attacker IP %s" % event['src_ip'])
            print("Victim IP %s " % event['dest_ip'])
            data = {
                "victim_ip": event['dest_ip'],
                "attacker_ip": event['src_ip']
            }
            try:
                r = requests.post(dvnh_api_url, json=data)
                if r.status_code == 201:
                    print("Sent to DVNH Success")
                elif r.status_code == 400:
                    print("DVNH is processing attack")
                else:
                    print("Something went wrong!!")
            except Exception as e:
                print("Something went wrong!! {}".format(str(e)))

if __name__ == '__main__':
    run()
