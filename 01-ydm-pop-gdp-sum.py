# -*- coding: utf-8 -*-
'''
* Updated on 2020/09/30
* python3
**
* summarize economic index in YDM
* features:
* - two index: population and GDP,
* - export in csv format.
'''

import pandas as pd
import pathlib, time, re
import numpy as np
from pypinyin import lazy_pinyin, Style

folder = pathlib.Path('pop-gdp-db')
#list of cities
cities = pd.read_csv(folder / 'ydm-city-list.csv', names=['cities'])['cities'].to_list()
#mark string contained in the headers
marks = {
	'population': '年末总人口',
	'gdp': 'GDP'
	}
for ikey, key in enumerate(marks):
	for icity, city in enumerate(cities):
		#access the original data
		file_city = folder / '{}.csv'.format(city)
		data_city = pd.read_csv(file_city, index_col='时间(年)')
		#filter the specific column by mark
		subdata = data_city.filter(regex=marks[key])
		#check. If multi-columns exist, prompt a warning.
		if len(subdata.columns)!=1:
			print('Warning -- {} -- {} -- does NOT exist.'.format(city, key))
			time.sleep(5)
			continue
		#rename
		subdata = subdata.rename(columns={subdata.columns[0]:city})
		print(key, city, icity)
		#join cities
		if icity==0:
			data = subdata
		else:
			data = data.join(subdata, how='outer')
	#descending order
	data.sort_index(ascending=False, inplace=True)
	
	#export by cities
	filename = folder / 'ydm-city-{}.csv'.format(key)
	data.to_csv(filename)
	
	#sum and join
	sum = pd.DataFrame(data.dropna().sum(axis=1), columns=[key])
	if ikey==0:
		merge = sum
	else:
		merge = merge.join(sum, how='outer')

#rename header of index
merge.index.name = 'year'
#descending order
merge.sort_index(ascending=False, inplace=True)
#export
filename = folder / 'ydm-pop-gdp.csv'.format(key)
merge.to_csv(filename)

print('Done')