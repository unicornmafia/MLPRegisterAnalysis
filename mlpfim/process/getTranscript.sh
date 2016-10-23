#!/bin/bash

seasonNumber="$1"
episodeNumber="$2"
episodeName="$3"

echo "getting dialog"
php getscripttext.php $seasonNumber $episodeNumber > mlpfim-s${seasonNumber}e${episodeNumber}-dialog-${episodeName}.txt
echo "removing actions from dialog"
sed -i 's/\[[^\]*]//g' mlpfim-s${seasonNumber}e${episodeNumber}-dialog-${episodeName}.txt
echo "removing emphasis from dialog"
sed -i "s/''//g" mlpfim-s${seasonNumber}e${episodeNumber}-dialog-${episodeName}.txt
echo "deleting empty lines"
sed -i '/^\s*$/d' mlpfim-s${seasonNumber}e${episodeNumber}-dialog-${episodeName}.txt

echo "getting speakers"
php getscriptspeakers.php $seasonNumber $episodeNumber > mlpfim-s${seasonNumber}e${episodeNumber}-speakers-raw-${episodeName}.txt
echo "finding unique speakers"
grep -o -E '\w+' mlpfim-s${seasonNumber}e${episodeNumber}-speakers-raw-${episodeName}.txt | sort -u -f > mlpfim-s${seasonNumber}e${episodeNumber}-speakers-unique-${episodeName}.txt



