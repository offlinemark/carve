#!/usr/bin/env python

import csv
import datetime
import os
import shutil
import sqlite3 as sql
import subprocess
import sys
import plistlib as pl
import pdb

# configs
root_dir = '/Users/mark/code/sec/forensics/ciphertech/iOS4_logical_acquisition/'
root_output_dir = '/Users/mark/code/sec/forensics/ciphertech/carvings/'
targets = ['AddressBook', 'Calendar', 'Cookies', 'Mail', 'Maps', 'Safari', 'SMS', 'Voicemail', 'Keyboard', 'Logs', 'SystemConfiguration']

### functions ##########

def die(msg=''):
    sys.exit(msg)

def dir_scrape():
    """Traverses directories, searching for sqlite databases and plist files, as specified in targets list."""

    for root, dirs, files in os.walk('.'):
        # print dirs
        # if (root in targets) or (root in dirs)
        for d in dirs:
            if d in targets:

                # the Mail directory setup is weird, so special case
                if d == 'Mail':
                    output_dir = root_output_dir + d
                    os.mkdir(output_dir)
                    os.chdir(root + '/Mail')
                    mail_pre_carve(output_dir)
                    os.chdir(root_dir)
                    continue

                if d == 'Cookies' or d == 'Keyboard':
                    output_dir = root_output_dir + d
                    try:
                        os.mkdir(output_dir)
                    except:
                        pass
                    for f in os.listdir(root + "/" + d):
                        shutil.copy(root + '/' + d + '/' + f, output_dir)
                    continue

                if d == 'Logs':
                    output_dir = root_output_dir + d
                    try:
                        os.mkdir(output_dir)
                    except:
                        pass
                    os.chdir(root + '/Logs')
                    log_pre_carve(output_dir)
                    os.chdir(root_dir)
                    continue

                # print d
                # print dirs
                # print root
                # print files
                output_dir = root_output_dir + d
                try:
                    os.mkdir(output_dir)
                except OSError:
                    continue
                # os.chdir(root)
                # print os.listdir(root + "/" + d)
                # print os.listdir(root + "/" + d)
                for f in os.listdir(root + "/" + d):
                    cmd = "file '%s'" % (root + "/" + d + "/" + f)
                    # print cmd
                    cmd_obj = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
                    cmd_output = cmd_obj.communicate()[0]
                    # print cmd_output
                    if ('SQLite' in cmd_output) or ('Apple binary' in cmd_output) or ('XML' in cmd_output) or ('Adapt' in cmd_output):
                        # print cmd_output
                        shutil.copy(root + "/" + d + "/" + f, output_dir) 
                        # print root + "/" + d + "/" + f + "   =>  " + output_dir
                        # print
                        # print

def log_pre_carve(output_dir):
    for root, dirs, files in os.walk('.'):
        if 'general.log' in files:
            shutil.copy(root + '/general.log', output_dir)
            break

def mail_pre_carve(output_dir):
    # how fucking scary does this look
    # not actually that bad ;)

    for item in os.listdir('.'):
        if 'Protected' in item:
            shutil.copy(item, output_dir)
            continue
        if item[0:4] == 'IMAP':
            for root, dirs, files in os.walk(item):
                if 'Messages' in root:
                    for f in files:
                        shutil.copy(root + '/' + f, output_dir)
    pass

def cal_carve():
    """Asssumes it is currently in the output directory (carvings). Finds /Calendar and performs analysis of db."""
    
    os.chdir('Calendar')
    cal_content = []
    start_ts = ''
    end_ts = ''

    # indexes
    id = 0
    summary = 1
    location = 2
    description = 3
    start_date = 4
    loc = 5
    end_date = 6

    for file in os.listdir('.'):
        conn = sql.connect(file)
        c = conn.cursor()

        c.execute('SELECT * from Event')
        cal_content = c.fetchall()

        with open(file.split('.')[0] + "_summary.txt", 'w') as f:
            for row in cal_content:
                start_ts = str(datetime.datetime.fromtimestamp(row[4]))
                end_ts = str(datetime.datetime.fromtimestamp(row[6]))

                f.write('Event ' + str(row[id]) + ':\n\n')
                f.write('Summary: ' + row[summary] + '\n')
                f.write('Description: ' + str(row[description]) + '\n')
                f.write('Location: ' + row[location] + '\n')
                f.write('Start: ' + start_ts + '\n')
                f.write('End: ' + end_ts + '\n')

        conn.close()

    os.chdir(root_output_dir)


def sms_carve():
    """Asssumes it is currently in the output directory (carvings). Finds /SMS and performs analysis of db."""

    os.chdir('SMS')
    sms_contents = []
    ts = ''
    destination = ''

    # indexes
    id = 0
    phone_number = 1
    date = 2
    text = 3
    recipient = 15

    for file in os.listdir('.'):
        conn = sql.connect(file)
        c = conn.cursor()

        c.execute('SELECT * from message')
        sms_contents = c.fetchall()

        with open(file.split('.')[0] + "_summary.txt", 'w') as f:
            for row in sms_contents:

                if row[phone_number] == None:
                    destination = str(row[recipient])
                    destination = destination[destination.find('<string>') + 8:destination.find('</string>')]
                else:
                    destination = row[phone_number]

                ts = str(datetime.datetime.fromtimestamp(row[date]))
                f.write('Message ' + str(row[id]) + ':\n\n')
                f.write('To: ' + destination + '\n')
                f.write('Date: ' + ts + '\n')
                f.write('Contents: ' + str(row[text]) + '\n\n')

        conn.close()

    os.chdir(root_output_dir)

def mail_carve():
    """Asssumes it is currently in the output directory (carvings). Finds /Mail and performs analysis of messages and db."""

    os.chdir('Mail')
    os.mkdir('Messages')

    # indexes
    sender = 1
    email = 3

    mail_summary = open('mail_summary.txt', 'w')
    mail_contents = ''
    recent_correspondents = []

    for file in os.listdir('.'):
        try:
            if file.split('.')[2] == 'emlxpart':
                shutil.move(file, 'Messages')
        except:
            pass # for the files without extensions

        if 'Protected' in file:
            conn = sql.connect(file)
            c = conn.cursor()
            c.execute('SELECT * from messages')
            mail_contents = c.fetchall()
            email_addr = mail_contents[0][email]
            mail_summary.write('Email Address: ' + email_addr + '\n\n')
            for row in mail_contents:
                if row[sender] in recent_correspondents:
                    continue
                else:
                    recent_correspondents.append(row[sender])
            mail_summary.write('Recent Correspondents:\n')
            for r in recent_correspondents:
                mail_summary.write(r + '\n')

            conn.close()

    mail_summary.close()
    os.chdir(root_output_dir)

def addbook_carve():
    """Asssumes it is currently in the output directory (carvings). Finds /Mail and performs analysis of messages and db."""

    os.chdir('AddressBook')

    # indexes
    id = 0
    first = 1
    last = 2

    conn = sql.connect('AddressBook.sqlitedb')
    c = conn.cursor()
    c.execute('SELECT * from ABPerson')

    addbook_contents = c.fetchall()
    with open('addressbook_summary.txt', 'w') as f:
        for row in addbook_contents:
            f.write('Person ' + str(row[id]) + ':\n\n')
            f.write('First: ' + row[first] + '\n')
            f.write('Last: ' + row[last] + '\n')
    os.chdir(root_output_dir)

def maps_carve():
    """Asssumes it is currently in the output directory (carvings). Finds /Maps and performs analysis of messages and db."""

    os.chdir('Maps')

    maps_summary = open('maps_history_geolocation.txt', 'w')

    cmd = 'plutil -p History.plist'
    cmd_obj = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    cmd_output = cmd_obj.communicate()[0]
    cmd_output = cmd_output[cmd_output.find("1 => {")+7:]
    cmd_output = cmd_output[:cmd_output.find("}")]
    maps_summary.write(cmd_output)


    maps_summary.close()
    os.chdir(root_output_dir)

def cookie_carve():
    """Asssumes it is currently in the output directory (carvings). Finds /Mail and performs analysis of messages and db."""

    os.chdir('Cookies')
    plist_contents = {}

    with open('cookies_summary.txt', 'w') as f:
        ind = 1
        plist_contents = pl.readPlist('Cookies.plist')
        for cookie in plist_contents:
            created_ts = str(datetime.datetime.fromtimestamp(cookie['Created']))
            f.write('Cookie ' + str(ind) + '\n\n')
            f.write('Domain: ' + cookie['Domain'] + '\n')
            f.write('Name: ' + cookie['Name'] + '\n')
            f.write('Created: ' + created_ts + '\n')
            f.write('Expires: ' + str(cookie['Expires']) + '\n')
            try:
                f.write('Value: ' + cookie['Value'] + '\n')
            except:
                pass
            f.write('\n')
            ind += 1

    with open('itunes_stored_cookies_summary.txt', 'w') as f:
        ind = 1
        plist_contents = pl.readPlist('com.apple.itunesstored.plist')
        for cookie in plist_contents:
            created_ts = str(datetime.datetime.fromtimestamp(cookie['Created']))
            f.write('Cookie ' + str(ind) + '\n\n')
            f.write('Domain: ' + cookie['Domain'] + '\n')
            f.write('Name: ' + cookie['Name'] + '\n')
            f.write('Created: ' + created_ts + '\n')
            f.write('Expires: ' + str(cookie['Expires']) + '\n')
            try:
                f.write('Value: ' + cookie['Value'] + '\n')
            except:
                pass
            f.write('\n')
            ind += 1

    os.chdir(root_output_dir)

def keyboard_carve():
    os.chdir('Keyboard')
    for f in os.listdir('.'):
        os.rename(f, 'keyboard_data.txt')
    os.chdir(root_output_dir)

def safari_carve():
    os.chdir('Safari')

    # indexes
    id = 0
    title = 4
    url = 5

    bookmark_contents = []

    for item in os.listdir('.'):
        if item.split('.')[1] == 'db':
            conn = sql.connect(item)
            c = conn.cursor()
            try:
                c.execute('SELECT * from bookmarks')
            except:
                continue
            bookmark_contents = c.fetchall()

            with open('safari_bookmarks_summary.txt', 'w') as f:
                for row in bookmark_contents:
                    f.write('Bookmark ' + str(row[id]) + '\n\n')
                    f.write('Title: ' + row[title] + '\n')
                    f.write('Url: ' + str(row[url]) + '\n')
                    f.write('\n') 
            conn.close()
        else:
            if 'Hist' in item:
                saf_hist_summary = open('safari_history.txt', 'w')

                cmd = 'plutil -p History.plist'
                cmd_obj = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
                cmd_output = cmd_obj.communicate()[0]
                saf_hist_summary.write(cmd_output)
                saf_hist_summary.close()
            elif 'Search' in item:
                with open('safari_seach_engines.txt', 'w') as f:
                    ind = 1
                    plist_contents = pl.readPlist('SearchEngines.plist')
                    # print plist_contents['SearchProviderList'][0]
                    f.write('Search Engines: \n\n')
                    for entry in plist_contents['SearchProviderList']:
                        f.write(entry['ScriptingName'] + '\n')
                        f.write(entry['SearchURLTemplate'] + '\n')
                        f.write('\n')
            elif 'Suspend' in item:
                saf_last_open = open('safari_last_open.txt', 'w')

                cmd = 'plutil -p SuspendState.plist'
                cmd_obj = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
                cmd_output = cmd_obj.communicate()[0]
                saf_last_open.write(cmd_output)
                saf_last_open.close()

    os.chdir(root_output_dir) 

def voicemail_carve():
    os.chdir('Voicemail')

    # indexes
    id = 0
    date = 2
    sender = 4
    callback = 5
    duration = 6
    expiration = 7

    date_ts = ''
    exp_ts = ''

    v_contents = []
    for item in os.listdir('.'):
        if 'db' in item:
            conn = sql.connect(item)
            c = conn.cursor()
            c.execute('SELECT * from voicemail')
            v_contents = c.fetchall()

            with open('voicemail_summary.txt', 'w') as f:
                f.write('Voicemail:\n\n')

                for row in v_contents:
                    date_ts = str(datetime.datetime.fromtimestamp(row[date]))
                    exp_ts = str(datetime.datetime.fromtimestamp(row[expiration]))
                    f.write('Call ' + str(row[id]) + '\n\n')
                    f.write('Date: ' + date_ts + '\n')
                    f.write('Sender: ' + str(row[sender]) + '\n')
                    f.write('Callback: ' + str(row[callback]) + '\n')
                    f.write('Expiration: ' + exp_ts + '\n')
                    f.write('\n')

            conn.close()

    os.chdir(root_output_dir)

def wificell_carve():
    os.chdir('SystemConfiguration')

    plist_contents = {}

    for item in os.listdir('.'):
        print item
        if 'identif' in item: # gets executed first, then 'wifi'
            with open('wifi_cell_networks.txt', 'wa') as f:
                f.write('Networks: \n\n')
                ind = 1
                plist_contents = pl.readPlist(item)
                for p in plist_contents['Signatures']:
                    f.write('ID: ' + p['Identifier'] + '\n')
                    for p2 in p['Services']:
                        f.write('Addr: ' + p2['IPv4']['Router']+ '\n')
                    f.write('\n')
                f.write('\n')
                ind += 1
        if 'wifi' in item:
            with open('wifi_cell_networks.txt', 'a') as f:
                ind = 1
                plist_contents = pl.readPlist(item)
                f.write('Wifi Networks:\n\n')
                f.write('SSID: ' + plist_contents['List of known networks'][0]['SSID_STR'] + '\n')
                f.write('BSSID: ' + plist_contents['List of known networks'][0]['BSSID'] + '\n')
                f.write('Secure?: ' + str(plist_contents['List of known networks'][0]['WiFiNetworkIsSecure']) + '\n')
                f.write('Password?: ' + str(plist_contents['List of known networks'][0]['WiFiNetworkRequiresPassword']) + '\n')
                f.write('Channel: ' + str(plist_contents['List of known networks'][0]['CHANNEL']) + '\n')
                f.write('\n')
                ind += 1

    os.chdir(root_output_dir)

### main ##########

def main():
    os.chdir(root_dir)
    os.mkdir(root_output_dir)

    dir_scrape();

    os.chdir(root_output_dir)

    cookie_carve()
    sms_carve()
    cal_carve()
    mail_carve()
    addbook_carve()
    maps_carve()
    keyboard_carve()
    safari_carve()
    voicemail_carve()
    wificell_carve()


if __name__ == '__main__':
    main()