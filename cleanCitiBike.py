from pathlib import Path
import pandas as pd
originPath = '202211-citibike-tripdata_2.csv'

pathList = ['202212-citibike-tripdata_2.csv',
'202301-citibike-tripdata_2.csv',
'202302-citibike-tripdata_2.csv']

readCsv = pd.read_csv(originPath)
df = pd.DataFrame(readCsv)

def unixConvert(timestamp):
    return (pd.to_datetime(timestamp) - pd.Timestamp("1970-01-01")) // pd.Timedelta("1s")

dfTest = df.copy()
dfTest['started_at_unix'] = dfTest['started_at'].apply(unixConvert)
dfTest['ended_at_unix'] = dfTest['ended_at'].apply(unixConvert)
dfTest['trip_duration'] = (round((dfTest['ended_at_unix'] - dfTest['started_at_unix'])/60, 0)).astype(int)
dfTest = dfTest.drop(['started_at_unix', 'ended_at_unix'], axis = 1)
dfTest = dfTest.dropna(axis = 0, how = 'any')
dfTest.to_csv('sampleTableauTextFile.csv')

for i in pathList:  
    readPath = pd.read_csv(i)
    newDf = (pd.DataFrame(readPath)).dropna(axis = 0, how = 'any')
    df = pd.concat([df, newDf], axis = 0)

mergeDf = df.copy()
mergeDf['started_at_unix'] = mergeDf['started_at'].apply(unixConvert)
mergeDf['ended_at_unix'] = mergeDf['ended_at'].apply(unixConvert)
mergeDf['trip_duration'] = (round((mergeDf['ended_at_unix'] - mergeDf['started_at_unix'])/60, 0)).astype(int)
cleanDf = mergeDf.copy()
cleanDf = cleanDf.drop(['started_at_unix', 'ended_at_unix'], axis = 1)

cleanDf.to_csv('citibike-2022-holiday-data.csv')