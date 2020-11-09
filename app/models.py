# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Mmlinkdata1(models.Model):
    uid = models.CharField(db_column='UID', max_length=45, blank=True, null=True)  # Field name made lowercase.
    cmd = models.CharField(db_column='CMD', max_length=45, blank=True, null=True)  # Field name made lowercase.
    rno = models.CharField(db_column='RNO', max_length=45, blank=True, null=True)  # Field name made lowercase.
    edt = models.DateTimeField(db_column='EDT', primary_key=True)  # Field name made lowercase.
    eid = models.CharField(db_column='EID', max_length=45, blank=True, null=True)  # Field name made lowercase.
    pdt = models.CharField(db_column='PDT', max_length=45, blank=True, null=True)  # Field name made lowercase.
    lat = models.CharField(db_column='LAT', max_length=45, blank=True, null=True)  # Field name made lowercase.
    lng = models.CharField(db_column='LNG', max_length=45, blank=True, null=True)  # Field name made lowercase.
    spdk = models.CharField(db_column='SPDK', max_length=45, blank=True, null=True)  # Field name made lowercase.
    head = models.CharField(db_column='HEAD', max_length=45, blank=True, null=True)  # Field name made lowercase.
    odo = models.CharField(db_column='ODO', max_length=45, blank=True, null=True)  # Field name made lowercase.
    lac = models.CharField(db_column='LAC', max_length=45, blank=True, null=True)  # Field name made lowercase.
    cid = models.CharField(db_column='CID', max_length=45, blank=True, null=True)  # Field name made lowercase.
    vin = models.FloatField(db_column='VIN', blank=True, null=True)  # Field name made lowercase.
    vbat = models.FloatField(db_column='VBAT', blank=True, null=True)  # Field name made lowercase.
    ti1 = models.CharField(db_column='TI1', max_length=45, blank=True, null=True)  # Field name made lowercase.
    ts1 = models.CharField(db_column='TS1', max_length=45, blank=True, null=True)  # Field name made lowercase.
    tv1 = models.CharField(db_column='TV1', max_length=45, blank=True, null=True)  # Field name made lowercase.
    th1 = models.CharField(db_column='TH1', max_length=45, blank=True, null=True)  # Field name made lowercase.
    td1 = models.CharField(db_column='TD1', max_length=45, blank=True, null=True)  # Field name made lowercase.
    edsc = models.CharField(db_column='EDSC', max_length=45, blank=True, null=True)  # Field name made lowercase.
    ti2 = models.CharField(db_column='TI2', max_length=45, blank=True, null=True)  # Field name made lowercase.
    ts2 = models.CharField(db_column='TS2', max_length=45, blank=True, null=True)  # Field name made lowercase.
    tv2 = models.CharField(db_column='TV2', max_length=45, blank=True, null=True)  # Field name made lowercase.
    th2 = models.CharField(db_column='TH2', max_length=45, blank=True, null=True)  # Field name made lowercase.
    td2 = models.CharField(db_column='TD2', max_length=45, blank=True, null=True)  # Field name made lowercase.
    ti3 = models.CharField(db_column='TI3', max_length=45, blank=True, null=True)  # Field name made lowercase.
    ts3 = models.CharField(db_column='TS3', max_length=45, blank=True, null=True)  # Field name made lowercase.
    tv3 = models.CharField(db_column='TV3', max_length=45, blank=True, null=True)  # Field name made lowercase.
    th3 = models.CharField(db_column='TH3', max_length=45, blank=True, null=True)  # Field name made lowercase.
    td3 = models.CharField(db_column='TD3', max_length=45, blank=True, null=True)  # Field name made lowercase.
    ti4 = models.CharField(db_column='TI4', max_length=45, blank=True, null=True)  # Field name made lowercase.
    ts4 = models.CharField(db_column='TS4', max_length=45, blank=True, null=True)  # Field name made lowercase.
    tv4 = models.CharField(db_column='TV4', max_length=45, blank=True, null=True)  # Field name made lowercase.
    th4 = models.CharField(db_column='TH4', max_length=45, blank=True, null=True)  # Field name made lowercase.
    td4 = models.CharField(db_column='TD4', max_length=45, blank=True, null=True)  # Field name made lowercase.
    col36 = models.CharField(max_length=45, blank=True, null=True)
    col37 = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mmlinkdata_1'
