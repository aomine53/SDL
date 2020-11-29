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
    for slu in device_list:
        query = f"SELECT RNO,VIN,VBAT,EDT,SPD,LAT,LNG FROM {slu} ORDER BY EDT DESC LIMIT 1 "
        cursor.execute(query)
        data = cursor.fetchone()
        if data is not None:
            datalist.append(data)

    # print(datalist)
    # rno,vin,vbat,edt,spdk,lat,lng = cursor.fetchone()
    cursor.close()
    cnx.close()
    # return rno,vin,vbat,edt,spdk,lat,lng
    return datalist


def searchdata(start, end, parameters):
    cnx = mysql.connector.connect(**config)
    cnx.time_zone = '+05:30'
    cursor = cnx.cursor()
    parameters = ",".join(parameters)
    print(parameters)
    query = f"SELECT EDT,{parameters} FROM $SLU355000082004871 WHERE EDT BETWEEN %s AND %s"
    cursor.execute(query, (start, end))
    data = cursor.fetchall()
    cursor.close()
    cnx.close()
    return data


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

    query = f"SELECT LAT,LONG,WBVSPDK FROM $SLU355000082004871 WHERE '{endedt}' >= EDT and EDT >= '{startedt}'"
    cursor.execute(query)
    result = cursor.fetchall()
    print(result)
    data = {
        "data": result,
    }
    cursor.close()
    cnx.close()
    return data


def get_device_parameters(device_id):
    cnx = mysql.connector.connect(**config)
    cnx.time_zone = '+05:30'
    cursor = cnx.cursor()
    device_parameters = []
    query = "SELECT PARAM FROM deviceinfo where DEVICEID=%s"
    cursor.execute(query, (device_id,))
    device_parameters = [i[0] for i in cursor.fetchall()]
    device_parameters = device_parameters[0].split(",")
    cursor.close()
    cnx.close()
    return device_parameters


if __name__ == "__main__":
    # print(get_device_parameters('$SLU355000082004871'))
    print(getdevicedata())
    print(getlivedata())
    # parameters = ",".join(get_device_parameters('$SLU355000082004871'))
    # print(parameters)
    # print(searchdata("2020-11-05 21:36:00", "2020-11-05 21:37:00",get_device_parameters('$SLU355000082004871')))
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
#  searchdata("2020-10-09 21:36:00","2020-10-09 21:37:00",)
# print(type(getdevicedata()))
# print(getdevicedata())
# getlivedata()
# print(searchdata("2020-10-09 21:36:00","2020-10-09 21:37:00"))
