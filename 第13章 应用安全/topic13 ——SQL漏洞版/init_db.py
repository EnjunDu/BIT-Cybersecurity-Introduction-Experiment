import sqlite3

connection = sqlite3.connect('login.db')
cursor = connection.cursor()

# 创建一个用户表
cursor.execute('''
CREATE TABLE users(id INTEGER PRIMARY KEY, username TEXT, password TEXT)
''')

# 插入示例用户
cursor.execute('''
INSERT INTO users(username, password) VALUES ('sky', 'sky666')
''')

connection.commit()
connection.close()
