import os
import hashlib

from drs_service.util import DRSBackend
from flask import send_file

class FSBackend(DRSBackend):
    def __init__(self, opts):
        self.files = {}

        self.cwd = os.getcwd()
        for dirpath, dirnames, filenames in os.walk(self.cwd):
            for f in filenames:
                hl = hashlib.sha256()
                with open(os.path.join(dirpath, f), "rb") as inp:
                    rel = dirpath[len(self.cwd)+1:]
                    sz = 0
                    stuff = inp.read(64*1024)
                    sz += len(stuff)
                    while stuff:
                        hl.update(stuff)
                        stuff = inp.read(64*1024)
                        sz += len(stuff)

                    hashid = hl.hexdigest()
                    print(hashid)
                    self.files[hashid] = {
                        'id': hashid,
                        'name': f,
                        'self_uri': "",
                        'size': sz,
                        'created_time': "",
                        'updated_time': "",
                        'version': "0",
                        'mime_type': "",
                        'access_methods': [{
                            "type": "https",
                            "access_url": {
                                "url": "/download/"+rel,
                                "headers": []
                            },
                            "region": ""
                            }],
                        'checksums': [{"type": "sha256", "checksum": hashid}],
                        'contents': [],
                        'description': "",
                        'aliases': ""
                    }

    def GetObject(self, object_id, expand, user):
        # required: ['id', 'self_uri', 'size', 'created_time', 'checksums']
        print("user is", user)
        return self.files[object_id]

    def GetAccessURL(self, object_id, access_id):
        pass

    def download(self, path):
        if "../" in path:
            raise Exception("Bad path")
        return send_file(os.path.join(self.cwd, path))

def auth(apikey, required_scopes):
    return {'sub': apikey}

def create_backend(app, opts):
    fsb = FSBackend(opts)
    app.app.route('/download/<path:path>')(fsb.download)
    return fsb