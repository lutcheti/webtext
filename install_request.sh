# to do before using the "request server"
# Tools for Weboob
sudo aptitude install python-html2text python-mechanize libyaml-0-2 python2.7-simplejson python-setuptools pyqt4-dev-tools python-dev libxml2-dev libxslt1-dev python-prettytable zlib1g-dev
# Weboob
sudo aptitude install weboob
# PHP
sudo aptitude install php5 
sudo aptitude install curl libcurl3 php5-curl

mkdir src/request/tmp
# for the webtext's API
sudo chgrp www-data -R /var/www/webtext
sudo mkdir /var/www/webtext
sudo mkdir /var/www/webtext/api
sudo cp sms.php /var/www/webtext/api
sudo chmod u+x /var/www/webtext/api/sms.php