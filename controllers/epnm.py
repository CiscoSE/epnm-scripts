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
This file contains all the API calls needed for the scripts in the root folder
"""
from Constants import *
import json
import requests
import base64
from jinja2 import Environment
from jinja2 import FileSystemLoader
import os
import urllib3

DIR_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
TEMPLATES = Environment(loader=FileSystemLoader(DIR_PATH + '/templates'))
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def makeCall(p_url, method, data=""):
    """
    Single exit point for all APIs calls for EPN-M
    :param p_url:
    :param method:
    :param data:
    :return:
    """
    credentials = base64.encodebytes(bytes(EPN_USER + ":" + EPN_PASSWORD, "utf-8")).decode("utf-8")

    headers = {
        'Authorization': "Basic " + credentials[:len(credentials) - 1],  # Remove the scape character at the end
        "Content-Type": "application/xml",
        "Accept": "application/json"
    }
    if method == "POST":
        response = requests.post(EPN_URL + p_url, data=data, headers=headers, verify=False)
    elif method == "GET":
        response = requests.get(EPN_URL + p_url, headers=headers, verify=False)
    else:
        raise Exception("Method " + method + " not supported by this controller")
    if 199 > response.status_code > 300:
        errorMessage = json.loads(response.text)["errorDocument"]["message"]
        raise Exception("Error: status code" + str(response.status_code) + " - " + errorMessage)
    return response


def getDevicesByType(productType=None):
    """
    Get all devices managed by EPN-M and creates an excel file
    :return:
    """
    query = ""
    if productType:
        query = "?product-type=" + productType
    response = makeCall(p_url="restconf/data/v1/cisco-resource-physical:node" + query,
                        method="GET")

    return response.json()


def getDevicesByName(nodeName=None):
    """
    Get all devices managed by EPN-M and creates an excel file
    :return:
    """
    query = ""
    if nodeName:
        query = "?name=" + nodeName
    response = makeCall(p_url="restconf/data/v1/cisco-resource-physical:node" + query,
                        method="GET")
    return response.json()


def getAlarms(perceivedSeverity):
    """
       Get all devices managed by EPN-M and creates an excel file
       :return:
       """
    query = "?perceived-severity=" + perceivedSeverity
    response = makeCall(p_url="restconf/data/v1/cisco-rtm:alarm" + query,
                        method="GET")

    return response.json()


def executeCliTemplate(templateName, nodes, params=None):
    """
    Executes a template and returns the job name
    :param templateName:
    :param deviceName:
    :return:
    """
    p_url = "restconf/operations/v1/cisco-resource-activation:run-cli-configuration"
    template = TEMPLATES.get_template('createCliTemplate.j2.xml')
    payload = template.render(templateName=templateName, nodes=nodes, params=params)
    response = makeCall(p_url, "POST", payload)
    return response.json()["ra.config-response"]["ra.job-status"]["ra.job-name"]


def getJob(jobName):
    """
    Return data about an specific job
    :param jobName:
    :return:
    """
    p_url = "restconf/operations/v1/cisco-resource-activation:get-cli-configuration-run-status/" + jobName
    response = makeCall(p_url, "GET")
    return response.json()


def getGroupByName(groupName):
    """
        Return all devices within a group per name
        :param jobName:
        :return:
        """
    p_url = "restconf/data/v1/cisco-resource-physical:group?fdn=MD=CISCO_EPNM!GR=" + groupName
    response = makeCall(p_url, "GET")
    return response.json()


def getDevicesByFdn(fdn):
    """
    Get all devices managed by EPN-M and creates an excel file
    :return:
    """
    query = "?fdn=" + fdn
    response = makeCall(p_url="restconf/data/v1/cisco-resource-physical:node" + query,
                        method="GET")
    return response.json()
