import os
import gzip
from debian.deb822 import Packages

def generate_packages(pool_dir, dist_dir):
    packages = []
    for filename in os.listdir(pool_dir):
        if filename.endswith('.deb'):
            deb_file = os.path.join(pool_dir, filename)
            package_info = f"Package: {filename}\nVersion: 1.0\nArchitecture: amd64\nFilename: pool/{filename}\nDescription: Custom Package\n\n"
            packages.append(package_info)

    packages_content = ''.join(packages)

    packages_path = os.path.join(dist_dir, 'Packages')
    with gzip.open(packages_path + '.gz', 'wt') as f:
        f.write(packages_content)

    print("File Packages.gz đã được tạo thành công!")

# Đường dẫn thư mục
pool_dir = 'C:/Users/THAIBAO/Desktop/New folder (5)/thaobao11111.github.io/pool'
dist_dir = 'C:/Users/THAIBAO/Desktop/New folder (5)/thaobao11111.github.io/dists/stable/main'

generate_packages(pool_dir, dist_dir)
