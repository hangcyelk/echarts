# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import json
import pandas as pd
import codecs
import numpy as np

nodes_df = pd.read_csv(r"D:\work\Neo4j\echarts\emission.csv",header=0)
relation_df = pd.read_csv(r"D:\work\Neo4j\echarts\relation.csv",header=0)

#nodes_df['idx'] = nodes_df.index 

#node json
nodes_df = nodes_df.iloc[:,:6]
nodes = nodes_df.rename(index =str, columns = {"清单属性":'category'})
category = nodes.category.unique()
nodes['category'] = nodes['category'].astype('category')
nodes['category'] = nodes['category'].cat.codes
nodes_dict = nodes.to_dict('records')


#relation json 
links = pd.DataFrame(columns=["source","target"]) 

for row in range(len(relation_df)):
    tempsource = relation_df['上级排放源编号'][row]
    temptarget = relation_df['清单ID'][row]
    source_idx = nodes.index[nodes['清单ID'] == tempsource].tolist()
    target_idx = nodes.index[nodes['清单ID'] == temptarget].tolist()
    tempdict = {}
    if source_idx != []:
        tempdict['source'] = source_idx[0] 
        tempdict['target'] = target_idx[0] 
        links = links.append(tempdict,ignore_index=True)
    else:
        continue 

links_dict = links.to_dict('records')
#category json
categories = pd.DataFrame(columns=["name","keyword","base"]) 
for i in range(len(category)):
    tempdict = {}
    tempdict['name'] = category[i]
    tempdict['base'] = category[i]+"base"
    categories = categories.append(tempdict,ignore_index=True)
cate_dict = categories.to_dict('records')

with open(r"D:\work\Neo4j\echarts\webkit-dep.json",'r') as load_f:
    load_dict = json.load(load_f)

load_dict['nodes'] = nodes_dict
load_dict['links'] = links_dict
load_dict['categories'] = cate_dict

jsonObject = codecs.open(r"D:\work\Neo4j\echarts\webkit-dep_self.json","w",encoding="utf-8")
jsonString = json.dump(load_dict,jsonObject,ensure_ascii=False)
jsonObject.close()