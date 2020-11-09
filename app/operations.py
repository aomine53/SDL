import mysql.connector

config = {
    "user": 'mmlink',
    "password": 'Mmlink@271020',
    "host": '143.110.187.187',
    "database": 'mytestdb'
}


def getdevicedata():
    slu = []
    mydb = mysql.connector.connect(**config)
    mydb.time_zone = '+05:30'
    cursor = mydb.cursor()
    query = 'SELECT SLU FROM devices'
    cursor.execute(query)
    # print(dir(cursor))
    # slu = cursor.fetchall()
    for SLU, in cursor:
        slu.append(SLU)
    cursor.close()
    mydb.close()
    return slu


def getlivedata():
    mydb = mysql.connector.connect(**config)
    mydb.time_zone = '+05:30'

    cursor = mydb.cursor()
    datalist = []
    slulist = getdevicedata()
    for slu in slulist:
        query = "SELECT RNO,VIN,VBAT,EDT,SPDK,LAT,LNG,APPD,TP,CELV,ECT,ES FROM $SLU355000082004871 ORDER BY EDT DESC LIMIT 1"
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
    mydb.time_zone = '+05:30'

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
    query = "SELECT EDT,VIN,VBAT,APPD,TP,SPDK,CELV,ECT,ES FROM $SLU355000082004871 WHERE EDT BETWEEN %s AND %s"
    cursor.execute(query, (start, end))
    for EDT, VIN, VBAT, APPD, TP, SPDK, CELV, ECT, ES in cursor:
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


def getreport():
    mydb = mysql.connector.connect(**config)
    mydb.time_zone = '+05:30'
    Report = []
    cursor = mydb.cursor()
    query = "SELECT TRIPID,STARTEDT,ENDEDT,STARTLAT,ENDLAT,STARTLNG,ENDLNG,STARTODO,ENDODO FROM " \
            "$SLU355000082004871report "
    cursor.execute(query)
    for tripid, startedt, endedt, startlat, endlat, startlng, endlng, startodo, endodo in cursor:
        record = {
            "TripID": tripid,
            "StartTime": startedt,
            "EndTime": endedt,
            'StartLAT': startlat,
            'EndLAT': endlat,
            'StartLNG': startlng,
            'EndLNG': endlng,
            'Distance': endodo - startodo
        }
        Report.append(record)
    return Report


if __name__ == "__main__":
    print(getreport())
# def getparameters():
#     mydb = mysql.connector.connect(**config)
#     mydb.time_zone = '+05:30'
#     cursor = mydb.cursor()
#     slulist = getdevicedata()
#     print(slulist)
#     paralist = []
#     for slu in slulist:
#         query = f"SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_SCHEMA`='mytestdb' AND `TABLE_NAME`= '{slu}'"
#         cursor.execute(query)
#         paralist1 = [i[0] for i in cursor.fetchall()]
#         paralist.append(paralist1)
#
#     #print(cursor.fetchall())
#     print(paralist)
#     cursor.close()
#     mydb.close()
#
#
# getparameters()
# searchdata("2020-10-09 21:36:00","2020-10-09 21:37:00")
# print(type(getdevicedata()))
# print(getdevicedata())
# getlivedata()
# print(searchdata("2020-10-09 21:36:00","2020-10-09 21:37:00"))
