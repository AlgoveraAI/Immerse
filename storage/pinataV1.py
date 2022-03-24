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
                    "pinata_secret_api_key":cred["API Secret"],
                  }


        f_bytes = {"file":(fn,open(fn,"rb"),'multipart/form-data')}
        
        payload = {"metadata":
                {"pinataMetadata": {
                        "name": "name",
                        "keyvalues": {
                            "customKey": 'customValue',
                            "customKey2": 'customValue2'
                        }
                    },
                    "pinataOptions": {
                        "cidVersion": 1
                        }
                    }
                }
        

        response = requests.post(base_url, headers=header,files=f_bytes,data=payload)

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
                    "hashToPin": cid,
            
                    
            }
    


        response = requests.post(base_url, headers=header,json=data)

        return response.json(),response.status_code
    
    
    #Appears in documentation, but invalid endpoint
    def unpin(self,cid,cred):

        base_url = "https://api.pinata.cloud/pinning/unpin/"

        header = {
          "pinata_api_key":cred["API Key"],
            "pinata_secret_api_key":cred["API Secret"]
          }

        response = requests.delete(base_url + cid,headers=header)

        return response.status_code
    
    
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
    
    def pin_policy(self,cid,cred,region="NYC1",replications=2):
        
        """
        FRA1 - Frankfurt, Germany (max 2 replications)
        NYC1 - New York City, USA (max 2 replications)
        """
        
        base_url = "https://api.pinata.cloud/pinning/hashPinPolicy"

        header = {
                  "pinata_api_key":cred["API Key"],
                    "pinata_secret_api_key":cred["API Secret"]
                  }
        
        data = {
                "ipfsPinHash": cid,
                "newPinPolicy": {
                    "regions": [
                        {
                            "id": region,
                            "desiredReplicationCount": replications
                        },
                    ]
                }
            }
        
        
        response = requests.put(base_url, headers=header,data=data)

        return response.json(),response.status_code
        
        
    def globalpin_policy(self,cred,region="NYC1",replications=2):
        
        """
        FRA1 - Frankfurt, Germany (max 2 replications)
        NYC1 - New York City, USA (max 2 replications)
        """
        
        base_url = "https://api.pinata.cloud/pinning/userPinPolicy"

        header = {
                  "pinata_api_key":cred["API Key"],
                    "pinata_secret_api_key":cred["API Secret"]
                  }
        
        data = {
                "newPinPolicy": {
                    "regions": [
                        {
                            "id": region,
                            "desiredReplicationCount": replications
                        },
                    ]
                }
            }
        
        
        response = requests.put(base_url, headers=header,data=data)

        return response.json(),response.status_code
    
    
    def get_pinned_jobs(self,cred,params=None):
        
        """
        "sort" - Sort the results by the date added to the pinning queue (see value options below)
        "ASC" - Sort by ascending dates
        "DESC" - Sort by descending dates
        "status" - Filter by the status of the job in the pinning queue (see potential statuses below)
        "prechecking" - Pinata is running preliminary validations on your pin request.
        "searching" - Pinata is actively searching for your content on the IPFS network. This may take some time if your content is isolated.
        "retrieving" - Pinata has located your content and is now in the process of retrieving it.
        "expired" - Pinata wasn't able to find your content after a day of searching the IPFS network. Please make sure your content is hosted on the IPFS network before trying to pin again.
        "over_free_limit" - Pinning this object would put you over the free tier limit. Please add a credit card to continue pinning content.
        "over_max_size" - This object is too large of an item to pin. If you're seeing this, please contact us for a more custom solution.
        "invalid_object" - The object you're attempting to pin isn't readable by IPFS nodes. Please contact us if you receive this, as we'd like to better understand what you're attempting to pin.
        "bad_host_node" - You provided a host node that was either invalid or unreachable. Please make sure all provided host nodes are online and reachable.
        "ipfs_pin_hash" - Retrieve the record for a specific IPFS hash
        "limit" - Limit the amount of results returned per page of results (default is 5, and max is 1000)
        "offset" - Provide the record offset for records being returned. This is how you retrieve records on additional pages (default is 0)
        """
        
        base_url = "https://api.pinata.cloud/pinning/pinJobs/"
        
        header = {
                  "pinata_api_key":cred["API Key"],
                    "pinata_secret_api_key":cred["API Secret"]
                  }
        
        
        response = requests.get(base_url, headers=header,params=params)

        return response.json(),response.status_code
        
    
    def get_pinned_files(self,cred,params=None):
        
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
    
    
    
    
 
    
    def get_datausage(self,cred,params=None):
                
        header = {
                  "pinata_api_key":cred["API Key"],
                    "pinata_secret_api_key":cred["API Secret"]
                  }
        
        base_url = "https://api.pinata.cloud/data/userPinnedDataTotal"
        
        
        response = requests.get(base_url, headers=header,params=params)

        return response.json(),response.status_code

        
        