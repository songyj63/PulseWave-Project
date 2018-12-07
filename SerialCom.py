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

        self.X = 0
        self.heartRateY = 0
        self.hrvY = 0

        print(ComName + " is connecting")

    def read_data(self):

        pkData = PacketRead()

        while True:
            data = self.ser.read(1)
            if(pkData.parsing_LXSDFT2(data)):
                # print(int.from_bytes(pkData.PacketStreamData[0], byteorder='little')*256 + int.from_bytes(pkData.PacketStreamData[1], byteorder='little'))
                # if(int.from_bytes(pkData.PacketCount, byteorder='little') == 2):
                #     print(int.from_bytes(pkData.PacketCyclicData, byteorder='little'))
                # print(int.from_bytes(pkData.PUD1, byteorder='little') * 256 + int.from_bytes(
                #     pkData.PUD0, byteorder='little'))

                self.X = (self.X + 1)%(256*10)

                self.heartRateY = int.from_bytes(pkData.PacketStreamData[0], byteorder='little')*256 + int.from_bytes(pkData.PacketStreamData[1], byteorder='little')
                # self.hrvY = int.from_bytes(pkData.PUD1, byteorder='little') * 256 + int.from_bytes(pkData.PUD0, byteorder='little')


