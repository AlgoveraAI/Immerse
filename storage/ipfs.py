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
    
    def get_dht(self,peerID):
        
        params = {"verbose":True}
        
        return requests.post(f"http://127.0.0.1:5001/api/v0/dht/query?arg={peerID}")
        
        

    def get_peers(self,verbose=True,streams=False,latency=False,direction=False):
        
        params = {"verbose":verbose,
                 "streams":streams,
                 "latency":latency,
                 "direction":direction}

        return requests.post("http://127.0.0.1:5001/api/v0/swarm/peers",params=params).json()

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

    def get_file(self,cid,local_node=True):
        params = (('arg', cid),)
        
        if local_node:

            response = requests.post('http://127.0.0.1:5001/api/v0/cat?', params=params)
            
            print("Retrieved file hash",cid,f"from Local Node","Response",response.status_code)
            
        else:
            
            
            #Sourced - All had green checkmarks as of 03/08/2022
            #https://ipfs.github.io/public-gateway-checker/
            gateways = ["https://infura-ipfs.io","https://cf-ipfs.com","https://dweb.link","https://astyanax.io"]
            
            selected_gateway = gateways[random.randint(0,len(gateways)-1)]
            
            
            response = requests.get(f"{selected_gateway}/ipfs/{cid}")
            

            print("Retrieved file hash",cid,f"from {selected_gateway}","Response",response.status_code)

        return response