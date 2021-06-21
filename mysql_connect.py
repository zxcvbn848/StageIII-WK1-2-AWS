from mysql.connector import pooling
from dotenv import load_dotenv
import os

load_dotenv()

try:
   connection_pool = pooling.MySQLConnectionPool(
      pool_name = "upload_pool",
      pool_size = 5,
      pool_reset_session = True,
      host = os.getenv("SERVER_HOST"),
      port = os.getenv("SERVER_PORT"),
      user = os.getenv("SERVER_USER"),
      password = os.getenv("SERVER_PASSWORD"),
      database = os.getenv("SERVER_DATABASE"),
      charset = "utf8")
except Exception as e:
   print(e)  

def closePool(connection_object, cursor):
   if connection_object.is_connected():
      cursor.close()
      connection_object.close()    
# ====================
# for /api/upload
def selectPosts():
   try:
      sql_cmd = """
               SELECT *
               FROM posts
               """

      connection_object = connection_pool.get_connection()

      if connection_object.is_connected():
         cursor = connection_object.cursor()
         cursor.execute(sql_cmd)
         results = cursor.fetchall()      

      dataList = []

      if results:
         for result in results:
            data = dict(zip(cursor.column_names, result))
            dataList.append(data)
         return dataList
      else:
         return None
   except Exception as e:
      print(e)
      return None
   finally:
      closePool(connection_object, cursor)   

def selectPost(**kwargs):
   try:
      sql_cmd = """
               SELECT *
               FROM posts
               WHERE
               """

      for key in kwargs:
        sql_cmd += f"{ key } = '{ kwargs[key] }' and "
      
      sql_cmd = sql_cmd[:-5] # 扣除掉 " and "

      connection_object = connection_pool.get_connection()

      if connection_object.is_connected():
         cursor = connection_object.cursor()
         cursor.execute(sql_cmd)
         result = cursor.fetchone()      

      if result:
         data = dict(zip(cursor.column_names, result))
         return data
      else:
         return None
   except Exception as e:
      print(e)
      return None
   finally:
      closePool(connection_object, cursor)      

def insertPost(**kwargs):
   try:
      insertColumn = ''
      insertValue = ''

      for key in kwargs:
        insertColumn += f"{ key }, "
        insertValue += f"'{ kwargs[key] }', "

      insertColumn = insertColumn[:-2]
      insertValue = insertValue[:-2]
      
      sql_cmd = f"""
            INSERT INTO posts ({ insertColumn })
            VALUES ({ insertValue })
            """

      connection_object = connection_pool.get_connection()

      if connection_object.is_connected():
         cursor = connection_object.cursor()
         cursor.execute(sql_cmd)
         connection_object.commit()
   except Exception as e:
      print(e)
   finally:
      closePool(connection_object, cursor)        