import struct
import os
import argparse

def extract_disk_file(disk_file_path, output_dir):
    with open(disk_file_path, 'rb') as disk_file:
        # Read the number of files
        file_count_data = disk_file.read(4)
        if len(file_count_data) < 4:
            raise ValueError("Invalid disk file header")
        
        file_count = struct.unpack('>I', file_count_data)[0]
        
        # Read the directory entries
        directory_entries = []
        for _ in range(file_count):
            entry_data = disk_file.read(72)
            if len(entry_data) < 72:
                raise ValueError("Invalid directory entry")
            
            file_name = entry_data[:64].decode('latin-1').rstrip('\x00')
            offset, size = struct.unpack('>II', entry_data[64:])
            directory_entries.append((file_name, offset, size))
        
        # Skip the total size of all contained files
        total_size_data = disk_file.read(4)
        if len(total_size_data) < 4:
            raise ValueError("Invalid total size field")
        
        # Extract each file
        for file_name, offset, size in directory_entries:
            # Seek to the file data offset
            disk_file.seek(4 + 72 * file_count + 4 + offset)
            
            # Read the file data
            file_data = disk_file.read(size)
            
            # Write the file data to the output directory
            sanitized_file_name = "".join([c for c in file_name if c.isalnum() or c in (' ', '.', '_')]).rstrip()
            output_file_path = os.path.join(output_dir, sanitized_file_name)
            os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
            sanitized_file_name = "".join([c for c in file_name if c.isalnum() or c in (' ', '.', '_')]).rstrip()
            output_file_path = os.path.join(output_dir, sanitized_file_name)
            with open(output_file_path, 'wb') as output_file:
                output_file.write(file_data)
            
            print(f"Extracted {file_name} to {output_file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract files from a .disk file")
    parser.add_argument("disk_file", help="Path to the .disk file")
    parser.add_argument("output_dir", help="Directory to extract files to")
    
    args = parser.parse_args()
    
    extract_disk_file(args.disk_file, args.output_dir)
