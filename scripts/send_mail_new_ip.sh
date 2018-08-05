. /home/develop/source.rc


echo "#" `date` "Start..." >> $FILE_LOG_SEND_MAIL;


grep -v '#' $FILE_LOG_MYIP | tail -n2 >  /tmp/temp;
IFS=$'\n' read -d '' -r -a lines < /tmp/temp;
rm /tmp/temp;


if [ "${lines[0]}" != "${lines[1]}" ]; then

    echo `date`" new ip: ${lines[1]} sending mail to: $MAILS" >> $FILE_LOG_SEND_MAIL;
    MAIL_TEXT="To: $MAILS\nSubject: New IP ${lines[1]}\n\n  ip was changed\n old: ${lines[0]}\n new: ${lines[1]}";
    echo -e $MAIL_TEXT | /usr/sbin/sendmail -t;

fi;


echo "# ...Finish" >> $FILE_LOG_SEND_MAIL;


