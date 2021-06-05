# opswatscanner

This is a simple program built to scan a file against the [Metadefender Opswat API](metadefender.opswat.com).

## Input

User must specify an input command
 - Sample command:
   - <upload_file filename.txt>

## API

Must have a/an **.env** file and assign your ***API key*** specifically to `OPSWAT_API` .
```Env
OPSWAT_API=API_KEY
```