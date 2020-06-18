# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 14:37:45 2020

@author: EmileVDH
"""
#PACKAGES
import pandas as pd
import streamlit as st
import os
import numpy as np
import seaborn as sns

st.title("Good Bad EDA Function")

####################import the data csv 
st.header('1. Upload Your Data')
#Widget to upload file
uploaded_file = st.file_uploader("Choose a csv file", type="csv")
#show total records and all the columns imported. 

df=pd.read_csv(uploaded_file)

st.text("Variable list:")
st.table(df.columns)


##    ##select the varible for time limiter variable any calendar object?? 
#time = st.selectbox('Which varible will be your Time Limiter?',df.columns)
##
#time_split_value=st.slider(time) 

# #neeed a between slider 
#df['Bad_Flag']=np.where(df['Months_To_Cancel_Only']<=time_split,1,0)
###make the data set smaller , default for all 

############select the varibles for Y 

st.header('2. Select The Target Varible:')
target = st.selectbox(
    'Which Varible will be your Target?',
    df.columns)


targettype = st.selectbox(
    'Which Varible Type is this Target?',
     ["Continuous", "Categorical"])


if targettype=="Continuous" :
      st.markdown('Max Value for bad:  ')
      target_split_value=st.slider(target)
      df['Bad_Flag']=np.where(df['Months_To_Cancel_Only']<=target_split_value,1,0)
else :
     st.markdown('Your Categories for bad will be  : ')
     targetselectedlist =st.multiselect( 'Select the Categories you want to see as BAD ', df[target].unique())
     df['Bad_Flag']=np.where(df[target].isin(targetselectedlist),1,0)

###CREATE SLIDER FOR ITS FULL DISTRIBUTION 

st.header('3. Here is the Target Varible Statistics:')

st.markdown('Count:')
st.table(df['Bad_Flag'].value_counts())
st.markdown('% :')
st.table(100*df['Bad_Flag'].value_counts(normalize=True))


st.header('4. Select the Feature variable:')
#if categorical selection for what is bad
feature = st.selectbox(
    'Which varible will be your Feature?',
    df.columns)
'You selected: ', feature

featuretype = st.selectbox(
    'Which varible Type is this Feature?',
     ["Continuous", "Categorical "])

#["Continuous", "Categorical (No Grouping Needed) ","Categorical (Grouping Needed) "])
#selectedlist1 =st.multiselect( 'Select the Categories you want to see G1', df[feature].unique(),key=88)
#selectedlist2 =st.multiselect( 'Select the Categories you want to see G2', df[feature].unique(),key=99)
#selectedlist3 =st.multiselect( 'Select the Categories you want to see G3 ', df[feature].unique())


#df[feature]
#if    df[feature].isin(selectedlist1) is True :
#      df[feature1]='G1'
#elif  df[feature].isin(selectedlist2) is True :
#      df[feature1]='G2'  
#else :
#      df[feature1]='G3'

#df[feature] = df[feature].map({'G1' ,selectedlist1
#                                      , 'G2': selectedlist2
#                                      , 'G3': selectedlist3})
#
#st.multiselect('feature values', df[feature])

#st.header(len(selectedlist))
#
#if  len(selectedlist)==0 :
#    df=df[df[feature]]
#else :
#    df=df[df[feature].isin(selectedlist)]

##convert only when its continous and then overwrite the variable

if featuretype=="Continuous" :
     firstLim=float(st.text_input("first limit goes here", int(np.percentile(df[feature], 25))))
     secondLim=float(st.text_input("second limit goes here", int(np.percentile(df[feature], 50))))
     thirdLim=float(st.text_input("third limit goes here", int(np.percentile(df[feature], 75))))
     cut_bins = [0, firstLim, secondLim, thirdLim,1000000000]
     df[feature] = pd.cut(df[feature], bins=cut_bins)
else :
    feature=feature

#df[feature]= np.where(featuretype=="Continous",pd.cut(df[feature], bins=cut_bins),df[feature])

#Show distribution of records and sample persent. 

#height of bad y axis (Not data dependant)
#target_bad_height=st.slider('lim',value=0.3, min_value=0.0, max_value=1.0, step=0.1)

st.header('5. Feature Variable vs Target Variable:')

z=0.3
st.markdown('Volume per category:')
w = sns.catplot(x =feature, hue ="Bad_Flag",  kind ="count", data = df,aspect=2.0) 
st.pyplot()
for p in w.ax.patches:
    txt = str(p.get_height())
    txt_x = p.get_x() 
    txt_y = p.get_height()
    w.ax.text(txt_x,txt_y,txt)
    
st.markdown('Percentage Bad per category:')
g = sns.catplot(x=feature, y='Bad_Flag',data=df, saturation=.5, kind="bar", ci=None, aspect=2.0)
st.pyplot()
    
(g.set_axis_labels(feature , "Default with 6 Months Rate")
 # .set_title('lalala')
.set_titles("{col_name} {col_var}")
.set(ylim=(0, z)) ##adjust for  size of rate 
.despine(left=True))
  
for p in g.ax.patches:
    txt = str(p.get_height().round(2)) #+ '%'
    txt_x = p.get_x() 
    txt_y = p.get_height()
    g.ax.text(txt_x,txt_y,txt)
        
w.set_xticklabels(rotation=65, horizontalalignment='right')
g.set_xticklabels(rotation=65, horizontalalignment='right')
    


##################

#first argument = Variable that must be categorical (Not to many splits)
#second argument = how high you want your bad rate y axis to be (value from 0.0 to 1.0)




######
