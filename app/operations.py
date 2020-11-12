import mysql.connector
from datetime import datetime, timedelta

config = {
    "user": 'mmlink',
    "password": 'Mmlink@271020',
    "host": '143.110.187.187',
    "database": 'mytestdb'
}


def getdevicedata():
    slu = []
    cnx = mysql.connector.connect(**config)
    cnx.time_zone = '+05:30'
    cursor = cnx.cursor()
    query = 'SELECT SLU FROM devices'
    cursor.execute(query)
    # print(dir(cursor))
    # slu = cursor.fetchall()
    for SLU, in cursor:
        slu.append(SLU)
    cursor.close()
    cnx.close()
    return slu


def getlivedata():
    cnx = mysql.connector.connect(**config)
    cnx.time_zone = '+05:30'

    cursor = cnx.cursor()
    datalist = []
    device_list = getdevicedata()
    for _ in device_list:
        query = "SELECT RNO,VIN,VBAT,EDT,SPDK,LAT,LNG,APPD,TP,CELV,ECT,ES FROM $SLU355000082004871 ORDER BY EDT DESC LIMIT 1"
        cursor.execute(query)
        datalist.append(cursor.fetchone())

    # print(datalist)
    # rno,vin,vbat,edt,spdk,lat,lng = cursor.fetchone()
    cursor.close()
    cnx.close()
    # return rno,vin,vbat,edt,spdk,lat,lng
    return datalist


def searchdata(start, end):
    cnx = mysql.connector.connect(**config)
    cnx.time_zone = '+05:30'

    cursor = cnx.cursor()
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
    cnx.close()
    return edt, vin, vbat, appd, tp, spdk, celv, ect, es


def getreport():
    cnx = mysql.connector.connect(**config)
    cnx.time_zone = '+05:30'
    Report = []
    cursor = cnx.cursor()
    query = "SELECT TRIPID,STARTEDT,ENDEDT,STARTADDRESS,ENDADDRESS,STARTODO,ENDODO FROM " \
            "$SLU355000082004871report ORDER BY TRIPID DESC"
    cursor.execute(query)
    record = {
        "TripID": '-',
        "StartTime": '-',
        "EndTime": '-',
        'Duration': '-',
        'StartAddress': '-',
        'EndAddress': '-',
        'Distance': '-',
    }

    for tripid, startedt, endedt, startadd, endadd, startodo, endodo in cursor:
        if startedt is not None and endedt is not None:
            record = {
                "TripID": tripid,
                "StartTime": startedt.strftime('%Y-%m-%d %H:%M:%S'),
                "EndTime": endedt.strftime('%Y-%m-%d %H:%M:%S'),
                'Duration': f"{round((endedt - startedt).total_seconds() / 60)} Minutes",
                'StartAddress': startadd,
                'EndAddress': endadd,
                'Distance': endodo - startodo
            }
        elif endedt is None:
            record = {
                "TripID": tripid,
                "StartTime": startedt.strftime('%Y-%m-%d %H:%M:%S'),
                "EndTime": '-',
                'Duration': '-',
                'StartAddress': startadd,
                'EndAddress': '-',
                'Distance': '-'
            }
        else:
            record = {
                "TripID": '-',
                "StartTime": '-',
                "EndTime": '-',
                'Duration': '-',
                'StartAddress': '-',
                'EndAddress': '-',
                'Distance': '-',
            }
        Report.append(record)

    if cursor.rowcount == 0:
        Report.append(record)
    cursor.close()
    cnx.close()
    return Report


def getmapreport(tripid):
    cnx = mysql.connector.connect(**config)
    cnx.time_zone = '+05:30'
    cursor = cnx.cursor()
    query = "SELECT TRIPID,STARTEDT,ENDEDT,STARTLAT,ENDLAT,STARTLNG,ENDLNG,STARTODO,ENDODO FROM " \
            f"$SLU355000082004871report where TRIPID = {tripid}"
    cursor.execute(query)
    result = cursor.fetchone()
    startedt = result[1].strftime('%Y-%m-%dT%H:%M:%S')
    endedt = result[2].strftime('%Y-%m-%dT%H:%M:%S')

    query = f"SELECT LAT,LNG,WBVSPDK FROM $SLU355000082004871 WHERE '{endedt}' >= EDT and EDT >= '{startedt}'"
    cursor.execute(query)
    result = cursor.fetchall()
    print(result)
    data = {
        "data": result,
    }
    cursor.close()
    cnx.close()
    return data


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
