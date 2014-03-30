# -*- coding: utf-8 -*-
import json
from pprint import pprint
import os

def main():
    json_data=open('faulty.json')
    data=json.load(json_data)
    #pprint(data)
    print data
    json_data.close()

if __name__ == '__main__':
    main()

#RET: [NEW]: 3ChicsPolitico : [NEW]: RT @raven_rainfall: @3ChicsPolitico
#"@Stone_SkyNews A profile of @HishammuddinH2O - the man at the centre of the search for #MH370
#http:/ΓÇª
