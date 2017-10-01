# Python-Scripts-
A collection of Python scripts that I've written for practical usage.

# clean_space.py usage:

`sudo python clean_space.py [target directory] [age of logs]`

# clean_space.py description:

The purpose of this script is to delete and archive log files that are taking up space on a drive. The script takes a target directory and age of logs to be deleted as parameters. The script then recursively searches through the specified target directory and deletes and archives all files that have "/var/log" in their path name or contain ".log" or "_log" in their file name. The archived files are place under /usr/local/ops/backups/logs udner a directory whose name contains a timestamp of when the script was ran. The script also generates a space report under /usr/local/ops/backups/space_reports which specifies the date the script was ran as well as which logs were deleted and archived, sorted in descending order by log size.
 
