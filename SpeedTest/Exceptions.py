'''
This file contains various exceptions that may occur when working with www.speedtest.net
'''

class SpeedTestServersError(Exception):
    '''
    Exception raised when no servers are found
    '''

    def __init__(self, message='Failed to get Speedtest.net servers'):
        super().__init__(message)

class NoConnectionError(Exception):
    '''
    Exception raised when no there is no internet connection
    '''

    def __init__(self, message):
        super().__init__(message)

class SpeedTestError(Exception):
    '''
    Exception raised when it was not possible to get a speed
    '''

    def __init__(self, message):
        super().__init__(message)
