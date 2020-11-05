import json
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import SimpleStatement
import os

keyspace='test'
              
def cassandraBDProcess(json_sentencia):
     
    sent_added=False

    #Connect to Cassandra
    objCC=CassandraConnection()
    cloud_config= {
        'secure_connect_bundle':objCC.cc_secureBundle
    }
    
    auth_provider = PlainTextAuthProvider(objCC.cc_user_test,objCC.cc_pwd_test)
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect()
    session.default_timeout=70
    row=''
    pdfname=json_sentencia['pdfname']
    #Check wheter or not the record exists, check by numberFile and date
    #Date in cassandra 2020-09-10T00:00:00.000+0000
    querySt="select id from "+keyspace+".tbcourtdecisiontfjfa where pdfname='"+str(pdfname)+"'  ALLOW FILTERING"
                
    future = session.execute_async(querySt)
    row=future.result()
        
    if row: 
        sent_added=False
        cluster.shutdown()
    else:        
        #Insert Data as JSON
        jsonS=json.dumps(json_sentencia,ensure_ascii=True)           
        insertSt="INSERT INTO "+keyspace+".tbcourtdecisiontfjfa JSON '"+jsonS+"';" 
        future = session.execute_async(insertSt)
        future.result()  
        sent_added=True
        cluster.shutdown()     
                    
                         
    return sent_added

def updatePage(strquery,page):

    #Connect to Cassandra
    objCC=CassandraConnection()
    cloud_config= {
        'secure_connect_bundle':objCC.cc_secureBundle
    }
    
    auth_provider = PlainTextAuthProvider(objCC.cc_user_test,objCC.cc_pwd_test)
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect()
    session.default_timeout=70
    row=''
    page=str(page)
    querySt="update "+keyspace+".cjf_control set page="+page+" where query='"+strquery+"' and id_control=2;"          
    future = session.execute_async(querySt)
    row=future.result()
                         
    return True

def getPageAndTopic():

    #Connect to Cassandra
    objCC=CassandraConnection()
    cloud_config= {
        'secure_connect_bundle':objCC.cc_secureBundle
    }
    
    auth_provider = PlainTextAuthProvider(objCC.cc_user_test,objCC.cc_pwd_test)
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect()
    session.default_timeout=70
    row=''
    #select page from  thesis.cjf_control where id_control=1 and query='Primer circuito'
    querySt="select query,page from "+keyspace+".cjf_control where id_control=2  ALLOW FILTERING"
                
    future = session.execute_async(querySt)
    row=future.result()
    lsInfo=[]
        
    if row: 
        for val in row:
            lsInfo.append(str(val[0]))
            lsInfo.append(str(val[1]))
            print('Value from cassandra:',str(val[0]))
            print('Value from cassandra:',str(val[1]))
        cluster.shutdown()
                    
                         
    return lsInfo    

   
class CassandraConnection():
    cc_user='quartadmin'
    cc_pwd='P@ssw0rd33'
    cc_user_test='test'
    cc_pwd_test='testquart'
    cc_secureBundle='/app/appCode/secure-connect-dbtest.zip'
        

