import string
import random
import serial
from time import sleep


NUM_KEY_DIGITS      = 32
SERIAL_SPEEDS       = [1, 2, 4, 9, 19, 38, 57, 115, 230, 460, 1000]
SERIAL_SPEEDS_TRUE  = [1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200, 230400, 460800, 1000000]
AIR_SPEEDS          = [12, 56, 64, 100, 125, 200, 250, 500, 750]
ANT_MODES           = [1, 2, 3]
NET_IDS             = list(range(500))
TX_PWRS             = list(range(31))
MIN_FREQS           = list(range(895000, 936000, 1000))
MAX_FREQS           = list(range(895000, 936000, 1000))
NUM_CHANNELS        = list(range(1, 51))
DUTY_CYCLES         = list(range(10, 110, 10))
LBT_RSSIS           = [0, 25, 50, 100, 150, 200, 220]
TARGET_RSSIS        = list(range(50, 256))
HYSTERESIS_RSSIS    = list(range(20, 51))
MAX_WINDOWS         = list(range(33, 132))
RATE_AND_FREQ_BANDS = list(range(4))
ANT_MODES           = list(range(4))
MAVLINK_MODES       = list(range(3))
MAVLINK_MODES_TRUE  = ['Raw Data', 'Mavlink', 'Low Latency']
COMMANDS            = {'+++':       'Enter AT mode',
                       'ATI':       'Shows the radio version',
                       'ATI2':      'Shows the board type',
                       'ATI3':      'Shows board frequency',
                       'ATI4':      'Shows board version',
                       'ATI5':      'Shows all user settable EEPROM parameters and their values',
                       'ATI5?':     'Shows all user settable EEPROM parameters and their possible range',
                       'ATI6':      'Displays TDM timing report',
                       'ATI7':      'Displays RSSI signal report',
                       'ATI8':      'Display Device 64 bit unique ID',
                       'ATI9':      'Display node ID [multipoint only]',
                       'ATO':       'Exits AT command mode',
                       'AT{n}?':    'Displays radio parameter number ‘n’',
                       'AT{n}={X}': 'Sets radio parameter number ‘n’ to ‘X’',
                       'ATZ':       'Reboots the radio',
                       'AT&W':      'Writes current parameters to EEPROM',
                       'AT&F':      'Resets all parameters to factory defaults',
                       'AT&T=RSSI': 'Enables RSSI debugging report',
                       'AT&T=TDM':  'Enables TDM debugging report',
                       'AT&UPDATE': 'Reset and enter boot mode',
                       'AT&T':      'Disables debugging report'}


def gen_key(num_digits=NUM_KEY_DIGITS):
    return ''.join([string.hexdigits[random.randint(0, len(string.hexdigits) - 1)].upper() for num in range(num_digits)])


class RFDConfig(object):
    def __init__(self):
        self.port = serial.Serial()
        self.port.timeout = 2
        self.params = {'radioVersion':    {'id':              'I',
                                           'description':     'Radio version',
                                           'curVal':          None,
                                           'desVal':          None,
                                           'curValRemote':    None,
                                           'desValRemote':    None,
                                           'sameOnAllModems': False},
                       'boardType':       {'id':              'I2',
                                           'description':     'Board type',
                                           'curVal':          None,
                                           'desVal':          None,
                                           'curValRemote':    None,
                                           'desValRemote':    None,
                                           'sameOnAllModems': False},
                       'boardFreq':       {'id':              'I3',
                                           'description':     'Board frequency',
                                           'curVal':          None,
                                           'desVal':          None,
                                           'curValRemote':    None,
                                           'desValRemote':    None,
                                           'sameOnAllModems': False},
                       'boardVersion':    {'id':              'I4',
                                           'description':     'Board version',
                                           'curVal':          None,
                                           'desVal':          None,
                                           'curValRemote':    None,
                                           'desValRemote':    None,
                                           'sameOnAllModems': False},
                       'tdmTimingReport': {'id':              'I6',
                                           'description':     'TDM Timing Report',
                                           'curVal':          None,
                                           'desVal':          None,
                                           'curValRemote':    None,
                                           'desValRemote':    None,
                                           'sameOnAllModems': False},
                       'rssiSignalReport':{'id':              'I7',
                                           'description':     'RSSI signal report',
                                           'curVal':          None,
                                           'desVal':          None,
                                           'curValRemote':    None,
                                           'desValRemote':    None,
                                           'sameOnAllModems': False},
                       'deviceUniqueID':  {'id':              'I8',
                                           'description':     'Device 64 bit unique ID',
                                           'curVal':          None,
                                           'desVal':          None,
                                           'curValRemote':    None,
                                           'desValRemote':    None,
                                           'sameOnAllModems': False},
                       'nodeID':          {'id':              'I9',
                                           'description':     'node ID [multipoint only]',
                                           'curVal':          None,
                                           'desVal':          None,
                                           'curValRemote':    None,
                                           'desValRemote':    None,
                                           'sameOnAllModems': False},
                       'FORMAT':          {'id':              'S0',
                                           'description':     'This is for EEPROM version, it should not be changed. It is set by the firmware',
                                           'curVal':          None,
                                           'desVal':          None,
                                           'curValRemote':    None,
                                           'desValRemote':    None,
                                           'sameOnAllModems': False},
                       'SERIAL_SPEED':    {'id':              'S1',
                                           'description':     'Serial speed in ‘one byte form’. Accepted values are 1, 2, 4, 9, 19, 38, 57, 115, 230, 460 and 1000 corresponding to 1200bps, 2400bps, 4800bps, 9600bps, 19200bps, 38400bps, 57600bps, 115200bps, 230400bps, 460800bps and 1000000bps respectively',
                                           'curVal':          None,
                                           'desVal':          None,
                                           'curValRemote':    None,
                                           'desValRemote':    None,
                                           'sameOnAllModems': False},
                       'AIR_SPEED':       {'id':              'S2',
                                           'description':     'Air data rate in ‘one byte form’. Accepted values are 12, 56, 64, 100, 125, 200, 250, 500 and 750 corresponding to 12000bps, 56000bps, 64000bps, 100000bps, 125000bps, 200000bps, 250000bps, 500000bps and 750000bps respectively',
                                           'curVal':          None,
                                           'desVal':          None,
                                           'curValRemote':    None,
                                           'desValRemote':    None,
                                           'sameOnAllModems': True},
                       'NETID':           {'id':              'S3',
                                           'description':     'Network ID. The same on both modems in the pair',
                                           'curVal':          None,
                                           'desVal':          None,
                                           'curValRemote':    None,
                                           'desValRemote':    None,
                                           'sameOnAllModems': True},
                       'TXPOWER':         {'id':              'S4',
                                           'description':     'Transmit power in dBm. Maximum is 30dBm',
                                           'curVal':          None,
                                           'desVal':          None,
                                           'curValRemote':    None,
                                           'desValRemote':    None,
                                           'sameOnAllModems': False},
                       'ECC':             {'id':              'S5',
                                           'description':     'Enables or disables the Golay error correcting code. When enabled, it doubles the over the air data usage',
                                           'curVal':          None,
                                           'desVal':          None,
                                           'curValRemote':    None,
                                           'desValRemote':    None,
                                           'sameOnAllModems': True},
                       'MAVLINK':         {'id':              'S6',
                                           'description':     'Enables or disables the MAVLink framing and reporting',
                                           'curVal':          None,
                                           'desVal':          None,
                                           'curValRemote':    None,
                                           'desValRemote':    None,
                                           'sameOnAllModems': False},
                       'OPPRESEND':       {'id':              'S7',
                                           'description':     'Opportunistic resend allows the node to resend packets if it has spare bandwidth',
                                           'curVal':          None,
                                           'desVal':          None,
                                           'curValRemote':    None,
                                           'desValRemote':    None,
                                           'sameOnAllModems': False},
                       'MIN_FREQ':        {'id':              'S8',
                                           'description':     'Min freq in KHz',
                                           'curVal':          None,
                                           'desVal':          None,
                                           'curValRemote':    None,
                                           'desValRemote':    None,
                                           'sameOnAllModems': True},
                       'MAX_FREQ':        {'id':              'S9',
                                           'description':     'Max freq in KHz',
                                           'curVal':          None,
                                           'desVal':          None,
                                           'curValRemote':    None,
                                           'desValRemote':    None,
                                           'sameOnAllModems': True},
                       'NUM_CHANNELS':    {'id':              'S10',
                                           'description':     'Number of frequency hopping channels',
                                           'curVal':          None,
                                           'desVal':          None,
                                           'curValRemote':    None,
                                           'desValRemote':    None,
                                           'sameOnAllModems': True},
                       'DUTY_CYCLE':      {'id':              'S11',
                                           'description':     'The percentage of time to allow transmit',
                                           'curVal':          None,
                                           'desVal':          None,
                                           'curValRemote':    None,
                                           'desValRemote':    None,
                                           'sameOnAllModems': False},
                       'LBT_RSSI':        {'id':              'S12',
                                           'description':     'Listen before talk threshold (This parameter shouldn’t be changed)',
                                           'curVal':          None,
                                           'desVal':          None,
                                           'curValRemote':    None,
                                           'desValRemote':    None,
                                           'sameOnAllModems': True},
                       'MANCHESTER':      {'id':              'S13',
                                           'description':     'Manchester encoding (This parameter shouldn’t be changed)',
                                           'curVal':          None,
                                           'desVal':          None,
                                           'curValRemote':    None,
                                           'desValRemote':    None,
                                           'sameOnAllModems': False},
                       'RTSCTS':          {'id':              'S14',
                                           'description':     'Ready-to-send and Clear-to-send flow control',
                                           'curVal':          None,
                                           'desVal':          None,
                                           'curValRemote':    None,
                                           'desValRemote':    None,
                                           'sameOnAllModems': False},
                       'MAX_WINDOW':      {'id':              'S15',
                                           'description':     'Max transit window size used to limit max time/latency if required otherwise will be set automatically',
                                           'curVal':          None,
                                           'desVal':          None,
                                           'curValRemote':    None,
                                           'desValRemote':    None,
                                           'sameOnAllModems': False},
                       'ENCRYPTION_LEVEL':{'id':              'S16',
                                           'description':     'Encryption level 0=off, 1=128bit AES',
                                           'curVal':          None,
                                           'desVal':          None,
                                           'curValRemote':    None,
                                           'desValRemote':    None,
                                           'sameOnAllModems': True},
                       'GPI1_1R/CIN':     {'id':              'S16',
                                           'description':     'Set GPIO 1.1 (pin 15) as R/C(PPM) input',
                                           'curVal':          None,
                                           'desVal':          None,
                                           'curValRemote':    None,
                                           'desValRemote':    None,
                                           'sameOnAllModems': False},
                       'GPO1_1R/COUT':    {'id':              'S17',
                                           'description':     'Set GPIO 1.1 (pin 15) as R/C(PPM) output',
                                           'curVal':          None,
                                           'desVal':          None,
                                           'curValRemote':    None,
                                           'desValRemote':    None,
                                           'sameOnAllModems': False},
                       'GPO1_1SBUSIN':    {'id':              'S18',
                                           'description':     'Set GPIO 1.1 (pin 12) as SBUS input',
                                           'curVal':          None,
                                           'desVal':          None,
                                           'curValRemote':    None,
                                           'desValRemote':    None,
                                           'sameOnAllModems': False},
                       'GPO1_1SBUSOUT':    {'id':             'S19',
                                           'description':     'Set GPIO 1.1 (pin 12) as SBUS output',
                                           'curVal':          None,
                                           'desVal':          None,
                                           'curValRemote':    None,
                                           'desValRemote':    None,
                                           'sameOnAllModems': False},
                       'ANT_MODE':        {'id':              'S20',
                                           'description':     '0= Diversity, 1= Antenna 1 only, 2= Antenna 2 only, 3= Antenna 1 TX and antenna 2 RX',
                                           'curVal':          None,
                                           'desVal':          None,
                                           'curValRemote':    None,
                                           'desValRemote':    None,
                                           'sameOnAllModems': False},
                       'GPO1_3STATLED ':  {'id':              'S21',
                                           'description':     'Set GPIO 1.1 (pin 12) as output with state that mirrors the status LED on the modem',
                                           'curVal':          None,
                                           'desVal':          None,
                                           'curValRemote':    None,
                                           'desValRemote':    None,
                                           'sameOnAllModems': False},
                       'GPO1_0TXEN485':   {'id':              'S22',
                                           'description':     'Set GPIO 1.0 (pin 13) as control signal on DINIO and RS485 interface boards.',
                                           'curVal':          None,
                                           'desVal':          None,
                                           'curValRemote':    None,
                                           'desValRemote':    None,
                                           'sameOnAllModems': False},
                       'RATE/FREQBAND':   {'id':              'S23',
                                           'description':     'Changes the frequencies bands and airspeeds within set ranges on compliant modems ensuring compliance is maintained',
                                           'curVal':          None,
                                           'desVal':          None,
                                           'curValRemote':    None,
                                           'desValRemote':    None,
                                           'sameOnAllModems': True},
                       'TARGET_RSSI':     {'id':              'R0',
                                           'description':     'Optimal RSSI value to try to sustain (off = 255)',
                                           'curVal':          None,
                                           'desVal':          None,
                                           'curValRemote':    None,
                                           'desValRemote':    None,
                                           'sameOnAllModems': False},
                       'HYSTERESIS_RSSI': {'id':              'R1',
                                           'description':     'Amount of change before power levels altered',
                                           'curVal':          None,
                                           'desVal':          None,
                                           'curValRemote':    None,
                                           'desValRemote':    None,
                                           'sameOnAllModems': False},
                       'EncryptionKey':   {'id':              '&E',
                                           'description':     'AES encryption key',
                                           'curVal':          None,
                                           'desVal':          None,
                                           'curValRemote':    None,
                                           'desValRemote':    None,
                                           'sameOnAllModems': True},
                       'Print':           {'id':              'PP',
                                           'description':     'Print all Pin Settings',
                                           'curVal':          None,
                                           'desVal':          None,
                                           'curValRemote':    None,
                                           'desValRemote':    None,
                                           'sameOnAllModems': False},
                       'Input':           {'id':              'PI={x}',
                                           'description':     'Set Pin x to Input',
                                           'curVal':          None,
                                           'desVal':          None,
                                           'curValRemote':    None,
                                           'desValRemote':    None,
                                           'sameOnAllModems': False},
                       'Read':            {'id':              'PR={x}',
                                           'description':     'Read Pin X value (When set to input)',
                                           'curVal':          None,
                                           'desVal':          None,
                                           'curValRemote':    None,
                                           'desValRemote':    None,
                                           'sameOnAllModems': False},
                       'Output':          {'id':              'PO={x}',
                                           'description':     'Set Pin x to Output (Default) can only be controlled by ATPC',
                                           'curVal':          None,
                                           'desVal':          None,
                                           'curValRemote':    None,
                                           'desValRemote':    None,
                                           'sameOnAllModems': False},
                       'ControlOn':       {'id':              'PC={x},1',
                                           'description':     'Turn pin x on -­‐ Output Mode / Set internal pull up resistor -­‐ Input Mode',
                                           'curValRemote':    None,
                                           'desValRemote':    None,
                                           'sameOnAllModems': False},
                       'ControlOff':      {'id':              'PC={x},0',
                                           'description':     'Turn pin x off -­‐ Output Mode / Set internal pull down resistor -­‐ Input Mode',
                                           'curVal':          None,
                                           'desVal':          None,
                                           'curValRemote':    None,
                                           'desValRemote':    None,
                                           'sameOnAllModems': False}}
    
    def send(self, command, wait=0.25):
        '''
        TODO
        '''
        
        if self.port.isOpen():
            if not command == '+++':
                command += '\r'
            
            self.port.write(command.encode())
            
            if command == '+++':
                sleep(1)
            else:
                sleep(wait)
    
    def send_and_rec(self, command, wait=0.25):
        '''
        TODO
        '''
        
        if self.port.isOpen():
            self.send(command, wait)
            
            try:
                return self.port.read_all().decode('utf-8')
            except UnicodeDecodeError:
                return None
        return None
    
    def responseGood(self, response):
        '''
        TODO
        '''
        
        if len(response.split()) >= 2:
            if (not response.split()[1].upper() == 'ERROR') and (not '?' in response):
                return True
        return False
    
    def flush(self):
        '''
        TODO
        '''
        
        if self.port.isOpen():
            self.port.read_all()
    
    def in_AT(self):
        '''
        TODO
        '''
        
        if self.port.isOpen():
            try:
                self.flush()
                response = self.send_and_rec('+++').strip().upper()
                
                if response == 'OK' or response == '+++':
                    return True
            except AttributeError:
                return False
        return False
    
    def autobaud(self):
        '''
        TODO
        '''
        
        for baud in reversed(serial.Serial.BAUDRATES):
            if self.port.isOpen():
                self.port.close()
            
            try:
                self.port.baudrate = baud
                self.port.open()
                
            except:
                import traceback
                traceback.print_exc()
                
                return False
            
            if self.in_AT():
                return True
        return False
    
    def open(self, port, baud=57600):
        '''
        TODO
        '''
        
        if not self.port.isOpen() or not self.port.baudrate == baud:
            try:
                self.port.port     = port
                self.port.baudrate = baud
                self.port.open()
                
            except:
                import traceback
                traceback.print_exc()
                
                return False
        
        if self.in_AT():
            return True
        
        return self.autobaud()
    
    def close(self, local=True):
        '''
        TODO
        '''
        
        if local:
            if self.port.isOpen():
                self.send('ATO')
                self.port.close()
        else:
            self.send('RTO')
    
    def loadParam(self, param, local=True):
        '''
        TODO
        '''
        
        if self.port.isOpen():
            if param in self.params.keys():
                if '=' in self.params[param]['id']:
                    return False
                
                if 'I' not in self.params[param]['id']:
                    if local:
                        response = self.send_and_rec('AT{}?'.format(self.params[param]['id']))
                    else:
                        response = self.send_and_rec('RT{}?'.format(self.params[param]['id']))
                else:
                    if local:
                        response = self.send_and_rec('AT{}'.format(self.params[param]['id']))
                    else:
                        response = self.send_and_rec('RT{}'.format(self.params[param]['id']))
                
                if len(response.split('\r\n')) >= 2:
                    response = response.split('\r\n')[1:-1]
                    response = '\n'.join(response)
                    
                    if 'ERROR' in response.upper():
                        if local:
                            self.params[param]['curVal'] = None
                        else:
                            self.params[param]['curValRemote'] = None
                    else:
                        try:
                            if local:
                                self.params[param]['curVal'] = int(response)
                            else:
                                self.params[param]['curValRemote'] = int(response)
                        except ValueError:
                            if local:
                                self.params[param]['curVal'] = response
                            else:
                                self.params[param]['curValRemote'] = response
                        return True
        return False
    
    def loadAll(self, local=True):
        '''
        TODO
        '''
        
        if self.port.isOpen():
            for param in self.params.keys():
                self.loadParam(param, local)
    
    def writeOutParam(self, param, local=True):
        '''
        TODO
        '''
        
        if self.port.isOpen():
            if param in self.params.keys():
                if ('S' in self.params[param]['id']) and self.params[param]['desVal']:
                    if local:
                        response = self.send_and_rec('AT{n}={X}'.format(n=self.params[param]['id'], X=self.params[param]['desVal']))
                    else:
                        response = self.send_and_rec('RT{n}={X}'.format(n=self.params[param]['id'], X=self.params[param]['desValRemote']))
                    return self.responseGood(response)
        return False

    def writeOutAll(self, local=True):
        '''
        TODO
        '''
        
        if self.port.isOpen():
            for param in self.params.keys():
                if 'S' in self.params[param]['id']:
                    self.writeOutParam(param, local)
                    sleep(0.1)
    
    def hasRemote(self):
        '''
        TODO
        '''
        
        return self.responseGood(self.send_and_rec('RTI5'))
    
    def enableRSSI(self):
        '''
        TODO
        '''
        
        if self.port.isOpen():
            self.send('AT&T=RSSI')
    
    def enabletDM(self):
        '''
        TODO
        '''
        
        if self.port.isOpen():
            self.send('AT&T=TDM')
    
    def disableDebug(self):
        '''
        TODO
        '''
        
        if self.port.isOpen():
            self.send('AT&T')
    
    def factoryDefaults(self):
        '''
        TODO
        '''
        
        if self.port.isOpen():
            self.send('AT&F')
    
    def reset(self):
        '''
        TODO
        '''
        
        if self.port.isOpen():
            self.send('ATZ')
    
    def save(self, local=True):
        '''
        TODO
        '''
        
        if self.port.isOpen():
            if local:
                self.send('AT&W')
                self.reset()
                self.reset()
                self.send('ATO')
            else:
                self.send('RT&W')
                self.reset()
                self.reset()
                self.send('RTO')
            sleep(1)
            self.open(self.port.port, self.port.baudrate)


if __name__ == '__main__':
    import pprint
    
    rfd = RFDConfig()
    rfd.open('COM9', 115200)
    
    rfd.loadAll()
    pprint.pprint(rfd.params)
    
    rfd.close()
