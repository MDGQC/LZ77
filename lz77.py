from bitarray import bitarray


class LZ77Algorithm:
    def __init__(self, window_size=200, buffer_size=20):
        self.window_size = window_size
        self.buffer_size = buffer_size

    def compress(self, input_file_path, output_file_path):
        try:
            with open(input_file_path.get(), 'rb') as input_file:
                input_data = input_file.read()
        except IOError:
            raise Exception('Failed to open file')

        current_position = 0
        output = bitarray(endian='big')
        while current_position < len(input_data):
            match = self._find_longest_match(input_data, current_position)
            if match:
                match_distance, match_length = match
                output.append(True)
                output.extend(format(match_distance, '012b'))
                output.extend(format(match_length, '04b'))
                current_position += match_length
            else:
                output.append(False)
                output.extend(format(input_data[current_position], '08b'))
                current_position += 1
        output.fill()

        try:
            with open(output_file_path.get(), 'wb') as output_file:
                output_file.write(output.tobytes())
        except IOError:
            raise Exception('Failed to save file')

    def decompress(self, input_file_path, output_file_path):
        input_data = bitarray(endian='big')
        try:
            with open(input_file_path.get(), 'rb') as input_file:
                input_data.fromfile(input_file)
        except IOError:
            raise Exception('Failed to open file')

        output = []
        while len(input_data) >= 9:
            if input_data.pop(0):
                distance = input_data[0:12]
                length = input_data[12:16]
                del input_data[0:16]
                for i in range(int(length.to01(), 2)):
                    output.append(output[-int(distance.to01(), 2)])
            else:
                byte = input_data[0:8].tobytes()
                output.append(byte)
                del input_data[0:8]
        output_string = ''.join([x.decode('utf-8') for x in output])

        try:
            with open(output_file_path.get(), 'wb') as output_file:
                output_file.write(output_string.encode('utf-8'))
        except IOError:
            raise Exception('Failed to save file')

    def _find_longest_match(self, input_data, current_position):
        buffer_end = min(current_position + self.buffer_size - 1, len(input_data) - 1)
        for i in range(buffer_end + 1, current_position + 1, -1):
            substring = input_data[current_position:i]
            substring_length = len(substring)
            start_position = max(current_position - self.window_size, 0)
            for j in range(start_position, current_position - substring_length + 1):
                if input_data[j:j+substring_length] == substring:
                    return current_position - j, substring_length

