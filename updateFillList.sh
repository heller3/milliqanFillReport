echo "Attempting to query for fill information."
./fills.py -y 2018
if [ `cat rawFillList2018.txt | wc -l` -gt 0 ]
then 
    echo "Got raw fill information. Converting for milliqanOffline format."
    ./processFillList.py
    if [ `cat processedFillList2018.txt | wc -l` -gt 0 ]
    then
	echo "Successfully converted."
	scp processedFillList2018.txt milliqan@cms2.physics.ucsb.edu:/net/cms26/cms26r0/milliqan/milliqanOffline/
	echo "Sent to UCSB."
    else
	echo "Error: processed fill list was empty."
	fi
else 
    echo "Error getting fill information."
fi
