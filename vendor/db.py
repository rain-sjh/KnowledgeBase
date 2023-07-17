import pymysql

from vendor.base import config


# 链接数据库
# 参数1：mysql服务器所在主机ip
# 参数2：用户名
# 参数3：密码
# 参数4：要链接的数据库名
class Db:
    def __init__(self, table):
        self.Limit = None
        self.db = None
        self.sql = None
        self.Where = ''
        self.WhereAffect = 'AND'
        self.Field = '*'
        self.Table = table
        self.getSql = False
        self.cursor = None
        self.Connection = 'default'

    # 指定数据库名称
    def connection(self, connection):
        self.Connection = connection
        return self

    # 链接数据库
    def connect(self):
        self.db = pymysql.connect(
            host=config(self.Connection, 'hostname'),
            user=config(self.Connection, 'username'),
            password=config(self.Connection, 'password'),
            database=config(self.Connection, 'database'),
            port=int(config(self.Connection, 'hostport')),
        )
        self.cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)

    # 链接数据表,指定表名
    def table(self, table='*'):
        self.Table = table
        return self

    # 链接数据表,指定表名
    def name(self, table='*'):
        self.Table = table
        return self

    # 设置返回条数
    def limit(self, limit=1):
        self.Limit = limit

    # 关闭链接
    def close(self):
        self.cursor.close()
        self.db.close()

    # 构造查询条件,多条件AND
    def condition(self, *param):
        if self.Where:
            self.Where += self.WhereAffect
        match len(param):
            case 1:
                for i, item in enumerate(param[0]):
                    if i != 0:
                        # print(self.Where)
                        self.Where += ' AND '
                    match len(item):
                        case 2:
                            self.Where += '`%s`=\'%s\'' % (str(item[0]), str(item[1]))
                        case 3:
                            self.Where += '`%s`%s\'%s\'' % (str(item[0]), str(item[1]), str(item[2]))
            case 2:
                self.Where += '`%s`=\'%s\'' % (str(param[0]), str(param[1]))
            case 3:
                self.Where += '`%s`%s\'%s\'' % (str(param[0]), str(param[1]), str(param[2]))
        return self

    def where(self, *param):
        self.WhereAffect = ' AND '
        self.condition(*param)
        return self

    def whereOr(self, *param):
        self.WhereAffect = ' OR '
        self.condition(*param)
        return self

    # 设置字段
    def field(self, field):
        self.Field = field
        return self

    # 输出sql
    def fetchSql(self):
        self.getSql = True
        return self

    # 生成查询sql
    def geneSelect(self):
        if self.Limit:
            self.sql = "SELECT %s FROM %s WHERE %s LIMIT %s" % (self.Field, self.Table, self.Where, self.Limit)
        else:
            self.sql = "SELECT %s FROM %s WHERE %s " % (self.Field, self.Table, self.Where)

        return self

    # 单条查询
    def find(self, *param):
        self.where(*param)
        return self.get()

    # 查询单个字段
    def value(self, field):
        self.field(field)
        res = self.get()
        if res is None:
            return res

        return res[field]

    # 查询所有字段
    def select(self):
        return self.get('all')

    # 生成插入sql
    def geneInsert(self, params):
        field, param = '', ''
        i = 0
        for key, item in params.items():
            if i != 0:
                field += ','
                param += ','
            i = 1
            field += '`%s`' % key
            param += '\'%s\'' % item
        self.sql = "INSERT INTO %s (%s) VALUES (%s) " % (self.Table, field, param)
        return self

    # 生成跟新sql
    def geneUpdate(self, params):
        param = ''
        i = 0
        for key, item in params.items():
            if i != 0:
                param += ','
            i = 1
            param += '`%s`=\'%s\'' % (key, item)
        if self.Where:
            self.sql = "UPDATE %s SET %s WHERE %s " % (self.Table, param, self.Where)
        else:
            self.sql = "UPDATE %s SET %s " % (self.Table, param)
        return self

    # 插入或更新一条数据 根据参数是否包含 键 来确定
    # 返回影响条数
    def save(self, param):
        if param.get('id'):
            self.where('id', param['id'])
            return self.update(param)
        elif self.Where:
            return self.update(param)
        else:
            return self.insert(param)

    def delete(self, sql):
        return self._edit(sql)

    def _edit(self, sql):
        count = 0
        try:
            self.count()
            count = self.cursor.execute(sql)
            self.db.commit()
            self.close()
        except:
            print("事物提交失败")
            self.db.rollback()
        return count

    # 查询一条数据
    # 默认 one
    # one 单条查询 all 查询全部
    def get(self, fetch='one'):
        if self.getSql:
            return self.sql
        res = None
        try:
            self.connect()
            if fetch == 'all':
                self.Limit = None
                self.geneSelect()
                self.cursor.execute(self.sql)
                res = self.cursor.fetchall()
            else:
                self.Limit = 1
                self.geneSelect()
                self.cursor.execute(self.sql)
                res = self.cursor.fetchone()
        except Exception as e:
            print('查询失败: %s' % e)
        print(self.sql)
        self.close()
        return res

    # 插入一条数据
    def insert(self, param):
        self.geneInsert(param)
        if self.getSql:
            return self.sql
        res = None
        try:
            self.connect()
            self.Limit = None
            res = self.cursor.execute(self.sql)
            self.db.commit()
        except Exception as e:
            print('插入失败: %s' % e)
        print(self.sql)
        self.close()
        return res

    # 更新多条数据
    def update(self, param):
        self.geneUpdate(param)
        if self.getSql:
            return self.sql
        res = None
        try:
            self.connect()
            self.Limit = None
            res = self.cursor.execute(self.sql)
            self.db.commit()
        except Exception as e:
            print('更新失败: %s' % e)
        print(self.sql)
        self.close()
        return res
