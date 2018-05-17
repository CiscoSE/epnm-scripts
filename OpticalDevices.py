"""
Copyright (c) 2018 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.0 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""
"""
This file contains all the API calls needed to get optical device information and save it in an excel file
"""

import xlsxwriter
from controllers import epnm

if __name__ == "__main__":

    headers = ["NAME", "IPADDR", "SWVER", "LOAD", "PROTSWVER", "PROTLOAD", "DEFDESC", "PLATFORM", "SECUMODE", "MODE",
               "IPMASK",
               "DEFRTR", "IPV6ENABLE", "IPV6ADDR", "IPV6PREFLEN", "IPV6DEFRTR", "IIOPPORT", "SUPPRESSIP",
               "MSPUBVLANID", "MSINTLVLANID", "AUTOPM", "SERIALPORTECHO", "OSIROUTINGMODE", "OSIL1BUFSIZE",
               "OSIL2BUFSIZE", "NET",
               "SYSTEMMODE", "NTP", "PROXYSRV", "FIREWALL", "BKUPNTP"]

    devices = epnm.getDevicesByType()
    workbook = xlsxwriter.Workbook('epnm-optical-devices.xlsx')
    worksheet = workbook.add_worksheet()

    row = 0
    col = 0

    for index in range(len(headers)):
        worksheet.write(row, index, headers[index])
    row += 1

    for node in devices["com.response-message"]["com.data"]["nd.node"]:
        print(node["nd.description"])
        write = False
        for item in node["nd.description"].split(','):
            if "=" in item:
                key = item.split("=")[0]
                value = item.split("=")[1]
                if not key in headers:
                    headers.append(key)
                    worksheet.write(0, headers.index(key), key)
                worksheet.write(row, headers.index(key), value)
                write = True
        if write:
            row += 1

    worksheet.autofilter('A1:Z' + str(row + 2))
    worksheet.set_column("A:Z", 50)
    workbook.close()
