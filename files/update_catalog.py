#!/usr/local/munki/munki-python

import sys
import optparse

sys.path.append('/usr/local/munki')
from munkilib import updatecheck
from munkilib import munkicommon

def main():    
    p = optparse.OptionParser()
    p.add_option('--catalog', '-c', action="append",
           help='Which catalog to consult. May be specified multiple times.')
    options, arguments = p.parse_args()
    cataloglist = options.catalog or ['production']
    updatecheck.MACHINE = munkicommon.getMachineFacts()
    updatecheck.CONDITIONS = munkicommon.get_conditions()
    updatecheck.catalogs.get_catalogs(cataloglist)

if __name__ == '__main__':
    main()