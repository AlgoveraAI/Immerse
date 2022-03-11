from io import StringIO
import pandas as pd

def read_file(b):

    s=str(b,'utf-8')

    data = StringIO(s) 

    df=pd.read_csv(data)
    
    return df

#https://docs.ipfs.io/reference/http/api/#getting-started
import requests
import random

class IPFS:

    def get_peers(self):

        return requests.post("http://127.0.0.1:5001/api/v0/swarm/peers",).json()

    #Flags aren't working
    def add(self,fn):

        params = {'progress':True,
                 "silent":False
                 }

        files = {
        'file': (fn, open(fn, 'rb')),
        }

        response = requests.post('http://127.0.0.1:5001/api/v0/add', json=params, files=files)

        print("Added",fn,"to IPFS - ","Response",response.status_code)

        return response

    def get_file(self,key,local_node=True):
        params = (('arg', key),)
        
        if local_node:

            response = requests.post('http://127.0.0.1:5001/api/v0/cat?', params=params)
            
        else:
            
            
            #Sourced - All had green checkmarks as of 03/08/2022
            #https://ipfs.github.io/public-gateway-checker/
            gateways = ["https://infura-ipfs.io","https://cf-ipfs.com","https://dweb.link","https://astyanax.io"]
            
            selected_gateway = gateways[random.randint(0,len(gateways)-1)]
            
            
            response = requests.get(f"{selected_gateway}/ipfs/{key}")
            

        print("Retrieved file hash",key,f"from {selected_gateway}","Response",response.status_code)

        return response