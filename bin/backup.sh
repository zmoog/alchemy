
DOMAIN_PATH=/home/django/domains/alchemy.selfip.net
PYTHON=$DOMAIN_PATH/alchemy.selfip.net/bin/python


ALCHEMY_HOME=$DOMAIN_PATH/alchemy
ALCHEMY_APP=cash

MESSAGE_SUBJECT="Backup database Alchemy"
MESSAGE_RECIPIENT=maurizio.branca@gmail.com
MESSAGE_ATTACHMENT=/tmp/$ALCHEMY_APP.json
MESSAGE_BODY=$ALCHEMY_HOME/bin/backup-message-body.txt

#
# export cash models data into a JSON encoded file using the Django
# manage.py script.
#
$PYTHON $ALCHEMY_HOME/manage.py dumpdata cash > $MESSAGE_ATTACHMENT

#
# Compress the JSON file.
#
gzip $MESSAGE_ATTACHMENT 
MESSAGE_ATTACHMENT=$MESSAGE_ATTACHMENT.gz

#
# Send the data to the destination email recipient.
#
mutt -s "$MESSAGE_SUBJECT" -a $MESSAGE_ATTACHMENT $MESSAGE_RECIPIENT < $MESSAGE_BODY

#
# Clear the tmp files.
#
rm $MESSAGE_ATTACHMENT
