cd ~
find . -type f -printf '%p ---- %k\n' > filesizes.txt

if [ $( wc -l < filesizes.txt ) -eq $( grep -o ' ---- ' filesizes.txt | wc -l ) ]
then
	echo "good"
else
	echo "bad"
fi