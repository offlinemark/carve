#!/usr/bin/env python

import os
import shutil
import sqlite3 as sql
import subprocess
import sys

root_dir = '/Users/mark/code/sec/forensics/ciphertech/iOS4_logical_acquisition/'
root_output_dir = '/Users/mark/code/sec/forensics/ciphertech/carvings/'
# targets = ['Library', 'Address Book', 'Calendar', 'Cookies', 'Mail', 'Maps', 'Safari', 'SMS', 'Voicemail']
# targets = ['./mobile/Library/AddressBook', './mobile/Library/Calendar']
targets = ['AddressBook', 'Calendar']

def die():
    sys.exit()

### main ##########

def main():
    os.chdir(root_dir);
    os.mkdir(root_output_dir)

    print os.getcwd()
    for root, dirs, files in os.walk('.'):
        # print dirs
        # if (root in targets) or (root in dirs)
        # print dirs
        for d in dirs:
            if d in targets:
                # print d
                # print dirs
                # print root
                # print files
                output_dir = root_output_dir + d
                os.mkdir(output_dir)
                # os.chdir(root)
                # print os.listdir(root + "/" + d)
                print os.getcwd()
                print root
                for f in os.listdir(root + "/" + d):
                    cmd = "file %s" % (root + "/" + d + "/" + f)
                    print cmd
                    cmd_obj = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
                    cmd_output = cmd_obj.communicate()[0]
                    print cmd_output
                    if 'SQLite' in cmd_output:
                        shutil.copy(root + "/" + d + "/" + f, output_dir) 


if __name__ == '__main__':
    main()