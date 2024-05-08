import struct

def compress(input_data):
    compressed = bytearray()
    dictionary = {bytes([b]): i for i, b in enumerate(range(256))}
    phrase = bytes()
    for byte in input_data:
        byte = bytes([byte])
        new_phrase = phrase + byte
        if new_phrase in dictionary:
            phrase = new_phrase
        else:
            compressed.extend(struct.pack('B', dictionary[phrase] >> 8))
            compressed.extend(struct.pack('B', dictionary[phrase] & 0xFF))
            if len(dictionary) < 2 ** 16:
                dictionary[new_phrase] = len(dictionary)
            phrase = byte
    if phrase:
        compressed.extend(struct.pack('B', dictionary[phrase] >> 8))
        compressed.extend(struct.pack('B', dictionary[phrase] & 0xFF))
    return bytes(compressed)

def decompress(compressed_data):
    decompressed = bytearray()
    dictionary = {i: bytes([i]) for i in range(256)}
    next_entry = len(dictionary)
    phrase = bytes()
    i = 0
    while i < len(compressed_data):
        code = struct.unpack('>H', compressed_data[i:i+2])[0]
        i += 2
        if code in dictionary:
            entry = dictionary[code]
        else:
            entry = phrase + bytes([phrase[0]])
        decompressed.extend(entry)
        if phrase:
            dictionary[next_entry] = phrase + bytes([entry[0]])
            next_entry += 1
        phrase = entry
    return bytes(decompressed)
