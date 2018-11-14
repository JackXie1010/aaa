# coding: utf8
import re
import os


def get_last_line(inputfile):
    # with open('access.log', 'r') as f:
    #     lines = f.readlines()
    #     # print(lines)
    #     last = lines[-1]
    #     print(last)
    # f.close()
    filesize = os.path.getsize(inputfile)
    print(filesize)
    blocksize = 1024
    dat_file = open(inputfile, 'rb')
    last_line = ""
    if filesize > blocksize:
        maxseekpoint = (filesize // blocksize)
        dat_file.seek((maxseekpoint - 1) * blocksize)
    elif filesize:
        dat_file.seek(0, 0)
    lines = dat_file.readlines()
    print('lines:', lines)
    if lines:
        last_line = lines[-1].strip()
    dat_file.close()
    return last_line


def extract_log(line):
    ret = dict()
    try:
        ip = re.match(r'.* - -', line).group()
        ip = re.sub(r' - -|\'|b', '', ip)
        print(line)
        print(ip)
        req_time = re.search(r'\[.*\]', line).group()
        print(req_time)
        api = re.search(r'(GET|POST).*HTTP', line).group()
        api = re.sub(r'GET|POST| |HTTP', '', api)
        print(api)
        union = re.search(r'HTTP/1\.1".*\d "', line).group()
        union = re.sub(r'HTTP/1\.1|"|-', '', union).split()
        status, use_time = tuple(union)
        ret['ip'], ret['api'], ret['status'], ret['req_time'], ret['use_time'] = ip, api, status, req_time, use_time
    except Exception:
        ip, api, status, req_time, use_time = '', '', '', '', ''
        ret['ip'], ret['api'], ret['status'], ret['req_time'], ret['use_time'] = ip, api, status, req_time, use_time
    print('status:', status, '用时:', use_time)
    return ret


def read_log():
    i = 1
    with open('access.log') as f:
        for line in f:
            print(i, '------------i------------')
            # if i == 50:
            #     break
            extract_log(line)
            print('-' * 30)
            i += 1
    f.close()


if __name__ == '__main__':
    with open('error.log', 'r') as f:
        lines = f.readlines()
        # print(lines)
        last = lines[-1]
        print(last)
    f.close()

