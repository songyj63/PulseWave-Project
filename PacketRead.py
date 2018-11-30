
class PacketRead:

    def __init__(self):
        # init values
        self.Sync_After = False
        self.Packet_TX_Index = 0
        self.Data_Prev = bytes(0)  # 직전값.
        self.CRD_PUD2_PCDT = bytes(0)
        self.PUD0 = bytes(0)
        self.PUD1 = bytes(0)
        self.PacketCount = bytes(0)
        self.PacketCyclicData = bytes(0)
        self.PacketStreamData = [None] * 2

    def parsing_LXSDFT2(self, data_crnt):
        retv = 0

        if (self.Data_Prev == b'\xff' and data_crnt == b'\xfe'):   # 싱크지점 찾았다.
            self.Sync_After = True
            self.Packet_TX_Index = 0    # 패킷 TX인덱스 0으로 초기화

        self.Data_Prev = data_crnt  # 현재 값을 직전 값으로 받아둔다.

        if(self.Sync_After == True):    # 싱크가 발견된 이후에만 실행된다.
            self.Packet_TX_Index = self.Packet_TX_Index+1   # TX인덱스 1증가. 254가 발견된 지점이 1이다. 시리얼로 1바이트 수신될때마다 1씩 증가하는것.

            if(self.Packet_TX_Index > 1):   # TX인덱스 2이상만 수행된다.

                if(self.Packet_TX_Index == 2):  # TX인덱스2 PUD0 확보.
                    self.PUD0 = data_crnt
                elif(self.Packet_TX_Index == 3):    # TX인덱스3 CRD, PUD2, PCD Type 확보
                    self.CRD_PUD2_PCDT = data_crnt
                elif(self.Packet_TX_Index == 4):    # TX인덱스4 PC 확보
                    self.PacketCount = data_crnt
                elif(self.Packet_TX_Index == 5):    # TX인덱스5 PUD1 확보
                    self.PUD1 = data_crnt
                elif(self.Packet_TX_Index == 6):    # TX인덱스6 PCD(패킷순환데이터) 확보
                    self.PacketCyclicData = data_crnt
                elif(self.Packet_TX_Index > 6):     # TX인덱스 7 이상에는 스트림데이터(파형 데이터) 1바이트씩 순차적으로 들어온다. 데이터 수신되는 순서 -> 채널1의 상위바이트, 하위 바이트, 채널2의 상위바이트 하위바이트 .. 순서로 기록되어있다.
                    psd_idx = self.Packet_TX_Index - 7  # PacketStreamData배열의 인덱스
                    self.PacketStreamData[psd_idx] = data_crnt      # crnt_data를 순차적으로 확보하여 스트림데이터만 확보한다.

                    if(self.Packet_TX_Index == (1 * 2 * 1 + 6)):  # 채널수 x 2(2바이트 점유) x 샘플링 수량 + 6(파형데이터 구간 앞부분까지의 인덱스값) 까지가 1패킷의 끝이다.
                        self.Sync_After = False     # 싱크지점 다시 검색되도록 false로 해둔다.
                        retv = 1                     # 1패킷 단위의 파싱이 완료되면 리턴한다

        return retv