import requests
import hashlib


class OPSWATSCAN:
    
    def __init__(self) -> None:
        pass

    def __init__(self, api_key, filename) -> None:
        self.__api_key = api_key
        self.__filename = filename
        self.__endpoint = "https://api.metadefender.com/v4/file"
        self.__hashlink = "https://api.metadefender.com/v4/hash/"

    
    def read_file(self):
        f=None
        try:
            f = open(self.__filename, "rb")
            return f,True
        except FileNotFoundError as e:
            print("File does not exist.\n")
        return f,False

    def test_api(self):
        link = "https://api.metadefender.com/v4/hash/66DA1A91E1ED5D59BECFAD85F53C05F9"
        params = {
            "apikey":self.__api_key
        }

        res = requests.post(url=link, params=params)
        print(res.json())

    def generate_hash_file(self, file):
        hash = hashlib.sha1()
        data_chunk = None
        while data_chunk != b'':
            data_chunk = file.read(1024)
            hash.update(data_chunk)
        return hash.hexdigest()

    def verify_file_existence(self, file):
        file_h = self.generate_hash_file(file)
        link = self.__hashlink+str(file_h)
        header = {
            "Content-Type": "application/json",
            "apikey":self.__api_key,
        }
        res = requests.get(url=link, headers=header)
        r = res.json()
        print(r)
        if r["data_id"]:
            return True
        else:
            return False

    def post_req(self, file):
        link = self.__endpoint
        #application/octet-stream
        #multipart/form-data
        header = {
                "Content-Type": "application/octet-stream",
                "apikey":self.__api_key,
                "filename":self.__filename
            }
        params = {}
        #params = json.dumps(params)

        res = requests.post(url=link, data=file, headers=header)
        print(res.json())


    def get_req(self):
        params = {
            "apikey":self.api_key
        }
        res = requests.post(url=self.__endpoint, params=params)
        print(res.json())


    def scan_file(self):
        f,success=self.read_file()
        if success:
            e=self.verify_file_existence(f)
            if not e:
                self.post_req(f)
            else:
                print("File has already being uploaded and scanned.")
        
        f.close()
            
