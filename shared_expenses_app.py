# shared_expenses is a streamlit dashboard where you can select a number of persons, 
# their days in charge and therit total expenses over time.
# shared_expenses will calculate a mean expens value person/day and tell everyone how much they have to pay

# dcfsdfsf
import pandas as pd
import streamlit as st
import numpy as np

st.set_page_config(layout="wide")


st.title('Dashboard for calculating shared expenses of your community')
st.write("""You need to count the days of participitaion for each person and also the sum of their expenses. \n
If you have this information you can use this dashboard to easily calculate the 'who owes how much'""")

st.markdown("""---""")


# slider for number of persons, text iput or total days

left_column, right_column = st.columns(2)

# create a slide to define how many people participated
num_ppl= left_column.slider('Number of people',min_value=2, max_value=20, value=5)

# define the timespan for the calculations
total_days = right_column.number_input('insert total number of days',step=1,min_value=1,value=31)
total_days = int(total_days)

# create as many columns as there are people defined
pplcols = st.columns(num_ppl)

# dicts to store inforamtion about payment and money spend
days ={}
spend={}

# for each column created this way create a text input for names with default values
#
for i, x in enumerate(pplcols):
    # up to 20 default names
    name_list=['Sophia','Joanna','Georg','Flo','Konrad','Ida','Nuri','Surname8', 'Surname9', 'Surname10', 'Surname11', 'Surname12', 'Surname13', 'Surname14', 'Surname15', 'Surname16', 'Surname17', 'Surname18', 'Surname19', 'Surname20']
    
    # get name of the person
    person= x.text_input(f"Person # {i+1}",name_list[i],key=i)

    # days are the days each person was participating. it will start with the same number 
    # as the total number of days defined beforehands
    days[person]=x.number_input('Days '+person+' was present',step=1,min_value=1,value=total_days, key=i)

    # input field for the money spend by the person
    spend[person]=x.number_input('money spend by '+person,step=10,key=i)

    # insert a warning if your number is higher than the total number of days defined
    if days[person] > total_days:
        x.write('**Warning:**') 
        x.write('Number of days for '+person+' is higher than total days, only do this if you sum up multiple people in one entity!')


# calcualte sums for days and money spend
total_ppl_days = sum(days.values())
total_spend = sum(spend.values())

# calculate average money spend per 'person day'
money_per_day = total_spend / total_ppl_days

# make a nice line
st.markdown("""---""")

# show the calculated metrics
col1, col2, col3 = st.columns(3)
col1.metric("Cost/day/person", str(round(money_per_day,2))+' €')
col2.metric("Total money spend", str(total_spend)+' €')
col3.metric("Sum of all days", str(total_ppl_days)+' Days')

# make a nice line
st.markdown("""---""")

# dump the stats in a dataframe
results = pd.DataFrame({'days':pd.Series(days),'spend':pd.Series(spend)})
# calculate cost per person and the difference
costs_person = round(results.days * money_per_day,2)
results['costs_person'] = costs_person
results['difference'] = results.costs_person - results.spend

# decie who is getting money
getting = results[results.difference < 0]

# and who have to pay
haveto = results[results.difference >= 0]

# show results in a text format thats easy to copy and paste
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

st.markdown("""---""")# make a nice line

# also show the the dataframe
st.write('Check the data here:')
st.write(results)
