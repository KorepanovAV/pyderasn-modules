# pyderasn-modules

The `pyderasn-modules` repository contains a collection of
[ASN.1](https://www.itu.int/rec/dologin_pub.asp?lang=e&id=T-REC-X.208-198811-W!!PDF-E&type=items)
data structures expressed as Python classes based on [PyDERASN](http://pyderasn.cypherpunks.ru)
data model.

# Usage

## Run

python -m cms_schema --nobered --allow-expl-oob --schema cms_schema:ContentInfo --oids oids:oids "sign.der" >dump

## Result

[dump](https://korepanovav.github.io/pyderasn-modules/)
