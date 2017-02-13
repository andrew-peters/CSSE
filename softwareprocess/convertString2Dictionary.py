"""
    Created on Feb 11, 2017

    @author: Andrew Peters
"""



import urllib



def convertString2Dictionary(inputString = ""):
    errorDict = {'error': 'true'}
    outputDict = {}

    #Checks to see if inputString is empty
    if inputString == '':
        return errorDict

    #Converts percent-encoded string into normal string
    unqotedString = urllib.unquote(inputString)

    #Separates input string on commas and puts into a list, resulting in a list of the key=value pairs
    listOfPairs =[str.strip() for str in unqotedString.split(',')]

    if len(listOfPairs) == 0:
        return errorDict

    #Iterate through the list of key value pairs and get each separate pair
    for i in range(len(listOfPairs)):
        kvPair = [str.strip() for str in listOfPairs[i].split('=')]

        #Checks to see if list is empty
        if len(kvPair) <= 1:
            print errorDict
            return errorDict

        #Assigns key and value in each pair
        key = kvPair[0]
        value = kvPair[1]


        #Checks to see if keys and values are valid inputs
        if not key[0].isalpha() or not key.isalnum() or not value.isalnum():
            print errorDict
            return errorDict


        #Checks for duplicates. If there are, return the error.
        if key in outputDict:
            print errorDict
            return errorDict

        #If all the previous checks pass, the key-value pair is valid and added to the dictionary.
        outputDict[key] = value


    print outputDict
    return outputDict









#Main program to use as a sandbox to test the function
def main():

    #Various test cases
    input = 'uname=mark,pwd=test,age=20'
    input2 = urllib.quote(input)
    input3 = 'abc%3D123'
    input4 = 'function%3D%20calculatePosition%2C%20sighting%3DBetelgeuse'
    input5 = '1function%3DcalculatePosition%2C%20sighting%3DBetelgeuse'
    input6 = '1key%3Dvalue'
    input7 = 'key%3Dvalue%2C%20key%3Dvalue'
    input8 = 'function%20%3D%20get_stars'
    input9 = 'key%3D'
    input10 = '&(*3'
    input11 = 'k%20e%20y%20%3D%20value'
    input12 = 'key1%3Dvalue%3B%20key2%3Dvalue'

    #When testing, change the input number to mach the test input you want to use
    convertString2Dictionary(input4)

#Run the program
main()
