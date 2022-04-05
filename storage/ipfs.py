#https://docs.ipfs.io/reference/http/api/#getting-started
import requests
import random

class IPFS:
    
    def dht_get_file(self,cid):
        
        params = {"verbose":True}
        
        return requests.post(f"http://127.0.0.1:5001/api/v0/dht/get?arg={cid}",params)
    
    def get_dht(self,peerID):
        
        params = {"verbose":True}
        
        return requests.post(f"http://127.0.0.1:5001/api/v0/dht/query?arg={peerID}",params=params)
        
        

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

    def get_file(self,cid,local_node=False):
        params = (('arg', cid),)
        
        if local_node:

            response = requests.post('http://127.0.0.1:5001/api/v0/cat?', params=params)
            
            print("Retrieved file hash",cid,f"from Local Node","Response",response.status_code)
            
        else:
            
            #Sourced - All had green checkmarks as of 03/08/2022
            #https://ipfs.github.io/public-gateway-checker/
            gateways = ["https://infura-ipfs.io","https://cf-ipfs.com","https://dweb.link","https://astyanax.io"]
            
            random.shuffle(gateways)
            
            log = []
            
            for gateway in gateways:

                response = requests.get(f"{gateway}/ipfs/{cid}")
                
                if response.status_code == 200:
                                                            
                    print("Retrieved file hash",cid,f"from {gateway}","Response",response.status_code)
                    
                    return response, log
                    
                    break

                    
                log.append(gateway)

        