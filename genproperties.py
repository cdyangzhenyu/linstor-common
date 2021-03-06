#!/usr/bin/env python

import argparse
import json
import datetime
import os
import pprint

now = datetime.datetime.utcnow()
basename = os.path.basename(__file__)
hdr = 'This file was autogenerated by %s' % basename
license = """
LINSTOR - management of distributed storage/DRBD9 resources
Copyright (C) 2017 - %s  LINBIT HA-Solutions GmbH
Author: %s

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.""" % (
    now.year, ', '.join(['Rene Peinthor', 'Gabor Hernadi']))


class MyPyKey(object):
    def __init__(self, keypath):
        self._keys = keypath

    def __str__(self):
        return " + '/' + ".join(['consts.' + x for x in self._keys])

    def __repr__(self):
        return str(self)


def lang_python(data):
    print('"""')
    print('{h}\n{lic}'.format(h=hdr, lic=license))
    print('"""')
    print('import linstor.sharedconsts as consts')

    properties = data['properties']
    objects = data['objects']
    p = {}

    # prefix keys with consts.
    for prop in properties:
        key = properties[prop]['key']
        properties[prop]['key'] = MyPyKey(key)

    print('properties = \\')
    for objkey in objects:
        obj_props = objects[objkey]
        resolved = []
        for prop in obj_props:
            resolved.append(properties[prop])

        p[objkey] = resolved

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(p)
    return True


def lang_java(data):
    pass


def main():
    parser = argparse.ArgumentParser(prog="genproperties.py")
    parser.add_argument('propfile')
    parser.add_argument('language', choices=['python', 'java'])

    args = parser.parse_args()

    propdata = None
    with open(args.propfile) as propfile:
        propdata = json.load(propfile)

    if args.language == 'python':
        lang_python(propdata)
    elif args.language == 'java':
        lang_java(propdata)


if __name__ == '__main__':
    main()
