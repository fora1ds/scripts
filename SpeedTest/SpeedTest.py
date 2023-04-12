'''
This program allows you to measure the speed of the incoming and outgoing speed of your Internet connection.

Author: Fora1ds
Version: 1.0.0
'''

from urllib.request import Request, urlopen
from urllib.parse import urlparse
from Exceptions import *
from json import loads
from time import time

SERVERS_URL = 'https://www.speedtest.net/api/js/servers'
DOWNLOAD_URL = '/download?size=25000000'
UPLOAD_URL = '/upload'

class Format:
    def __init__(self, round_byte=True, units=True, digits=3):
        self.Round = round_byte
        self.Units = units
        self.Digits = digits

    def set_type(self, byte_value, units) -> [float, str]:
        '''
        Set a new byte type:

        1. 4836849.75 -> 38.694 Mbps
        2. 4836849.75 -> 38.694
        3. 4836849.75 -> 39
        '''

        Value = byte_value

        if self.Round == True:
            Value = round(Value, self.Digits)

        if self.Units == True:
            Value = '{} {}'.format(Value, units)

        return Value

    def to_Bps(self, value) -> [float, str]:
        '''
        Convert bytes to Bps
        '''

        return self.set_type(byte_value=value / 0.125, units='Bps')

    def to_Kbps(self, value) -> [float, str]:
        '''
        Convert bytes to Kbps
        '''

        return self.set_type(byte_value=value / 125, units='Kbps')

    def to_Mbps(self, value) -> [float, str]:
        '''
        Convert bytes to Mbps
        '''

        return self.set_type(byte_value=value / 125000, units='Mbps')

    def to_Gbps(self, value) -> [float, str]:
        '''
         Convert bytes to Gbps
        '''

        return self.set_type(byte_value=value / 125000000, units='Gbps')

    def to_Tbps(self, value) -> [float, str]:
        '''
        Convert bytes to Tbps
        '''

        return self.set_type(byte_value=value / 125000000000, units='Tbps')

class SpeedTest:
    def __init__(self):
        # Standard Ookla packet size
        self.PACKET_SIZE = 25000000

        self.select_server(number=0)

    def _request(self, url, content=None, url_method='GET') -> bytes:
        '''
        Sending a request with headers, data and method
        '''

        Url = Request(url, data=content,
            headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0',
                     'Accept': 'application/json, text/plain, */*',
                     'Accept-Language': 'en-US,en;q=0.5'}, method=url_method)

        try:
            URL_Request = urlopen(Url).read()
        except :
            raise NoConnectionError(message='Failed to connect to {}'.format(urlparse(url).netloc))

        return URL_Request

    def servers(self) -> list:
        '''
        Get Ookla servers
        '''

        Servers = loads(self._request(url=SERVERS_URL))

        if not Servers:
            raise SpeedTestServersError(message='No Servers Found')

        return Servers

    def select_server(self, number) -> None:
        '''
        Based on the server name, upload and download URLs are generated
        '''

        Server = self.servers()[number]
        Name = Server.get('host')

        self.DOWNLOAD = 'https://{}{}'.format(Name, DOWNLOAD_URL)
        self.UPLOAD = 'https://{}{}'.format(Name, UPLOAD_URL)

    def _get_speed(self, speed) -> float:
        '''
        Each speed is calculated according to the formula:

        Speed = PACKET_SIZE
                -----------
                T2   -   T1
        '''

        Start = time()

        try:
            if speed == 'DOWNLOAD':
                self._request(url=self.DOWNLOAD)
            else:
                self._request(url=self.UPLOAD, content=b'Q' * self.PACKET_SIZE, url_method='POST')
        except :
            raise SpeedTestError(message='Failed to get {} speed'.format(speed.lower()))

        Done = time()

        Result = self.PACKET_SIZE / (Done - Start)

        return Result

    def download(self) -> float:
        '''
        Get download speed
        '''

        return self._get_speed(speed='DOWNLOAD')

    def upload(self) -> float:
        '''
        Get upload speed
        '''

        return self._get_speed(speed='UPLOAD')
