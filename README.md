## Flask based mysql to REST transformer

### Install

Requires anaconda

```bash
$ conda env create -f pymysql.yml
```

### Deploy

`CFG_PATH='path to mysql.json' gunicorn -w 4 -b 127.0.0.1:5000 main:app`

`mysql.json`

```json
{
  "host": "",
  "port": 3306,
  "user": "root",
  "password": "",
  "db": ""
}
```

#### Dev

```bash
$ ./start_dev.sh
```

#### API

`GET /<table_name>/<field>/<field_val>/<limit>/<fields_to_get>`

Where <fields_to_get> is like `field1,field2,field3`

> POST
> PUT
> DELETE
