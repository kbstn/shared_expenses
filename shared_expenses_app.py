# shared_expenses is a streamlit dashboard where you can select a number of persons, 
# their days in charge and therit total expenses over time.
# shared_expenses will calculate a mean expens value person/day and tell everyone how much they have to pay


import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(layout="wide")


st.title('Dashboard for calculating shared expenses of your community')
st.write("""You need to count the days of participitaion for each person and also the sum of their expenses. \n
If you have this information you can use this dashboard to easily calculate the 'who owes how much'""")

st.markdown("""---""")

# 
# slider for number of persons, text iput or total days

left_column, right_column = st.columns(2)

num_ppl= left_column.slider('Number of people',min_value=2, max_value=20, value=7)
total_days = right_column.number_input('insert total number of days',step=1,min_value=1,value=31)

total_days = int(total_days)

left_column.write(num_ppl)
right_column.write(total_days)

pplcols = st.columns(num_ppl)
ppl=[]

for i, x in enumerate(pplcols):
    ppl.append(x.selectbox(f"Person # {i+1}",['Sophia','Joanna','Georg','Flo','Konrad','Ida','Nuri','Surname8', 'Surname9', 'Surname10', 'Surname11', 'Surname12', 'Surname13', 'Surname14', 'Surname15', 'Surname16', 'Surname17', 'Surname18', 'Surname19', 'Surname20'],key=i,index=i))

days ={}
spend={}

for i,x in enumerate(pplcols):
    days[ppl[i]]=x.slider('Days '+ppl[i]+' was present',min_value=1, max_value=total_days,key=i, value=total_days)
    spend[ppl[i]]=x.number_input('money spend by '+ppl[i],step=1,key=i)

total_ppl_days = sum(days.values())
total_spend = sum(spend.values())
money_per_day = total_spend / total_ppl_days

st.markdown("""---""")

# metrics
col1, col2, col3 = st.columns(3)
col1.metric("Cost/day/person", str(round(money_per_day,2))+' €')
col2.metric("Total money spend", str(total_spend)+' €')
col3.metric("Sum of all days", str(total_ppl_days)+' Days')

st.markdown("""---""")

results = pd.DataFrame({'days':pd.Series(days),'spend':pd.Series(spend)})

costs_person = round(results.days * money_per_day,2)
results['costs_person'] = costs_person
results['difference'] = results.costs_person - results.spend

# getting money
getting = results[results.difference < 0]

# have to pay
haveto = results[results.difference >= 0]


left_column2, right_column2 = st.columns(2)

left_column2.markdown('## People that get money back')
right_column2.markdown('## People that have to pay them')

for person in getting.index.values:
    left_column2.markdown("### **{}**".format(person))
    left_column2.markdown("{} participated for {} days".format(person, days[person]))
    left_column2.markdown("In that time {} **consumed stuff with a value of {} Euro and paid {} Euro**".format(person,costs_person[0],getting.loc[person,'spend'],2))
    left_column2.markdown("{} purchased more than the avarage thus **{} will get {} € from the others**".format(person,person,abs(round(getting.loc[person,'difference'],2))))

for person in haveto.index.values:
    right_column2.markdown("### **{}**".format(person))
    right_column2.markdown("{} participated for {} days".format(person, days[person]))
    right_column2.markdown("In that time {} **consumed stuff with a value of {} Euro and paid {} Euro**".format(person,costs_person[0],haveto.loc[person,'spend'],2))
    right_column2.markdown("{} purchased less than the avarage thus **{} will have to pay {} € to the others**".format(person,person,abs(round(haveto.loc[person,'difference'],2))))

st.markdown("""---""")
st.write('Check the data here:')
st.write(results)

#     print("{} war {} Tage da".format(person, days[person]))
#     print("Daher hat {} Nahrungsmittel im Wert von {} Euro konsumiert".format(person, costs_person))
#     print("{} hatte dabei Ausgaben von {}".format(person, spend[person]))
#     if spend[person] > costs_person:
#         print("{} hat bereits mehr ausgegeben als Kosten entstanden sind".format(person))
#         print("Daher bekommt {} noch {} Euro".format(person, spend[person] - costs_person))
#     else:
#         print("{} hat weniger ausgegeben als Kosten entstanden sind".format(person))
#         print("Daher muss {} noch {} Euro zahlen".format(person, costs_person - spend[person]))
#     print("\n")

# for i, x in enumerate(ppl):
#     x.number_input('insert total number of days',step=1)

# for number in range(num_ppl):
#     left_column.st.text_input('Name of person'+str(number+1))

# # for each number selcted by slider create one text input for days and one for total spend

# # for each text input

# people = input("Wer hat mitgegessen? Namen bitte mit Komma trennen\n")
# people = people.replace(" ", "").split(",")
# days = {}
# spend = {}

# for person in people:
#     days[person] = float(input("Wie viele Tage war " + person + " anwesend?\n"))
#     spend[person] = float(input("Wie viel Geld hat " + person + " ausgegeben?\n"))
    
# total_days = sum(days.values())
# total_spend = sum(spend.values())
# money_per_day = total_spend / total_days

# print("\nPro Personentag sind " + str(money_per_day) + " Euro Kosten entstanden")
# print("Daraus ergibt sich:\n")

# for person in people:
#     costs_person = money_per_day * days[person]
#     print("{} war {} Tage da".format(person, days[person]))
#     print("Daher hat {} Nahrungsmittel im Wert von {} Euro konsumiert".format(person, costs_person))
#     print("{} hatte dabei Ausgaben von {}".format(person, spend[person]))
#     if spend[person] > costs_person:
#         print("{} hat bereits mehr ausgegeben als Kosten entstanden sind".format(person))
#         print("Daher bekommt {} noch {} Euro".format(person, spend[person] - costs_person))
#     else:
#         print("{} hat weniger ausgegeben als Kosten entstanden sind".format(person))
#         print("Daher muss {} noch {} Euro zahlen".format(person, costs_person - spend[person]))
#     print("\n")