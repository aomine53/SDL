import mysql.connector
import os
from datetime import datetime, timedelta
from app.models import *
from userforms.models import *
import string
import random
import pytz

config = {
    "user": 'mmlink',
    "password": 'Mmlink@271020',
    "host": '139.59.28.3',
    "database": 'mytestdb'
}


def get_all_data(device):
    cnx = mysql.connector.connect(**config)
    cnx.time_zone = '+05:30'
    cursor = cnx.cursor()
    for i in device:
        query = f"CREATE TABLE IF NOT EXISTS {i.device_id} (UID varchar(45) DEFAULT NULL,CMD varchar(45) DEFAULT NULL,RNO varchar(45) DEFAULT NULL,EDT datetime NOT NULL,EID varchar(45) DEFAULT NULL,PDT varchar(45) DEFAULT NULL,LAT varchar(45) DEFAULT NULL,LNG varchar(45) DEFAULT NULL,SPD varchar(45) DEFAULT NULL,HEAD varchar(45) DEFAULT NULL,ODO int DEFAULT NULL,LAC varchar(45) DEFAULT NULL,CID varchar(45) DEFAULT NULL,VIN float DEFAULT NULL,VBAT float DEFAULT NULL,TI1 varchar(45) DEFAULT NULL,TS1 varchar(45) DEFAULT NULL,TV1 varchar(45) DEFAULT NULL,TH1 varchar(45) DEFAULT NULL,TD1 varchar(45) DEFAULT NULL,EDSC varchar(45) DEFAULT NULL,TI2 varchar(45) DEFAULT NULL,TS2 varchar(45) DEFAULT NULL,TV2 varchar(45) DEFAULT NULL,TH2 varchar(45) DEFAULT NULL,TD2 varchar(45) DEFAULT NULL,TI3 varchar(45) DEFAULT NULL,TS3 varchar(45) DEFAULT NULL,TV3 varchar(45) DEFAULT NULL,TH3 varchar(45) DEFAULT NULL,TD3 varchar(45) DEFAULT NULL,TI4 varchar(45) DEFAULT NULL,TS4 varchar(45) DEFAULT NULL,TV4 varchar(45) DEFAULT NULL,TH4 varchar(45) DEFAULT NULL,TD4 varchar(45) DEFAULT NULL)"
        cursor.execute(query)
    cursor.close()
    cnx.close()


def get_livedata_device(device):
    cnx = mysql.connector.connect(**config)
    cnx.time_zone = '+05:30'
    cursor = cnx.cursor()
    datalist = []
    for i in device:
        query = f"SELECT {i.device_parameters} FROM {i.device_id} ORDER BY EDT DESC LIMIT 1 "
        cursor.execute(query)
        data = cursor.fetchone()
        datalist.append(data)
    cursor.close()
    cnx.close()
    return datalist


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


def searchdata(start, end, parameters, selecteddevice):
    cnx = mysql.connector.connect(**config)
    cnx.time_zone = '+05:30'
    cursor = cnx.cursor()
    parameters = ",".join(parameters)
    print(parameters)
    query = f"SELECT EDT,{parameters} FROM {selecteddevice} WHERE EDT BETWEEN %s AND %s"
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

    query = f"SELECT LAT,LNG,SPD FROM $SLU355000082004871 WHERE '{endedt}' >= EDT and EDT >= '{startedt}'"
    cursor.execute(query)
    result = cursor.fetchall()
    print(result)
    data = {
        "data": result,
    }
    cursor.close()
    cnx.close()
    return data


def getmap(deviceid, start, end):
    startedt = start.strftime('%Y-%m-%dT%H:%M:%S')
    endedt = end.strftime('%Y-%m-%dT%H:%M:%S')
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    query = f"SELECT LAT,LNG,WBVSPDK FROM {deviceid} WHERE '{endedt}' >= EDT and EDT >= '{startedt}'"
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


def get_anchortag():
    cnx = mysql.connector.connect(**config)
    cnx.time_zone = '+05:30'
    cursor = cnx.cursor()
    datalist = []
    query = "SELECT an0,an0_x,an0_y,an0_z,an0_d,an1,an1_x,an1_y,an1_z,an1_d,an2,an2_x,an2_y,an2_z,an2_d,an3,an3_x," \
            "an3_y,an3_z,an3_d,pos_x,pos_y,pos_z FROM anchor_tag ORDER BY id DESC LIMIT 1 "
    cursor.execute(query)
    data = cursor.fetchone()
    for d in data:
        datalist.append(d)
    cursor.close()
    cnx.close()
    return datalist


def get_tag(tag):
    cnx = mysql.connector.connect(**config)
    cnx.time_zone = '+05:30'
    cursor = cnx.cursor()
    datalist = []
    query = f"SELECT tag_x,tag_y,tag_z FROM {tag} ORDER BY id DESC LIMIT 1 "
    cursor.execute(query)
    data = cursor.fetchone()
    for d in data:
        datalist.append(d)
    cursor.close()
    cnx.close()
    return datalist


# Archive Data for solardevice
# def get_solar_data(SCB, fromdate, todate):
#     cnx = mysql.connector.connect(**config)
#     cursor = cnx.cursor(buffered=True)
#     query = f"SELECT * FROM {SCB}  where  '{fromdate}' <= Date and Date <= '{todate}' "
#     cursor.execute(query)
#     data = cursor.fetchall()
#     print(data)
#     cursor.close()
#     cnx.close()
#     return data


def search_solardata(start, end, parameters, selecteddevice, weather):
    cnx = mysql.connector.connect(**config)
    cnx.time_zone = '+05:30'
    cursor = cnx.cursor()
    print(parameters)
    data = []
    parameters = "`,`".join(parameters)
    # {'`%s`' + (',`%s`' * (len(parameters) - 1))}
    for device in selecteddevice:
        query = f"SELECT Date,`{parameters}` FROM {device} WHERE Date BETWEEN '{start}' AND '{end}'"
        # print(query)
        cursor.execute(query)
        data.append(cursor.fetchall())
    if len(weather) != 0:
        weather = "`,`".join(weather)
        query1 = f"SELECT Date,`{weather}` FROM wms WHERE Date BETWEEN '{start}' AND '{end}'"
        cursor.execute(query1)
        data.append(cursor.fetchall())
    cursor.close()
    cnx.close()
    return data


# Live data of solardevice
def get_livedata_solar(device):
    cnx = mysql.connector.connect(**config)
    cnx.time_zone = '+05:30'
    cursor = cnx.cursor(buffered=True)
    datalist = []
    IST = pytz.timezone('Asia/Kolkata')
    # print(datetime.now(IST).strftime('%Y-%m-%d %H:%M:%S'))
    if int(datetime.now(IST).strftime('%M')) % 5 == 0:
        date = datetime.now(IST)
    elif int(datetime.now(IST).strftime('%M')) % 5 <= 5:
        date = datetime.now(IST) - timedelta(minutes=int(datetime.now(IST).strftime('%M')) % 5)

    updateddate = "2021-01-23 " + date.strftime('%H:%M') + ":00"

    for i in device:
        # device_parameters = (",").join(get_solar_column_name(i))
        # print(device_parameters)
        # {'%s' + (',%s' * (len(get_solar_column_name(i)) - 1))}
        query = f"SELECT * FROM {i} where Date = '{updateddate}'"
        cursor.execute(query)
        data = cursor.fetchone()
        data = list(data)
        data[0] = data[0].replace(day=datetime.now(IST).day, month=datetime.now().month, year=datetime.now().year)
        # print(data[0])
        datalist.append(data)
    cursor.close()
    cnx.close()
    return datalist


# to get the parameter names of device
def get_solar_column_name(devicename):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(buffered=True)
    query = f"SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_SCHEMA`='mytestdb' AND `TABLE_NAME`='{devicename}' ORDER BY ORDINAL_POSITION    "
    cursor.execute(query)
    col_name = []
    data = cursor.fetchall()
    # [('Date',), ('STB 2.2.2 - 1 - I1 [A]',), ('STB 2.2.2 - 1 - I10 [A]',), ('STB 2.2.2 - 1 - I11 [A]',), ('STB 2.2.2 - 1 - I12 [A]',), ('STB 2.2.2 - 1 - I13 [A]',), ('STB 2.2.2 - 1 - I14 [A]',), ('STB 2.2.2 - 1 - I15 [A]',), ('STB 2.2.2 - 1 - I16 [A]',), ('STB 2.2.2 - 1 - I2 [A]',), ('STB 2.2.2 - 1 - I3 [A]',), ('STB 2.2.2 - 1 - I4 [A]',), ('STB 2.2.2 - 1 - I5 [A]',), ('STB 2.2.2 - 1 - I6 [A]',), ('STB 2.2.2 - 1 - I7 [A]',), ('STB 2.2.2 - 1 - I8 [A]',), ('STB 2.2.2 - 1 - I9 [A]',), ('STB 2.2.2 - 1 - Total power [W]',), ('STB 2.2.2 - 1 - Total voltage [V]',)]
    for d in range(0, len(data)):
        # print(d[0])
        col_name.append(data[d][0])
    # print(col_name)

    cursor.close()
    cnx.close()
    return col_name


def solar_genration():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(buffered=True)
    query = f"SELECT `Power AC (Inv 5.1) [W]` FROM inv_1"
    cursor.execute(query)
    data = cursor.fetchall()
    newdata = []
    solardata = [0 for i in range(24)]
    for d, in data:
        newdata.append(d)
    for i in range(0, len(newdata)):
        solardata[i // 12] += newdata[i]/12000

    cursor.close()
    cnx.close()
    return solardata


#
# def abcd(devices, parameters):
#     cnx = mysql.connector.connect(**config)
#     cnx.time_zone = '+05:30'
#     cursor = cnx.cursor(buffered=True)
#     # devices = ["SCB1",SCB2]
#     # params = ["I1"]
#
#     IST = pytz.timezone('Asia/Kolkata')
#     # print(datetime.now(IST).strftime('%Y-%m-%d %H:%M:%S'))
#     if int(datetime.now(IST).strftime('%M')) % 5 == 0:
#         date = datetime.now(IST)
#     elif int(datetime.now(IST).strftime('%M')) % 5 <= 5:
#         date = datetime.now(IST) - timedelta(minutes=int(datetime.now(IST).strftime('%M')) % 5)
#
#     updateddate = "2021-01-23 " + date.strftime('%H:%M') + ":00"
#
#     str1 = []
#     for d in devices:
#         for p in parameters:
#             # print(d + "." + p)
#             str = d + "." + p
#             str1.append(str)
#
#     # convert into tuple
#     str2 = tuple(str1)
#     # to get SCB1.I1,SCB1.I2,SCB2.I1,SCB2.I2
#     str3 = ",".join(str2)
#     print(str3)
#     # to get device list like SCB1,SCB2
#     str4 = tuple(devices)
#     str5 = ",".join(str4)
#     print(str5)
#
#     query = f"SELECT {str3} from {str5} where %s.Date = %s.Date"
#     cursor.execute(query)
#     data = cursor.fetchall()
#     print(data)
#     cursor.close()
#     cnx.close()


def random_string(len):
    res = ''.join(random.choices(string.ascii_uppercase +
                                 string.digits, k=len))
    return res


if __name__ == "__main__":
    # print(get_device_parameters('$SLU355000082004871'))
    # # get_anchortag()
    # get_solar_data('SCB2', '2021-01-23 09:55:00', '2021-01-23 12:55:00')
    # print((',').join(get_solar_column_name('inv_1')))
    # print(get_livedata_solar(["SCB1", "SCB2", "SCB3", "inv_1"]))
    # print(search_solardata("2021-01-23 14:35:00", "2021-01-23 14:45:00",
    #                        ['I1', 'I10'], ["SCB1", "SCB2"], ["Ambient Temp", "Irradiance"]))
    # abcd(['SCB1', 'SCB2'], ["I1", "I2"])
    print(solar_genration())
    # print(getdevicedata())
    # # print(getlivedata())
    # device = Device.objects.filter(firm=FirmProfile.objects.get(user=User.objects.get(username="machinemath")))
    # print(get_livedata_device(device))
    # print(getdeviceinfo("machinemath"))
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
