import pymysql


def GetList(sql):
    db = pymysql.connect(user='root', db='root', passwd='123456', host='localhost')
    cursor = db.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    db.close()
    return data


def GetSingle(sql):
    db = pymysql.connect(user='root', db='root', passwd='123456', host='localhost')
    cursor = db.cursor()
    cursor.execute(sql)
    data = cursor.fetchone()
    db.close()
    return data