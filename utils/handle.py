import os
import struct
from utils.compress import compress, decompress

HEADER_STRUCT = "!8sIII"
HEADER_SIZE = struct.calcsize(HEADER_STRUCT)
MAGIC_NUMBER = b"ILA_FILE"

def create_ila_file(output_filename, input_files, pre, f0):
    """
    Creates an .ila file by bundling the specified input files and storing metadata.

    Args:
        output_filename (str): The name of the output .ila file.
        input_files (list): A list of file paths to include in the bundle.
        pre (str): The value of the 'pre' metadata.
        f0 (str): The value of the 'f0' metadata.
    """
    with open(output_filename, "wb") as ila_file:
        header = struct.pack(HEADER_STRUCT, MAGIC_NUMBER, len(input_files), len(pre.encode()), len(f0.encode()))
        ila_file.write(header)

        ila_file.write(pre.encode())
        ila_file.write(f0.encode())

        for file_path in input_files:
            file_name = os.path.basename(file_path)
            file_name_len = len(file_name.encode())
            ila_file.write(struct.pack("!Q", file_name_len))
            ila_file.write(file_name.encode())

            with open(file_path, "rb") as f:
                file_data = f.read()
                file_len = len(file_data)
                ila_file.write(struct.pack("!Q", file_len))
                ila_file.write(file_data)
        ila_file.close()

        with open(output_filename, "rb") as f:
            bytes = f.read()
            print(len(bytes))
            bytes = compress(bytes)

        with open(output_filename, "wb") as f:
            f.write(bytes)
            
        print("Compressed file size: ", len(bytes))
    return output_filename

def extract_ila_file(ila_filename, output_dir):
    """
    Extracts files from an .ila file.

    Args:
        ila_filename (str): The path to the .ila file.
        output_dir (str): The directory where extracted files will be saved.
    """
    with open(ila_filename, "rb") as f:
        bytes = f.read()
        temp = bytes
        bytes = decompress(bytes)
    with open(ila_filename, "wb") as f:
        f.write(bytes)
    with open(ila_filename, "rb") as ila_file:
        file_dirs = []
        header = ila_file.read(HEADER_SIZE)
        magic_number, file_count, pre_len, f0_len = struct.unpack(HEADER_STRUCT, header)

        if magic_number != MAGIC_NUMBER:
            raise ValueError("Invalid file format")

        pre = ila_file.read(pre_len).decode()
        f0 = ila_file.read(f0_len).decode()

        for i in range(file_count):
            file_name_len = struct.unpack("!Q", ila_file.read(8))[0]
            file_name = ila_file.read(file_name_len).decode()

            file_len = struct.unpack("!Q", ila_file.read(8))[0]
            file_data = ila_file.read(file_len)

            output_path = os.path.join(output_dir, file_name)
            with open(output_path, "wb") as f:
                f.write(file_data)
            file_dirs.append(output_path)
    with open(ila_filename, "wb") as f:
        f.write(temp)
    return file_dirs, pre, f0
