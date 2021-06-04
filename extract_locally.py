from pathlib import Path
import os
import zipfile,os.path


def unzip(source_filename, dest_dir):
    # Source https://stackoverflow.com/questions/12886768/how-to-unzip-file-in-python-on-all-oses
    with zipfile.ZipFile(source_filename) as zf:
        for member in zf.infolist():
            # Path traversal defense copied from
            # http://hg.python.org/cpython/file/tip/Lib/http/server.py#l789
            words = member.filename.split('/')
            path = dest_dir
            for word in words[:-1]:
                while True:
                    drive, word = os.path.splitdrive(word)
                    head, word = os.path.split(word)
                    if not drive:
                        break
                if word in (os.curdir, os.pardir, ''):
                    continue

                path = os.path.join(path, word)

            if(member.filename.split('/').pop()):
                member.filename = member.filename.split('/').pop()
                zf.extract(member, path)


# Find all zipped files
zipped_dataset_path_list = []
for path in Path('datasets_zipped/').rglob('*.zip'):
    zipped_dataset_path_list.append(path)

# Create same folder path in another subdirectory called dataset_extracted
for zip_path in zipped_dataset_path_list:
    path_organization = os.path.dirname(str(zip_path.resolve()).split("datasets_zipped/")[-1])
    print(path_organization)
    extracted_path = os.path.join("datasets_extracted_locally", path_organization)
    print(extracted_path)
    if not os.path.exists(extracted_path):
        os.makedirs(extracted_path)

    # Unzip file in the subpath
    unzip(source_filename=zip_path, dest_dir=extracted_path)

    #print(os.path.join(os.path.join(zip_path.absolute.split("/")[1:-1])))

