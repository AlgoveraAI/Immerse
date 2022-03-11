import requests
import json

#Old API - https://docs.pinata.cloud/api-pinning/pinning-services-api
#New API - https://managed.mypinata.cloud/api/v1/api-docs/#/

#https://medium.com/pinata/how-to-pin-to-ipfs-effortlessly-ba3437b33885
class PinataV1:
    
    def get_creds(self):

        with open("creds.json") as f:

            cred = json.loads(f.read())

        return cred["Pinata"]

    def upload_file(self,fn,cred):

        base_url = "https://api.pinata.cloud/pinning/pinFileToIPFS"

        header = {
                  "pinata_api_key":cred["API Key"],
                    "pinata_secret_api_key":cred["API Secret"]
                  }
        
        
        #Filename,file, content_type, cookie expiration?
        files = {'file': (fn, open(fn, 'rb'),
                          "multipart/form-data", {'Expires': '0'})
                }


        response = requests.post(base_url, headers=header,files=files)

        return response.json(),response.status_code
    
    
    def pin(self,fn,cid,cred):

        base_url = "https://api.pinata.cloud/pinning/pinByHash"

        header = {
                  "pinata_api_key":cred["API Key"],
                    "pinata_secret_api_key":cred["API Secret"]
                  }
        
        data = {
                    # The "pinataMetadata" object will not be part of your content added to IPFS
                    # Pinata simply stores the metadata provided to help you easily query the content you've pinned with Pinata
                    "pinataMetadata": {
                        "name": fn,
                        "keyvalues": {}
                    },
                    "hashToPin": cid
            }
    


        response = requests.post(base_url, headers=header,json=data)

        return response.json(),response.status_code
    
    
    #Appears in documentation, but invalid endpoint
    def unpin(self,cid,cred):

        base_url = "https://api.pinata.cloud/pinning/unpin"

        header = {
                  "pinata_api_key":cred["API Key"],
                    "pinata_secret_api_key":cred["API Secret"]
                  }
        
        data = {"hashToUnpin":cid} #The hash of the content you wish to have Pinata unpin from its nodes.
    


        response = requests.delete(base_url, headers=header,data=data)

        return response.json(),response.status_code
    
    
    #Appears in documentation, but invalid endpoint
    def edit_hash(self,fn,cid,cred):

        base_url = "https://api.pinata.cloud/pinning/hashMetadata"

        header = {
                  "pinata_api_key":cred["API Key"],
                    "pinata_secret_api_key":cred["API Secret"]
                  }
        
        data = {
        "ipfsPinHash": cid,
        "name": fn,
        "keyvalues": {
            "newKey": 'newValue',
            "existingKey": 'newValue',
            "existingKeyToRemove": None
            }
        }
    


        response = requests.put(base_url, headers=header,data=data)

        return response.status_code
        
    
    def get_pinned_files(self,cred,params):
        
        """
        Query Parameters = params
        
        hashContains: (string) - Filter on alphanumeric characters inside of pin hashes. Hashes which do not include the characters passed in will not be returned.

        pinStart: (must be in ISO_8601 format) - Exclude pin records that were pinned before the passed in "pinStart" datetime.

        pinEnd: (must be in ISO_8601 format) - Exclude pin records that were pinned after the passed in "pinEnd" datetime.

        unpinStart: (must be in ISO_8601 format) - Exclude pin records that were unpinned before the passed in "unpinStart" datetime.

        unpinEnd: (must be in ISO_8601 format) - Exclude pin records that were unpinned after the passed in "unpinEnd" datetime.

        pinSizeMin: (integer) - The minimum byte size that pin record you're looking for can have

        pinSizeMax: (integer) - The maximum byte size that pin record you're looking for can have

        status: (string) -
            * Pass in "all" for both pinned and unpinned records
            * Pass in "pinned" for just pinned records (hashes that are currently pinned)
            * Pass in "unpinned" for just unpinned records (previous hashes that are no longer being pinned on pinata)

        pageLimit: (integer) - This sets the amount of records that will be returned per API response. (Max 1000)

        pageOffset: (integer) - This tells the API how far to offset the record responses. For example, 
        if there's 30 records that match your query, and you passed in a pageLimit of 10, providing a pageOffset of 10 would return records 11-20.
        """
        
        base_url = "https://api.pinata.cloud/data/pinList?"
        
        header = {
                  "pinata_api_key":cred["API Key"],
                    "pinata_secret_api_key":cred["API Secret"]
                  }
        
        
        response = requests.get(base_url, headers=header,params=params)

        return response.json(),response.status_code
        
        