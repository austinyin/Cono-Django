import pymysql

ins_db = pymysql.connect('localhost', 'root', 'python', 'ins', charset="utf8")
ins_cur = ins_db.cursor()

cono_db = pymysql.connect('localhost', 'root', 'python', 'cono', charset="utf8")
cono_cur = cono_db.cursor()


def get_user():
    sql = "SELECT full_name,username,password FROM ins_user"
    ins_cur.execute(sql)
    return ins_cur.fetchall()


def insert_user_to_cono(users):
    sql = """INSERT INTO EMPLOYEE(FIRST_NAME,
   LAST_NAME, AGE, SEX, INCOME)
   VALUES (%s, %s, %s)"""
    for user in users:
        cono_cur.execute(sql)


def main():
    users = get_user()
    insert_user_to_cono(users)


if __name__ == '__main__':
    main()
