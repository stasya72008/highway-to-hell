. /home/develop/source.rc

MYIP=`curl -s checkip.dyndns.org | sed -e 's/.*Current IP Address: //' -e 's/<.*$//'`

MAIL_TEXT="To: $MAILS\nSubject: IP $MYIP\n\n  System rebooted, IP: $MYIP";
     
echo -e $MAIL_TEXT | /usr/sbin/sendmail -t;

