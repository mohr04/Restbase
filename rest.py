import pandas as pd
import streamlit as st
from PIL import Image
import mysql.connector as connection
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
import seaborn as sns

sns.set()
# Connect to the database
restbase = connection.connect(host="relational.fit.cvut.cz", database='restbase', user="guest", passwd="relational", use_pure=True)

# Display the banner picture in the streamlit app
img = Image.open('rest.jpeg')
st.image(img)


# Read SQL query or database table into a pandas DataFrame
query = "SELECT loc.id_restaurant, loc.street_num, loc.street_name, loc.city, gef.label, gef.food_type, gef.review, ggp.county, ggp.region FROM location AS loc LEFT JOIN generalinfo AS gef ON loc.id_restaurant = gef.id_restaurant RIGHT JOIN geographic AS ggp ON gef.city = ggp.city"
resturants_del = pd.read_sql_query(query, restbase)
         
# Sidebar filter
st.sidebar.title("Filter")
food_type_filter = st.sidebar.selectbox('Filter by County', resturants_del['county'].unique())

# Filter the DataFrame based on the selected food type
filtered_df = resturants_del[resturants_del['county'] == food_type_filter]

# Display the filtered DataFrame
st.title('Live Visualization of Charts')
st.write(filtered_df)

# Create a figure with multiple subplots
fig, ax1 = plt.subplots(1, 1, figsize=(20, 20))

# Bar chart of restaurant counts by city
ax1.set_title('Restaurant Counts by City',fontsize=60)
city_counts = filtered_df['city'].value_counts()
sns.barplot(x=city_counts.index, y=city_counts.values, ax=ax1)
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45,fontsize=25)
ax1.set_yticklabels(ax1.get_yticklabels(),fontsize=25)
ax1.set_xlabel('City',fontsize=40)
ax1.set_ylabel('Count',fontsize=40)
st.pyplot(fig)
# Pie chart of food type distribution
fig, ax2= plt.subplots(1, 1, figsize=(50, 70))
# Generate the pie chart
label_distance = 1.2
autopct_distance = 1.1
counts = Counter(filtered_df['city'])
counts_dict = dict(counts)
piechart = ax2.pie(counts_dict.values(), labels=counts_dict.keys(),autopct='%1.2f%%', textprops={'fontsize': 40},labeldistance=label_distance, pctdistance=autopct_distance)

# Set the aspect ratio to make it a perfect circle

#ax2.axis('equal')
 #Increase the size of the labels
for label in ax2.pie(counts_dict.values())[1]:
    label.set_fontsize(60)  # Set the desired font size here

# Set the title with increased font size
ax2.set_title('Food Type Distribution', fontsize=100)

# Set the font weight of pie chart labels
for text in piechart[1]:
    text.set_fontweight('bold')
    text.set_fontsize(40)

# Add a legend with increased font size
#ax2.legend(facecolor='m', fontsize=45)


st.pyplot(fig)