import struct


class Data:
    def __init__(self, binary_data):
        self.format_str = '<ciiidddddddddddd'

        self.expected_size = struct.calcsize(self.format_str)

        if len(binary_data) != self.expected_size:
            raise ValueError(f"Invalid binary data size, expected {self.expected_size} bytes, was {len(binary_data)}")

        values = struct.unpack(self.format_str, binary_data)

        self.sensorID = values[0]
        self.xCo = values[1]
        self.yCo = values[2]
        self.zCo = values[3]
        self.sensVect = values[4]
        self.Fg = values[5]
        self.s2 = values[6]
        self.s3 = values[7]
        self.s4 = values[8]
        self.s5 = values[9]
        self.s6 = values[10]
        self.s7 = values[11]
        self.s8 = values[12]
        self.s9 = values[13]
        self.s10 = values[14]

    def printOneOfEachType(self):
        print(f"SensorID {self.sensorID}, xCo {self.xCo}, s2 {self.s2}")
