import math

def dispatch(values=None):

    #Validate parm
    if(values == None):
        return {'error': 'parameter is missing'}
    if(not(isinstance(values,dict))):
        return {'error': 'parameter is not a dictionary'}
    if (not('op' in values)):
        values['error'] = 'no op is specified'
        return values

    #Perform designated function
    if(values['op'] == 'adjust'):
        return adjustValues(values)
    elif(values['op'] == 'predict'):
        return values    #This calculation is stubbed out
    elif(values['op'] == 'correct'):
        return values    #This calculation is stubbed out
    elif(values['op'] == 'locate'):
        return values    #This calculation is stubbed out
    else:
        values['error'] = 'op is not a legal operation'
        return values


#Returns the output dict for adjust
def adjustValues(values):

    #default values for elements
    height = 0
    temp = 72
    pressure = 1010
    horizon = 'natural'

    #set the values of the elements if they are in the input dict
    if 'height' in values:
        #height = int(values['height'])
        if height < 0 or values['height'].isalpha():
            values['error'] = 'height must be >= 0 and must be a numeric value only'
            return values
        height = float(values['height'])

    if 'temperature' in values:
        temp = int(values['temperature'])

    if 'pressure' in values:
        pressure = int(values['pressure'])

    if 'horizon' in values:
        horizon = values['horizon']


    #check for invalid inputs
    if 'observation' not in values:
        values['error'] = 'missing observation'
        return values

    if 'altitude' in values:
        values['error'] = 'altitude already exists'
        return values


    if temp < -20 or temp > 120:
        values['error'] = 'temperature must be >= -20 and <= 120'
        return values

    if pressure < 100 or pressure > 1100:
        values['error'] = 'pressure must be >= 100 and <= 1100'
        return values

    if horizon != 'artificial' and horizon != 'natural':
        values['error'] = 'horizon is invalid'
        return values


    #get values for the observation and split into degrees and minutes
    observationValues = values['observation'].split('d')
    observationDegrees = int(observationValues[0])
    observationMinutes = float(observationValues[1])

    if observationDegrees < 0 or observationDegrees >= 90:
        values['error'] = 'degrees are out of range, should be between 0 and 90'
        return values

    if observationMinutes < 0.0 or observationMinutes >= 60:
        values['error'] = 'minutes should be greater than or equal to 0.0 and less than 60'
        return values

    total_observation = observationDegrees + (observationMinutes / 60)

    #Calculate the dip
    if horizon == 'artificial':
        dip = 0
    else:
        dip = (-0.97 * (math.sqrt(height))) / 60

    #Calculate the refraction
    refraction = (-0.00452 * pressure) / (273 + convert_to_celcius(temp)) / math.tan(math.radians(total_observation))

    #Calculate the adjusted altitude:
    altitude = total_observation + dip + refraction
    adjusted_altitude = format_altitude(altitude)

    values['altitude'] = adjusted_altitude
    return values


def convert_to_celcius(x):
    return (x - 32) * 5/9

def format_altitude(altitude):
    altMinutes = round((altitude - math.floor(altitude)) * 60, 1)
    altDegrees = math.floor(altitude)
    outputAlt = '%d'%(altDegrees) + 'd' + '%.1f'%(altMinutes)
    return outputAlt


# inputval = {'observation': '30d1.5', 'height': '19.0', 'pressure': '1000', 'horizon': 'artificial', 'op': 'adjust', 'temperature': '85'}
# inputval2 = {'observation': '45d15.2', 'height': '6', 'pressure': '1010', 'horizon': 'natural', 'op': 'adjust', 'temperature': '71'}
# inputval3 = {'observation': '101d15.2', 'height': '6', 'pressure': '1010', 'horizon': 'natural', 'op': 'adjust', 'temperature': '71'}
# output = dispatch(inputval3)
# print output
