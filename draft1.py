import pandas as pd
import  pymysql
from prettytable import PrettyTable
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
import numpy as np
import sys

# reading file from excel and converting to a data frame
dataframe = pd.read_excel("HAPPY3.xlsx",na_values=0)
#print(dataframe)

engine = create_engine("mysql+pymysql://root:Home%405095@localhost/information")
mycon=pymysql.connect(host="localhost",user="root",passwd="Home@5095",database="information")
cursor=mycon.cursor()
cursor.execute("show tables")
flag=0
for x in cursor:
    print(x,type(x))
    if(x[0]=="draft2"):
        print("hi")
        flag=1

if(flag==0):
    dataframe.to_sql('draft2', con = engine)#creates the table only if does not exist
    query = "ALTER TABLE draft2 \
    ADD tag VARCHAR(100) DEFAULT 'miscellaneous'"
    cursor.execute(query)
cursor.execute("SELECT * FROM draft2")

# Fetch all the matching rows
result = cursor.fetchall()

# Get column names
columns = [desc[0] for desc in cursor.description]

# Create a PrettyTable instance
table = PrettyTable(columns)

# Add rows to the table
for row in result:
    table.add_row(row)

# Print the table
print(table)
#categorising data
sql = "SELECT Narration FROM draft2"
cursor.execute(sql)

# adding the custom tags
tags=[]
count=0
result = cursor.fetchall()
for row in result:
    column3_value = row[0]  # Assuming 'Narration' is at index 0
    update_query = """
    UPDATE draft2
    SET tag = %s
    WHERE Narration = %s
    """
    print("Narration:", column3_value)
    # Prompt user for a new 'tag' value
    new_val = input("Enter new tag value: ")
    if new_val not in tags:
        count+=1
    if(count==9):
        print("WARNING!!!after this tag no more new tags can be added(if added code will terminate)")
    elif(count>10):
        print("ERROR!!!Too many tags code ending here.......")
        sys.exit()
    if(new_val==""):
        new_val="miscellaneous"
    update_values = (new_val, column3_value)
    cursor.execute(update_query, update_values)
    mycon.commit()

#printing data
cursor.execute("SELECT * FROM draft2")
result = cursor.fetchall()
columns = [desc[0] for desc in cursor.description]
table = PrettyTable(columns)
for row in result:
    table.add_row(row)
print(table)
#converting to dataframe
cursor.execute("SELECT * FROM draft2")
result = cursor.fetchall()
columns = [desc[0] for desc in cursor.description]
df = pd.DataFrame(result, columns=columns)
print(df)
grouped_df = df.groupby('tag')['Withdrawal Amt.'].sum().reset_index()
debit = grouped_df['Withdrawal Amt.'].tolist()
tags = grouped_df['tag'].tolist()
#pie chart 
colors = ['#FF66B2', '#B39CD0', '#87CEFA', '#98FB98', '#FFD700', 
          '#98FB98', '#7CFC00', '#32CD32', '#00FA9A', '#00FF7F', 
          '#FFA500', '#FFD700', '#DAA520', '#FFC0CB', '#FF69B4', 
          '#836FFF', '#6A5ACD', '#483D8B', '#87CEEB', '#5F9EA0']

fig, ax = plt.subplots(figsize=(14, 14))
wedges, texts, autotexts = ax.pie(debit, labels=tags, autopct='%1.1f%%', startangle=90, colors=colors)

# Add a legend directly without bbox_to_anchor
legend = ax.legend(wedges, [f'{t} ({p.get_text()})' for t, p in zip(tags, autotexts)]
, title='Tags', loc="center left", title_fontsize='15')
# Adjust the position of the legend
ax.add_artist(legend)
legend.set_bbox_to_anchor((1.05, 0.5))

# Annotate the largest percentage below the legend
largest_index = np.argmax(debit)
largest_percentage = autotexts[largest_index].get_text()
ax.text(1.05, -0.2, f'Largest Percentage :{largest_percentage} tag "{tags[largest_index]}"', ha='center', va='center', size=10, color='black')


# Add a title
ax.set_title('Expenditure Distribution', fontsize=16, pad=20)

# Save the figure with adjusted bounding box and padding
plt.savefig('your_pie_chart.png', bbox_inches='tight', pad_inches=3)

# Show the pie chart
plt.show()