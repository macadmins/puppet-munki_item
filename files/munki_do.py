#!/usr/local/munki/munki-python
# encoding: utf-8
#
# Copyright 2009-2024 Greg Neagle.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
munki_do
"""
import datetime
import optparse
import os
import tempfile
import sys

sys.path.append("/usr/local/munki")

from munkilib import FoundationPlist
from munkilib import updatecheck
from munkilib import installer
from munkilib import munkicommon
from munkilib import reports


def write_report(old_report=None):
    if old_report:
        reports.report = old_report
    reports.savereport()


def catalogs_older_than_30_mins(cataloglist):
    for catalog in cataloglist:
        catalogpath = os.path.join(
            munkicommon.pref("ManagedInstallDir"), "catalogs", catalog
        )
        if not os.path.exists(catalogpath):
            print("Catalog %s does not exist." % catalog)
            return True
        try:
            catalogstat = os.stat(catalogpath)
        except OSError:
            print("Could not stat %s." % catalogpath)
            return True
        catalogage = datetime.datetime.fromtimestamp(catalogstat.st_mtime)

        diff = datetime.datetime.now() - catalogage
        # return true if the catalog is older than 30 minutes
        if diff.seconds > 1800:
            print("Catalog %s is older than 30 minutes." % catalog)
            return True
    return False


def main():
    p = optparse.OptionParser()
    p.add_option(
        "--catalog",
        "-c",
        action="append",
        help="Which catalog to consult. May be specified multiple times.",
    )
    p.add_option(
        "--install",
        "-i",
        action="append",
        help="An item to install. May be specified multiple times.",
    )
    p.add_option(
        "--uninstall",
        "-u",
        action="append",
        help="An item to uninstall. May be specified multiple times.",
    )
    p.add_option(
        "--checkstate",
        action="append",
        help="Check the state of an item. May be specified multiple times.",
    )
    p.add_option(
        "--force-catalog-update",
        type="string",
        default="False",
        help="Force a check of the catalogs before proceeding.",
    )

    options, arguments = p.parse_args()
    force_catalog_update = options.force_catalog_update.lower() == "true"
    cataloglist = options.catalog or ["production"]
    updatecheck.MACHINE = munkicommon.getMachineFacts()
    updatecheck.CONDITIONS = munkicommon.get_conditions()
    if catalogs_older_than_30_mins(cataloglist) or force_catalog_update:
        if force_catalog_update:
            print("Forcing catalog update...")
            
        updatecheck.catalogs.get_catalogs(cataloglist)
    report = reports.readreport()
    if options.checkstate:
        updatecheck.MACHINE = munkicommon.getMachineFacts()
        updatecheck.CONDITIONS = munkicommon.get_conditions()
        if cataloglist != ["production"]:
            updatecheck.catalogs.get_catalogs(cataloglist)
        for check_item in options.checkstate:
            exit_code = 2
            item_pl = updatecheck.catalogs.get_item_detail(check_item, cataloglist)
            if item_pl:
                if updatecheck.installationstate.installed_state(item_pl):
                    exit_code = 0
                else:
                    exit_code = 1
            write_report(report)
            sys.exit(exit_code)

    if not options.install and not options.uninstall:
        sys.exit()
    manifest = {}
    manifest["catalogs"] = cataloglist
    manifest["managed_installs"] = options.install or []
    manifest["managed_uninstalls"] = options.uninstall or []
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_filename = temp_file.name

    FoundationPlist.writePlist(manifest, temp_filename)
    munkicommon.report["ManifestName"] = "munki_do_localmanifest"
    updatecheckresult = updatecheck.check(localmanifestpath=temp_filename)
    if updatecheckresult == 1:
        need_to_restart = installer.run()
        if need_to_restart:
            print("Please restart immediately!")
    os.remove(temp_filename)
    write_report(report)


if __name__ == "__main__":
    main()
