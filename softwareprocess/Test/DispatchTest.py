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
    def test200_ShouldReturnCorrectLatAndLong(self):
        input = {
            'op': 'predict',
            'body': 'Betelgeuse',
            'date': '2016-01-17',
            'time': '03:15:42'
        }
        output = {
            'op':'predict',
            'body': 'Betelgeuse',
            'date': '2016-01-17',
            'time': '03:15:42',
            'long': '75d53.6',
            'lat': '7d24.3'
        }
        self.assertDictEqual(nav.dispatch(input), output)
