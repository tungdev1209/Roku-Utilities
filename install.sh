#!/bin/sh
# Created by TungDev1209

# Config
path="path/to/project/dir"
rokuIP="192.168.x.x"
rokuName="rokudev"
rokuPass="xxxx"

cd $path
rm out/channel.zip

# Compress
zip -r out/channel.zip .settings .buildpath .project manifest components configs fonts images source

# Install
HTTPSTATUS=$(curl --silent --write-out "\n%{http_code}\n" $rokuIP)
if [ $HTTPSTATUS == "401" ];
then
	curl --user $rokuName:$rokuPass --digest -s -S -F "mysubmit=Install" -F "archive=@out/channel.zip" -F "passwd=" http://$rokuIP/plugin_install > out/response.html
	lynx -dump out/response.html > out/response.txt
	response=$(cat out/response.txt)
	if [[ $response = *"Install Failure"* ]]; then
		echo $response
	elif [[ $response = *"Install Success"* ]]; then
		echo $response
	else
		echo "Identical to previous version - launching..."
		curl -d '' 'http://$rokuIP:8060/launch/dev'
	fi
else
	echo $HTTPSTATUS
	curl -s -S -F "mysubmit=Install" -F "archive=@out/channel.zip" -F "passwd=" http://$rokuIP/plugin_install
fi

rm out/response.html
rm out/response.txt
