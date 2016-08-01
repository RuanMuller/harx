# Description
HAR eXtractor.

This utility was developed to assist security analysts working with HTTP Archive (HAR) files to list and extract the contained objects.

More information about the HTTP Archive (HAR) format can be read here: https://dvcs.w3.org/hg/webperf/raw-file/tip/specs/HAR/Overview.html

# Disclaimer
* This code is a proof of concept only and is not warranted for production use
* No support is available for this software
* This code has not been audited for security issues
* Use entirely at your own risk

# Requirements
**Python 2.7**

* Python Magic Module: `pip install python-magic`

For quick module installation:
```bash
pip install -r requirements.txt
```

# Usage
```
usage: harx.py [-h] [-c CSV] [-l] [-x EXTRACT] [-xa] [-d DIRECTORY] har_file

positional arguments:
  har_file

optional arguments:
  -h, --help            show this help message and exit
  -c CSV, --csv CSV     Save object list to [CSV]
  -l, --list            List objects
  -x EXTRACT, --eXtract EXTRACT
                        eXtract object matching index from -l output
  -xa, --eXtractAll     eXtract all objects
  -d DIRECTORY, --directory DIRECTORY
                        [DIRECTORY] to extract files to
```

# Example Execution
## List objects
```
./harx.py -l ek_traffic.har
[  0] [2015-08-31T17:56:12.104071Z] [   GET] [                    text/plain] [Size:       14] [http://www.msftncsi.com/ncsi.txt]
[  1] [2015-08-31T17:56:46.994169Z] [   GET] [                     text/html] [Size:     1305] [http://api.bing.com/qsml.aspx?query=go&maxwidth=32765&rowheight=20&sectionHeight=160&FORM=IESS02&market=en-US]
[  2] [2015-08-31T17:56:47.544066Z] [   GET] [                     text/html] [Size:     1346] [http://api.bing.com/qsml.aspx?query=google&maxwidth=32765&rowheight=20&sectionHeight=160&FORM=IESS02&market=en-US]
[  3] [2015-08-31T17:56:47.807992Z] [   GET] [                     text/html] [Size:     1369] [http://api.bing.com/qsml.aspx?query=google.c&maxwidth=32765&rowheight=20&sectionHeight=160&FORM=IESS02&market=en-US]
...
[209] [2015-08-31T18:01:22.238266Z] [  POST] [     application/ocsp-response] [Size:     1336] [http://gtssl-ocsp.geotrust.com/]
[210] [2015-08-31T18:01:23.122156Z] [  POST] [     application/ocsp-response] [Size:     1453] [http://ocsp.verisign.com/]
[211] [2015-08-31T18:01:23.248269Z] [  POST] [     application/ocsp-response] [Size:     1762] [http://ocsp.verisign.com/]
[212] [2015-08-31T18:01:23.442410Z] [  POST] [     application/ocsp-response] [Size:     1725] [http://sf.symcd.com/]
```

## Extract object matching index from -l output
```
./harx.py -x 137 ek_traffic.har
[137] [       41keG5PBKbL-274x300.jpg] [Size:  32.5KiB] [3b58d7efe887212e2b1b631bdd417034] [                    image/jpeg] [http://example.com/wp-content/uploads/2015/06/41keG5PBKbL-274x300.jpg]
```

## Extract all objects to a folder
```
./harx.py -xa -d ek_traffic_analysis ek_traffic.har
[  0] [                      ncsi.txt] [Size:    14.0B] [cd5a4d3fdd5bffc16bf959ef75cf37bc] [                    text/plain] [http://www.msftncsi.com/ncsi.txt]
[  1] [                     qsml.aspx] [Size:   110.0B] [b0c846fc56e41d5eec6adf8e92a59fef] [      application/octet-stream] [http://api.bing.com/qsml.aspx?query=go&maxwidth=32765&rowheight=20&sectionHeight=160&FORM=IESS02&market=en-US]
[  2] [                     qsml.aspx] [Size:   113.0B] [e78f910e1a340736b2e5e81aea8d0880] [      application/octet-stream] [http://api.bing.com/qsml.aspx?query=google&maxwidth=32765&rowheight=20&sectionHeight=160&FORM=IESS02&market=en-US]
[  3] [                     qsml.aspx] [Size:   128.0B] [307f529a949ee293872b226dd7c2668c] [      application/octet-stream] [http://api.bing.com/qsml.aspx?query=google.c&maxwidth=32765&rowheight=20&sectionHeight=160&FORM=IESS02&market=en-US]
...
[209] [  gtssl-ocsp.geotrust.com.file] [Size:   1.3KiB] [09a6f239fd0bd44d43a739b64253057b] [      application/octet-stream] [http://gtssl-ocsp.geotrust.com/]
[210] [        ocsp.verisign.com.file] [Size:   1.4KiB] [45f667114e55de8ee7c8bfc0bb0e7744] [      application/octet-stream] [http://ocsp.verisign.com/]
[211] [        ocsp.verisign.com.file] [Size:   1.7KiB] [eadb300a3afed5b2cb378cbb8548386a] [      application/octet-stream] [http://ocsp.verisign.com/]
[212] [             sf.symcd.com.file] [Size:   1.7KiB] [516235e7ad11627ed89b9b8248ee89b7] [      application/octet-stream] [http://sf.symcd.com/]
```