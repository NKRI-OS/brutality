# Brutality

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

#### What is this?
A 'brutality' fuzzer for any GET entries

#### Features
- [x] Multi-threading on demand
- [x] Fuzzing, bruteforcing GET params
- [x] Find admin panels
- [x] Colored output
- [x] Hide results by return code, word numbers
- [x] Proxy support
- [x] Big wordlist

#### Usages
- Install
```
git clone https://github.com/ManhNho/brutality.git
chmod 755 -R brutality/
cd brutality/
pip install -r requirements.txt
```
- Helps
```
python brutality -h
```

#### Examples
- Use default wordlist with 5 threads (-t 5) and hide 404 messages (–e 404) to fuzz the given URL (http://192.168.1.1/FUZZ):
```
python brutality.py -u 'http://192.168.1.1/FUZZ' -t 5 -e 404
```

- Use common_pass.txt wordlist (-f ./wordlist/common_pass.txt), remove response with 6969 length (-r 6969) and proxy at 127.0.0.1:8080 (-p http://127.0.0.1:8080) to fuzz the given URL (http://192.168.1.1/brute.php?username=admin&password=FUZZ&submit=submit#):
```
python brutality.py -u 'http://192.168.1.1/brute.php?username=admin&password=FUZZ&submit=submit#' -f ./wordlist/common_pass.txt -r 6969 -p http://127.0.0.1:8080
```

#### Images
![Example](/demo/Example.PNG)

#### Videos
[![Demo](/demo/Screenshot.png)](https://www.youtube.com/watch?v=1JQIjRVzVYA "Demo")
