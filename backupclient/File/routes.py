from backupclient.File import bp
from flask import (
    request,send_from_directory
)

import os


@bp.route('/download', methods=['POST'])
def download():
    """Downloads a file. Expects a JSON via POST, example:
        {
            "file": "filename.txt"
            "direcotry: "/some/directory"
        }
    """

    # parse the received json
    data = request.json

    return send_from_directory(data["directory"], data["file"])

@bp.route('/generate_file_list', methods=['POST'])
def backup() -> dict:
    """Returns a JSON with a list of files. Expects a JSON via POST, example:
        {
            "type": "filelist",
            "path": "/some/directory"
        }
    """
    # parse the received json
    data = request.json
    
    # generate a dict which contains all filesystem entries on the given path
    file_list = recursive_scan_dir(data["path"])

    # return the dict
    return file_list

def recursive_scan_dir(path: str) -> dict:
    """Scans the given path recursive for files and directories.
    Returns a dict with the following structure:
    """
    stat = os.stat(path)
    file_list = {
        "name": path,
        "type": "directory",
        "stat": {
            "modified": stat.st_mtime_ns,
            "changed": stat.st_ctime_ns,
            "size": stat.st_size
        },
        "items": []
    }
    # scan through the list of files.
    with os.scandir(path) as it:
        
        # loop through the found entries in path
        for entry in it:

            # if entry is a file, store it as type file then go next in loop.
            if entry.is_file():
                # build dict
                file = {
                        "name": entry.name,
                        "type": "file",
                        "stat": {
                            "modified": stat.st_mtime_ns,
                            "changed": stat.st_ctime_ns,
                            "size": stat.st_size
                        },
                    }
                
                # append dict to file_list dict
                file_list["items"].append(file)
                continue
            
            # if it's not a file, it's a directory, call itself with the the path
            # and search for files.
            element = recursive_scan_dir(f"{path}/{entry.name}")

            # append it to the file list
            file_list["items"].append(element)

    # return file_list
    return file_list
