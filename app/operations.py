import mysql.connector

config = {"user": 'root',
          "password": '1234',
          "host": '127.0.0.1',
          "database": 'mytestdb'
          }


def getdevicedata():
    slu = []
    mydb = mysql.connector.connect(**config)
    cursor = mydb.cursor()
    query = 'SELECT SLU FROM devices'
    cursor.execute(query)
    # print(dir(cursor))
    # slu = cursor.fetchall()
    for SLU in cursor:
        slu.append(SLU[0])
    cursor.close()
    mydb.close()
    return slu


def getlivedata():
    mydb = mysql.connector.connect(**config)
    cursor = mydb.cursor()
    datalist = []
    slulist = getdevicedata()
    for slu in slulist:
        query = "SELECT RNO,VIN,VBAT,EDT,SPDK,LAT,LNG,APPD,TP,CELV,ECT,ES FROM $slu355000082004871 ORDER BY EDT DESC LIMIT 1"
        cursor.execute(query)
        datalist.append(cursor.fetchone())

    # print(datalist)
    # rno,vin,vbat,edt,spdk,lat,lng = cursor.fetchone()
    cursor.close()
    mydb.close()
    # return rno,vin,vbat,edt,spdk,lat,lng
    return datalist


def searchdata(start, end):
    mydb = mysql.connector.connect(**config)
    cursor = mydb.cursor()
    edt = []
    vin = []
    vbat = []
    appd = []
    tp = []
    spdk = []
    celv = []
    ect = []
    es = []
    query = "SELECT EDT,VIN,VBAT,APPD,TP,SPDK,CELV,ECT,ES FROM $slu355000082004871 WHERE EDT BETWEEN %s AND %s"
    cursor.execute(query, (start, end))
    for EDT, VIN, VBAT, APPD, TP,SPDK,CELV,ECT,ES in cursor:
        edt.append(EDT)
        vin.append(VIN)
        vbat.append(VBAT)
        appd.append(APPD)
        tp.append(TP)
        spdk.append(SPDK)
        celv.append(CELV)
        ect.append(ECT)
        es.append(ES)

    cursor.close()
    mydb.close()
    return edt, vin, vbat, appd, tp, spdk, celv, ect, es

# searchdata("2020-10-09 21:36:00","2020-10-09 21:37:00")
# print(type(getdevicedata()))
# print(getdevicedata())
# getlivedata()
# print(searchdata("2020-10-09 21:36:00","2020-10-09 21:37:00"))
