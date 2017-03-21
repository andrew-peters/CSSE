import dispatch as dispatch
import re

def lambda_handler(event, context):
    try:
        if('querystring' in event):
            eventParms = event['querystring'].strip('{}').replace(',',' ')
            eventDict = dict(re.findall(r'(\S+)=(".*?"|\S+)', eventParms))
            returnValue = dispatch.dispatch(eventDict)
            return returnValue
        else:
            return u"None\n"
    except:
        return u"None\n"


'''

{
    "querystring": "$input.params().querystring"
}


'''


