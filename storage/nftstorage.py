#Source https://nft.storage/api-docs/
import requests
# from scipy.io import wavfile
# import argparse
# import numpy as np
import json
import pprint

class NFTStorage:

    def get_creds(self):

        with open("creds.json") as f:

            cred = json.loads(f.read())

        return cred["NFTStorage"]

    def upload_file(self,fn,cred):

        base_url = "https://api.nft.storage/upload"

        header = {
                "Content-Type": "form-data",
                  "Authorization":"Bearer " + cred,
                  }
        
        
        data = open(fn,"rb")

        response = requests.post(base_url, headers=header,data=data)

        return response.json(),response.status_code


    def get_file(self,cid,cred):

        base_url = f"https://api.nft.storage/{cid}"

        header = {"Content-Type": "form-data",
                  "Authorization":"Bearer " + cred
                  }

        response = requests.get(base_url, headers=header)

        return response.json()

    def get_all_files(self,cred):

        base_url = f"https://api.nft.storage/"

        header = {"Content-Type": "form-data",
                  "Authorization":"Bearer " + cred
                  }

        response = requests.get(base_url, headers=header)

        return response


    def unpin(self,cid,cred):

        base_url = f"https://api.nft.storage/{cid}"

        header = {"Content-Type": "form-data",
                  "Authorization":"Bearer " + cred
                  }

        response = requests.delete(base_url, headers=header)

        return response


    def check(self,cid,cred):
        header = {"Content-Type": "form-data",
                  "Authorization":"Bearer " + cred
                  }
        response = requests.get(f"https://api.nft.storage/check/{cid}",headers=header)

        return response.json()

    def flow(self,blob,cid=None):

        cred = get_creds()

        if cid:
            check_response = check(cid,cred)

            if check_response["ok"]:

                return check_response

            else:
                print("file does not exist")


        else:
            u_response = upload_file(blob,cred)
            check_response = check(cid,cred)

            return (u_response,check_response)
