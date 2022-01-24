## filter url

This script performs HEAD HTTP requests to URLs from a list and filters URLs by specified HTTP status code(s).

A list of URLs (one URL per line) can be taken either from a file (or several files) or stdin. Outputs to stdout.

Requires Python 3.9+.

### Usage

```
filter_url.py [-h] [-d delay] [-c codes | -nc codes] file [file ...]

  file                  Files to process or '-' for stdin.

  -d delay, --delay delay
                        Delay between requests. Default is 0.
  -c codes, --http-codes codes
                        HTTP status codes to filter. Default is 200. Several codes can be separated by commas.
  -nc codes, --no-http-codes codes
                        HTTP status codes to exclude. Several codes can be separated by commas.
```

```
python3 filter_url.py -nc 200,301,302 list_of_urls.txt | tee not_valid_urls.txt
```
