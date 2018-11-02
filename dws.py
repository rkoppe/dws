'''


python -m pip install pandas
'''
from _io import StringIO
from datetime import date
import json
import urllib

import requests

import pandas as pd
import datetime



class dws:
    SENSOR_BASE_URL = 'https://sensor.awi.de/rest'
    DATA_BASE_URL = 'https://dashboard.awi.de/data-xxl/rest'
   
   
   
    @staticmethod
    def sensors(pattern: str = None):
        url = dws.DATA_BASE_URL + '/sensors'
        if pattern != None:
            url += '?pattern=' + pattern
        
        response = requests.get(url, stream = True)
        
        if response.status_code != 200:
            raise Exception('Error loading sensors.'.format(response.reason))
        
        j = json.loads(response.content)

        return j
        
        
        
    @staticmethod
    def get(sensors, begin: date, end: date, aggregate: str = 'hour'):
        if sensors == None or len(sensors) == 0:
            raise Exception('Sensor(s) must be defined.')

        if begin == None:
            raise Exception('Begin timestamp must be defined.')
        
        if end == None:
            raise Exception('End timestamp must be defined.')
        
        if isinstance(sensors, str):
            sensors = [sensors]
            
        if isinstance(begin, str):
            if len(begin) == 10:
                begin = datetime.datetime.strptime(begin, '%Y-%m-%d')
            else:
                begin = datetime.datetime.strptime(begin, '%Y-%m-%dT%H:%M:%S')
                
        if isinstance(end, str):
            if len(end) == 10:
                end = datetime.datetime.strptime(end, '%Y-%m-%d')
            else:
                end = datetime.datetime.strptime(end, '%Y-%m-%dT%H:%M:%S')
        
        
        url = dws.DATA_BASE_URL + '/data' + \
            '?format=text/tab-separated-values' + \
            '&beginDate=' + begin.strftime('%Y-%m-%dT%H:%M:%S') + \
            '&endDate=' + end.strftime('%Y-%m-%dT%H:%M:%S') + \
            '&aggregate=' + aggregate.upper()
        
        for sensor in sensors:
            url += '&sensors=' + urllib.parse.quote_plus(sensor)
        
        response = requests.get(url, stream = True)
        
        if response.status_code != 200:
            raise Exception('Error loading data.'.format(response.reason))

        # build the data frame
        df = pd.read_csv(StringIO(response.content.decode('UTF-8')), sep = '\t')
        df['datetime'] = pd.to_datetime(df['datetime'])
        return df



    @staticmethod
    def sensor(code: str):
        url = dws.SENSOR_BASE_URL + '/sensors/sensorOutputs/getSensorOutputByUrn/' + urllib.parse.quote_plus(code)
        response = requests.get(url)
        
        if response.status_code != 200:
            raise Exception('Error loading sensor metadata.')
        
        j = json.loads(response.content)
        
        r = {
            'id': j['id'],
            'name': j['name'],
            'type': j['sensorOutputType']['generalName'],
            'description': j['sensorOutputType']['description'],
            'definition': j['sensorOutputType']['vocableValue'],
            'unit': j['unitOfMeasurement']['code'],
        }
        
        url = dws.SENSOR_BASE_URL + '/sensors/measurementProperties/getSensorOutputMeasurementProperties/' + str(r['id'])
        response = requests.get(url)
        
        j = json.loads(response.content)
        
        properties = {}
        for i in j:
            name = i['measurementName'].lower().replace(' ', '_')
            properties[name] = {
                'id': i['id'],
                'lower': i['lowerBound'],
                'upper': i['upperBound'],
                'unit': i['unitOfMeasurement']['code']
            }
        
        r['properties'] = properties
        
        return r
        
        
    
    @staticmethod
    def platform(code: str):
        parts = code.split(':')
        
        if len(parts) < 2:
            raise Exception('Code is to short and cannot be resolved to a platform code.')
        
        base = ':'.join(parts[0:2])
        url = dws.SENSOR_BASE_URL + '/sensors/device/getDeviceByUrn/' + urllib.parse.quote_plus(base)
        response = requests.get(url, stream = True)
        
        if response.status_code != 200:
            raise Exception('Error loading platform metadata.')
        
        j = json.loads(response.content)
        
        r = {
            'id': j['ID'],
            'code': j['urn'],
            'shortName': j['shortName'],
            'longName': j['longName'],
            'description': j['description'],
            'definition': j['rootItemType']['vocableValue']
        }
        
        return r
        
    
    
    @staticmethod
    def meta(code: str):
        platform = dws.platform(code)
        
        url = dws.SENSOR_BASE_URL + \
            '/sensors/device/getDetailedItem/' + str(platform['id']) + \
            '?includeChildren=true'
        response = requests.get(url, stream = True)
        
        if response.status_code != 200:
            raise Exception('Error loading detailed platform metadata.')
        
        j = json.loads(response.content)
        
        r = dws._parseItems(j['childItem'])
        platform['children'] = r['items']
        platform['map'] = r['map']
        
        return platform
        
        
        
    @staticmethod
    def meta_json(code: str):
        platform = dws.platform(code)
        
        url = dws.SENSOR_BASE_URL + \
            '/sensors/device/getDetailedItem/' + str(platform['id']) + \
            '?includeChildren=true'
        response = requests.get(url, stream = True)
        
        if response.status_code != 200:
            raise Exception('Error loading detailed platform metadata.')
        
        j = json.loads(response.content)
        
        return j
    
    
    
    @staticmethod
    def meta_sensorML(code: str):
        platform = dws.platform(code)
        
        url = dws.SENSOR_BASE_URL + \
            '/sensors/device/getDeviceAsSensorML/' + str(platform['id'])
        response = requests.get(url, stream = True)
        
        if response.status_code != 200:
            raise Exception('Error loading detailed platform metadata.')
        
        return response.content
    
        
        
    @staticmethod
    def _parseItems(sensorItems: list):
        items = []
        map = {}
        
        for sensorItem in sensorItems:
            item = {
                'id': sensorItem['ID'],
                'code': sensorItem['urn'],
                'shortName': sensorItem['shortName'],
                'longName': sensorItem['longName'],
                'description': sensorItem['description'],
                'definition': sensorItem['rootItemType']['vocableValue'] if 'rootItemType' in sensorItem else ''
            }
        
            parameters = []
            for sensorOutputItem in sensorItem['sensorOutput_Item']:
                sensorOutput = sensorOutputItem['sensorOutput']
                parameter = {
                    'id': sensorOutput['id'],
                    'name': sensorOutput['name'],
                    'code': sensorOutput['shortname'] if sensorOutput['shortname'] != '' else sensorOutput['name'],
                    'type':  sensorOutput['sensorOutputType']['generalName'],
                    'description':  sensorOutput['sensorOutputType']['description'],
                    'definition':  sensorOutput['sensorOutputType']['vocableValue'],
                    'unit':  sensorOutput['unitOfMeasurement']['code']
                }
                
                
                properties = []
                propertyMap = {}
                if 'measurementPropertySensorOutputs' in sensorOutput:
                    for sensorProperty in sensorOutput['measurementPropertySensorOutputs']:
                        property = {
                            'name': sensorProperty['measurementProperty']['measurementName'],
                            'lower': sensorProperty['measurementProperty']['lowerBound'],
                            'upper': sensorProperty['measurementProperty']['upperBound'],
                            'unit': sensorProperty['measurementProperty']['unitOfMeasurement']['code']
                        }
                        
                        properties.append(property)
                        propertyMap[property["name"].lower().replace(' ', '_')] = property
                
                parameter['properties'] = properties
                parameters.append(parameter)
                
                code = item['code'] + ':' + parameter['code']
                map[code] = parameter
                map[code]['properties'] = propertyMap

            items.append(item)
            
            
            r = dws._parseItems(sensorItem['childItem'])
            item['children'] = r['items']
            map = {**map, **r['map']}
        
        r = {
            'items': items,
            'map': map
        }
        return r
 