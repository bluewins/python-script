#!/usr/bin/env python
# -*- coding: utf-8 -*-
##########################################################################
# NAME          : db_backup.py
# LAST UPDATE   : 2019-02-14
# Verersion     : 1.0
##########################################################################
import datetime
import commands
import os
import sys

### 기본 설정 
DB_USER = ''
DB_PASS = ''
FULL_BACKUP_DIR = '/data/backup/full/'
INC_BACKUP_DIR = '/data/backup/inc/'
FULL_DAY = 0 # 0 = Monday, 6 = Sunday

### 날짜 관련 함수 
now = datetime.datetime.now()
week = now.weekday()
###

# 설정한 요일에 Full Backup
def maria_backup():
    if week == FULL_DAY:
        print(' === Full Backup ===')
        os.system('mariabackup --backup --compress --no-lock --target-dir=' + FULL_BACKUP_DIR + str(now.strftime("%Y-%m-%d_%H:%M:%S")) + ' --user=' + DB_USER + ' --password=' + DB_PASS)

# 다른 날일 경우 증분 백업
    else:
        print('===Increment Backup===')
        full_cmd = ('ls -r /data/backup/full/ | sed -n 1p')
        inc_cmd = ('ls -r /data/backup/inc/ | sed -n 1p')
        last_full_backup = commands.getoutput(full_cmd)
        last_inc_backup = commands.getoutput(inc_cmd)

# Full 백업이 존재하지 않으면 Full 백업
        if last_full_backup == '':
            print('Full 백업이 존재하지 않습니다.')
            os.system('mariabackup --backup --compress --no-lock --target-dir=' + FULL_BACKUP_DIR + str(now.strftime("%Y-%m-%d_%H:%M:%S")) + ' --user=' + DB_USER + ' --password=' + DB_PASS)
            sys.exit();

# 증분 백업이 존재하지 않으면 Full 백업을 기준으로 증분 백업
        if last_inc_backup == '':
            print('마지막 증분 백업이 존재하지않습니다.')
            print('full 백업으로 증분 백업')
            os.system('mariabackup --backup --compress --no-lock --target-dir=' + INC_BACKUP_DIR + str(now.strftime("%Y-%m-%d_%H:%M:%S")) + ' --incremental-basedir=' + FULL_BACKUP_DIR + last_full_backup + ' --user=' + DB_USER + ' --password=' + DB_PASS)
            sys.exit()
# Full 백업과 증분백업의 날짜를 비교 Full 백업의 날짜가 오래됐을 경우 Full 백업을 기준으로 증분 백업을 진행
# 증분 백업의 날짜가 오래됬을 경우 증분 백업을 기준으로 증분 백업 진행
        convert_inc = datetime.datetime.strptime(last_inc_backup, "%Y-%m-%d_%H:%M:%S").date()
        convert_full = datetime.datetime.strptime(last_full_backup, "%Y-%m-%d_%H:%M:%S").date()
        if convert_full > convert_inc:
            print('full 백업으로 증분 백업')
            os.system('mariabackup --backup --compress --no-lock --target-dir=' + INC_BACKUP_DIR + str(now.strftime("%Y-%m-%d_%H:%M:%S")) + ' --incremental-basedir=' + FULL_BACKUP_DIR + last_full_backup + ' --user=' + DB_USER + ' --password=' + DB_PASS)
        else :
            print('증분 백업 기준 증분 백업')
            os.system('mariabackup --backup --compress --no-lock --target-dir=' + INC_BACKUP_DIR + str(now.strftime("%Y-%m-%d_%H:%M:%S")) + ' --incremental-basedir=' + INC_BACKUP_DIR + last_inc_backup + ' --user=' + DB_USER + ' --password=' + DB_PASS)

maria_backup()