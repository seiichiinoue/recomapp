# recomapp

[WIP] this repository is to develop recommendation engine for my blog.


## Requirements

- Python3
- Flask


## Usage

- start server

```
$ python run_server.py
```

- get recommendation

```
$ curl http://0.0.0.0:5000/infer -X POST -H 'Content-Type:application/json' -d '{"filename":"cstm.txt"}'
```

- if successed request

```
{"Content-Type":"application/json","prediction":["cstm.txt","vpylm.txt","hmm.txt","tobit.txt","lsgan.txt","bit.txt","modinv.txt","nlp.txt","procon.txt","roberta.txt"],"success":true}
```
