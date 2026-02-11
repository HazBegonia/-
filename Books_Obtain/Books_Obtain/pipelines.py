# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql


class BooksObtainPipeline:
    def __init__(self):
        try:
            self.conn = pymysql.connect(
                host = 'localhost',
                port = 3306,
                user = 'root',
                password = '0716',
                database = 'book_db',
                charset = 'utf8mb4'
            )

            self.cursor = self.conn.cursor()
            print('连接成功')
        except Exception as e:
            print('连接失败')
        
    def process_item(self, item, spider):
        sql = """
            insert into book_info (name, price, subject, stock, reviewers, upc, description, rating, image)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            on duplicate key update name = values(name), price = values(price), stock = values(stock)
        """
        try:
            self.cursor.execute(
                sql, (
                    item['name'], item['price'], item['subject'],
                    item['stock'], item['reviewers'], item['UPC'],
                    item['description'], item['rating'], item['image']
                )
            )
            self.conn.commit()
            print(f"数据库插入成功")
        except Exception as e:
            self.conn.rollback()
            print(f"数据库入库出错: {e}")
        return item
    
    def close_spider(self, spider):
        self.conn.close()
