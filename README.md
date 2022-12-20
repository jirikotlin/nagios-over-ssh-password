# nagios-over-ssh-password

Perform nagios check over ssh with password.

Example:

over_ssh_check.py -H example.com -l userslogin -p passw0rd -c '/home/userlogin/check_disk -w 15% -c 10% -W 15% -K 10% -p /dev/sda1'

Optionally, check for the presence of a given string in the output
with: -s string
