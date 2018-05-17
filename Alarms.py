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
This file contains all the API calls needed to get device information and save it in an excel file
"""

import xlsxwriter
from controllers import epnm

if __name__ == "__main__":

    alarmsCritical = epnm.getAlarms(perceivedSeverity="critical")
    alarmsMajor = epnm.getAlarms(perceivedSeverity="major")
    alarmsMinor = epnm.getAlarms(perceivedSeverity="minor")

    workbook = xlsxwriter.Workbook('epnm-alarms.xlsx')
    worksheet = workbook.add_worksheet()

    row = 0
    col = 0

    worksheet.write(row, col, "Alarm")
    worksheet.write(row, col + 1, "Severity")
    worksheet.write(row, col + 2, "Device")
    worksheet.write(row, col + 3, "Probable cause")
    row += 1

    for alarm in alarmsCritical["com.response-message"]["com.data"]["alm.alarm"]:
        print(str(alarm))

        worksheet.write(row, col, alarm["alm.description"])
        worksheet.write(row, col + 1, alarm["alm.perceived-severity"])
        worksheet.write(row, col + 2, alarm["alm.node-ref"])
        worksheet.write(row, col + 3, alarm["alm.probable-cause"])
        row += 1
    for alarm in alarmsMajor["com.response-message"]["com.data"]["alm.alarm"]:
        print(str(alarm))

        worksheet.write(row, col, alarm["alm.description"])
        worksheet.write(row, col + 1, alarm["alm.perceived-severity"])
        worksheet.write(row, col + 2, alarm["alm.node-ref"])
        worksheet.write(row, col + 3, alarm["alm.probable-cause"])
        row += 1
    for alarm in alarmsMinor["com.response-message"]["com.data"]["alm.alarm"]:
        print(str(alarm))

        worksheet.write(row, col, alarm["alm.description"])
        worksheet.write(row, col + 1, alarm["alm.perceived-severity"])
        worksheet.write(row, col + 2, alarm["alm.node-ref"])
        worksheet.write(row, col + 3, alarm["alm.probable-cause"])
        row += 1
    worksheet.autofilter('A1:D' + str(row + 2))
    worksheet.set_column("A:D", 50)
    workbook.close()
