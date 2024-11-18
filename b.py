import os
import shutil
import subprocess
from debian.deb822 import Packages

# Các biến cấu hình
REPO_NAME = "Sileo Repo"
REPO_DESCRIPTION = "A custom repo for iOS tweaks"
ARCHITECTURE = "iphoneos-arm"
SUITE = "stable"
COMPONENT = "main"
BASE_DIR = "thaobao11111.github.io"
DIST_DIR = os.path.join(BASE_DIR, "dists", SUITE, COMPONENT, f"binary-{ARCHITECTURE}")
POOL_DIR = os.path.join(BASE_DIR, "pool", COMPONENT)

# Tạo cấu trúc repo nếu chưa tồn tại
def create_repo_structure():
    os.makedirs(DIST_DIR, exist_ok=True)
    os.makedirs(POOL_DIR, exist_ok=True)

# Thêm file .deb vào thư mục pool
def add_deb_file(deb_file):
    if not os.path.exists(deb_file):
        return False, f"Lỗi: File {deb_file} không tồn tại!"
    shutil.copy(deb_file, POOL_DIR)
    return True, f"File {os.path.basename(deb_file)} đã được thêm vào repo."

# Tạo file Packages bằng python-debian
def generate_packages_file():
    try:
        # Danh sách các file .deb trong thư mục pool
        packages = []
        for filename in os.listdir(POOL_DIR):
            if filename.endswith(".deb"):
                package = {
                    'Package': filename,
                    'Version': '1.0',
                    'Architecture': ARCHITECTURE,
                    'Description': f"{REPO_NAME} package"
                }
                packages.append(package)

        # Tạo file Packages
        with open(os.path.join(DIST_DIR, "Packages"), "w") as packages_file:
            pkg = Packages()
            for package in packages:
                pkg.add_entry(package)
            pkg.write(packages_file)
        return True, "File Packages đã được tạo thành công."
    except Exception as e:
        return False, f"Lỗi khi tạo file Packages: {e}"

# Tạo file Release
def generate_release_file():
    try:
        release_path = os.path.join(BASE_DIR, "dists", SUITE, "Release")
        with open(release_path, "w") as release_file:
            release_file.write(f"""Origin: {REPO_NAME}
Label: {REPO_NAME}
Suite: {SUITE}
Version: 1.0
Codename: {SUITE}
Architectures: {ARCHITECTURE}
Components: {COMPONENT}
Description: {REPO_DESCRIPTION}
""")
        return True, "File Release đã được tạo thành công."
    except Exception as e:
        return False, f"Lỗi khi tạo file Release: {e}"

# Đẩy repo lên GitHub Pages
def push_to_github():
    try:
        # Khởi tạo git nếu chưa có
        if not os.path.exists(os.path.join(BASE_DIR, ".git")):
            subprocess.run(["git", "init"], cwd=BASE_DIR, check=True)
            subprocess.run(["git", "remote", "add", "origin", "https://github.com/thaobao11111/thaobao11111.github.io.git"], cwd=BASE_DIR, check=True)

        # Thêm file, commit và push
        subprocess.run(["git", "add", "."], cwd=BASE_DIR, check=True)
        subprocess.run(["git", "commit", "-m", "Update repo"], cwd=BASE_DIR, check=True)
        subprocess.run(["git", "push", "-u", "origin", "main", "--force"], cwd=BASE_DIR, check=True)

        return True, "Repo đã được đẩy lên GitHub Pages thành công."
    except Exception as e:
        return False, f"Lỗi khi đẩy lên GitHub: {e}"

# Giao diện GUI
def main_gui():
    import tkinter as tk
    from tkinter import filedialog, messagebox

    def select_deb_file():
        file_path = filedialog.askopenfilename(
            title="Chọn file .deb",
            filetypes=[("Debian Package", "*.deb")],
        )
        if file_path:
            success, message = add_deb_file(file_path)
            messagebox.showinfo("Kết quả", message)
            if success:
                deb_listbox.insert(tk.END, os.path.basename(file_path))

    def create_repo():
        create_repo_structure()
        success_pkg, msg_pkg = generate_packages_file()
        success_rel, msg_rel = generate_release_file()

        # Hiển thị kết quả
        if success_pkg and success_rel:
            messagebox.showinfo("Thành công", f"Repo đã được cập nhật thành công!\nURL: https://github.com/thaobao11111/thaobao11111.github.io")
        else:
            error_msg = "\n".join([msg_pkg if not success_pkg else "", msg_rel if not success_rel else ""])
            messagebox.showerror("Lỗi", f"Xảy ra lỗi:\n{error_msg}")

    def push_repo():
        success, message = push_to_github()
        if success:
            messagebox.showinfo("Thành công", message)
        else:
            messagebox.showerror("Lỗi", message)

    # Tạo cửa sổ chính
    root = tk.Tk()
    root.title("Quản lý Repo Sileo")

    # Giao diện
    tk.Label(root, text="Quản lý Repo Sileo", font=("Arial", 16)).pack(pady=10)

    # Khu vực chọn file .deb
    tk.Button(root, text="Thêm file .deb", command=select_deb_file).pack(pady=5)
    deb_listbox = tk.Listbox(root, width=50, height=10)
    deb_listbox.pack(pady=5)

    # Nút tạo repo
    tk.Button(root, text="Cập nhật Repo", command=create_repo, bg="green", fg="white").pack(pady=10)

    # Nút đẩy lên GitHub
    tk.Button(root, text="Đẩy lên GitHub", command=push_repo, bg="blue", fg="white").pack(pady=10)

    # Chạy giao diện
    root.mainloop()

if __name__ == "__main__":
    main_gui()
