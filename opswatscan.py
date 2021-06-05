import requests
import hashlib
import time


class OPSWATSCAN:
    
    def __init__(self) -> None:
        self.__api_key = ""
        self.__filename = ""
        self.__endpoint = "https://api.metadefender.com/v4/file"
        self.__hashlink = "https://api.metadefender.com/v4/hash"

    def __init__(self, api_key, filename) -> None:
        self.__api_key = api_key
        self.__filename = filename
        self.__endpoint = "https://api.metadefender.com/v4/file"
        self.__hashlink = "https://api.metadefender.com/v4/hash"


    #set a desire api
    def set_api_key(self, api_key):
        self.__api_key = api_key

    def set_filename(self, filename):
        self.__filename = filename
    
    def read_file(self):
        f=None
        try:
            f = open(self.__filename, "rb")
            return f,True
        except FileNotFoundError as e:
            print("File does not exist.\n")
        return f,False

    def generate_hash_file(self, file):
        hash = hashlib.sha1()
        data_chunk = None
        while data_chunk != b'':
            data_chunk = file.read(1024)
            hash.update(data_chunk)
        return hash.hexdigest()

    def verify_file_existence(self, file):
        file_h = self.generate_hash_file(file)
        link = self.__hashlink+"/"+str(file_h)
        header = {
            "Content-Type": "application/json",
            "apikey":self.__api_key,
        }
        res = requests.get(url=link, headers=header)
        r = res.json()
        #print(r)
        try:
            if r["data_id"]:
                #print("File was found in the Cloud!")
                scan_details = r["scan_results"]["scan_details"]
                msg="filename: {0}\noverall_status: Clean".format(self.__filename)
                print(msg)
                for e,d in scan_details.items():
                    print("engine: {0}".format(e))
                    self.display_engine(d)
                    #print("\n")

                return True
        except KeyError:
            pass
        return False

    def display_engine(self, details):
        if details["threat_found"] == '':
            details["threat_found"] ="None"

        #msg = "".format()
        
        for i,j in details.items():
            if i == "scan_result_i":
                i = "scan_result"
            print("{0}: {1}".format(i,j))


    def post_req(self, file):
        link = self.__endpoint
        #application/octet-stream
        #multipart/form-data
        header = {
                "Content-Type": "application/octet-stream",
                "apikey":self.__api_key,
                "filename":self.__filename
            }
        #params = {}
        #params = json.dumps(params)

        res = requests.post(url=link, data=file, headers=header)
        r=res.json()
        id=None
        try:
            id = r["data_id"]
        except KeyError:
            pass
        
        if id:
            res = self.get_req(id)
            while res["scan_results"] == None:
                res = self.get_req(id)
                time.sleep(2)
            scan_details = res["scan_results"]["scan_details"]
            msg="filename: {0}\noverall_status: Clean".format(self.__filename)
            print(msg)
            for e,d in scan_details.items():
                print("engine: {0}".format(e))
                self.display_engine(d)


    def get_req(self, id):
        link = self.__endpoint+"/"+str(id)
        header = {
            "Content-Type": "application/json",
            "apikey":self.__api_key,
        }
        res = requests.get(url=link, headers=header)
        return res.json()


    def scan_file(self):
        f,success=self.read_file()
        if success:
            e=self.verify_file_existence(f)
            if not e:
                self.post_req(f)
        
        f.close()
            
