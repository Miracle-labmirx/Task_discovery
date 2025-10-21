import requests
import json
API_KEY = "sato_1oyQx-XWRQ1tq7VjLxIw_2NNWwLct7onsRGbQNNYTzs"
HEADERS = {"x-api-key": API_KEY}

KPI_DEF = {"id":"KPI:Max-Supply-Pressure-Deviation","type":"Task","description":"KPI definition for the maximum supply pressure deviation in the AHU, takes as input a timeseries of supply pressure and supply pressure setpoints and outputs the maximum supply pressure deviation over the entire timeseries as a float","category":"KPI","requires":{"SupPres":{"type":"Device","category":"Sensor","measuresProperty":"Air-Pressure-Supply","unit":"PAL"},"SupPresSetp":{"type":"Device","category":"Actuator","controlsProperty":"Setpoint-Air-Pressure-Supply","unit":"PAL"}},"arguments":{"scope":{"type":"enum","values":["1 minute","5 minutes","15 minutes","hourly","daily","weekly","yearly"]}},"taskId":"A28-K:SC000-V02","name":"Max Supply Pressure Deviation"}

#load json file
with open('json_files/tasks_kpi.json') as f:
    kpi_definitions = json.load(f)

for kpi in kpi_definitions:
    requirements = kpi["requires"]
    type = category = unit = measuresProperty = controlsProperty = ""
    for req in requirements:
        if "type" in requirements[req]:
            type = requirements[req]["type"]
            # if 'Building' in type or 'Zone' in type or 'Space' in type:
            #     print(type)
        if "category" in requirements[req]:
            category = requirements[req]["category"]
        if "unit" in requirements[req]:
            unit = requirements[req]["unit"]
        if "measuresProperty" in requirements[req]:
            measuresProperty = requirements[req]["measuresProperty"]
        if "controlsProperty" in requirements[req]:
            controlsProperty = requirements[req]["controlsProperty"]
        print(kpi["id"],kpi["taskId"],len(requirements),type,category, measuresProperty, controlsProperty, unit, sep=",")

#print(KPI_DEF["id"])
#print(KPI_DEF["type"])
#print(KPI_DEF["description"])
#print(KPI_DEF["category"])
#requirements = KPI_DEF["requires"]
#for req in requirements:
 #   type = requirements[req]["type"]
    #category = requirements[req]["category"]
    #unit = requirements[req]["unit"]
  #  print(type)
    #print(req)
    #print(requirements[req])


#print(KPI_DEF["requires"]["SupPres"]["type"])
#print(KPI_DEF["requires"]["SupPres"]["category"])
#print(KPI_DEF["requires"]["SupPres"]["measuresProperty"])
#print(KPI_DEF["requires"]["SupPres"]["unit"])
#print(KPI_DEF["requires"]["SupPresSetp"]["type"])
#print(KPI_DEF["requires"]["SupPresSetp"]["category"])
#print(KPI_DEF["requires"]["SupPresSetp"]["controlsProperty"])
#print(KPI_DEF["requires"]["SupPresSetp"]["unit"])
#print(KPI_DEF["arguments"]["scope"]["type"])
#print(KPI_DEF["arguments"]["scope"]["values"])
#print(KPI_DEF["taskId"])
