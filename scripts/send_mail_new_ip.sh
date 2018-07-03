# MAILS="wwwouser@gmail.com"
MAILS="wwwouser@gmail.com, balakhovskastanislava@gmail.com"

echo "#" `date` "Start..." >> /home/den/Documents/send_mail.log;


tail /home/den/Documents/myip.log -n 3 | grep -v '#' > /tmp/temp;
IFS=$'\n' read -d '' -r -a lines < /tmp/temp;
rm /tmp/temp;



if [ "${lines[0]}" != "${lines[1]}" ]; then


    echo `date`" new ip: ${lines[1]} sending mail to: $MAILS" >> /home/den/Documents/send_mail.log;
    
    MAIL_TEXT="To: $MAILS\nSubject: New IP ${lines[1]}\n\n  ip was changed\n old: ${lines[0]}\n new: ${lines[1]}";
     
    echo -e $MAIL_TEXT | /usr/sbin/sendmail -t;
 
 fi;







