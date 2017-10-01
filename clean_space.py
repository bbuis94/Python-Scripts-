#!/usr/bin/env python
#Owner: Bill Buis
#Automatically removes all log files in a specified directory that are older than a specified number of days

import os, time,sys, datetime, zipfile

now = datetime.datetime.now()
if len(sys.argv) < 3:
    print "Incorrect number of arguments, you must specify the target directory and how old the logs are that you want to be deleted"
    sys.exit()
if sys.argv[2].isdigit():
    days = int(sys.argv[2])
else:
    print "Incorrect argument, please specify a correct integer"
    print sys.argv[2]
    sys.exit()

#Converts byte count for files into human-readable units
def sizeof_fmt(num):
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s" % (num, unit)
        num /= 1024.0
    return "%.1f%s" % (num, 'Y')


if not os.path.exists("/usr/local/backups/logs"):
    os.mkdir("/usr/local/backups/")
    os.mkdir("/usr/local/backups/logs")
if not os.path.exists("/usr/local/backups/space_reports"):
    os.mkdir("/usr/local/backups/space_reports")

fixed_files=[]
present = time.time()

#Guarantees that only files that are 30 days or older will be deleted
test = days*86400
f = open("files", "wt")
f2 = open("sizes","wt")

#Writes all log files that are 30 days or older to temporary files for the file's size
#and file name
print "Removing and archiving these files..\n"
for subdir, dirs, files in os.walk(sys.argv[1]):
    for file in files:
        filepath = os.path.join(subdir,file)
        file_time = os.path.getmtime(filepath)
        if filepath.find("/var/log") == 0 and filepath.find("lastlog") < 0:
            if (present - file_time) >= test:
                f.write(filepath + "\n")
                f2.write(str(os.path.getsize(filepath)) + "\n")
                print filepath + " " + sizeof_fmt(os.path.getsize(filepath))
        else:
            if filepath.find(".log") >= 0 or filepath.find("_log") >=0:
                if (present - os.path.getmtime(filepath)) >= test:
                    f.write(filepath + "\n")
                    f2.write(str(os.path.getsize(filepath)) + "\n")
                    print filepath + " " + sizeof_fmt(os.path.getsize(filepath))
            else:
                pass
f.close()
f2.close()
#Collect the file names and sizes and place them into two separate arrays
with open("files") as f3:
    files=f3.readlines()
with open("sizes") as f4:
    file_sizes=f4.readlines()

os.remove("files")
os.remove("sizes")

#Creates new space report if one hasn't been created today or appends an existing one
#if it was created today
file_name = "/usr/local/backups/space_reports/spacereport" + now.strftime("%m-%d-%Y")
if not os.path.exists(file_name):
    report = open(file_name, "wt")
else:
    report = open(file_name,"a")
report.write("Time done: " +time.strftime("%c") + "\n")
report.write("Directory target: " + sys.argv[1] + "\n")
report.write("Removed files:\n\n")
file_sizes = map(int, file_sizes)
for file in files:
    file = file.replace("\n", "")
    fixed_files.append(file)

dir_name = "/usr/local/backups/logs" + now.strftime("%m-%d-%Y") + "logs/"
if not os.path.exists(dir_name):
    os.mkdir(dir_name)

file_sizes = sorted(file_sizes, key=int, reverse=True)

#Writes each file and its size in descending order to a report file and moves the file to a
#compressed zip folder
for size in file_sizes:
    for file in fixed_files:
        if os.path.getsize(file) == size:
            log_path = dir_name + str(os.path.basename(file)) + now.strftime("%m-%d-%Y-%H:%M:%S") + ".zip"
            zf = zipfile.ZipFile(log_path, "w", zipfile.ZIP_DEFLATED, allowZip64 = True)
            zf.write(file, os.path.basename(file))
            report.write(file + " " + str(sizeof_fmt(size)) + "\n")
            fixed_files.remove(file)
            zf.close()
            remove_command = "sudo bash -c 'echo '' > " + file + "'"
            os.system(remove_command)
            os.remove(file)
report.write("\n")
report.close()

