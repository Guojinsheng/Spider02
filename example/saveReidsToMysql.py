import redis
import pymysql
import time
import json

# 把redis中的数据迁移到Mysql

# 连接redis
redis_con = redis.Redis(
    host='localhost',
    port=6379,
    db=0,
    password=''
)
# print(redis_con)

# 连接Mysql
mysql_con = pymysql.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password='root',
    database='spiderdb',
    charset='utf8'
)
mysql_cursor = mysql_con.cursor()
# print(mysql_con)


# 每隔0.1秒从redis中取出数据，并存入mysql中
while True:
    # 从redis中取出, 从redis队列的左边取出
    key, val = redis_con.blpop('mybaikecrawler_redis:items')
    item = json.loads(val.decode())
    # print(item)  # {'title': '扎菲曼尼里的木雕工艺', 'sub_title': '副标题', 'content': '扎菲曼尼里的木雕工艺是马达加斯加传统知识技艺，属于非洲的工艺。'}

    # 存入mysql
    sql = "insert into baike(title, sub_title, content) values(%r, %r, %r)" % \
          (item['title'], item['sub_title'], item['content'])
    mysql_cursor.execute(sql)
    mysql_con.commit()

    print("存入成功：", item['title'], item['sub_title'])

    time.sleep(0.1)

# 关闭
mysql_cursor.close()
mysql_con.close()






