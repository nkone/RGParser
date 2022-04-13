import pandas as pd
import glob
import os

files = os.path.join("C:\\Users\\CX Lab\\Documents\\RGPrelimAutomation\\", "*.csv")

files = glob.glob(files)
df = pd.concat(map(pd.read_csv, files), ignore_index=True)
df.to_csv('merged.csv')
