import pandas as pd

df = pd.read_csv('1tarihduzenlenmis.csv', usecols=['FL_DATE', 'AIRLINE', 'DOT_CODE', 'FL_NUMBER', 
                                             'ORIGIN', 'ORIGIN_CITY', 'DEST', 'DEST_CITY', 
                                             'CRS_DEP_TIME', 'CRS_ARR_TIME', 'CANCELLED', 
                                             'CRS_ELAPSED_TIME', 'DISTANCE'])

df.to_csv('2gereksizsutunlarsilinmis.csv', index=False)
