from utils.handle import create_ila_file, extract_ila_file
import os

input_files = ["test.py"]
output_filename = "checco.ila"
pre = "Ov2Super32k" # example metadata
f0 = "RMVPE" # example metadata

create_ila_file(output_filename, input_files, pre, f0)

#output_dir = "extracted"
#os.makedirs(output_dir, exist_ok=True)
#
#files, pre, f0 = extract_ila_file(output_filename, output_dir)
#for i in range(len(files)):
#    print(f"File {i}: {files[i]}")
#print(f"pre: {pre}")
#print(f"f0: {f0}")

# pre = pretrain
# f0 = f0 method
# input_files = list of files to compress
# output_filename = output file name
