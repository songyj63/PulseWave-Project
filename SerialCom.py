import serial
from PacketRead import PacketRead

class SerialCom:

    def __init__(self, ComName):
        self.ComName = ComName

        self.ser = serial.Serial(
            port=self.ComName,
            baudrate=9600,
            bytesize=serial.EIGHTBITS,
            stopbits=serial.STOPBITS_ONE,
            parity=serial.PARITY_NONE,
        )

        print(ComName + " is connecting")

    def read_data(self):

        pkData = PacketRead()

        while True:
            data = self.ser.read(1)
            if(pkData.parsing_LXSDFT2(data)):
                # print(int.from_bytes(self.PacketStreamData[0], byteorder='little')*256 + int.from_bytes(self.PacketStreamData[1], byteorder='little'))
                # if(int.from_bytes(pkData.PacketCount, byteorder='little') == 2):
                #     print(int.from_bytes(pkData.PacketCyclicData, byteorder='little'))
                print(int.from_bytes(pkData.PUD1, byteorder='little') * 256 + int.from_bytes(
                    pkData.PUD0, byteorder='little'))

