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

parser.add_argument('-s','--stype',help="Stats type\n [async|replication|auditor|updater|expirer|quarantine|md5]", required=True) 

args = parser.parse_args()

STATE_OK=0
STATE_WARNING=1
STATE_CRITICAL=2
STATE_UNKNOWN=4

state = STATE_UNKNOWN

def validate_output(rcon_output):
    for line in rcon_output:
        if line.find("Failed:") != -1:
            if line.find("Failed: 0.0%") != -1:
                print line
            else:
                print line
                sys.exit(STATE_CRITICAL)


def async():
    process = subprocess.Popen(["swift-recon", "--async"], stdout=subprocess.PIPE)
    validate_output(process.stdout.readlines())

def replication():
    process = subprocess.Popen(["swift-recon", "--replication"], stdout=subprocess.PIPE)
    validate_output(process.stdout.readlines())

def auditor():
    process = subprocess.Popen(["swift-recon", "--auditor"], stdout=subprocess.PIPE)
    validate_output(process.stdout.readlines())

def updater():
    process = subprocess.Popen(["swift-recon", "--updater"], stdout=subprocess.PIPE)
    validate_output(process.stdout.readlines())

def expirer():
    process = subprocess.Popen(["swift-recon", "--expirer"], stdout=subprocess.PIPE)
    validate_output(process.stdout.readlines())

def quarantine():
    process = subprocess.Popen(["swift-recon", "--quarantine"], stdout=subprocess.PIPE)
    validate_output(process.stdout.readlines())

def md5():
    process = subprocess.Popen(["swift-recon", "--md5"], stdout=subprocess.PIPE)
    for line in process.stdout.readlines():
        if line.find("error") != -1:
            if line.find("0 error") != -1:
                print line
                sys.exit(STATE_OK)
            else:
                print line
                sys.exit(STATE_CRITICAL)


option_types =  {   "async" : async,
                    "replication": replication,
                    "auditor" : auditor,
                    "updater" : updater,
                    "expirer" : expirer,
                    "quarantine" : quarantine,
                    "md5" : md5,
                }

option_types[args.stype]()


