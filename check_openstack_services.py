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

import argparse

from oslo.config import cfg
from sqlalchemy import *
from logging.handlers import SysLogHandler




LOG = logging.getLogger('openstack_service_checker')
LOG_FORMAT='%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
LOG_DATE = '%m-%d %H:%M'
DESCRIPTION="OpenStack Service Checker"
DB_METADATA = ""
CONF = cfg.CONF

def parse_args():

        # Keystone and Database configurations will be parse with the neutron.conf file

    ap = argparse.ArgumentParser(description=DESCRIPTION)
    ap.add_argument('-d', '--debug', action='store_true',
                    default=False, help='Show debugging output')
    ap.add_argument('--service', action='store_true',
                    default="nova", help='Choose service ["nova","cinder","neutron"]', required=True)
    return ap.parse_args()


def setup_logging(args):
    level = logging.INFO
    if args.debug:
        level = logging.DEBUG
    logging.basicConfig(level=level, format=LOG_FORMAT, date_fmt=LOG_DATE)
    handler = SysLogHandler(address = '/dev/log')
    syslog_formatter = logging.Formatter('%(name)s: %(levelname)s %(message)s')
    handler.setFormatter(syslog_formatter)
    LOG.addHandler(handler)

def check_service(args, client):


def get_client(args):
    


if __name__ == '__main__':
    args = parse_args()
    setup_logging(args)
    
    try:
        get_client(args)
    
    except Exception as err:
        LOG.exception("Error: %s" % err)
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(1)

