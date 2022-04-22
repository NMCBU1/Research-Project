# -*- coding: utf-8 -*-


import pandas as pd
import twint
import schedule
import datetime
import time
import nest_asyncio
nest_asyncio.apply()

df = pd.read_csv("consolidado_cantidad_casos_criminalidad_por_anio_mes.csv", sep = ";")
def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + datetime.timedelta(n)

start_dt = datetime.date(2003, 1, 1)
end_dt = datetime.date(2007, 2, 1)
for dt in daterange(start_dt, end_dt):
    df.drop(df[dt.strftime("%Y-%m") == df["Fecha_hecho"]].index, inplace=True)
    
    

def monthplus(date):
    month = int(date.split("-")[1])
    year = int(date.split("-")[0])
    if month < 12:
        newmonth = month + 1
        year = str(year)
    else:
        newmonth = 1
        year = str(year + 1)
    if newmonth < 10:
        return year + "-0" + str(newmonth)
    else:
        return year + "-" + str(newmonth)


def changeday(month, oldday):
    newday = 0
    if oldday != 1:
        newday = oldday -1
    else: 
        if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
            newday = 31
        elif month == 9 or month == 4 or month == 6 or month == 11:
            newday = 30
        else:
            newday = 28
    return newday
    
    
def searchtweets(date, until):
    c = twint.Config()
    c.Search = "Medellin OR medellin OR MEDALLO OR medallo OR MEDELLIN OR Medallo"
    c.Since = date + "-01"
    c.Until = until
    c.Limit = 1000000
    c.Store_csv = True
    c.timedelta = 1
    c.Output = date + ".csv"
    c.Debug = True
    twint.run.Search(c)

def collectfordates():
    for date in df['Fecha_hecho'].unique():
        df2 = pd.read_csv(date + ".csv")
        until = df2["date"][len(df2["date"])-1]
        month = int(until.split("-")[1])
        day = int(until.split("-")[2]) 
        day = changeday(month, day)
        until = until.split("-")[0] + "-" + until.split("-")[1] + "-" + str(day)
        print("collecting tweets for " + date)
        searchtweets(date, until)


collectfordates()

schedule.every(5).minutes.do(collectfordates)
#schedule.every().hour.do(collectfordates)
# schedule.every().day.at("10:30").do(collectfordates)
# schedule.every().monday.do(collectfordates)
# schedule.every().wednesday.at("13:15").do(collectfordates)


while True:
  schedule.run_pending()
  time.sleep(1)