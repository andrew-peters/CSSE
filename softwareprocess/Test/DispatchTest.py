import unittest
import softwareprocess.dispatch as DT
import math



class DispatchTest(unittest.TestCase):
    #-------------------------------------------------
    #--------Acceptance Test
    # Desired level of confidence: boundary value analysis
    #-------------------------------------

    #Sad Path

    def test_dispatch_empty_input(self):
        #DT.dispatch({}) 
        output = DT.dispatch({})
        self.assertEquals(output == {'error': 'no op is specified'})
