import math
import datetime
import StarCatalog as Star

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
        return predict(values)
    elif(values['op'] == 'correct'):
        return correct(values)    #This calculation is stubbed out
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


#returns output dict for predict
def predict(values):
    #Check for missing or invalid inputs:
    if 'body' not in values:
        values['error'] = 'Missing mandatory information (body)'
        return values

    starName = values['body']
    if starName not in Star.starCatalog:
        values['error'] = 'star not in catalog'
        return values

    if 'lat' in values or 'long' in values:
        values['error'] = 'lat or long already in values'
        return values

    starData = Star.getStarData(starName).split(',')
    sha = splitDegAndMin(starData[0])
    latitude = starData[1]

    #Set default values:
    date = datetime.datetime.strptime('2001-01-01', '%Y-%m-%d')#.isoformat() == '2001-01-01'

    #Get values from input dict:
    if 'date' in values:
        inputDate = values['date'].split('-')
        year = inputDate[0]
        month = inputDate[1]
        day = inputDate[2]

        if year < 2001 or len(year) != 4 or len(month) != 2 or int(month) <= 0 or int(month) >= 13 or len(day) != 2:
            values['error'] = 'Invalid date'
            return values
        date = datetime.datetime.strptime(values['date'], '%Y-%m-%d')

    if 'time' in values:
        inputTime = values['time'].split(':')
        hours = inputTime[0]
        minutes = inputTime[1]
        seconds = inputTime[2]

        if int(hours) < 0 or int(hours) > 24 or len(hours) != 2:
            values['error'] = 'invalid time'
            return values
        date = date.replace(hour=int(hours))

        if int(minutes) < 0 or int(minutes) > 59 or len(minutes) != 2:
            values['error'] = 'invalid time'
            return values
        date = date.replace(minute=int(minutes))

        if int(seconds) < 0 or int(seconds) > 59 or len(seconds) != 2:
            values['error'] = 'invalid time'
            return values
        date = date.replace(second=int(seconds))

    #Values for the reference year and observation year
    referenceYear = 2001
    observationYear = date.year

    #calculates the cumulative progression
    cumulativeProgression = ((observationYear - referenceYear) * splitDegAndMin('-0d14.31667'))

    #The GHA of Aries on date 2001-01-01
    initialGhaAries = splitDegAndMin('100d42.6')

    #standard values
    numLeapYears = calcLeapYears(referenceYear, observationYear)
    earthRotationalPeriod = 86164.1
    earthClockPeriod = 86400
    earthRotationDeg = splitDegAndMin('360d0.00')

    dailyRotation = abs(earthRotationDeg - earthRotationalPeriod / earthClockPeriod * earthRotationDeg)
    leapYearProgression = dailyRotation * numLeapYears

    #calculates how far the prime meridian has rotated since the beginning of the observation year
    obsGhaAries = initialGhaAries + cumulativeProgression + leapYearProgression

    #calculates the angle of the earth's rotation since the beginning of the observation year
    totalSeconds = (date - datetime.datetime.strptime('2016-01-01', '%Y-%m-%d')).total_seconds()
    rotationAmount = totalSeconds / 86164.1 * splitDegAndMin('360d0.00')

    #total gha of aries
    ghaAries = obsGhaAries + rotationAmount

    #calculates the star's gha
    ghaStar = ghaAries + sha

    values['long'] = formatFinalVal(ghaStar)
    values['lat'] = latitude

    return values


#Returns output dict for correct
def correct(values):
    #Check for missing/invalid inputs and set corresponding values
    if 'lat' not in values or 'long' not in values:
        values['error'] = 'Missing mandatory information (lat or long)'
        return values

    latValuesIn = values['lat']
    lat = splitDegAndMin(latValuesIn)

    longValuesIn = values['long']
    longitude = splitDegAndMin(longValuesIn)

    if 'altitude' not in values:
        values['error'] = 'Missing mandatory information (altitude)'
        return values

    altIn = values['altitude']
    altitude = splitDegAndMin(altIn)

    if 'assumedLat' not in values or 'assumedLong' not in values:
        values['error'] = 'Missing mandatory information (assumedLat or assumedLong)'
        return values

    assumedLatIn = values['assumedLat']
    if 'd' not in assumedLatIn:
        values['error'] = 'assumedLat must be of format xdyy.y'
    assumedLatDegAndMin = assumedLatIn.split('d')
    assumedLatDeg = float(assumedLatDegAndMin[0])
    assumedLatMin = float(assumedLatDegAndMin[1])

    if assumedLatDeg < -90 or assumedLatDeg > 90 or assumedLatMin <= 0 or assumedLatMin > 60:
        values['error'] = 'Invalid  input for assumedLat'
        return values

    assumedLat = splitDegAndMin(assumedLatIn)

    assumedLongIn = values['assumedLong']
    if 'd' not in assumedLongIn:
        values['error'] = 'assumedLong must be of format xdyy.y'
    assumedLongDegAndMin = assumedLongIn.split('d')
    assumedLongDeg = float(assumedLongDegAndMin[0])
    assumedLongMin = float(assumedLongDegAndMin[1])

    if assumedLongDeg < 0 or assumedLongDeg > 360 or assumedLongMin <= 0 or assumedLongMin > 60:
        values['error'] = 'Invalid  input for assumedLong'
        return values

    assumedLong = splitDegAndMin(assumedLongIn)

    if 'correctedDistance' in values or 'correctedAzimuth' in values:
        values['error'] = 'correctedDistance or correctedAzimuth already in values'

    #Calculate LHA
    lha = longitude + assumedLong
    # print formatNum(lha)
    # print format_altitude(lha)
    intermediateDist = ((math.sin(math.radians(lat)) * math.sin(math.radians(assumedLat))) + (math.cos(math.radians(lat)) * math.cos(math.radians(assumedLat)) * math.cos(math.radians(lha))))

    correctedAltitude = math.degrees(math.asin(intermediateDist))
    #print formatNum(correctedAltitude)

    correctedDistance = altitude - correctedAltitude
    #correctedDistance = math.degrees(correctedDistanceRad)
    # print formatNum(correctedDistance)
    # print convertToArcMin(correctedDistance)

    latDeg = convertToCorrectFormat(latValuesIn)
    assLatDeg = convertToCorrectFormat(assumedLatIn)

    latRad = math.radians(latDeg)
    assLatRad = math.radians(assLatDeg)
    correctedAzimuthRad = math.acos(((math.sin(latRad)) - math.sin(assLatRad) * intermediateDist) / (math.cos(assLatRad) * math.cos(math.asin(intermediateDist))))
    correctedAzimuth = round(math.degrees(correctedAzimuthRad), 3)
    # print convertToArcMin(correctedDistance)
    # print formatNum(correctedAzimuth)

    values['correctedDistance'] = convertToArcMin(correctedDistance)
    values['correctedAzimuth'] = formatNum(correctedAzimuth)
    return values


def convert_to_celcius(x):
    return (x - 32) * 5/9


def format_altitude(altitude):
    altDegrees = math.floor(altitude)
    altMinutes = round((altitude - altDegrees) * 60, 1)
    outputAlt = '%d'%(altDegrees) + 'd' + '%.1f'%(altMinutes)
    return outputAlt


def formatNum(x):
    x_degrees = math.floor(x)
    if x < 0:
        x_degrees = math.ceil(x)
    x_minutes = abs(round((x - x_degrees) * 60, 1))
    output = '%dd%.1f' % (x_degrees, x_minutes)
    return output


def formatFinalVal(x):
    x_degrees = math.floor(x)
    newDegrees = x_degrees % 360
    x_minutes = abs(round((x - x_degrees) * 60, 1))
    output = '%dd%.1f' % (newDegrees, x_minutes)
    return output


def splitDegAndMin(x):
    degreesAndMin = x.split('d')
    degrees = int(degreesAndMin[0])
    minutes = float(degreesAndMin[1])
    total = (abs(degrees) + (minutes / 60))
    if degreesAndMin[0].__contains__('-'):
        return -1 * total
    return total


def calcLeapYears(refYear, obsYear):
    count = 0
    for x in range(refYear, obsYear):
        if x % 4 == 0 or ((x % 100 == 0) and (x % 400 == 0)):
            count = count + 1
    return count

def convertToArcMin(x):
    degAndMin = formatNum(x).split('d')
    deg = int(degAndMin[0])
    min = float(degAndMin[1])
    arcMin = (deg * 60 + min)
    return round(arcMin, 0)

def convertToCorrectFormat(x):
    degAndMin = x.split('d')
    deg = float(degAndMin[0])
    min = float(degAndMin[1])
    min = min / 60
    if deg < 0:
        deg = deg - min
    else:
        deg = deg + min

    return deg



# inputval = {'observation': '30d1.5', 'height': '19.0', 'pressure': '1000', 'horizon': 'artificial', 'op': 'adjust', 'temperature': '85'}
# inputval2 = {'observation': '45d15.2', 'height': '6', 'pressure': '1010', 'horizon': 'natural', 'op': 'adjust', 'temperature': '71'}
# inputval3 = {'observation': '101d15.2', 'height': '6', 'pressure': '1010', 'horizon': 'natural', 'op': 'adjust', 'temperature': '71'}
# inputVal4 = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2016-01-17', 'time': '03:15:42'}
inputVal5 = {'op': 'predict'}
# inputVal6 = {'op': 'predict', 'body': 'unknown', 'date': '2016-01-17', 'time': '03:15:42'}
# inputVal7 = {'op': 'predict', 'body': 'Acrux', 'date': '2016-01-17', 'time': '03:15:42'}
# inputVal8 = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2016-01-17', 'time': '03:15:99', 'lat': '65d89', 'long': '75d35'}
inputVal9 = {'op': 'correct', 'lat':'16d32.3', 'long': '95d41.6', 'altitude': '13d42.3', 'assumedLat': '-53d38.4', 'assumedLong': '74d35.3'}
output = dispatch(inputVal9)
print output
