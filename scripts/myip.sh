touch /home/den/Documents/myip.log;

echo '#' `date` >> /home/den/Documents/myip.log ;
curl -s checkip.dyndns.org | sed -e 's/.*Current IP Address: //' -e 's/<.*$//' >>/home/den/Documents/myip.log
