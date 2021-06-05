# opswatscanner

This is a simple program built to scan a file against the [Metadefender Opswat API](metadefender.opswat.com).

## API

Must have a/an **.env** file and assign your ***API key*** specifically to `OPSWAT_API`. You can have it in your environmental variables too but the key name must always be `OPSWAT_API`.
```Env
OPSWAT_API=API_KEY
```

## Packages

- pip install dotenv
- pip install requests
- hashlib
- time

## How to Run

To run this program, type:
- ***python main.py***

## Input

User must specify an input command after running the app
 - Sample command:
   - <upload_file filename.txt>

## Results 1

Results will be displayed as follows if the file has already being cached
```Python
filename: cmds.txt   
overall_status: Clean
engine: AegisLab
def_time: 2021-06-05T01:00:39.000Z
scan_result: 0
scan_time: 0
threat_found: None
engine: Ahnlab
def_time: 2021-06-05T00:00:00.000Z
scan_result: 0
scan_time: 1
threat_found: None
```

## Results 2

Results will be displayed as follows if file does not exist in the cloud.

```Python
scanning...5%...
scanning...5%...
filename: cmds.txt
overall_status: Clean
engine: AegisLab
def_time: 2021-06-05T01:00:39.000Z
scan_result: 0
scan_time: 0
threat_found: None
engine: Ahnlab
def_time: 2021-06-05T00:00:00.000Z
scan_result: 0
scan_time: 1
threat_found: None
engine: Antiy
def_time: 2021-06-04T12:30:00.000Z
scan_result: 0
scan_time: 0
threat_found: None
engine: Avira
def_time: 2021-06-05T04:16:00.000Z
scan_result: 0
scan_time: 1
threat_found: None

```


