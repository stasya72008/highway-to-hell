. /home/develop/source.rc

touch $FILE_LOG_MYIP;

echo '#' `date` >> $FILE_LOG_MYIP;
curl -s checkip.dyndns.org | sed -e 's/.*Current IP Address: //' -e 's/<.*$//' >> $FILE_LOG_MYIP;

