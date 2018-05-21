#!/usr/bin/env python

import datetime
import argparse
import sys
import urllib
import urllib2
import json
import ast


OMS_API_SERVER = 'http://cmsomsapi.cern.ch:8080/api/v1'

class OmsApi:
    """
    OMS API object
    """

    def __init__(self, url = None, debug = False):
        """
        Construct API object.
        url: URL to OMS API server
        debug: should debug messages be printed out? Verbose!
        """
        if not url:
            self.url = OMS_API_SERVER
        else:
            self.url = url
        self.debug = debug

    def dprint(self, *args):
        """
        Print debug information
        """
        if self.debug: 
            print "OmsApi:",
            for arg in args:
                print arg, 
            print
            
    @staticmethod
    def defaultServer():
        return OMS_API_SERVER

    @staticmethod
    def buildFilters( filter_list ):
        """
        filter_list: list of filters
        each filter: 3 items: column, comparator, value
        returned: dictionary to be converted by urlencode and appended to url
        """
        if not filter_list:
            return {}
        filters = {}
        for filter in filter_list:
            name = 'filter[' + filter[0] + '][' + filter[1] + ']'
            filters[name] = filter[2]
        return filters
    
    @staticmethod
    def rows( response ):
        """
        extract data rows from OMS object
        """
        rows = []
        data = response['data']
        if isinstance( data, list ):
            for row in data:
                rows.append(row['attributes'])
        else:
            rows.append( data )
        return rows
    
    def getRows(self, resource, filters, fields = None ):
        """
        get data rows from OMS API server according to filters and selected fields
        """
        response = self.getOmsObject( resource, filters, fields )
        return self.rows( response )

    def getOmsObject(self, resource, filters = None, fields = None ):
        """
        get OMS API object from server accroding to filters and selected fields
        """
        params = self.buildFilters(filters)
        if fields:
            params['fields[' + resource + ']'] = ','.join( fields )

        if type(params) != dict: 
            params = {}
        all_params = dict( params )
        all_params['page[limit]'] = 100000
        all_params['include'] = 'dataonly,meta'

        #
        # Constructing request path
        #
        url_values = urllib.urlencode( all_params )
        callurl = self.url + '/' + resource + '?' + url_values

        #
        # Do the query and respond
        #
        self.dprint( callurl )

        request = urllib2.Request( callurl )
        response = urllib2.urlopen(request)
        data = json.load( response )
        return data



def dumpMap(some_map):
    print ""
    print ""
    for key in some_map.keys():
        print key
    print ""
    for key in some_map.keys():
        print key,some_map[key]
        print ""
    print ""
    print ""

parser = argparse.ArgumentParser( description='python example script to get fill info from OMSAPI', formatter_class=argparse.ArgumentDefaultsHelpFormatter )
parser.add_argument( '-y', '--year', type = int, help='get info for all fills of this year')
parser.add_argument( "-s", "--server", help = "server URL, default=" + OmsApi.defaultServer(), default=None )

args = parser.parse_args()


api = OmsApi( args.server, debug = False )
if args.year:
    Jan1 = datetime.datetime( args.year, 1, 1 )
    Dec31 = datetime.datetime( args.year, 12, 31 )
    fills = api.getOmsObject( 'fills', 
              filters = [ [ 'start_time', 'GT', Jan1.isoformat() + 'Z'], [ 'start_time', 'LT', Dec31.isoformat() + 'Z'], ['start_stable_beam', 'NEQ', 'null'] ],
              fields = ['fill_number','peak_lumi','peak_pileup','efficiency_lumi','bunches_target','start_stable_beam','end_time','to_ready_time','delivered_lumi,recorded_lumi'] 
    )
#    dumpMap(fills)
    data = sorted(fills["data"])
    outFile = open("rawFillList2018.txt","w")
    for fill in data:
#        dumpMap(fill)
        if "attributes" in fill:
            atts=fill["attributes"]
            meta=fill["meta"]
            fillNum=fill["id"]
            start_time=atts["start_stable_beam"].replace("T"," ").replace("Z","")
            if atts["end_time"] != None:
                end_time=atts["end_time"].replace("T"," ").replace("Z","")
            else:
                end_time=""

            lumi = str(atts["delivered_lumi"])

            if "pb" in meta["row"]["delivered_lumi"]["units"]: #### skip for heavy ion collisions (which are measured in ub)
                outFile.write(",".join([fillNum,start_time,end_time,lumi+"\n"]))

            #     print ",".join([fill["id"],atts["start_time"],atts["end_time"],str(atts["delivered_lumi"])+" "+meta["row"]["delivered_lumi"]["units"]])
            # else:
            #     print ",".join([fill["id"],atts["start_time"],"-1",str(atts["delivered_lumi"])])

        
#    print fills.split("[")[2].split("]")[0]
    #print ast.literal_eval(fills)

       
 
 
