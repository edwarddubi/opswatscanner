import os
from dotenv import load_dotenv
load_dotenv()
from opswatscan import OPSWATSCAN

    

def main():
    op_api = os.getenv("OPSWAT_API")
    if op_api == None:
        print("API Key cannot be empty. Please provide an API Key.\n")  
    else:
        inp = input()
        inp = "upload_file cmds.txt"
        if inp[:11] == "upload_file":
            filename = inp[11:]
            if len(filename) != 0:
                op = OPSWATSCAN(op_api, filename.strip())
                op.scan_file()
                op.test_api()
            else:
                print("Invalid file name input.\n")
        else:
            print("Invalid command.\n")
        
        

main()
