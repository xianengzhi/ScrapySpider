# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import pymongo
from openpyxl import Workbook
import logging



class JobspiderPipeline:
    def process_item(self, item, spider):

        return item
    pass
# 保存到excel
class ExcelPipeline(object):
    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(['省', '市', '区', '小区名', '小区详情页链接', '详细地址', '经纬度', '交通',
                        '参考价格', '物业类型', '物业费', '总建面积', '总户数', '竣工时间', '停车位', '容积率', '绿化率',
                        '物业公司', '开发商'])

    def process_item(self, item, spider):
        line = [item['province'], item['city'], item['district'], item['name'], item['url'], item['detail_address'],
                item['coord'], item['traffic'], item['price'], item['property_type'],
                item['property_fee'], item['area'], item['house_count'], item['completion_time'], item['parking_count'],
                item['plot_ratio'], item['greening_rate'], item['property_company'], item['developers']]
        self.ws.append(line)
        # keys = spider.settings.get('KEYS')
        self.wb.save('../小区' + '.xlsx')
        return item
# 写入mysql
class MysqlPipeline(object):
    """
    同步操作
    """
    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        pass

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            port=crawler.settings.get('MYSQL_PORT'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            database=crawler.settings.get('MYSQL_DATABASE'),
        )
    def open_spider(self, spider):
        # 建立连接
        self.db = pymysql.connect(self.host, self.user, self.password, self.database,port=self.port, charset='utf8')
        # 创建游标
        self.cursor = self.db.cursor()
 
    def process_item(self,item,spider):
        keys = ','.join(item.keys())
        values = ','.join(['%s']*len(item))
        updateKeyValue = ','.join(['%s=%r' % (k, item[k]) for k in item])

        # sql语句
        sql = 'insert into %s(%s) values(%s) ON DUPLICATE KEY UPDATE %s' % (item.table,keys,values,updateKeyValue)
        sql_param = tuple(item.values())

        # print('-----开始写入数据库')
        # print('item.table',item.table)
        # print('sql',sql)
        # print('sql_param',sql_param)
        # print('--------结束写入数据库')

        # 执行插入数据到数据库操作
        self.cursor.execute(sql,sql_param)
        # 提交，不进行提交无法保存到数据库
        self.db.commit()
        # try:
        #     # 执行插入数据到数据库操作
        #     self.cursor.execute(sql,sql_param)
        #     # 提交，不进行提交无法保存到数据库
        #     self.db.commit()
        # except Exception as erp'ri
        #     logging.log(error)
        # return item
 
    def close_spider(self,spider):
        # 关闭游标和连接
        self.cursor.close()
        self.db.close()

# 写入mongodb
class MongoPipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        collection_name = item.__class__.__name__
        self.db[collection_name].insert(dict(item))
        return item
