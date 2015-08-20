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

import os.path
import sys
import logging


from oslo.config import cfg
from sqlalchemy import *
from logging.handlers import SysLogHandler

from keystoneclient.v2_0 import client as k_client


LOG = logging.getLogger('openstack_service_checker')
LOG_FORMAT='%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
LOG_DATE = '%m-%d %H:%M'
DESCRIPTION="OpenStack Service Checker"
CONF = cfg.CONF
CREDENTIALS = {}


def parse_args():

    cli_ops = [
            cfg.StrOpt('service', default="nova", help='Choose service ["nova","cinder","neutron"]', required=True),
            cfg.BoolOpt('debug', default=False, help="Show debugging output")
            ]
    CONF.register_cli_opts(cli_ops)


def setup_logging():
    level = logging.INFO
    if CONF.debug:
        level = logging.DEBUG
    logging.basicConfig(level=level, format=LOG_FORMAT, date_fmt=LOG_DATE)
    handler = SysLogHandler(address = '/dev/log')
    syslog_formatter = logging.Formatter('%(name)s: %(levelname)s %(message)s')
    handler.setFormatter(syslog_formatter)
    LOG.addHandler(handler)


def get_auth():
    keystone_grp = cfg.OptGroup(name='keystone_authtoken', title='Keystone options')
    CONF.register_group(keystone_grp)
    keystone_opts = [ cfg.StrOpt('auth_uri', default=''), 
                      cfg.StrOpt('admin_tenant_name'),
                      cfg.StrOpt('admin_user'),
                      cfg.StrOpt('admin_password'),
                      cfg.StrOpt('admin_tenant_id')]
    CONF.register_opts(keystone_opts, keystone_grp)
    config_files = ["/etc/{service}/{service}.conf".format(service=CONF.service)]
    # Config files must be in an array
    if os.path.isfile(config_files[0]):
        CONF(default_config_files=config_files)
        
        CREDENTIALS['auth_url'] = CONF.keystone_authtoken.auth_uri
        CREDENTIALS['username'] = CONF.keystone_authtoken.admin_user
        CREDENTIALS['password'] = CONF.keystone_authtoken.admin_password
        CREDENTIALS['tenant_name'] = CONF.keystone_authtoken.admin_tenant_name
        
        keystone = k_client.Client(**CREDENTIALS)
        for tenant in keystone.tenants.list():
            if tenant.name == CONF.keystone_authtoken.admin_tenant_name:
                CONF.keystone_authtoken.admin_tenant_id = tenant.id
    else:
        print "Config File not found"
        sys.exit(2)
    

# Clients objects
def check_nova_services():
    from novaclient import client
    nova = client.Client("2", CREDENTIALS['username'],
                              CREDENTIALS['password'],
                              CREDENTIALS['tenant_name'],
                              CREDENTIALS['auth_url'])


    for service in nova.services.list():
        if service.state != "up" and service.status == "enabled":
            print "Server not runnning: {service} on host {host}".format(service=service.binary,host=service.host)
            sys.exit(2)

    
def check_neutron_services():
    from neutronclient.neutron import client
    neutron = client.Client("2.0", **CREDENTIALS)

    for agent in neutron.list_agents():
        print agent.__dict__

def check_cinder_services():
    from cinderclient import client
    cinder = client.Client('2', **CREDENTIALS)


def get_client():
    get_auth()
    clients = {
        'nova': check_nova_services,
        'cinder': check_cinder_services,
        'neutron': check_neutron_services
    }
    client_obj = clients[CONF.service]()
    return client_obj




if __name__ == '__main__':
    parse_args()
    setup_logging()
    
    try:
        get_client()
    except Exception as err:
        LOG.exception("Error: %s" % err)
        sys.exit(2)
    except KeyboardInterrupt:
        sys.exit(2)

