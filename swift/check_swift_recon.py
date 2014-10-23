#!/usr/bin/python
#
# Author: Heiko Kraemer
# Email: hkraemer@anynines.com
#
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import sys
import os
import subprocess
import argparse

__author__ = "Heiko Kraemer"

parser = argparse.ArgumentParser(description="This is a Nagios check script for Swift recon")

parser.add_argument('-s','--stype',help="Stats type\n [async|replication|auditor|updater|expirer|load|quarantine|md5]", required=True) 
parser.add_argument('-u','--umounted',help="Check cluster for unmounted devices", required=False)
parser.add_argument('-d','--disc-usage',help="Get disk usage stats", required=False)
parser.add_argument('-p','--suppress',help="Suppress most connection related errors", required=False)

args = parser.parse_args()

STATE_OK=0
STATE_WARNING=1
STATE_CRITICAL=2
STATE_UNKNOWN=3
STATE_DEPENDENT=4

state = STATE_UNKNOWN

def async():
    process = subprocess.Popen(["swift-recon", "--async"], stdout=subprocess.PIPE)
    for line in process.stdout.readlines():
        if line.find("Failed: 0.0%") != -1:
            print line
            sys.exit(STATE_OK)
        else:
            sys.exit(STATE_CRITICAL)
            print line
     


def replication():
    process = subprocess.Popen(["swift-recon", "--replication"], stdout=subprocess.PIPE)

def auditor():
    process = subprocess.Popen(["swift-recon", "--auditor"], stdout=subprocess.PIPE)

def updater():
    process = subprocess.Popen(["swift-recon", "--updater"], stdout=subprocess.PIPE)

def expirer():
    process = subprocess.Popen(["swift-recon", "--expirer"], stdout=subprocess.PIPE)

def load():
    process = subprocess.Popen(["swift-recon", "--loadstats"], stdout=subprocess.PIPE)

def quarantine():
    process = subprocess.Popen(["swift-recon", "--quarantine"], stdout=subprocess.PIPE)

def md5():
    process = subprocess.Popen(["swift-recon", "--md5"], stdout=subprocess.PIPE)



option_types =  {   "async" : async,
                    "replication": replication,
                    "auditor" : auditor,
                    "updater" : updater,
                    "expirer" : expirer,
                    "load" : load,
                    "quarantine" : quarantine,
                    "md5" : md5,
                }

option_types[args.stype]()


