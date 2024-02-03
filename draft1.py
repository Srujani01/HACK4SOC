import pandas as pd
import  pymysql
from prettytable import PrettyTable
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
import numpy as np


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

# Fetch all the matching rows
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
    if(new_val==""):
        new_val="miscellaneous"
    # Tuple containing the values to be updated
    update_values = (new_val, column3_value)

    # Execute the update query with parameters
    cursor.execute(update_query, update_values)

    # Commit the changes to the database
    mycon.commit()
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
cursor.execute("SELECT * FROM draft2")

# Fetch all the rows
result = cursor.fetchall()

# Get column names
columns = [desc[0] for desc in cursor.description]

# Create a DataFrame
df = pd.DataFrame(result, columns=columns)

# Print the DataFrame
print(df)

# Group by 'tag' and calculate the sum of 'Withdrawal Amt.'
grouped_df = df.groupby('tag')['Withdrawal Amt.'].sum().reset_index()

# Extract columns from the grouped DataFrame
debit = grouped_df['Withdrawal Amt.'].tolist()
tags = grouped_df['tag'].tolist()

colors = ['#FF66B2', '#B39CD0', '#87CEFA', '#98FB98', '#FFD700', 
          '#98FB98', '#7CFC00', '#32CD32', '#00FA9A', '#00FF7F', 
          '#FFA500', '#FFD700', '#DAA520', '#FFC0CB', '#FF69B4', 
          '#836FFF', '#6A5ACD', '#483D8B', '#87CEEB', '#5F9EA0']

# Create a pie chart
plt.figure(figsize=(10, 10))
plt.pie(debit, labels=tags, autopct='%1.1f%%', startangle=90, colors=colors)

# Add a legend
plt.legend(tags, title='Tags', bbox_to_anchor=(1, 0.5), loc="center left", title_fontsize='15')

# Add a title
plt.title('Expenditure Distribution', fontsize=16)

# Show the pie chart
plt.show()
plt.figure(figsize=(10, 10))
plt.pie(debit, labels=tags, autopct='%1.1f%%', startangle=90, colors=colors)

# Add a legend
plt.legend(tags, title='Tags', bbox_to_anchor=(1, 0.5), loc="center left", title_fontsize='15')

# Add a title
plt.title('Expenditure Distribution', fontsize=16)

# Show the pie chart with adjusted bounding box
plt.savefig('your_pie_chart.png', bbox_inches='tight')  # Save the figure with adjusted bounding box
plt.show()