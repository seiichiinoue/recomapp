# recomapp

[WIP] this repository is to develop recommendation engine for my blog.


## Requirements

- Python3
- Flask


## Usage

### local server

- start server

```
$ python run_server.py
```

- get recommendation via `POST` method

```
$ curl http://0.0.0.0:5000/infer -X POST -H 'Content-Type:application/json' -d '{"filename":"hmm"}'
```

- get recommendation via `GET` method

```
$ curl http://0.0.0.0:5000/infer -X GET -H 'Content-Type:application/json' -d '{"filename":"hmm"}'

- if successed request

```
{"Content-Type":"application/json","prediction":["cstm.txt","vpylm.txt","hmm.txt","tobit.txt","lsgan.txt","bit.txt","modinv.txt","nlp.txt","procon.txt","roberta.txt"],"success":true}
```

### web server (heroku)

- get recommendation

```
$ curl https://recomapp.herokuapp.com/infer -X POST -H 'Content-Type:application/json' -d '{"filename":"hmm"}'
```

- check log

```
$ heroku logs --tail
```
