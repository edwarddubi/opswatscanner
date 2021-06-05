import os
from dotenv import load_dotenv
load_dotenv()
from opswatscan import OPSWATSCAN

    

def main():
    ##get the api key
    op_api = os.getenv("OPSWAT_API")
    #if none we ask user to provide the key  
    if op_api == None:
        print("API Key cannot be empty. Please provide an API Key.\n")  
    else:
        #get input from the user
        inp = input("Type an input: ")
        #inp = "upload_file cmds.txt"
        #validating acceptable token
        if inp[:11] == "upload_file":
            filename = inp[11:]
            #make sure we dont have an empty filename
            #cant do anything with empty filename
            if len(filename) != 0:
                #construct an OPSWATSCAN object
                #print(filename)
                op = OPSWATSCAN(op_api, filename.strip())
                #call scan_file to scan file and show results
                op.scan_file()
            else:
                print("Invalid file name input.\n")
        else:
            print("Invalid command.\n")
        
        
if __name__ == "__main__":
    ##make sure our package is the main file
    main()
