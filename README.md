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
$ curl http://0.0.0.0:5000/infer -X POST -H 'Content-Type:application/json' -d '{"name":"cstm"}'
```

- get recommendation via `GET` method

```
$ curl http://0.0.0.0:5000/infer -X GET -H 'Content-Type:application/json' -d '{"name":"cstm"}'
```

### web server (heroku)

- get recommendation

```
$ curl https://recomapp.herokuapp.com/infer -X POST -H 'Content-Type:application/json' -d '{"name":"cstm"}'
```

- check log

```
$ heroku logs --tail
```


## Dev Memo

- ~~Hugo内でapiを扱うため，`サイト名`から，`サイト名`のリストと，`固定url以下の文字列`のjsonを返すapiに変更した方が良さそう．~~
- `scrape.py`内で記事一覧を取得するところを今はローカルのdirを使ってるが，web上で完結できるようにしたい．

- build 

```
$ ./build.sh
```
