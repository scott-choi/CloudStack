import pymysql
import cloudstackException
import sys
import os
class dbConnection(object):
    def __init__(self, host="localhost", port=3306, user='cloud', passwd='cloud', db='cloud'):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.database = db
        
        try:
            self.db = pymysql.Connect(host=host, port=port, user=user, passwd=passwd, db=db)
        except:
            raise cloudstackException.InvalidParameterException(sys.exc_value)
        
    def __copy__(self):
        return dbConnection(self.host, self.port, self.user, self.passwd, self.database)
    
    def close(self):
        try:
            self.db.close()
        except:
            pass
    
    def execute(self, sql=None):
        if sql is None:
            return None
        
        resultRow = []
        cursor = None
        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
        
            result = cursor.fetchall()
            if result is not None:
                for r in result:
                    resultRow.append(r)
            return resultRow
        except pymysql.MySQLError, e:
            if cursor is not None:
                cursor.close()
            raise cloudstackException.dbException("db Exception:%s"%e[1]) 
        except:
            if cursor is not None:
                cursor.close()
            raise cloudstackException.internalError(sys.exc_value)
        
        
    def executeSqlFromFile(self, fileName=None):
        if fileName is None:
            raise cloudstackException.InvalidParameterException("file can't not none")
        
        if not os.path.exists(fileName):
            raise cloudstackException.InvalidParameterException("%s not exists"%fileName)
        
        sqls = open(fileName, "r").read()
        return self.execute(sqls)
    
if __name__ == "__main__":
    db = dbConnection()
    '''
    try:
     
        result = db.executeSqlFromFile("/tmp/server-setup.sql")
        if result is not None:
            for r in result:
                print r[0], r[1]
    except cloudstackException.dbException, e:
        print e
    '''
    print db.execute("update vm_template set name='fjkd' where id=200")
    result = db.execute("select created,last_updated from async_job where id=13")
    print result
    delta = result[0][1] - result[0][0]
    print delta.total_seconds()
    #print db.execute("update vm_template set name='fjkd' where id=200")