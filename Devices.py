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
This file contains all the API calls needed to get device information
"""

import xlsxwriter
from controllers import epnm


if __name__ == "__main__":
    devices = epnm.getDevicesByType()
    workbook = xlsxwriter.Workbook('epnm-devices.xlsx')
    worksheet = workbook.add_worksheet()

    row = 0
    col = 0

    worksheet.write(row, col, "Device Name")
    worksheet.write(row, col + 1, "Type")
    worksheet.write(row, col + 2, "IP")
    row += 1

    for node in devices.json()["com.response-message"]["com.data"]["nd.node"]:
        print(node["nd.name"] + " - " + node["nd.product-type"] + " - " + node["nd.management-address"])
        worksheet.write(row, col, node["nd.name"])
        worksheet.write(row, col + 1, node["nd.product-type"])
        worksheet.write(row, col + 2, node["nd.management-address"])
        row += 1
    worksheet.autofilter('A1:C' + str(row + 2))
    worksheet.set_column("A:C", 50)

