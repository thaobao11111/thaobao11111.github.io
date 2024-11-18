import os
import gzip

# Đường dẫn tới thư mục repo của bạn
repo_dir = "./dists/stable/main"

# Tạo file Release
release_content = """Origin: myrepo
Label: myrepo
Suite: stable
Codename: stable
Architectures: iphoneos-arm, iphoneos-arm64
Components: main
Description: My Custom Repo for Jailbreak Apps
"""
with open(os.path.join(repo_dir, "Release"), "w") as release_file:
    release_file.write(release_content)

# Tạo file Packages
packages_content = """Package: myapp
Version: 1.0.0
Architecture: iphoneos-arm
Maintainer: me@myemail.com
Depends: com.apple.later, libirecovery
Description: My Custom App for Jailbreak
"""
with open(os.path.join(repo_dir, "Packages"), "w") as packages_file:
    packages_file.write(packages_content)

# Nén file Packages thành Packages.gz
with open(os.path.join(repo_dir, "Packages"), "rb") as f_in:
    with gzip.open(os.path.join(repo_dir, "Packages.gz"), "wb") as f_out:
        f_out.writelines(f_in)

print("Repo files (Release, Packages, Packages.gz) have been created and compressed successfully.")
