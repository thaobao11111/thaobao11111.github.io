import os
import gzip

# Bước 1: Tạo tệp Release
release_content = """Origin: My Repo
Label: My Repo
Suite: stable
Codename: stable
Version: 1.0
Architectures: iphoneos-arm
Components: main
Description: My custom repo for iPhone
"""

# Lưu tệp Release
with open('./dists/stable/Release', 'w') as f:
    f.write(release_content)

print("File Release đã được tạo thành công!")

# Bước 2: Tạo tệp Packages
deb_directory = './dists/stable/main/binary-iphoneos-arm'

with open('./dists/stable/main/Packages', 'w') as f:
    for deb_file in os.listdir(deb_directory):
        if deb_file.endswith('.deb'):
            # Lấy kích thước của gói .deb
            file_size = os.path.getsize(os.path.join(deb_directory, deb_file))
            f.write(f"Package: {deb_file}\n")
            f.write(f"Architecture: iphoneos-arm\n")
            f.write(f"Version: 1.0\n")
            f.write(f"Filename: dists/stable/main/binary-iphoneos-arm/{deb_file}\n")
            f.write(f"Size: {file_size}\n")
            f.write(f"Description: My custom package\n\n")

print("File Packages đã được tạo thành công!")

# Bước 3: Nén tệp Packages thành Packages.gz
with open('./dists/stable/main/Packages', 'rb') as f_in:
    with gzip.open('./dists/stable/main/Packages.gz', 'wb') as f_out:
        f_out.writelines(f_in)

print("File Packages.gz đã được tạo thành công!")
