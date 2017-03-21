from softwareprocess.dispatch import dispatch
import unittest




class DispatchTest(unittest.TestCase):
    #-------------------------------------------------
    #--------Acceptance Test
    # Desired level of confidence: boundary value analysis
    #-------------------------------------

    #Sad Path

    def test_dispatch_empty_input(self):
        inputDict = {}
        output = dispatch(inputDict)
        self.assertEquals(output == {'error': 'no op is specified'})
