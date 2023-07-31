#!/usr/bin/env python
# coding: utf-8

# This notebook lets you play around with an AI coding assistant. Here are some instructions on how to use it:
# - The assistant will attempt to autocomplete code automatically
# - You can also guide it by creating a comment indicating what you want to do, press enter and wait
#     - As the comments are already placed for this exercise: place your cursor at the end of each comment and press enter, and wait for the code suggestion
# - If there is a suggestion, you can press Tab to accept it
#     - You can also hover over the suggestion (before accepting it) to go through alternative suggestions if you think the code is not right
# 
# Other ways to use the assistant:
# - Select a code snippet and right click, you will see a couple of things Codeium can do for you
# - Chat with the AI assistant by clicking on the VSCode extension on the left

# Data dictionary of the data that we will use:
# 
# | Variable | Definition | Key             |
# |----------|------------|-----------------|
# | PassengeId | Passenger ID | |
# | Survived | Survival   | 0 = No, 1 = Yes |
# | Pclass | Ticket class	| 1 = 1st, 2 = 2nd, 3 = 3rd |
# | Name | Passenger name | |
# | Sex | Sex	| |
# | Age | Age in years | 	|
# | Sibsp | # of siblings / spouses aboard the Titanic | 
# | Parch | # of parents / children aboard the Titanic |	
# | Ticket | Ticket number | |
# | Fare | Passenger fare	| |
# | Cabin | Cabin number | |
# | Embarked | Port of Embarkation | C = Cherbourg, Q = Queenstown, S = Southampton|

# ## Exercise 1

# In this exercise, we will load the Titanic dataset from a CSV file and perform some initial exploratory data analysis to get acquainted with the data.
# 
# We will use the coding assistant to guide us with this. The instructions (commented) are already there to start off easily. 

# In[ ]:


# import necessary functions
from functions import load_titanic_dataset, visualize_age_distribution
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[ ]:


# Load the titanic dataset and store it in a DataFrame


# In[ ]:


# Show the first 5 rows of the DataFrame


# In[ ]:


# Describe the statistics of the dataframe


# In[ ]:


# Visualise the age distribution of the passengers


# Now lets try to check the following:
# - Check the shape of the dataset (number of rows and columns).
# - Inspect the column names and data types of each column.
# - Check for any missing values in the dataset.
# 
# You should create the instructions yourself in the following cells.

# In[ ]:





# In[ ]:





# In[ ]:





# # Exercise 2 
# 
# In this exercise, we want to find out the title for each passenger and add it in a new column. 
# 
# There is already an example function that uses regex (regular expressions) for this. However, it does not work correctly yet. 
# Don't worry if you are not an expert in regex, we will let the coding assistant explain what the function does, and let it guide us in improving it.
# 
# There are a couple of steps to perform. 

# Look at the "Name" column below, and try to think about what separates the title from the rest of the name

# In[ ]:


# Display the Name column
df["Name"].head(15)


# Test the function that is already present, and look at the initial output

# In[ ]:


def extract_titles(df):
    df["Title"] = df["Name"].str.extract(" ([A-Za-z]+)\,", expand=False)
    return df


# In[ ]:


# Extract the titles of the passengers and put in a new column
df = extract_titles(df)


# In[ ]:


df.head()


# The new "Title" column does not actually contain the titles, so something is wrong.
# 
# Highlight the extract_titles function above, right click, and click "Codeium: Explain Selected Code Block"
# 
# Try to find out what is wrong, and fix the function. You can ask your coding assistant for help, and use the notebook cells below.

# In[ ]:





# In[ ]:





# In[ ]:





# If the functionality is correct, try to improve the function by letting the coding assistant create docstrings for you.
# 
# Also play around a bit to find out what more things the assistant can improve for you (e.g. modify the code to deal with potential errors)

# In[ ]:





# In[ ]:





# ## Exercise 3

# Let's find out how easy it is to clean and visualise parts of the dataset with the help of a coding assistant.
# 
# Try to perform the following things:
# 1. Clean the dataset 
#     - Fill missing values in the "Age" column with the average age
#     - For the "Embarked" colum, fill missing values with the most frequent port of embarkation
#     - For the "Cabin" column, handle missing values by either dropping the column or categorizing passengers into "Cabin" and "No Cabin" groups
# 2. Feature engineering
#     - Create a "Family Size" column with the family size (try to see if the AI assistant knows which columns are are needed for this, and what they mean)
#         - p.s. don't forget to count the passenger itself
# 3. Outlier detection
#     - Investigate if there are any outliers in the numerical columns (e.g., "Age," "Fare")
# 4. Bin the age of the passenger into groups ("Child", "Young Adult", "Adult", "Senior") and visualise these
# 5. Calculate the survival rate by gender, passenger class and title

# In[ ]:





# In[ ]:





# In[ ]:





# ## Exercise 4
# 
# In the functions.py file are some more functions that can be used with this dataset: extract_ticket_prefix, family_survival_info
# 
# Open the functions.py file and try to following:
# - Use the "Explain" button above the functions to find out what the functions do
# - Use the "Generate docstring" button above the functions to generate code documentation
# - Use the "Refactor" button above the functions to try various functionalities to improve the code:
#     - Add typing
#     - Check for bugs
#     - Make this faster and more efficient
#     - Generate unit tests

# In[ ]:





# In[ ]:





# In[ ]:





# ## Exercise 5
# 
# Let's try some more advanced stuff, and see how far the coding assistant takes us. We will use sklearn for this.
# 
# We will try to predict whether a passenger survived or not based on features like age, sex, class, etc. We will use a Machine learning model (Random Forest Classifier) for this. We will also visualise the results to understand the model's performance.
# 

# In[ ]:


# Re-read the data to be sure we start with the raw data
df = load_titanic_dataset("titanic.csv")
df.head()


# 1. Prepare the data
# 
# Steps we need to perform:
# - Only keep the Age, Sex, and Pclass columns, as well as the Survived column
# - Convert the "Sex" column to a numeric representation, 0 for female and 1 for male
# - Fill missing values in the "Age" column with the mean age
# - Split the dataset into features (X) and the target variable (y). The target variable should be the "Survived" column

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# 2. Train-Test split
# 
# - Split the data into training and testing sets, with 80% of the data in the training set and 20% in the testing set.

# In[ ]:





# In[ ]:





# 3. Model training
# 
# - Import the Random Forest Classifier from scikit-learn
# - Initialize the model and specify any hyperparameters (e.g., the number of trees in the forest)
# - Train the model on the training data using the fit() method

# In[ ]:





# In[ ]:





# In[ ]:





# 4. Model Evaluation
# 
# - Use the trained model to make predictions on the testing set using the predict() method
# - Calculate accuracy by comparing the predicted results with the actual survival status to evaluate the model's performance
# - Create a confusion matrix
# - Plot the feature importance to show how much influence each feature has on survival
# - Create a countplot for predictions vs. ground truth

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




