import json
import pymysql.cursors
from flask import Flask, abort
from typing import List, Dict
import os
app = Flask(__name__)

cfg_path = os.environ.get("CFG_PATH")
if cfg_path is None:
    cfg_path = "./mysql.json"
cfg = json.loads(open(cfg_path).read())

connection = pymysql.connect(
    host=cfg.get("host"),
    user=cfg.get("user"),
    password=cfg.get("password"),
    db=cfg.get("db"),
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

cursor = connection.cursor()


def list_tables()->List[str]:
    result = []
    sql = "SHOW TABLES"
    cursor.execute(sql)
    tables = cursor.fetchall()
    result = tables
    return result


all_tables = {t.get("Tables_in_business_data_db"): True for t in list_tables()}


@app.route("/<table_name>/<field>/<field_val>", defaults={"limit": 1, "fields_to_get": "*"}, methods=["GET"])
@app.route("/<table_name>/<field>/<field_val>/<limit>", defaults={"fields_to_get": "*"}, methods=["GET"])
@app.route("/<table_name>/<field>/<field_val>/<limit>/<fields_to_get>", methods=["GET"])
def get(table_name: str, field: str, field_val: str, limit: int, fields_to_get: str):
    if not all_tables.get(table_name):
        abort(404)
    result = {}
    sql = """SELECT {fields_to_get} FROM 
                {table_name} 
             WHERE 
                {field} = {field_val} 
             LIMIT 
                {limit}""".format(
        fields_to_get=fields_to_get,
        table_name=table_name,
        field=field,
        field_val=field_val,
        limit=limit
    )
    cursor.execute(sql)
    r = cursor.fetchall()
    result = r
    return json.dumps(result, indent=4, ensure_ascii=False)


@app.route("/<table_name>/<field>/<field_val>/<limit>", methods=["DELETE"])
def delete(table_name: str, field: str, field_val: str, limit: int):
    records_to_delete = get(table_name, field, field_val, limit, "*")
    sql = """
        DELETE FROM 
            {table_name} 
        WHERE 
            {field} = {field_val}
        LIMIT {limit}
    """.format(
        table_name=table_name,
        field=field,
        field_val=field_val,
        limit=limit
    )
    cursor.execute(sql)
    return records_to_delete
