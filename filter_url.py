from string import printable
from sys import stderr
from fileinput import input
from argparse import ArgumentParser
from pathlib import Path
from time import sleep
from urllib.request import urlopen, Request
from urllib.error import URLError
from urllib.parse import urlparse, quote, ParseResult
from typing import Union, Any


def process(url: str) -> str:
    req = Request(url=quote(url, safe=printable), method="HEAD")
    req.add_header(key="User-Agent", val="Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0")
    code = 0
    try:
        with urlopen(url=req, timeout=4) as response:
            code = response.status
    except URLError as e:
        if hasattr(e, 'code'):
            code = e.code
        elif hasattr(e, 'reason'):
            print("Processing error: " + url + " -> " + str(e.reason), file=stderr)
    return str(code)


def check_url(url: str) -> Union[ParseResult, bool]:
    u = urlparse(url)
    return u if u.scheme in ["http", "https"] else False


def check_code(code: str, codes: set[str], exclude: bool) -> bool:
    return (code not in codes) if exclude \
        else (code in codes)


def process_file(file: str, codes: set[str], exclude: bool, delay: int):
    try:
        with input(file) as f:
            for line in f:
                url = check_url(line.strip())
                if not url:
                    break
                sleep(delay)
                code = process(url.geturl())
                if check_code(code, codes, exclude):
                    print(url.geturl())
    except PermissionError as e:
        print("Permission denied: " + e.filename, file=stderr)


def process_files(params: dict[str, Any]):
    for file in params['files']:
        if Path(file).is_file() or file == '-':
            process_file(file, params['codes'], params['exclude'], params['delay'])


if __name__ == '__main__':
    parser = ArgumentParser(description="Performs HEAD HTTP request to URLs from a list, "
                                        "and filters URL by specified HTTP status code(s). "
                                        "A file should contain one URL per line.")
    parser.add_argument("files", metavar="file", default="-", nargs="+", help="Files to process or '-' for stdin.")
    parser.add_argument("-d", "--delay", metavar="delay", dest="delay", default=0, type=int,
                        help="Delay between requests. Default is 0.")
    cgroup = parser.add_mutually_exclusive_group()
    cgroup.add_argument("-c", "--http-codes", metavar="codes", dest="http_codes", default="200",
                        help="HTTP status codes to filter. Default is 200. Several codes can be separated by commas.")
    cgroup.add_argument("-nc", "--no-http-codes", metavar="codes", dest="no_http_codes",
                        help="HTTP status codes to exclude. Several codes can be separated by commas.")
    args = parser.parse_args()
    if args.no_http_codes is None:
        config = {"codes": set(args.http_codes.split(sep=',')), "exclude": False,
                  "delay": args.delay, "files": set(args.files)}
    else:
        config = {"codes": set(args.no_http_codes.split(sep=',')), "exclude": True,
                  "delay": args.delay, "files": set(args.files)}
    process_files(config)
