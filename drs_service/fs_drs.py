import os
import hashlib
import copy

from drs_service.util import DRSBackend
import flask

class FSBackend(DRSBackend):
    def __init__(self, opts):
        self.files = {}

        self.cwd = os.getcwd()
        dp = {}
        for dirpath, dirnames, filenames in os.walk(self.cwd, topdown=False):
            dot = False
            for sp in dirpath.split("/"):
                if sp.startswith(".") or sp.startswith("_"):
                    dot = True
            if dot:
                continue
            ck = []
            for f in filenames:
                if f.startswith("."):
                    continue
                hl = hashlib.sha256()
                dp[dirpath] = []
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
                    fileobj = {
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
                                "url": "%s/%s" % (rel, f),
                                "headers": []
                            },
                            "access_id": "",
                            "region": ""
                            }],
                        'checksums': [{"type": "sha256", "checksum": hashid}],
                        'contents': [],
                        'description': "",
                        'aliases': ""
                    }
                    self.files[hashid] = fileobj
                    ck.append(hashid)
            for d in dirnames:
                if d.startswith(".") or d.startswith("_"):
                    continue
                ck.append(dp[os.path.join(dirpath, d)])
            ck.sort()
            hl = hashlib.sha256()
            hl.update(("".join(ck)).encode("UTF-8"))
            hashid = hl.hexdigest()
            dp[dirpath] = hashid

            dirobj = {
                'id': hashid,
                'name': os.path.basename(dirpath),
                'self_uri': "",
                'size': 0,
                'created_time': "",
                'updated_time': "",
                'version': "0",
                'mime_type': "",
                'access_methods': [],
                'checksums': [{"type": "sha256", "checksum": hashid}],
                'contents': [],
                'description': "",
                'aliases': ""
            }
            for c in ck:
                dirobj['contents'].append({
                    'name': self.files[c]['name'],
                    'id': self.files[c]['id'],
                    'drs_uri': ["drs://127.0.0.1:8080/%s" % self.files[c]['id']],
                    'contents': self.files[c]['contents']
                })
            self.files[hashid] = dirobj


    def GetObject(self, object_id, expand, user):
        # required: ['id', 'self_uri', 'size', 'created_time', 'checksums']
        found = False
        with open(".secrets", "rt") as secrets:
            for s in secrets:
                s = s.rstrip()
                if s == user:
                    found = True
        if not found:
            return None, 401
        if object_id not in self.files:
            return None, 404

        ob = copy.deepcopy(self.files[object_id])
        if len(ob['access_methods']) == 1:
            ob['access_methods'][0]['access_url']['url'] = "%s://%s/download/%s" % (flask.request.scheme, flask.request.host, ob['access_methods'][0]['access_url']['url'])
        return ob

    def GetAccessURL(self, object_id, access_id):
        pass

    def download(self, path):
        if "../" in path:
            raise Exception("Bad path")
        return flask.send_file(os.path.join(self.cwd, path))


def create_backend(app, opts):
    fsb = FSBackend(opts)
    app.app.route('/download/<path:path>')(fsb.download)
    return fsb
