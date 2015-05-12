#!/usr/bin/env python
#
# pull-lp-bin -- pull a binary package from Launchpad
#
# Copyright (C) 2013, Canonical Ltd.
#
# Based on the pull-lp-source script (ubuntu-dev-tools) made by:
#  - Iain Lane <iain@orangesquash.org.uk>
#  - Stefano Rivera <stefanor@ubuntu.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# See file /usr/share/common-licenses/GPL for more details.
#
# Author: Ricardo Salveti <ricardo.salveti@canonical.com>

import os
import sys
import urllib2
from optparse import OptionParser
from launchpadlib.launchpad import Launchpad

cachedir = "~/.launchpadlib/cache"

def main():
    usage = "Usage: %prog [-a|--arch <arch>] [-o|--output <dir>] [-t|--team <team>] [-p|--ppa <ppa>] <package> [release]"
    opt_parser = OptionParser(usage)
    opt_parser.add_option('-a', '--arch', default='armhf', dest='ubuntu_arch',
                  help='Architecture for the binary package (default: armhf)')
    opt_parser.add_option('-o', '--output',
                  help='Directory used to output the desired package')
    opt_parser.add_option('-t', '--team',
                  help='Launchpad team that owns the PPA (to be used with --ppa)')
    opt_parser.add_option('-p', '--ppa',
                  help='PPA used to look for the binary package')
    (options, args) = opt_parser.parse_args()
    if not args:
        opt_parser.error("Must specify a package name")

    package = str(args[0]).lower()

    # Login anonymously to LP
    lp = Launchpad.login_anonymously('pull-lp-bin', 'production',
                                      cachedir, version="devel")
    distro = lp.distributions['ubuntu']

    if options.ppa and not options.team:
        print "To use a PPA you also need to provide a team (from Launchpad)"
        return

    if options.ppa:
        archive = lp.people[options.team].getPPAByName(name=options.ppa)
    else:
        archive = lp.distributions['ubuntu'].main_archive

    if len(args) > 1:
        release = str(args[1])
    else:
        release = distro.current_series_link.split('/')[-1]

    pocket = 'Release'
    bin_url = None
    bpph = None

    series = distro.getSeries(name_or_version=release)
    arch_series = series.getDistroArchSeries(archtag=options.ubuntu_arch)
    bpph = archive.getPublishedBinaries(binary_name=package,
                            distro_arch_series=arch_series,
                            status="Published", pocket=pocket,
                            exact_match=True)

    if bpph:
        version = bpph[0].binary_package_version
        bin_url = bpph[0].binaryFileUrls()[0]

    if bin_url:
        print 'Downloading %s version %s' % (package, version)
        url = urllib2.urlopen(bin_url)
        data = url.read()
        package_name = "%s_%s_%s.deb" % (package, version, options.ubuntu_arch)
        if options.output:
            target = "%s/%s" % (options.output, package_name)
        else:
            target = package_name
        with open(target, "wb") as package:
            package.write(data)
    else:
        print "Unable to find a published version of package %s (%s) at %s" % (
                                        package, options.ubuntu_arch, release)

if __name__ == '__main__':
    main()
