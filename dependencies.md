# Remote Dependencies

- pronunciation_dict_parser
- g2p_en
- sentence2pronunciation

## Pipfile

### Local

```Pipfile
pronunciation_dict_parser = {editable = true, path = "./../pronunciation_dict_parser"}
g2p_en = {editable = true, path = "./../g2p"}
sentence2pronunciation = {editable = true, path = "./../sentence2pronunciation"}
```

### Remote

```Pipfile
pronunciation_dict_parser = {editable = true, ref = "master", git = "https://github.com/stefantaubert/pronunciation_dict_parser.git"}
g2p_en = {editable = true, ref = "master", git = "https://github.com/stefantaubert/g2p.git"}
sentence2pronunciation = {editable = true, ref = "main", git = "https://github.com/jasminsternkopf/sentence2pronunciation.git"}
```

## setup.cfg

```cfg
pronunciation_dict_parser@git+https://github.com/stefantaubert/pronunciation_dict_parser@master
g2p_en@git+https://github.com/stefantaubert/g2p@master
sentence2pronunciation@git+https://github.com/jasminsternkopf/sentence2pronunciation@main
```
