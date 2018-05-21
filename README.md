# milliqanFillReport

This repository includes scripts for querying the OMS database for the fill report, processing it for milliqanOffline, and sending it to UCSB.

The first script, `fills.py`, is mostly written by the WBM experts for querying the OMS API.
I have added a few lines at the end to print the information to a text file, `rawFillList2018.txt`
It can be executed like this:
```
    ./fills.py -y 2018
``` 

The next script, `processFillList.py`, reorganizes this information with timestamps for milliqanOffline, and outputs `processedFillList2018.txt`

The entire process can be executed with a single script which gets the new fill list and sends it to UCSB:

```
    ./updateFillList.sh
```
