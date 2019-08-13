import os
import glob
import logging
import datetime
import pandas
date = str(datetime.date.today())

def concatenate(indir=f"D://News_Spider/News_Spider/Crawled data/Links/Links{date}", outfile= "D://News_Spider/News_Spider/Crawled data/AllLinks.csv" ):
    os.chdir(indir)
    fileList= glob.glob("*.csv")
    dfList=[]
    for filename in fileList:
        df =pandas.read_csv(filename,header=None)
        dfList.append(df)
    concatDF= pandas.concat(dfList, axis = 0, sort= True)
    logging.info("All csv files containing links being concatenated into one csv file- AllLinks.csv")
    concatDF.to_csv(outfile,header=None, index=False)


