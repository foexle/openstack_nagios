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
import os.path
import sys

from oslo.config import cfg
from sqlalchemy import *
from logging.handlers import SysLogHandler

from keystoneclient.auth.identity import v2
from keystoneclient import session



LOG = logging.getLogger('openstack_service_checker')
LOG_FORMAT='%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
LOG_DATE = '%m-%d %H:%M'
DESCRIPTION="OpenStack Service Checker"
CONF = cfg.CONF
AUTH = ""


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
    

def get_auth(arg_service):
    keystone_grp = cfg.OptGroup(name='keystone_authtoken', title='Keystone options')
    CONF.register_group(keystone_grp)
    keystone_opts = [ cfg.StrOpt('auth_uri', default=''), 
                      cfg.StrOpt('admin_tenant_name'),
                      cfg.StrOpt('admin_user'),
                      cfg:StrOpt('admin_password')]
    CONF.register_opts(keystone_opts, keystone_grp)
    config_files = ["/etc/{service}/{service}.conf".format(service=arg_service)]
    # Config files must be in an array
    if os.path.isfile(config_files[0]):
        CONF(default_config_files=config_files)
        key_auth = v2.Password( auth_url=CONF.keystone_authtoken.auth_uri, 
                                username=CONF.keystone_authtoken.admin_user,
                                password=CONF.keystone_authtoken.admin_password,
                                tenant_name=CONF.keystone_authtoken.admin_tenant_name)
        AUTH = session.Session(auth=key_auth)
    else:
        print "Config File not found"
        sys.exit(2)
    

# Clients objects
def check_nova_services():
    from novaclient import client
    nova = client.Client("1.1", session=AUTH)
    print nova.service.list()


def get_neutron_client():
    from neutronclient.neutron import client
    neutron = client.Client("2.0", session=AUTH)
    return neutron

def get_cinder_client():
    from cinderclient import client
    cinder = client.Client('2', session=AUTH)
    return cinder


def get_client(args):
    get_auth()
    clients = {
        'nova': get_nova_client,
        'cinder': get_cinder_client,
        'neutron': get_neutron_client
    }
    client_obj = clients[args.service]
    return client_obj




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

