import struct


def doubleToRawLongBits(value):
    """

    :param value: A float value
    :return: The IEEE 754 biit representation of the given double-precision floating-point value.
    """
    return struct.unpack('Q', struct.pack('d', value))[0]


def longBitsToDouble(bits):
    """
    @type  bits: long
    @param bits: the bit pattern in IEEE 754 layout
    @rtype:  float
    @return: the double-precision floating-point value corresponding
             to the given bit pattern C{bits}.
    """
    return struct.unpack('d', struct.pack('Q', bits))[0]


def __HI(x):
    transducer = doubleToRawLongBits(x)
    return int(transducer >> 32)


def __LO(x):
    transducer = doubleToRawLongBits(x)
    return int(transducer)


def __HI2(x, high):
    """
    Return a double with its high-order bits of the second argument
    and the low-order bits of the first argument..
    :param x:
    :param high:
    :return:
    """
    transX = doubleToRawLongBits(x)
    return longBitsToDouble((transX & 0x0000_0000_FFFF_FFFF) | (int(high)) << 32)


def __LO2(x, low):
    """
    Return a double with its low-order bits of the second argument and the high-order bits of the first argument..
    :param x:
    :param low:
    :return:
    """
    transX = doubleToRawLongBits(x)
    return longBitsToDouble((transX & 0x0000_0000_FFFF_FFFF) | (low    & 0x0000_0000_FFFF_FFFF))