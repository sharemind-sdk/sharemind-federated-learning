import struct
import sys


class IncompleteInput(Exception):
    pass


def parseArguments(
        inFile=sys.stdin,
        sizeTypeFormat='Q',
        sizeTypeSize=8,
        encoding='utf-8'):

    def readBlock(size):
        buf = inFile.buffer.read(size) if hasattr(inFile, 'buffer') else inFile.read(size)
        if len(buf) != size:
            raise IncompleteInput()
        return buf

    def readString(size):
        return readBlock(size).decode(encoding)

    def parseData(typeName, data):
        if typeName == 'bool':
            return list(struct.unpack('%s?' % len(data), data))
        elif typeName == 'float32':
            return list(struct.unpack('%sf' % (len(data) // 4), data))
        elif typeName == 'float64':
            return list(struct.unpack('%sd' % (len(data) // 8), data))
        elif typeName == 'int8':
            return list(struct.unpack('%sb' % len(data), data))
        elif typeName == 'int16':
            return list(struct.unpack('%sh' % (len(data) // 2), data))
        elif typeName == 'int32':
            return list(struct.unpack('%sl' % (len(data) // 4), data))
        elif typeName == 'int64':
            return list(struct.unpack('%sq' % (len(data) // 8), data))
        elif typeName == 'uint8':
            return list(struct.unpack('%sB' % len(data), data))
        elif typeName == 'uint16':
            return list(struct.unpack('%sH' % (len(data) // 2), data))
        elif typeName == 'uint32':
            return list(struct.unpack('%sL' % (len(data) // 4), data))
        elif typeName == 'uint64':
            return list(struct.unpack('%sQ' % (len(data) // 8), data))
        elif typeName == 'string':
            return data.decode(encoding)
        else:
            return data

    args = {}

    try:
        while True:
            argNameSize = struct.unpack(sizeTypeFormat, readBlock(sizeTypeSize))[0]
            argName = readString(argNameSize)
            pdNameSize = struct.unpack(sizeTypeFormat, readBlock(sizeTypeSize))[0]
            pdName = readString(pdNameSize)
            typeNameSize = struct.unpack(sizeTypeFormat, readBlock(sizeTypeSize))[0]
            typeName = readString(typeNameSize)
            argDataSize = struct.unpack(sizeTypeFormat, readBlock(sizeTypeSize))[0]
            argData = parseData(typeName, readBlock(argDataSize))
            args[argName] = argData
    except IncompleteInput:
        pass

    return args


if __name__ == "__main__":
    with open(sys.argv[1], 'r') as file:
        args = parseArguments(inFile=file)
    for arg, val in args.items():
        print(f"name: {arg}, value: {str(val).replace('[', '{').replace(']', '}')}")
