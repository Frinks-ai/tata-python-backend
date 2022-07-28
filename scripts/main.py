import json
import time
import subprocess
# import os
# import sys

BASE_PATH = "/tata-python-backend"

try:
    first = subprocess.Popen(
        [f"python3 {BASE_PATH}/scripts/dimension.py {BASE_PATH}/images/upload.bmp"], stdout=subprocess.PIPE, shell=True)
    second = subprocess.Popen(
        [f"python3 {BASE_PATH}/scripts/deviation.py {BASE_PATH}/images/upload.bmp"], stdout=subprocess.PIPE, shell=True)
    start = time.time()
    fout, ferr = first.communicate()
    sout, serr = second.communicate()
    end = time.time()
    # print(fout)
    # print(sout)
    fres = json.loads(fout.decode('ascii'))
    sres = json.loads(sout.decode('ascii'))
    flen = len(fres)
    findex = 0
    for i, value in enumerate(sres):
        if findex >= flen:
            break
        if value["name"] == fres[findex]["name"]:
            value["dim"] = fres[findex]["dim"]
            findex += 1
            sres[i] = value
    sres.insert(0, end-start)
    print(json.dumps(sres))
except Exception as e:
    # exc_type, exc_obj, exc_tb = sys.exc_info()
    # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    # print(exc_type, fname, exc_tb.tb_lineno)
    print(json.dumps(''))
    pass
