#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 16:53:27 2020

@author: macpro
"""

# scraping data for 2018

from bs4 import BeautifulSoup
import urllib.request

user_name_list = []
content_list = []
post_list = []

for p in [0, 50, 100]:
    URL = 'https://mathematicsgre.com/viewtopic.php?f=1&t=3867&start='f'{p}'
    page = urllib.request.urlopen(URL)
    soup = BeautifulSoup(page, 'html.parser')
    print(soup.prettify())

    user_name = soup.find_all('a', attrs={'class': 'username'})
    
    for a in user_name:
        user_name_list.append(a.getText().split('\n')[0])
        #print(user_name_list)

    content = soup.find_all('div', attrs={'class': 'content'})
    
    for div in content:
        content_list.append(div.getText().split('\n')[0])
        #print(content_list)

    
    for i in range(len(content)):
        post_list.append(content[i].getText().split('\n'))
        
# print length for each post

    for post in range(len(post_list)):
        print(len(post_list[post]))
    
# print type for each post
    
    for post in range(len(post_list)):
        print(type(post_list[post]))         
        
# remove first template post 
    
del post_list[0]         
        
# unique user names
        
unique_user_list = list(dict.fromkeys(user_name_list))

# remove the first user name as template name and others

del unique_user_list[0]          
        
# indices for useless posts without 'applying to where' expression
        
boolean_useless = []  
for i in range(len(post_list)):
    k = False
    for j in range(len(post_list[i])):
        if 'applying to where' in post_list[i][j].lower():
            k = True
    boolean_useless.append(k)


index_usefull = [i for i, x in enumerate(boolean_useless) if x]         
        
# create temp list without useless posts

post_temp = []
for ind in index_usefull:
     post_temp.append(post_list[ind])          
               
# Applying to 
        
applying_list = []

for i in range(len(post_temp)):
    for j in range(len(post_temp[i])):
        if 'applying to where' in post_temp[i][j].lower():
            applying_list.append(post_temp[i][j:len(post_temp[i])])  
            break          
        
# acceptance list
            
acceptance_words = ['accepted', 'acceptance', 'admitted']         
            
accepted_list = []
for i in range(len(applying_list)):
    count = 0
    for j in range(len(applying_list[i])):
        for word in acceptance_words:
            if word in applying_list[i][j].lower():
                count += 1
                
    accepted_list.append(count)        
        
# rejection list
    
rejection_words = ['reject']
                
rejected_list = []
for i in range(len(applying_list)):
    count = 0
    for j in range(len(applying_list[i])):
        for word in rejection_words:
            if word in applying_list[i][j].lower():
                count += 1
    rejected_list.append(count)         
        
# number of universities applied to
    
universities = []

for i in range(len(accepted_list)):
    universities.append(accepted_list[i]+rejected_list[i])           
        
# create final post_list without zero universities
    
index_zero = []
for i in range(len(universities)):
    if universities[i] == 0:
        index_zero.append(i)
        
index_not_zero = []
for i in range(len(universities)):
    if universities[i] != 0:
        index_not_zero.append(i)


post_final = []
for ind in index_not_zero:
     post_final.append(post_temp[ind])   

# delete zero universities from accepted_list
     
for ind in sorted(index_zero, reverse=True):
    del accepted_list[ind]
    
# delete zero universities from rejected_list
     
for ind in sorted(index_zero, reverse=True):
    del rejected_list[ind]
    
# delete zero universities from universities
     
for ind in sorted(index_zero, reverse=True):
    del universities[ind]      
        
# Major(s) list

major_list =[]

for i in range(len(post_final)):
    r = 'NA'
    for j in range(len(post_final[i])):
        if "Major" in post_final[i][j]:
            r = post_final[i][j]
            break
    major_list.append(r)     
    
# remove 'Major(s)'
    
for i in range(len(major_list)):
    if "Major(s):" in major_list[i]:
        major_list[i] = major_list[i].replace("Major(s):", "")
    elif "Majors:" in major_list[i]:
        major_list[i] = major_list[i].replace("Majors:", "")
    elif "Major:" in major_list[i]:
        major_list[i] = major_list[i].replace("Major:", "")         
        
# remove :, s, " ", "(", "[" from major_list
        
for i in range(len(major_list)):
    if major_list[i][0] in [':', 's', ' ', "(", "["] :
        major_list[i] = major_list[i][1:len(major_list[i])]        
    
# GPA list

GPA_list =[]

for i in range(len(post_final)):
    t = 'NA'
    for j in range(len(post_final[i])):
        if "GPA:" in post_final[i][j]:
            t = post_final[i][j]
            break
    GPA_list.append(t)    
    
# take everything after 'GPA:'
    
for i in range(len(GPA_list)):
    if 'GPA:' in GPA_list[i]:
        GPA_list[i] = GPA_list[i][GPA_list[i].find('GPA:')+4:
            len(GPA_list[i])]    
        
# remove first whitespaces and Overall from GPA_list 
            
for i in range(len(GPA_list)):
    if len(GPA_list[i]) > 0:
        if GPA_list[i][0] == ' ':
            GPA_list[i] = GPA_list[i][1:len(GPA_list[i])]
        else:
            GPA_list[i] = GPA_list[i]   
    else:
        GPA_list[i] = "NA"
        
for i in range(len(GPA_list)):
    if GPA_list[i][0].lower() == 'o':
        GPA_list[i] = GPA_list[i][8:len(GPA_list[i])]
    else:
        GPA_list[i] = GPA_list[i]      
    
# remove extra words [a horrible, ~ , Math:, General:, Converts to] 

for i in range(len(GPA_list)):
    if 'Cumulative: ' in GPA_list[i]:
        GPA_list[i] = GPA_list[i].replace('Cumulative: ', '')
    if 'Total: ' in GPA_list[i]:
        GPA_list[i] = GPA_list[i].replace('Total: ', '')
    if ': '  in GPA_list[i]:
        GPA_list[i] = GPA_list[i].replace(': ' , '')
    if '> '  in GPA_list[i]:
        GPA_list[i] = GPA_list[i].replace('> ' , '')  
    if 'UG: '  in GPA_list[i]:
        GPA_list[i] = GPA_list[i].replace('UG: ' , '')     

# extract only numbers from GPA_list
        
GPA_final = []
           
numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']       

for i in range(len(GPA_list)):
    if GPA_list[i][0] in numbers:
        if len(GPA_list[i]) <= 3:
            GPA_final.append(GPA_list[i])
        else:
            GPA_final.append(GPA_list[i][0:4])
    else:
        GPA_final.append('NA')      
    
# clean GPA_final from " ", "/", ",", '%', '+'
        
for i in range(len(GPA_final)):
    if " " in GPA_final[i]:
        GPA_final[i] = GPA_final[i].replace(" ", "")
    if "/" in GPA_final[i]:
        GPA_final[i] = GPA_final[i].split('/')[0]
    if "," in GPA_final[i]:
        GPA_final[i] = GPA_final[i].replace(",", "")   
    if "%" in GPA_final[i]:
        GPA_final[i] = GPA_final[i].replace("%", "") 
    if "-" in GPA_final[i]:
        GPA_final[i] = GPA_final[i].replace("-", "") 
    if 'i' in GPA_final[i]:
        GPA_final[i] = GPA_final[i].replace('i', '')    
    if '+' in GPA_final[i]:
        GPA_final[i] = GPA_final[i].replace('+', '')  
    if 'st' in GPA_final[i]:
        GPA_final[i] = 'NA'
    
# create scale_list
        
scale_list = []

for i in range(len(GPA_list)):
    if "/" in GPA_list[i]:
        scale_list.append(GPA_list[i].split('/')[1])
    else:
        scale_list.append("4")
    
# remove first whitespaces  from scale_list
            
for i in range(len(scale_list)):
    if len(scale_list[i]) > 0:
        if scale_list[i][0] == ' ':
            scale_list[i] = scale_list[i][1:len(scale_list[i])]
        else:
            scale_list[i] = scale_list[i]     
    
# extract numbers only from scale_list
        
for i in range(len(scale_list)):
    if len(scale_list[i]) > 0:
        if scale_list[i][0] in numbers:
            if len(scale_list[i]) < 3:
                scale_list[i] = scale_list[i]
            else:
                scale_list[i] = scale_list[i][0:3]         
        else:
            scale_list[i] = "NA"
    else:
        scale_list[i] = "NA"    
    
for i in range(len(scale_list)):
    if " " in scale_list[i]:
        scale_list[i] = scale_list[i].replace(" ", "")
    if "," in scale_list[i]:
        scale_list[i] = scale_list[i].replace(",", "")   
    if ")" in scale_list[i]:
        scale_list[i] = scale_list[i].replace(")", "")  
    if "c" in scale_list[i]:
        scale_list[i] = scale_list[i].replace("c", "")  
    if "[" in scale_list[i]:
        scale_list[i] = scale_list[i].replace("[", "") 
    if "(" in scale_list[i]:
        scale_list[i] = scale_list[i].replace("(", "")  
    if "]" in scale_list[i]:
        scale_list[i] = scale_list[i].replace("]", "")
        
for i in range(len(scale_list)):
    if scale_list[i][-1] == '.':
        scale_list[i] = scale_list[i][0:(len(scale_list[i])-1)]     
    
# add 100 to scale_list
        
for i in range(len(scale_list)):
    if GPA_final[i] != 'NA':
        if float(GPA_final[i]) > 5 and float(GPA_final[i]) < 11:
            scale_list[i] = '10'
        if float(GPA_final[i]) > 50:
            scale_list[i] = '100'     
    
# type of student

type_list = []
            
for i in range(len(post_final)):
    m = 'NA'
    for j in range(len(post_final[i])):
        if "type of student" in post_final[i][j].lower():
            m = post_final[i][j]
    type_list.append(m)     
    
# domestic=1/international=0
        
origin_list = []

domestic_list = ['domestic', 'dwm', 'american', 'us', 'dam', 'dwf']
international_list = ['international', 'canadian', 'russian', 'turkey', 'italy',
                      'african', 'chinese', 'british', 'european']

for i in range(len(type_list)):
    s = 'NA'
    for word in domestic_list:
        if word in type_list[i].lower():
            s = '1'
    for word in international_list:
        if word in type_list[i].lower():
            s = '0'
    origin_list.append(s)    
    
    
# male=0/female=1
        
sex_list = []

for i in range(len(type_list)):
    if 'female' in type_list[i].lower() or 'chick' in type_list[i].lower() or \
    'dwf' in type_list[i].lower():
        sex_list.append('1')
    elif ' male' in type_list[i].lower() or 'guy' in type_list[i].lower() or \
    'dwm' in type_list[i].lower() or 'dude' in type_list[i].lower() or \
    'boy' in type_list[i].lower() :
        sex_list.append('0')
    else:
        sex_list.append('NA') 
        
    
# GRE_q_list
        
GRE_q_list = []
GRE_words = ['GRE General', 'GRE Scores:' , 'GRE Revised', 
             'GRE Original General Test:', 'GRE (pre-2012):', 
             'GRE (old)', 'GRE:']

for i in range(len(post_final)):
    s = "NA"
    for j in range(len(post_final[i])):
        for word in GRE_words:
            if word in post_final[i][j]:
               s = post_final[i][j+1]
    GRE_q_list.append(s)        
        
# replace empty for NA in GRE_q_list
    
for i in range(len(GRE_q_list)):
    if len(GRE_q_list[i]) == 0:
        GRE_q_list[i] = "NA"         
        
# remove Q: from  GRE_q_list
            
for i in range(len(GRE_q_list)):
    if "Q: " in GRE_q_list[i]:
        GRE_q_list[i] = GRE_q_list[i].replace("Q: ", "") 
    elif "Q:" in GRE_q_list[i]:
        GRE_q_list[i] = GRE_q_list[i].replace("Q:", "") 
    
# remove first whitespaces from GRE_q_list  

for i in range(len(GRE_q_list)):
    if GRE_q_list[i][0] == " ":
        GRE_q_list[i] = GRE_q_list[i][1:len(GRE_q_list[i])]  
        
for i in range(len(GRE_q_list)):
    if GRE_q_list[i][0] == "(":
        GRE_q_list[i] = GRE_q_list[i][1:len(GRE_q_list[i])] 
    if GRE_q_list[i][0] == "~":
        GRE_q_list[i] = GRE_q_list[i][1:len(GRE_q_list[i])]     
    
# GRE_q_list split into gre_q_scores and gre_q_percent
        
gre_q_scores = []

for i in range(len(GRE_q_list)):
    if GRE_q_list[i][0] in numbers:
        gre_q_scores.append(GRE_q_list[i][0:3])
    else:
        gre_q_scores.append("NA")      
        
gre_q_percent = []

for i in range(len(GRE_q_list)):
    if '(' in GRE_q_list[i]:
        gre_q_percent.append(GRE_q_list[i].split('(')[1])
    else:
        gre_q_percent.append('NA')     

# remove  " " and "(" from gre_q_scores
        
for i in range(len(gre_q_scores)):
    if " " in gre_q_scores[i]:
        gre_q_scores[i] = gre_q_scores[i].replace(" ", "")
    if "(" in gre_q_scores[i]:
        gre_q_scores[i] = gre_q_scores[i].replace("(", "")
    if "]" in gre_q_scores[i]:
        gre_q_scores[i] = gre_q_scores[i].replace("]", "")  
    
# extract only numbers from gre_q_percent 
        
for i in range(len(gre_q_percent)):
    if gre_q_percent[i][0] in numbers:
        gre_q_percent[i] = gre_q_percent[i][0:2]
    else:
        gre_q_percent[i] = "NA"     
    
# make dictionary of perc and scores

gre_q_sc_temp = []
gre_q_perc_temp =[]

for i in range(len(gre_q_scores)):
    if '%' not in  gre_q_scores[i]: 
        gre_q_sc_temp.append(gre_q_scores[i])
        gre_q_perc_temp.append(gre_q_percent[i])
                
dict_q_sc = dict(zip(gre_q_sc_temp, gre_q_perc_temp))
dict_q_perc = dict(zip(gre_q_perc_temp, gre_q_sc_temp))

# replace percentages with scores in gre_v_scores

for i in range(len(gre_q_scores)):
    if '%' in  gre_q_scores[i]: 
        try:
            r = dict_q_perc[gre_q_scores[i].replace("%","")]
        except KeyError:
            gre_q_scores[i] = 'NA'
        else:
            gre_q_scores[i] = r
        
# add perc in gre_v_percents
        
for i in range(len(gre_q_percent)):
    if  gre_q_percent[i] == 'NA' and gre_q_scores[i] != 'NA': 
        gre_q_percent[i] = dict_q_sc[gre_q_scores[i]]     
    
# GRE_v_list
        
GRE_v_list = []
GRE_words = ['GRE General', 'GRE Scores:' , 'GRE Revised', 
             'GRE Original General Test:', 'GRE (pre-2012):', 
             'GRE (old)', 'GRE:']

for i in range(len(post_final)):
    s = "NA"
    for j in range(len(post_final[i])):
        for word in GRE_words:
            if word in post_final[i][j]:
               s = post_final[i][j+2]
    GRE_v_list.append(s)     
    
# remove V: from  GRE_v_list
            
for i in range(len(GRE_v_list)):
    if "V: " in GRE_v_list[i]:
        GRE_v_list[i] = GRE_v_list[i].replace("V: ", "") 
    elif "V:" in GRE_v_list[i]:
        GRE_v_list[i] = GRE_v_list[i].replace("V:", "")
    
# replace empty for NA in GRE_v_list
    
for i in range(len(GRE_v_list)):
    if len(GRE_v_list[i]) == 0:
        GRE_v_list[i] = "NA" 

# remove first white spaces from GRE_v_list
    
for i in range(len(GRE_v_list)):
    if GRE_v_list[i][0] == " ":
        GRE_v_list[i] = GRE_v_list[i][1:len(GRE_v_list[i])]      
    
for i in range(len(GRE_v_list)):
    if GRE_v_list[i][0] == "(":
        GRE_v_list[i] = GRE_v_list[i][1:len(GRE_v_list[i])] 
    if GRE_v_list[i][0] == "~":
        GRE_v_list[i] = GRE_v_list[i][1:len(GRE_v_list[i])]  
    if GRE_v_list[i][0] == "[":
        GRE_v_list[i] = GRE_v_list[i][1:len(GRE_v_list[i])]

# GRE_v_list split into gre_v_scores and gre_v_percent
        
gre_v_scores = []       
        
for i in range(len(GRE_v_list)):
    if GRE_v_list[i][0] in numbers:
        gre_v_scores.append(GRE_v_list[i][0:3])
    else:
        gre_v_scores.append('NA')
        
gre_v_percent = []

for i in range(len(GRE_v_list)):
    if '(' in GRE_v_list[i]:
        gre_v_percent.append(GRE_v_list[i].split('(')[1][0:2])
    else:
        gre_v_percent.append('NA')  

# remove  " " and "(" from gre_v_scores
        
for i in range(len(gre_v_scores)):
    if " " in gre_v_scores[i]:
        gre_v_scores[i] = gre_v_scores[i].replace(" ", "")
    if "(" in gre_v_scores[i]:
        gre_v_scores[i] = gre_v_scores[i].replace("(", "")
    if "]" in gre_v_scores[i]:
        gre_v_scores[i] = gre_v_scores[i].replace("]", "")  
       
# extract only numbers from gre_v_percent
        
for i in range(len(gre_v_percent)):
    if gre_v_percent[i][0] in numbers:
        gre_v_percent[i] = gre_v_percent[i]
    else:
        gre_v_percent[i] = "NA"  

# remove %, " " and ")" from gre_v_percent
        
for i in range(len(gre_v_percent)):
    if " " in gre_v_percent[i]:
        gre_v_percent[i] = gre_v_percent[i].replace(" ", "")
    if ")" in gre_v_percent[i]:
        gre_v_percent[i] = gre_v_percent[i].replace(")", "")
    if "%" in gre_v_percent[i]:
        gre_v_percent[i] = gre_v_percent[i].replace("%", "") 

# make dictionary of perc and scores

gre_v_sc_temp = []
gre_v_perc_temp =[]

for i in range(len(gre_v_scores)):
    if '%' not in  gre_v_scores[i]: 
        gre_v_sc_temp.append(gre_v_scores[i])
        gre_v_perc_temp.append(gre_v_percent[i])
                
dict_v_sc = dict(zip(gre_v_sc_temp, gre_v_perc_temp))
dict_v_perc = dict(zip(gre_v_perc_temp, gre_v_sc_temp))



# replace percentages with scores in gre_v_scores

for i in range(len(gre_v_scores)):
    if '%' in  gre_v_scores[i]: 
        try:
            r = dict_v_perc[gre_v_scores[i].replace("%","")]
        except KeyError:
            gre_v_scores[i] = 'NA'
        else:
            gre_v_scores[i] = r

# add perc in gre_v_percents
        
for i in range(len(gre_v_percent)):
    if  gre_v_percent[i] == 'NA' and gre_v_scores[i] != 'NA': 
        gre_v_percent[i] = dict_v_sc[gre_v_scores[i]]
        
# GRE_w_list
        
GRE_w_list = []

for i in range(len(post_final)):
    s = "NA"
    for j in range(len(post_final[i])):
        for word in GRE_words:
            if word in post_final[i][j]:
               s = post_final[i][j+3]
    GRE_w_list.append(s) 

# remove W: from  GRE_w_list
            
for i in range(len(GRE_w_list)):
    if "W: " in GRE_w_list[i]:
        GRE_w_list[i] = GRE_w_list[i].replace("W: ", "") 
    elif "W:" in GRE_w_list[i]:
        GRE_w_list[i] = GRE_w_list[i].replace("W:", "")  

# replace empty for NA in GRE_w_list
    
for i in range(len(GRE_w_list)):
    if len(GRE_w_list[i]) == 0:
        GRE_w_list[i] = "NA"         

# remove first white spaces from GRE_w_list
    
for i in range(len(GRE_w_list)):
    if len(GRE_w_list[i]) > 0:
        if GRE_w_list[i][0] == " ":
            GRE_w_list[i] = GRE_w_list[i][1:len(GRE_w_list[i])]  
    else:
        GRE_w_list[i] = 'NA' 

for i in range(len(GRE_w_list)):
    if GRE_w_list[i][0] == "(":
        GRE_w_list[i] = GRE_w_list[i][1:len(GRE_w_list[i])] 
    if GRE_w_list[i][0] == "~":
        GRE_w_list[i] = GRE_w_list[i][1:len(GRE_w_list[i])] 
    if GRE_w_list[i][0] == "[":
        GRE_w_list[i] = GRE_w_list[i][1:len(GRE_w_list[i])]

# GRE_w_list split into gre_w_scores and gre_w_percent
        
gre_w_scores = []       
        
for i in range(len(GRE_w_list)):
    if GRE_w_list[i][0] in numbers:
        gre_w_scores.append(GRE_w_list[i][0:3])
    else:
        gre_w_scores.append('NA')
        
gre_w_percent = []

for i in range(len(GRE_w_list)):
    if '(' in GRE_w_list[i]:
        gre_w_percent.append(GRE_w_list[i].split('(')[1][0:2])
    else:
        gre_w_percent.append('NA')

# remove  " " and "(" from gre_w_scores
        
for i in range(len(gre_w_scores)):
    if " " in gre_w_scores[i]:
        gre_w_scores[i] = gre_w_scores[i].replace(" ", "")
    if "(" in gre_w_scores[i]:
        gre_w_scores[i] = gre_w_scores[i].replace("(", "")
    if "]" in gre_w_scores[i]:
        gre_w_scores[i] = gre_w_scores[i].replace("]", "") 
    
# extract only numbers from gre_w_percent
        
for i in range(len(gre_w_percent)):
    if gre_w_percent[i][0] in numbers:
        gre_w_percent[i] = gre_w_percent[i]
    else:
        gre_w_percent[i] = "NA"    

# remove %, " " and ")" from gre_w_percent
        
for i in range(len(gre_w_percent)):
    if " " in gre_w_percent[i]:
        gre_w_percent[i] = gre_w_percent[i].replace(" ", "")
    if ")" in gre_w_percent[i]:
        gre_w_percent[i] = gre_w_percent[i].replace(")", "")
    if "%" in gre_w_percent[i]:
        gre_w_percent[i] = gre_w_percent[i].replace("%", "") 

# make dictionary of perc and scores

gre_w_sc_temp = []
gre_w_perc_temp =[]

for i in range(len(gre_w_scores)):
    if '%' not in  gre_w_scores[i]: 
        gre_w_sc_temp.append(gre_w_scores[i])
        gre_w_perc_temp.append(gre_w_percent[i])
                
dict_w_sc = dict(zip(gre_w_sc_temp, gre_w_perc_temp))
dict_w_perc = dict(zip(gre_w_perc_temp, gre_w_sc_temp))

# replace percentages with scores in gre_v_scores

for i in range(len(gre_w_scores)):
    if '%' in  gre_w_scores[i]: 
        try:
            r = dict_w_perc[gre_w_scores[i].replace("%","")]
        except KeyError:
            gre_w_scores[i] = 'NA'
        else:
            gre_w_scores[i] = r
        
# add perc in gre_v_percents
        
for i in range(len(gre_w_percent)):
    if  gre_w_percent[i] == 'NA' and gre_w_scores[i] != 'NA': 
        gre_w_percent[i] = dict_w_sc[gre_w_scores[i]] 
        
# GRE_m_list
        
GRE_m_list = []

for i in range(len(post_final)):
    t = 'NA'
    for j in range(len(post_final[i])):
        if "GRE Subject" in str(post_final[i][j]):
            if post_final[i][j] != post_final[i][-1]:
                t = post_final[i][j+1]
                break
    GRE_m_list.append(t) 
    
# remove M: from  GRE_m_list
            
for i in range(len(GRE_m_list)):
    if "M: " in GRE_m_list[i]:
        GRE_m_list[i] = GRE_m_list[i].replace("M: ", "") 
    elif "M:" in GRE_m_list[i]:
        GRE_m_list[i] = GRE_m_list[i].replace("M:", "")           
            
# replace empty for NA in GRE_m_list
    
for i in range(len(GRE_m_list)):
    if len(GRE_m_list[i]) == 0:
        GRE_m_list[i] = "NA"   

# remove first white spaces from GRE_m_list
       
for i in range(len(GRE_m_list)):
    if len(GRE_m_list[i]) > 0:
        if GRE_m_list[i][0] == " ":
            GRE_m_list[i] = GRE_m_list[i][1:len(GRE_m_list[i])]  
    else:
        GRE_m_list[i] = 'NA' 

            
# GRE_m_list split into gre_m_scores and gre_m_percent
        
gre_m_scores = []       
        
for i in range(len(GRE_m_list)):
    if len(GRE_m_list[i]) > 2:
        if GRE_m_list[i][0] in numbers:
            gre_m_scores.append(GRE_m_list[i][0:3])
        else:
            gre_m_scores.append('NA') 
    else:
        gre_m_scores.append('NA')   
        
gre_m_percent = []

for i in range(len(GRE_m_list)):
    if '(' in GRE_m_list[i]:
        gre_m_percent.append(GRE_m_list[i].split('(')[1][0:2])
    else:
        gre_m_percent.append('NA')  

# remove  " " and "(" from gre_m_scores
        
for i in range(len(gre_m_scores)):
    if " " in gre_m_scores[i]:
        gre_m_scores[i] = gre_m_scores[i].replace(" ", "")
    if "(" in gre_m_scores[i]:
        gre_m_scores[i] = gre_m_scores[i].replace("(", "")
    if "]" in gre_m_scores[i]:
        gre_m_scores[i] = gre_m_scores[i].replace("]", "")  

# extract only numbers from gre_m_percent
        
for i in range(len(gre_m_percent)):
    if gre_m_percent[i][0] in numbers:
        gre_m_percent[i] = gre_m_percent[i]
    else:
        gre_m_percent[i] = "NA"  
        
# remove %, " " and ")" from gre_m_percent
        
for i in range(len(gre_m_percent)):
    if " " in gre_m_percent[i]:
        gre_m_percent[i] = gre_m_percent[i].replace(" ", "")
    if ")" in gre_m_percent[i]:
        gre_m_percent[i] = gre_m_percent[i].replace(")", "")
    if "%" in gre_m_percent[i]:
        gre_m_percent[i] = gre_m_percent[i].replace("%", "") 

# make dictionary of perc and scores

gre_m_sc_temp = []
gre_m_perc_temp =[]

for i in range(len(gre_m_scores)):
    if '%' not in  gre_m_scores[i]: 
        gre_m_sc_temp.append(gre_m_scores[i])
        gre_m_perc_temp.append(gre_m_percent[i])
                
dict_m_sc = dict(zip(gre_m_sc_temp, gre_m_perc_temp))
dict_m_perc = dict(zip(gre_m_perc_temp, gre_m_sc_temp))

# replace percentages with scores in gre_v_scores

for i in range(len(gre_m_scores)):
    if '%' in  gre_m_scores[i]: 
        try:
            r = dict_m_perc[gre_m_scores[i].replace("%","")]
        except KeyError:
            gre_m_scores[i] = 'NA'
        else:
            gre_m_scores[i] = r
        
# add perc in gre_v_percents
        
for i in range(len(gre_m_percent)):
    if  gre_m_percent[i] == 'NA' and gre_m_scores[i] != 'NA': 
        gre_m_percent[i] = dict_m_sc[gre_m_scores[i]] 

# TOEFL
            
toefl_list = []

for i in range(len(post_final)):
    t = "NA"
    for j in range(len(post_final[i])):
        if 'TOEFL Score' in post_final[i][j]:
            t = post_final[i][j]
    toefl_list.append(t)      
    
# remove TOEFL Score: from toefl_list
    
for i in range(len(toefl_list)):
    if "TOEFL Score:" in toefl_list[i]:
        toefl_list[i] = toefl_list[i].replace("TOEFL Score:", "")  

# remove first white spaces from toefl_list
        
for i in range(len(toefl_list)):
    if len(toefl_list[i]) > 0:
        if toefl_list[i][0] == " ":
            toefl_list[i] = toefl_list[i][1:len(toefl_list[i])] 
    else:
        toefl_list[i] = 'NA' 

# replace "("
        
for i in range(len(toefl_list)):
    if len(toefl_list[i]) > 0:
        if toefl_list[i][0] == "(":
            toefl_list[i] = toefl_list[i][1:len(toefl_list[i])]         
        
# extract only numbers from toefl_list
     
numbers2 = ['1']
numbers3 = ['6','7','8','9']

for i in range(len(toefl_list)):
    if len(toefl_list[i]) > 0:
        if toefl_list[i][0] in numbers2:
            toefl_list[i] = toefl_list[i][0:3]
        elif toefl_list[i][0] in numbers3:
            toefl_list[i] = toefl_list[i][0:2]
        else:
            toefl_list[i] = "NA"       
    else:
        toefl_list[i] = "NA" 
        
# extract research experience
            
research_list = []


for i in range(len(post_final)):
    r = "NA"
    for j in range(len(post_final[i])):
        if 'Research Experience' in post_final[i][j]:
            r = post_final[i][j]
    research_list.append(r)  
        
# check length of research_list
    
research_sort = []
    
for i in range(len(research_list)):
    research_sort.append(len(research_list[i]))
    
sorted(research_sort)
        
for i in range(len(research_list)):
    if len(research_list[i]) < 72:
        print(research_list[i])          
        
# form dummy for research_list
            
research_dummy = []

for i in range(len(research_list)):
    if len(research_list[i]) > 71:
        research_dummy.append('1')
    else:
        research_dummy.append('0')        
        
# write to a file GPA_final
     
import csv
        
with open("GPA_final_18.txt", "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in GPA_final:
        writer.writerow([val]) 
        
# write to a file Accepted
          
with open("Accepted_18.txt", "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in accepted_list:
        writer.writerow([val])        
        
# write to a file gre_m_percent
          
with open("gre_m_perc_18.txt", "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in gre_m_percent:
        writer.writerow([val]) 
        
# write to a file gre_m_scores
          
with open("gre_m_scores_18.txt", "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in gre_m_scores:
        writer.writerow([val])        
        
# write to a file gre_q_percent
          
with open("gre_q_percent_18.txt", "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in gre_q_percent:
        writer.writerow([val])        
        
# write to a file gre_q_scores
          
with open("gre_q_scores_18.txt", "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in gre_q_scores:
        writer.writerow([val])          
 
# write to a file gre_v_percent      
          
with open("gre_v_percent_18.txt", "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in gre_v_percent:
        writer.writerow([val])            
        
# write to a file gre_v_scores   
          
with open("gre_v_scores_18.txt", "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in gre_v_scores:
        writer.writerow([val])           
        
# write to a file gre_w_percent
          
with open("gre_w_percent_18.txt", "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in gre_w_percent:
        writer.writerow([val])            
        
# write to a file gre_w_scores
          
with open("gre_w_scores_18.txt", "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in gre_w_scores:
        writer.writerow([val])         
        
# write to a file major_list
          
with open("major_18.txt", "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in major_list:
        writer.writerow([val])         
        
# write to a file origin_list
          
with open("origin_18.txt", "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in origin_list:
        writer.writerow([val])           

# write to a file post_final
          
with open("post_final_18.txt", "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in post_final:
        writer.writerow([val])   

# write to a file rejected_list
          
with open("rejected_18.txt", "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in rejected_list:
        writer.writerow([val])
        
# write to a file rejected_list
          
with open("rejected_18.txt", "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in rejected_list:
        writer.writerow([val])       
        
# write to a file research_dummy
          
with open("research_18.txt", "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in research_dummy:
        writer.writerow([val])          
        
# write to a file research_dummy
          
with open("research_18.txt", "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in research_dummy:
        writer.writerow([val])           
        
# write to a file scale_list
          
with open("gpa_scale_18.txt", "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in scale_list:
        writer.writerow([val])           
        
# write to a file sex_list
          
with open("sex_18.txt", "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in sex_list:
        writer.writerow([val])           
        
# write to a file toefl_list
          
with open("toefl_18.txt", "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in toefl_list:
        writer.writerow([val])  

# write to a file universities
          
with open("universities_18.txt", "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in universities:
        writer.writerow([val])  
        
# write to a file universities
          
with open("universities_18.txt", "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in universities:
        writer.writerow([val])     

        