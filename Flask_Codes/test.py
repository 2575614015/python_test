


with open("./schema.sql","r") as f:



    sqls = f.read().strip().replace("\n", "").split(";")
    sqls.pop()
    for sql in sqls:
        sql = sql + ";"

