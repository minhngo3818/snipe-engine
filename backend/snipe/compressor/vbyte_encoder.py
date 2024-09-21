def vb_encode(number):
    # Encode a number to a byte array in integer form

    bin_num = bin(number)[2::][::-1]
    byte_block = []
    for i in range(0, len(bin_num), 7):
        block_bstr = format(int(bin_num[i : i + 7], 2), "08b")

        byte_block.append(int(block_bstr, 2))

    byte_block = byte_block[::-1]
    byte_block[0] |= 0b10000000

    return byte_block


def vb_decode(byte_seq):
    # Decode a variable byte sequence

    result = []
    reset_byte = 0b01111111
    number = reset_byte
    i = 0

    for j in range(len(byte_seq)):
        first_bit = byte_seq[j] >> 7

        if first_bit == 1:
            if i < j:
                i = j
                result.append(number)
                number = reset_byte

            number &= byte_seq[j]
        else:
            number <<= 7
            number |= byte_seq[j]

        if j == len(byte_seq) - 1:
            result.append(number)

    return result


def vb_encode_list(num_list, is_group=False):
    # Encode a list of number into a variable byte sequence

    gvb_arr = []

    if not is_group:
        # Encode each number to vbyte
        for num in num_list:
            gvb_arr.extend(vb_encode(num))
    else:
        # Encode a list of number into series of group-4 vbyte
        # Min bytes for group is 5
        #
        # Structure:
        #   |------header--------|----------blocks--------------|
        #   [len1 len2 len3 len4][block1][block2][block3][block4]...

        for i in range(0, len(num_list), 4):
            byte_group = [0]  # first item is byte header

            for number in num_list[i : min(i + 4, len(num_list))]:
                byte_block = vb_encode(number)

                # Shift left by 2 bits to indicate byte size of next number
                if byte_group[0] != 0:
                    byte_group[0] <<= 2

                byte_group[0] |= len(byte_block) - 1
                byte_group.extend(byte_block)

            # Adding remaining empty byte blocks correspond to header
            remains = (i + 4) - len(num_list)
            if 0 < remains < 4:
                for i in range(remains):
                    byte_group.append(0b10000000)

            gvb_arr.extend(byte_group)

    return bytes(gvb_arr)
