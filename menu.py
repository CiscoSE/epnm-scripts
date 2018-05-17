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
import subprocess
import time

DEVICES_FILE_NAME = "epnm-optical-devices.xlsx"
ALARMS_FILE_NAME = "epnm-alarms.xlsx"


def ExportDevicesByType(nodeType):
    print("Getting the devices per type " + nodeType)
    headers = ["NAME", "IPADDR", "SWVER", "LOAD", "PROTSWVER", "PROTLOAD", "DEFDESC", "PLATFORM", "SECUMODE", "MODE",
               "IPMASK",
               "DEFRTR", "IPV6ENABLE", "IPV6ADDR", "IPV6PREFLEN", "IPV6DEFRTR", "IIOPPORT", "SUPPRESSIP",
               "MSPUBVLANID", "MSINTLVLANID", "AUTOPM", "SERIALPORTECHO", "OSIROUTINGMODE", "OSIL1BUFSIZE",
               "OSIL2BUFSIZE", "NET",
               "SYSTEMMODE", "NTP", "PROXYSRV", "FIREWALL", "BKUPNTP"]

    devices = epnm.getDevicesByType(nodeType)
    workbook = xlsxwriter.Workbook(DEVICES_FILE_NAME)
    worksheet = workbook.add_worksheet()

    row = 0

    for index in range(len(headers)):
        worksheet.write(row, index, headers[index])
    row += 1

    for node in devices["com.response-message"]["com.data"]["nd.node"]:
        # print(node["nd.description"])
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
        if not write:
            worksheet.write(row, headers.index("NAME"), node["nd.name"])
        row += 1

    worksheet.autofilter('A1:Z' + str(row + 2))
    worksheet.set_column("A:Z", 50)
    workbook.close()

    subprocess.Popen(["open " + DEVICES_FILE_NAME], shell=True)


def ExportDevicesByName(name):
    print("Getting the devices per name " + name)
    headers = ["NAME", "IPADDR", "SWVER", "LOAD", "PROTSWVER", "PROTLOAD", "DEFDESC", "PLATFORM", "SECUMODE", "MODE",
               "IPMASK",
               "DEFRTR", "IPV6ENABLE", "IPV6ADDR", "IPV6PREFLEN", "IPV6DEFRTR", "IIOPPORT", "SUPPRESSIP",
               "MSPUBVLANID", "MSINTLVLANID", "AUTOPM", "SERIALPORTECHO", "OSIROUTINGMODE", "OSIL1BUFSIZE",
               "OSIL2BUFSIZE", "NET",
               "SYSTEMMODE", "NTP", "PROXYSRV", "FIREWALL", "BKUPNTP"]

    devices = epnm.getDevicesByName(name)
    workbook = xlsxwriter.Workbook(DEVICES_FILE_NAME)
    worksheet = workbook.add_worksheet()

    row = 0

    for index in range(len(headers)):
        worksheet.write(row, index, headers[index])
    row += 1

    for node in devices["com.response-message"]["com.data"]["nd.node"]:
        # print(node["nd.description"])
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
        if not write:
            worksheet.write(row, headers.index("NAME"), node["nd.name"])
        row += 1

    worksheet.autofilter('A1:Z' + str(row + 2))
    worksheet.set_column("A:Z", 50)
    workbook.close()

    subprocess.Popen(["open " + DEVICES_FILE_NAME], shell=True)


def ExportDevicesByGroup(groupName):
    print("Getting the devices per group " + groupName)
    headers = ["NAME", "IPADDR", "SWVER", "LOAD", "PROTSWVER", "PROTLOAD", "DEFDESC", "PLATFORM", "SECUMODE", "MODE",
               "IPMASK",
               "DEFRTR", "IPV6ENABLE", "IPV6ADDR", "IPV6PREFLEN", "IPV6DEFRTR", "IIOPPORT", "SUPPRESSIP",
               "MSPUBVLANID", "MSINTLVLANID", "AUTOPM", "SERIALPORTECHO", "OSIROUTINGMODE", "OSIL1BUFSIZE",
               "OSIL2BUFSIZE", "NET",
               "SYSTEMMODE", "NTP", "PROXYSRV", "FIREWALL", "BKUPNTP"]

    deviceNames = []
    nodes = []
    for group in epnm.getGroupByName(groupName)["com.response-message"]["com.data"]["nd.group"]:
        deviceNames.extend(group["nd.node"])

    for deviceName in deviceNames:
        nodes.extend(epnm.getDevicesByFdn(deviceName)["com.response-message"]["com.data"]["nd.node"])

    workbook = xlsxwriter.Workbook(DEVICES_FILE_NAME)
    worksheet = workbook.add_worksheet()

    row = 0

    for index in range(len(headers)):
        worksheet.write(row, index, headers[index])
    row += 1

    for node in nodes:
        # print(node["nd.description"])
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
        if not write:
            worksheet.write(row, headers.index("NAME"), node["nd.name"])
        row += 1

    worksheet.autofilter('A1:Z' + str(row + 2))
    worksheet.set_column("A:Z", 50)
    workbook.close()

    subprocess.Popen(["open " + DEVICES_FILE_NAME], shell=True)


def ExportAlarms():
    print("Getting alarms")
    alarmsCritical = epnm.getAlarms(perceivedSeverity="critical")
    alarmsMajor = epnm.getAlarms(perceivedSeverity="major")
    alarmsMinor = epnm.getAlarms(perceivedSeverity="minor")

    workbook = xlsxwriter.Workbook(ALARMS_FILE_NAME)
    worksheet = workbook.add_worksheet()

    row = 0
    col = 0

    worksheet.write(row, col, "Alarm")
    worksheet.write(row, col + 1, "Severity")
    worksheet.write(row, col + 2, "Device")
    worksheet.write(row, col + 3, "Probable cause")
    row += 1

    if "com.response-message" in alarmsCritical.keys():
        if isinstance(alarmsCritical["com.response-message"]["com.data"]["alm.alarm"], type([])):
            for alarm in alarmsCritical["com.response-message"]["com.data"]["alm.alarm"]:
                worksheet.write(row, col, alarm["alm.description"])
                worksheet.write(row, col + 1, alarm["alm.perceived-severity"])
                worksheet.write(row, col + 2, alarm["alm.node-ref"])
                worksheet.write(row, col + 3, alarm["alm.probable-cause"])
                row += 1
        else:
            worksheet.write(row, col, alarmsCritical["com.response-message"]["com.data"]["alm.alarm"][
                "alm.description"])
            worksheet.write(row, col + 1, alarmsCritical["com.response-message"]["com.data"]["alm.alarm"][
                "alm.perceived-severity"])
            worksheet.write(row, col + 2, alarmsCritical["com.response-message"]["com.data"]["alm.alarm"][
                "alm.node-ref"])
            worksheet.write(row, col + 3, alarmsCritical["com.response-message"]["com.data"]["alm.alarm"][
                "alm.probable-cause"])
            row += 1

    if "com.response-message" in alarmsMajor.keys():
        if isinstance(alarmsMajor["com.response-message"]["com.data"]["alm.alarm"], type([])):
            for alarm in alarmsMajor["com.response-message"]["com.data"]["alm.alarm"]:
                worksheet.write(row, col, alarm["alm.description"])
                worksheet.write(row, col + 1, alarm["alm.perceived-severity"])
                if "alm.node-ref" in alarm.keys():
                    worksheet.write(row, col + 2, alarm["alm.node-ref"])
                worksheet.write(row, col + 3, alarm["alm.probable-cause"])
                row += 1
        else:
            worksheet.write(row, col, alarmsMajor["com.response-message"]["com.data"]["alm.alarm"][
                "alm.description"])
            worksheet.write(row, col + 1,
                            alarmsMajor["com.response-message"]["com.data"]["alm.alarm"]["alm.perceived-severity"])
            if "alm.node-ref" in alarmsMajor["com.response-message"]["com.data"]["alm.alarm"].keys():
                worksheet.write(row, col + 2,
                                alarmsMajor["com.response-message"]["com.data"]["alm.alarm"][
                                    "alm.node-ref"])
            worksheet.write(row, col + 3, alarmsMajor["com.response-message"]["com.data"]["alm.alarm"][
                "alm.probable-cause"])
            row += 1

    if "com.response-message" in alarmsMinor.keys():
        if isinstance(alarmsMinor["com.response-message"]["com.data"]["alm.alarm"], type([])):
            for alarm in alarmsMinor["com.response-message"]["com.data"]["alm.alarm"]:
                worksheet.write(row, col, alarm["alm.description"])
                worksheet.write(row, col + 1, alarm["alm.perceived-severity"])
                worksheet.write(row, col + 2, alarm["alm.node-ref"])
                worksheet.write(row, col + 3, alarm["alm.probable-cause"])
                row += 1
        else:
            worksheet.write(row, col, alarmsMinor["com.response-message"]["com.data"]["alm.alarm"]["alm.description"])
            worksheet.write(row, col + 1,
                            alarmsMinor["com.response-message"]["com.data"]["alm.alarm"]["alm.perceived-severity"])
            worksheet.write(row, col + 2,
                            alarmsMinor["com.response-message"]["com.data"]["alm.alarm"]["alm.node-ref"])
            worksheet.write(row, col + 3, alarmsMinor["com.response-message"]["com.data"]["alm.alarm"][
                "alm.probable-cause"])
            row += 1
    worksheet.autofilter('A1:D' + str(row + 2))
    worksheet.set_column("A:D", 50)
    workbook.close()
    subprocess.Popen(["open " + ALARMS_FILE_NAME], shell=True)


def PrintCommandResult(devices, command):
    params = [{"name": "command", "value": command}]
    print("Executing commands")
    jobName = epnm.executeCliTemplate("custom_command", devices, params=params)

    print("Retrieving results... this takes some time")
    while True:
        job = epnm.getJob(jobName=jobName)
        if "ra.run-status" in job["ra.config-response"]["ra.job-status"].keys():
            if job["ra.config-response"]["ra.job-status"]["ra.run-status"] == "COMPLETED":
                break
        time.sleep(2)

    if job["ra.config-response"]["ra.job-status"]["ra.status"] == "FAILURE":
        print("The command failed in one or more devices")

    if isinstance(job["ra.config-response"]["ra.deploy-result-list"]["ra.deploy-result"], type([])):
        for item in job["ra.config-response"]["ra.deploy-result-list"]["ra.deploy-result"]:
            print(item["ra.node-ref"].split("ND=")[1])
            print("============================")
            if "ra.transcript" in item.keys():
                print(item["ra.transcript"].split("[CDATA[")[2].split("]]")[0])
            elif "ra.message" in item.keys():
                print(item["ra.message"])
            else:
                print("No result or message")
            print("\n\n")
    else:
        result = job["ra.config-response"]["ra.deploy-result-list"]["ra.deploy-result"]["ra.transcript"]
        print(job["ra.config-response"]["ra.deploy-result-list"]["ra.deploy-result"]["ra.node-ref"].split("ND=")[1])
        print("============================")
        if "ra.transcript" in result.keys():
            print(result["ra.transcript"].split("[CDATA[")[2].split("]]")[0])
        elif "ra.message" in result.keys():
            print(result["ra.message"])
        else:
            print("No result or message")
        print("\n\n")


if __name__ == "__main__":
    while True:
        print("\n")
        print("********* Menu *********")
        print("\n")
        print("1. Get devices by name")
        print("2. Get devices by type")
        print("3. Get devices by group")
        print("4. Get alarms")
        print("5. Execute command by name")
        print("6. Execute command by type")
        print("7. Exit")
        print("\n")
        option = input("Select an option: ")

        if option == "1":
            deviceName = input("Insert name pattern: ")
            ExportDevicesByName(deviceName)
        elif option == "2":
            deviceType = input("Insert type pattern: ")
            ExportDevicesByType(deviceType)
        elif option == "3":
            groupName = input("Insert group pattern: ")
            ExportDevicesByGroup(groupName)
        elif option == "4":
            ExportAlarms()
        elif option == "5":
            deviceName = input("Insert device pattern: ")
            command = input("Insert command: ")
            devices = epnm.getDevicesByName(deviceName)
            nodes = []
            for device in devices["com.response-message"]["com.data"]["nd.node"]:
                nodes.append({"name": device["nd.name"]})
            PrintCommandResult(nodes, command)
        elif option == "6":
            deviceName = input("Insert device type pattern: ")
            command = input("Insert command: ")
            devices = epnm.getDevicesByType(deviceName)
            nodes = []
            for device in devices["com.response-message"]["com.data"]["nd.node"]:
                nodes.append({"name": device["nd.name"]})
            PrintCommandResult(nodes, command)
        elif option == "7":
            exit(0)
        else:
            print("Invalid option")
