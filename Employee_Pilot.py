#Load the necessary libraries
import pandas as pd
import streamlit as st
import altair as alt
from PIL import Image


# Data needed for the app
data_stage = pd.read_csv('C:/Users/jefft/OneDrive/Documents/Python Scripts/Streamlit/Employee_Example_Data.csv')
data = pd.DataFrame(data_stage)

# Main body of the application.
st.title('Employee Locator')
st.subheader('Find Health Catalyst team members in your area to connect with.')


# Filters on the left.
image = Image.open('C:/Users/jefft/OneDrive/Documents/Python Scripts/Streamlit/Company_Logo.jpg')
#st.sidebar.image(image,width=100)
st.sidebar.header('Company')
st.sidebar.text('Filters')

# Variables.
states = data['State'].unique()
office = data['Location'].unique()
remote = data['RemoteFLG'].unique()

# Actual filters that will be displayed.
state_choice = st.sidebar.selectbox('Select a state', states)
zip = data["Home Zip Code"].loc[data["State"] == state_choice].unique()
zip_choice = st.sidebar.selectbox('',zip)
office_choice = st.sidebar.selectbox('Select an office', office)


#data.loc[(df['state']=make_choice) & (df['office']=office_choice)]
if state_choice == 'ID':
    filtered_data = data[data['State'] == state_choice]
else:
    filtered_data = data

employee_count = (data['Team Member ID'].count())*1.0
remote = data.RemoteFLG[data['RemoteFLG'] == 1].count()
remote_pct = (remote / employee_count)*1.0
HQ_stage = data[data['Location'] == 'US SLC Headquarters']
HQ = (HQ_stage['Team Member ID'].count())*1.0

col1, col2, col3 = st.columns(3)
col1.metric("Employee Count", employee_count)
col2.metric("Remote", "{:.2%}".format(remote_pct)) #remote_pct
col3.metric("Size of Headquarters", HQ)


st.subheader('Map of Employees')
st.map(filtered_data)

bar_chart = data['State'].value_counts()
bar_chart = pd.DataFrame(bar_chart)
bar_chart = bar_chart.reset_index()


bars = alt.Chart(bar_chart).mark_bar().encode(
    x=alt.X("State",axis=None), #alt.Axis(grid=False)),
    y=alt.Y("index", sort='-x',axis=alt.Axis(grid=False)),
    color=alt.condition(
        alt.datum.index == bar_chart['index'].max(),  # If the year is 1810 this test returns True,
        alt.value('blue'),     # which sets the bar orange.
        alt.value('steelblue')   # And if it's not true it sets the bar steelblue.
    )
)

text = bars.mark_text(
    align='left',
    baseline='middle',
    dx=3  # Nudges text to right so it doesn't appear on top of the bar
).encode(
    text='State:Q'
)

bars + text
