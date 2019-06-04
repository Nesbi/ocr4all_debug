#!bin/bash
##########################################################################################
# Skript for uploading artifacts to out artifactory that exceed the 100mb cap in the GUI #
##########################################################################################

# Data to upload
read -p "WAR:" WAR
read -p "POM:" POM

read -p "Project name:" NAME
read -p "Project version:" VERSION


# Ask for user
read -p "User:" USER

# Ask for password
echo -n "Password:"
read -s PW
echo 

curl -X PUT -u $USER:$PW -T "$POM" "http://artifactory-ls6.informatik.uni-wuerzburg.de/artifactory/libs-snapshot/de/uniwue/$NAME/$VERSION/$NAME-$VERSION.pom"
curl -X PUT -u $USER:$PW -T "$WAR" "http://artifactory-ls6.informatik.uni-wuerzburg.de/artifactory/libs-snapshot/de/uniwue/$NAME/$VERSION/$NAME-$VERSION.war"
