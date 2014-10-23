find . -type f -exec head -1 \{\} \; | sort -t " " -k 2 -g -r > AA_listing.txt
