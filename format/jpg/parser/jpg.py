import os

def bytes_to_int(bytes):
    result = ord(bytes[0])
    for b in bytes[1:]:
        result = result + ord(b) * 256
    return result

def int_to_bytes(value, length):
    result = []
    for i in range(0, length):
        result.append(value >> (i * 8) & 0xff)
    return result

class JPG():
    def __init__(self):
        self.marker = {
            b"\xff\xc4": "DHT",
            b"\xff\xdb": "DQT",
            b"\xff\xdd": "DRI",
            b"\xff\xda": "SOS",
            b"\xff\xd9": "EOI",
            b"\xff\xe0": "APP0",
            b"\xff\xe1": "APP1",
            b"\xff\xe2": "APP2",
            b"\xff\xed": "APP13",
            b"\xff\xfe": "COM",
            b"\xff\xc0": "SOF0", # start of frame 0, baseline DCT
            b"\xff\xc1": "SOF1", # start of frame 1, extended sequential DCT, Huffman coding
            b"\xff\xc2": "SOF2", # start of frame 2, progressive DCT, Huffman coding
            b"\xff\xc3": "SOF3", # start of frame 3, lossless sequential, Huffman coding
            b"\xff\xc5": "SOF5", # start of frame 5, differential sequential DCT, Huffman coding
            b"\xff\xc6": "SOF6", # start of frame 6, differential progressive DCT, Huffman coding
            b"\xff\xc7": "SOF7", # start of frame 7, differential lossless, Huffman coding
            b"\xff\xc9": "SOF9", # start of frame 9, extended sequential DCT, arithmetic coding
            b"\xff\xca": "SOF10", # start of frame 10, progressive DCT, arithmetic coding
            b"\xff\xcb": "SOF11", # start of frame 11, lossless sequential, arithmetic coding
            b"\xff\xcd": "SOF13", # start of frame 13, differential sequential DCT, arithmetic coding
            b"\xff\xce": "SOF14", # start of frame 14, progressive DCT, arithmetic coding
            b"\xff\xcf": "SOF15", # start of frame 15, differential lossless, arithmetic coding
        }

    def load_jpg_from_file(self, file_path):
        with open(file_path, "rb") as jpg_file:
            self.jpg_data = jpg_file.read()
        self.jpg_file = open(file_path, "rb")

    def print_jpg_data(self):
        for byte in self.jpg_data:
            print "{:02x}".format(ord(byte)),
    
    def is_jpg(self):
        if self.jpg_data[0:2] == b"\xff\xd8":
            return True
        else:
            return False
    
    def get_segment_length(self, bin):
        return bytes_to_int(bin) - 2

    def get_next_segment(self):
        if self.jpg_file.tell() == 0:
            self.jpg_file.seek(0)
            self.jpg_file.read(2)
        elif self.jpg_file.tell() == os.fstat(self.jpg_file.fileno()).st_size:
            return None
        marker_name = self.marker[self.jpg_file.read(2)]
        if marker_name != "SOS":
            segment_length = self.get_segment_length(self.jpg_file.read(2))
            segment_body = self.jpg_file.read(segment_length)
            return {"marker_name": marker_name, "segment_length": segment_length, "segment_body": segment_body}
        return None
