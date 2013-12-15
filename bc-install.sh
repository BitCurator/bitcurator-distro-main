#!/bin/bash

# BitCurator Install Scripts
# Last updated: December 15, 2013
#
# BitCurator is free and open source. You can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License version 3. 
#
# You should have received a copy of the GNU General Public License
# along with Archivematica. If not, see <http://www.gnu.org/licenses/>.

# @package BitCurator 
# @author Kam Woods <kamwoods@bitcurator.net>
# @version svn: $Id$

user_home=$HOME
curr_dir=`pwd`
cd `dirname $0`

echo "Ok, let's get started."
echo ""
echo "It looks like your current working directory is ${curr_dir}"
echo "We'll be installing some software in ${user_home}"

# Check for next available UID
uid_avail=`awk -F: '{uid[$3]=1}END{for(x=1000; x<=1100; x++) {if(uid[x] != ""){}else{print x; exit;}}}' /etc/passwd`
echo "Next UID available: ${uid_avail}"

# Need to add nopasswdlogin here
part="create the default BitCurator user (bcadmin)"
echo -n "\"Would you like to ${part}?\" (y/N) "
read a
if [[ $a == "Y" || $a == "y" ]]; then
echo "Going to ${part} ..."
        #echo "sudo adduser --uid ${uid_avail} --group --system --home /home/bcadmin bcadmin"
        #echo "sudo gpasswd -a $USER bcadmin"
        sudo adduser --uid ${uid_avail} --group --system --home /home/bcadmin bcadmin
        sudo gpasswd -a $USER bcadmin
else
echo "Not going to ${part}"
fi

part_a="install BitCurator dependencies (this may take some time)"
part_b="install BitCurator dependencies"
echo -n "\"Would you like to ${part_a}?\" (y/N) "
read a
if [[ $a == "Y" || $a == "y" ]]; then
echo "Going to ${part_b} ..."
        #echo "sudo apt-get install bitcurator-dep_0.5.6_all.deb -y"
        sudo dpkg -i debs/bitcurator-dep_0.5.6_all.deb
else
echo "Not going to ${part}"
fi

part="add the Guymager repository and install the latest version"
echo -n "\"Would you like to ${part}?\" (y/N) "
read a
if [[ $a == "Y" || $a == "y" ]]; then
	sudo wget -nH -rP /etc/apt/sources.list.d/ http://deb.pinguin.lu/pinguin.lu.list        
	wget -q http://deb.pinguin.lu/debsign_public.key -O- | sudo apt-key add -
	sudo apt-get update
	sudo apt-get install guymager-beta
else
echo "Not going to ${part}"
fi

part="add the YaD PPA repository and install YaD"
echo -n "\"Would you like to ${part}?\" (y/N) "
read a
if [[ $a == "Y" || $a == "y" ]]; then
        sudo apt-get install python-software-properties -y
        sudo apt-add-repository ppa:webupd8team/y-ppa-manager
        sudo apt-get update
        sudo apt-get install yad
else
echo "Not going to ${part}"
fi

part="copy BitCurator folders and shortcuts to the desktop"
echo -n "\"Would you like to ${part}?\" (y/N) "
read a
if [[ $a == "Y" || $a == "y" ]]; then
	curr_dir=${pwd}
	cp -r $pwd/env/desktop-folders ${user_home}/Desktop
else
echo "Not going to ${part}"
fi

exit
