#!/usr/bin/env python
#    This file is part of python-evtx.
#
#   Copyright 2012, 2013 Willi Ballenthin <william.ballenthin@mandiant.com>
#                    while at Mandiant <http://www.mandiant.com>
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
#   Version v0.1.1
import os
import Evtx.Evtx as evtx
import Evtx.Views as e_views

def xml_converter(path):
    base_path, _ = os.path.splitext(path)
    xml_path = f"{base_path}.xml"

    with open(xml_path, 'w+') as xmlfile:
        with evtx.Evtx(path) as log:
            print(e_views.XML_HEADER, file=xmlfile)
            print("<Events>", file=xmlfile)
            for record in log.records():
                print(record.xml(), file=xmlfile)
            print("</Events>", file=xmlfile)
