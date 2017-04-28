import unittest
import softwareprocess.dispatch as DT




class DispatchTest(unittest.TestCase):
    #100 dispatch-------------------------------------------------
    #--------Acceptance Test
    # Desired level of confidence: boundary value analysis
    #------------------------------------------------

    #Sad Path

    def test_dispatch_empty_input(self):
        #DT.dispatch({})
        output = DT.dispatch({})
        self.assertTrue(output == {'error': 'no op is specified'})

    def test_dispatch_invalid_dict(self):
        output = DT.dispatch(42)
        self.assertTrue(output == {'error':'parameter is not a dictionary'})

    def test_dispatch_invalid_observation(self):
        output = DT.dispatch({'observation': '101d15.2', 'height': '6', 'pressure': '1010', 'horizon': 'natural',
                              'op': 'adjust', 'temperature': '71'})
        self.assertTrue(output == {'temperature': '71', 'height': '6', 'pressure': '1010', 'horizon': 'natural',
                                   'error': 'degrees are out of range, should be between 0 and 90', 'observation': '101d15.2', 'op': 'adjust'})




    #200 predict   -------------------------------------------------
    #--------Acceptance Test
    # Desired level of confidence: boundary value analysis
    #------------------------------------------------


    #Happy Path
    def test200_01_ShouldReturnCorrectLatAndLong(self):
        input = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2016-01-17', 'time': '03:15:42'}
        output = {'op':'predict', 'body': 'Betelgeuse', 'date': '2016-01-17', 'time': '03:15:42', 'long': '75d53.6','lat': '7d24.3'}
        self.assertDictEqual(DT.dispatch(input), output)


    def test200_02_ShouldReturnCorrectLatAndLong(self):
        input = {'op': 'predict', 'body': 'Acrux', 'date': '2016-01-17', 'time': '03:15:42'}
        output = {'body': 'Acrux', 'long': '338d1.7', 'lat': '-63d10.9', 'time': '03:15:42', 'date': '2016-01-17', 'op': 'predict'}
        self.assertDictEqual(DT.dispatch(input), output)


    #Sad Path
    def test200_03_ShouldReturnErrorForMissingInformation(self):
        input = {'op': 'predict'}
        output = {'error': 'Missing mandatory information (body)', 'op': 'predict'}
        self.assertDictEqual(DT.dispatch(input), output)

    def test200_04_ShouldReturnErrorForStarNotInCatalog(self):
        input = {'op': 'predict', 'body': 'Unknown', 'date': '2016-01-17', 'time': '03:15:42'}
        output = {'body': 'Unknown', 'date': '2016-01-17', 'time': '03:15:42', 'error': 'star not in catalog', 'op': 'predict'}
        self.assertDictEqual(DT.dispatch(input), output)



    #300 correct   -------------------------------------------------
    #--------Acceptance Test
    # Desired level of confidence: boundary value analysis
    #------------------------------------------------

    def test300_01_ShouldRetrunError(self):
        input = {'op': 'correct', 'lat': '5d87'}
        output = {'op': 'correct','lat': '5d87', 'error': 'Missing mandatory information'}
        self.assertDictEqual(DT.dispatch(input), output)

     def test300_02_ShouldReturnCorrectOutput(self):
        input = {'op': 'correct', 'lat':'16d32.3', 'long': '95d41.6', 'altitude': '13d42.3', 'assumedLat': '-53d38.4', 'assumedLong': '74d35.3'}
        output = {'assumedLat': '-53d38.4', 'correctedDistance': 3950.0, 'altitude': '13d42.3', 'assumedLong': '74d35.3', 'long': '95d41.6', 'lat': '16d32.3', 'correctedAzimuth': '164d43.0', 'op': 'correct'}

        self.assertDictEqual(DT.dispatch(input), output)
