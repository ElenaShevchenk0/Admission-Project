#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 28 13:03:37 2020

@author: macpro
"""

# scraping data for 2011

from bs4 import BeautifulSoup
import urllib.request

user_name_list = []
content_list = []
post_list = []

for p in [0, 50]:
    URL = 'https://mathematicsgre.com/viewtopic.php?f=1&t=495&start='f'{p}'
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

indices = [0,1,3,21,44,45,46]

for ind in sorted(indices, reverse=True):
    del unique_user_list[ind]
    

# indices for useless posts without 'applying to where' expression
        

boolean_useless = []  
for i in range(len(post_list)):
    k = False
    for j in range(len(post_list[i])):
        if 'applying to where' in post_list[i][j].lower() or \
        'applying to (a' in post_list[i][j].lower():
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
        if 'Applying to' in post_temp[i][j]:
            applying_list.append(post_temp[i][j:len(post_temp[i])])
        
    
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
    
# delete names for zero universities

for ind in sorted(index_zero, reverse=True):
    del unique_user_list[ind] 
    
   
# Major(s) list

major_list =[]

for i in range(len(post_final)):
    for j in range(len(post_final[i])):
        if "Major(s)" in post_final[i][j]:
            major_list.append(post_final[i][j])
    
del  major_list[11] 
    
# remove 'MAjor(s)'
    
for i in range(len(major_list)):
    major_list[i] = major_list[i].replace("Major(s):", "")
            
            
# remove first whitespaces

for i in range(len(major_list)):
    if major_list[i][0] == ' ':
        major_list[i] = major_list[i][1:len(major_list[i])]
    else:
        major_list[i] = major_list[i]  
            
        
# GPA list

GPA_list =[]

for i in range(len(post_final)):
    for j in range(len(post_final[i])):
        if "GPA:" in post_final[i][j]:
            GPA_list.append(post_final[i][j])
            
del GPA_list[1]           
del GPA_list[12]             
            
# take everything after 'GPA:'
    
for i in range(len(GPA_list)):
    if 'GPA:' in GPA_list[i]:
        GPA_list[i] = GPA_list[i][GPA_list[i].find('GPA:')+4:
            len(GPA_list[i])]
             
# remove first whitespaces and ~        
            
for i in range(len(GPA_list)):
    if GPA_list[i][0] == ' ':
        GPA_list[i] = GPA_list[i][1:len(GPA_list[i])]
    else:
        GPA_list[i] = GPA_list[i]  
                  
for i in range(len(GPA_list)):
    if GPA_list[i][0] == '~':
        GPA_list[i] = GPA_list[i][1:len(GPA_list[i])]
    else:
        GPA_list[i] = GPA_list[i]  
        
# extract numbers for final GPA    
 
GPA_final = []
           
numbers = ['3', '9', '5', '4', '8']       

for i in range(len(GPA_list)):
    if GPA_list[i][0] in numbers:
        if len(GPA_list[i]) <= 3:
            GPA_final.append(GPA_list[i])
        else:
            GPA_final.append(GPA_list[i][0:4])
    else:
        GPA_final.append('NA')
        
# remove whitespaces from GPA_final
        
for i in range(len(GPA_final)):
    if ' ' in GPA_final[i]:
        GPA_final[i] = GPA_final[i].replace(' ', '')

# print as numeric
        
for i in range(len(GPA_final)):
    if GPA_final[i] != 'NA':
        print(float(GPA_final[i]))

# create scale list
        
            
scale_list = []

for i in range(len(GPA_final)):
    if GPA_final[i][0] in ['8', '9']:
        scale_list.append('10')
    elif GPA_final[i][0] == '5':
        scale_list.append('6')
    elif GPA_final[i][0] in ['3','4']:
        scale_list.append('4')
    else:
        scale_list.append(GPA_final[i])

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

domestic_list = ['domestic', 'dwm', 'american', 'us']

for i in range(len(type_list)):
    s = '0'
    for word in domestic_list:
        if word in type_list[i].lower():
            s = '1'
        else:
            if "NA" in type_list[i]:
                s = type_list[i]
    origin_list.append(s)

# male=0/female=1
        
sex_list = []

for i in range(len(type_list)):
    if 'female' in type_list[i].lower() or 'chick' in type_list[i].lower():
        sex_list.append('1')
    elif ' male' in type_list[i].lower() or 'guy' in type_list[i].lower() or \
    'dwm' in type_list[i].lower():
        sex_list.append('0')
    else:
        sex_list.append('NA')


# GRE_q_list
        
GRE_q_list = []

for i in range(len(post_final)):
    for j in range(len(post_final[i])):
        if "GRE Scores" in str(post_final[i][j]):
            GRE_q_list.append(post_final[i][j+1])
          
# remove Q: from  GRE_q_list
            
for i in range(len(GRE_q_list)):
    GRE_q_list[i] = GRE_q_list[i].replace("Q: ", "")
            
# GRE_q_list split into gre_q_scores and gre_q_percent
    
gre_q_scores = []

for i in range(len(GRE_q_list)):
    gre_q_scores.append(GRE_q_list[i][0:3])


gre_q_percent = []

for i in range(len(GRE_q_list)):
    if '(' in GRE_q_list[i]:
        gre_q_percent.append(GRE_q_list[i].split('(')[1])
    else:
        gre_q_percent.append('NA')
    
# remove %, " " and ")" from gre_q_percent
        
for i in range(len(gre_q_percent)):
    if " " in gre_q_percent[i]:
        gre_q_percent[i] = gre_q_percent[i].replace(" ", "")
    if ")" in gre_q_percent[i]:
        gre_q_percent[i] = gre_q_percent[i].replace(")", "")
    if "%" in gre_q_percent[i]:
        gre_q_percent[i] = gre_q_percent[i].replace("%", "")

# GRE_v_list
        
GRE_v_list = []

for i in range(len(post_final)):
    for j in range(len(post_final[i])):
        if "GRE Scores" in str(post_final[i][j]):
            GRE_v_list.append(post_final[i][j+2])
            
# remove V: from  GRE_v_list
            
for i in range(len(GRE_v_list)):
    GRE_v_list[i] = GRE_v_list[i].replace("V: ", "")
                  
# remove first white spaces from GRE_v_list
    
for i in range(len(GRE_v_list)):
    if GRE_v_list[i][0] == " ":
        GRE_v_list[i] = GRE_v_list[i][1:len(GRE_v_list[i])]

# GRE_v_list split into gre_v_scores and gre_v_percent
    
gre_v_scores = []

for i in range(len(GRE_v_list)):
    gre_v_scores.append(GRE_v_list[i][0:3])


gre_v_percent = []

for i in range(len(GRE_v_list)):
    if '(' in GRE_v_list[i]:
        gre_v_percent.append(GRE_v_list[i].split('(')[1])
    else:
        gre_v_percent.append('NA')
        
# extract only numbers from gre_v_percent
        
numbers1 = ['9','8','7','6','5','4','3','2','1']  

for i in range(len(gre_v_percent)):
        if gre_v_percent[i][0] in numbers1:
            gre_v_percent[i] = gre_v_percent[i][0:2]
        
# GRE_w_list
        
GRE_w_list = []

for i in range(len(post_final)):
    for j in range(len(post_final[i])):
        if "GRE Scores" in str(post_final[i][j]):
            GRE_w_list.append(post_final[i][j+3])     
        
# remove W: from  GRE_w_list
            
for i in range(len(GRE_w_list)):
    GRE_w_list[i] = GRE_w_list[i].replace("W: ", "")       
        

# GRE_w_list split into gre_w_scores and gre_w_percent
    
gre_w_scores = []
gre_w_percent = []

for i in range(len(GRE_w_list)):
    if '(' in GRE_w_list[i]:
        gre_w_scores.append(GRE_w_list[i].split('(')[0])
        gre_w_percent.append(GRE_w_list[i].split('(')[1])
    else:
        gre_w_scores.append(GRE_w_list[i])
        gre_w_percent.append("NA")


# remove whitespaces from gre_w_scores
        
for i in range(len(gre_w_scores)):
    if " " in gre_w_scores[i]:
        gre_w_scores[i] = gre_w_scores[i].replace(" ", "")
        
# remove %, " " and ")" from gre_w_percent
        
for i in range(len(gre_w_percent)):
    if " " in gre_w_percent[i]:
        gre_w_percent[i] = gre_w_percent[i].replace(" ", "")
    if ")" in gre_w_percent[i]:
        gre_w_percent[i] = gre_w_percent[i].replace(")", "")
    if "%" in gre_w_percent[i]:
        gre_w_percent[i] = gre_w_percent[i].replace("%", "")

# GRE_m_list
        
GRE_m_list = []

for i in range(len(post_final)):
    for j in range(len(post_final[i])):
        if "GRE Scores" in str(post_final[i][j]):
            GRE_m_list.append(post_final[i][j+4]) 
            
        
# remove M: from  GRE_m_list
            
for i in range(len(GRE_m_list)):
    if "M: " in GRE_m_list[i]: 
        GRE_m_list[i] = GRE_m_list[i].replace("M: ", "")  
    if "Subject: " in GRE_m_list[i]: 
        GRE_m_list[i] = GRE_m_list[i].replace("Subject: ", "")  
        
# GRE_m_list split into gre_m_scores and gre_m_percent
        
gre_m_scores = []
        
for i in range(len(GRE_m_list)):
    if len(GRE_m_list[i]) >= 1:
        if GRE_m_list[i][0] in numbers1:
            gre_m_scores.append(GRE_m_list[i][0:3])
        else:
            gre_m_scores.append("NA")
    else:
        gre_m_scores.append("NA")
        
gre_m_percent = []

for i in range(len(GRE_m_list)):
    if '(' in GRE_m_list[i]:
        gre_m_percent.append(GRE_m_list[i].split('(')[1])
    else:
        gre_m_percent.append('NA')

# extract only numbers from gre_m_percent
        
numbers1 = ['9','8','7','6','5','4','3','2','1']  

for i in range(len(gre_m_percent)):
        if gre_m_percent[i][0] in numbers1:
            gre_m_percent[i] = gre_m_percent[i][0:2]
            
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
        toefl_list[i] = toefl_list[i].replace("TOEFL Score: ", "")

# replace "("
        
for i in range(len(toefl_list)):
    if toefl_list[i][0] == "(":
        toefl_list[i] = toefl_list[i][1:len(toefl_list[i])]

# extract only numbers from toefl_list
     
numbers2 = ['1']
numbers3 = ['6','7','8','9']

for i in range(len(toefl_list)):
    if toefl_list[i][0] in numbers2:
        toefl_list[i] = toefl_list[i][0:3]
    elif toefl_list[i][0] in numbers3:
        toefl_list[i] = toefl_list[i][0:2]
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
       
# form dummy for research_list
            
research_dummy = []

for i in range(len(research_list)):
    if len(research_list[i]) > 50:
        research_dummy.append('1')
    else:
        research_dummy.append('0')
   
# write to a file
     
import csv
        
with open("universities_11.txt", "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in universities:
        writer.writerow([val])  







       
