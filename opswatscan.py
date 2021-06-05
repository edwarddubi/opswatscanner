import requests
import hashlib
import time

#creat a class to make sure code is organized
class OPSWATSCAN:
    #default constructor
    def __init__(self) -> None:
        self.__api_key = ""
        self.__filename = ""
        self.__endpoint = "https://api.metadefender.com/v4/file"
        self.__hashlink = "https://api.metadefender.com/v4/hash"

    #parameterized constructor
    def __init__(self, api_key, filename) -> None:
        ##make the class attributes private using __
        self.__api_key = api_key
        self.__filename = filename
        self.__endpoint = "https://api.metadefender.com/v4/file"
        self.__hashlink = "https://api.metadefender.com/v4/hash"


    #set a desire api key
    def set_api_key(self, api_key):
        self.__api_key = api_key

    #set a desired file name
    def set_filename(self, filename):
        self.__filename = filename
    
    #read the file with the provided file name
    def read_file(self):
        f=None
        #we use a try catch to protect our block or code and let
        #the user know if the file does not exist
        try:
            f = open(self.__filename, "rb")
            #if there is no exception caught, we return the file and success True
            return f,True
        except FileNotFoundError as e:
            print("File does not exist.")
        except Exception as e:
            print(e)
        #if an exception occurred, we return file for closing and success set to False
        return f,False

    #generating a SHA-1 hash of a file
    def generate_hash_file(self, file):
        #we create a hash object
        hash = hashlib.sha1()
        data_chunk = None
        #we loop through till we reach the end of the file
        while data_chunk != b'':
            #read 1024 bytes everytime 
            data_chunk = file.read(1024)
            #update the data chunk into the hash object
            hash.update(data_chunk)

        #we return the hex representation of the digest
        return hash.hexdigest()

    #check if the file is cached in the cloud 
    def verify_file_existence(self, file):
        #print(file.read())
        file_h = self.generate_hash_file(file)
        #concat the hash file key to the endpoint
        link = self.__hashlink+"/"+str(file_h)
        #set the header
        header = {
            "Content-Type": "application/json",
            "apikey":self.__api_key,
        }
        #make a request to retrieve the cached data
        res = requests.get(url=link, headers=header)
        #parse to json
        r = res.json()
        #print(r)
        #print(res.text)
        #get the data id and if there is a key error we return False
        try:
            if r["data_id"]:
                #print("File was found in the Cloud!")
                scan_details = r["scan_results"]["scan_details"]
                #display the scan result details to the user based on the instructions given
                found_virus="Infected"
                if r["scan_results"]["scan_all_result_a"] == "No Threat Detected":
                    found_virus = "Clean"

                msg="filename: {0}\noverall_status: {1}".format(self.__filename,found_virus)
                print(msg)
                for e,d in scan_details.items():
                    print("engine: {0}".format(e))
                    self.display_engine(d)
                    #print("\n")
                #self.delete(r["data_id"])
                return True
        except KeyError:
            #file does not exist in the cloud, pass
            pass
        return False

    def display_engine(self, details):
        #set to None if no threat was found
        if details["threat_found"] == '':
            details["threat_found"] ="None"

        #msg = "".format()
        #loop through to display the keys and values of each scanning engine
        for i,j in details.items():
            if i == "scan_result_i":
                i = "scan_result"
            print("{0}: {1}".format(i,j))

    def post_req(self, file):
        #get the endpoint
        link = self.__endpoint
        #application/octet-stream
        #multipart/form-data
        #set the header
        #content type must be application/octet-stream
        # it is preferable when uploading files
        # set the api key
        # set the filename
        #print(file.read())
        header = {
                "Content-Type": "application/octet-stream",
                "apikey":self.__api_key,
                "filename":self.__filename
            }
        #params = {}
        #params = json.dumps(params)
        #make a post request to upload the file to the cloud
        res = requests.post(url=link, data=file, headers=header)
        #get the response from the opswat cloud
        r=res.json()
        #print(r)
        id=None
        try:
            #retrieve the data id of the uploaded file
            id = r["data_id"]
        except KeyError:
            #failed to upload file
            print("An error occurred while uploading the file.")
            return
        except Exception as e:
            #print the actual error
            print(e)
            return
        
        if id:
            res = self.get_req(id)
            progress = res["scan_results"]["progress_percentage"]
            #tracking progress until the scan results are available
            while progress != 100:
                print("scanning...{0}%...".format(progress))
                res = self.get_req(id)
                progress = res["scan_results"]["progress_percentage"]
                time.sleep(3)
            #scanning is done so we now display the results to the user
            scan_details = res["scan_results"]["scan_details"]
            found_virus="Infected"
            if res["scan_results"]["scan_all_result_a"] == "No Threat Detected":
                found_virus = "Clean"
            msg="filename: {0}\noverall_status: {1}".format(self.__filename, found_virus)
            print(msg)
            for e,d in scan_details.items():
                print("engine: {0}".format(e))
                self.display_engine(d)

            #self.delete(id)

    #request scan result from opswat cloud with file/data id
    def get_req(self, id):
        link = self.__endpoint+"/"+str(id)
        header = {
            "Content-Type": "application/json",
            "apikey":self.__api_key,
        }
        #we make a request to retrieve the scan result of a file 
        res = requests.get(url=link, headers=header)
        return res.json()

    def delete(self, id):
        link = self.__endpoint+"/converted/"+str(id)
        header = {
            "apikey":self.__api_key,
        }
        #we make a request to retrieve the scan result of a file 
        res = requests.delete(url=link, headers=header)


    def scan_file(self):
        #call the read file function and store the returned results
        f,success=self.read_file()
        if success:
            #since multi-scan is costly, we first check to see if the file exist in the cloud
            e=self.verify_file_existence(f)  
            f.close()
            if not e:
                f,success=self.read_file()
                #it doesn't so we upload the file and get its scanning results
                #print("dont exist in cloud")
                self.post_req(f)
                f.close()
        #close the file object
        print("\n")
            
            
