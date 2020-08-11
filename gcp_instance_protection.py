#!/usr/bin/env python
# -*- coding: utf-8 -*-
##########################################################################
# NAME          : gcp_instance_protection.py
# LAST UPDATE   : 
# Verersion     : 
##########################################################################
# https://cloud.google.com/compute/docs/instances/preventing-accidental-vm-deletion?hl=ko
import datetime
import subprocess


##############################
# 1. Instances Setting
instances = [
'test-01',
'test-02' 
]

# 2. Zone Setting
zone = 'asia-northeast3-a'
##############################

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 보호설정 확인
# gcloud compute instances describe example-instance | grep "deletionProtection"
def InstancesProtectionStats(instances,zone):
    try:
        print('### STATUS '+ now + ' ###')
        for x in instances:
            status = subprocess.check_output('gcloud compute instances describe ' + x + ' --zone=' + zone + '| grep "deletionProtection"' ,shell=True).strip()
            print ( i +  "-" +  status)
        print('### DONE ###')
    except Exception as ex:
        print(ex)

# 보호 설정
# gcloud compute instances update example-vm --deletion-protection
def InstancesProtectionOn(instances,zone):
    try : 
        print('### START : ' + now +' ###')
        for y in instances:
            subprocess.check_output('gcloud compute instances update ' + y + ' --zone=' + zone + ' --deletion-protection',shell=True).strip()
        print("### END ###")
    except Exception as ex:
        print(ex)

# 보호 삭제
# gcloud compute instances update example-vm --no-deletion-protection
def InstancesProtectionOff(instances,zone):
    try :
        print('### START : ' + now +' ###')
        for z in instances:
            subprocess.check_output('gcloud compute instances update ' + z + ' --zone=' + zone + ' --no-deletion-protection',shell=True).strip()
        print("### END ###")
    except Exception as ex:
        print(ex)


# Run
def main():
    try :
        while True :
            num = input("1 - 보호설정 확인\n2 - 보호\n3 - 보호 해제\n")
            if (num == 1) :
                InstancesProtectionStats(instances, zone)
            elif (num == 2):
                InstancesProtectionOn(instances, zone)
            elif (num == 3):
                InstancesProtectionOff(instances, zone)
            else :
                print("1-3을 입력해주세요.")
    except Exception as ex:
        print(ex)

# main 
if __name__ == "__main__":
	main()
