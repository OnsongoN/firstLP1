# %%
%pip install pyodbc  
%pip install python-dotenv 

# %%
import pyodbc      #just installed with pip
from dotenv import dotenv_values    #import the dotenv_values function from the dotenv package
import pandas as pd
import warnings 

warnings.filterwarnings('ignore')

# %%
# Load environment variables from .env file into a dictionary
environment_variables = dotenv_values('.env')


# Get the values for the credentials you set in the '.env' file
server = environment_variables.get("SERVER")
database = environment_variables.get("DATABASE")
username = environment_variables.get("USERNAME")
password = environment_variables.get("PASSWORD")
connection_string = f"DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"

# %%
# Use the connect method of the pyodbc library and pass in the connection string.
# This will connect to the server and might take a few seconds to be complete. 
# Check your internet connection if it takes more time than necessary

connection = pyodbc.connect(connection_string)

# %%
# Reading the 2020 dataset. 

query = "Select * from LP1_startup_funding2020"

data2020 = pd.read_sql(query, connection)

# %%
# Reading the 2021 dataset. 

query = "Select * from LP1_startup_funding2021"

data2021 = pd.read_sql(query, connection)

# %%
# Reading the 2019 dataset. 

data2019 = pd.read_csv('startup_funding2019.csv')

# %%
data2018 = pd.read_csv('startup_funding2018.csv')

# %%
data2019.head(5)

# %% [markdown]
# datasets highlights, shape and composition
# 

# %%
data2018.shape

# %%
data2019.shape

# %%
data2020.shape

# %%
data2021.shape

# %%
data2018.dtypes

# %% [markdown]
# the amount column need to be changed, 
# we can investigate the company about to see if it has relevant information
# 

# %%
data2018.head(5)

# %% [markdown]
# ,,  ,the industry, round/series, amount, location columns need to be synchronized 
# we should use columns in the 2018 data only

# %%
data2019.dtypes

# %% [markdown]
#  the founded, HeadQuarter, founders, investors column, do we need it?, what it does is like about company in 2018, stage is similar to round/series, 

# %% [markdown]
# 

# %%
data2019.head(5)

# %%
data2020.dtypes

# %%
data2020.head(10)

# %%
data2021.dtypes

# %%
data2021.head(10)

# %% [markdown]
# Assuming we will use company name, industry, type of funding, amount and location
# 
# Null hypothesis: The amount of funding a company receives is not affected by its location, type of industry, and the type of funding
# alternative hypothesis; the amount of funding received by a company is significantly affected by the location of the company, type of funding and the industry the company is.
# 
# Questions:
# 1. The industry in which a startup operates is related to the amount of funding it receives
# 2. The location of a startup is related to the amount of funding it receives.
# 3. The funding type of the company is related to the amount the company receives in funding
# 4. The time when the startups were funded affects the amount the startups received.

# %% [markdown]
# Cleaning Data

# %%
data2019.isnull().sum()

# %%
data2018.isnull().sum()

# %%
data2020.isnull().sum()

# %%
data2021.isnull().sum()

# %% [markdown]
# Given thata the 2018 data does not have null values, and the columns we are using for the 2018, 2019, 2020 and 2021 data have just a few missing variables, I will extract them then investigate them further.

# %%
data2018.describe()

# %%
data2019.describe()

# %%
data2020.describe()

# %% [markdown]
# 

# %%
data2021.describe()

# %% [markdown]
# a number of variables in the datasets have wrong data types and their summary statistics do not show up. They need to be changed

# %%
data2018.info()

# %% [markdown]
# the amount variable need to be changed to an integer or float

# %%
data2019.info()

# %%
data2020.info()

# %%
data2021.info()

# %% [markdown]
# renaming the columns before merging

# %%
#renaming 2018
data2018.rename(columns = {"Round/Series":"Stage"}, inplace = True)

# %%
#renaming 2019
data2019.rename(columns = {"Company/Brand":"Company Name","Sector":"Industry","What it does":"About Company","Amount($)":"Amount","HeadQuarter":"Location"}, inplace = True)
data2019.head(5)

# %%
#renaming 2020 data
data2020.rename(columns = {"Company_Brand":"Company Name","Sector":"Industry","What_it_does":"About Company","HeadQuarter":"Location"}, inplace = True)
data2020.sample(5)

# %%
#renaming 2021 columns
data2021.rename(columns = {"Company_Brand":"Company Name","Sector":"Industry","What_it_does":"About Company","HeadQuarter":"Location"}, inplace = True)
data2021.head(5)

# %% [markdown]
# dropping irrelevant columns

# %%
nwdata2019 = data2019[['Company Name','Founded','Industry','About Company','Amount','Stage','Location']]
nwdata2019.tail(5)

# %%
nwdata2020 = data2020[['Company Name','Founded','Industry','About Company','Amount','Stage','Location']]
nwdata2020.tail(5)

# %%
nwdata2021 = data2021[['Company Name','Founded','Industry','About Company','Amount','Stage','Location']]
nwdata2021.tail(5)

# %%
#adding a year column to each dataset
data2018["Year"]= 2018

# %%
#adding a year column to each dataset
nwdata2019["Year"]= 2019

# %%
#adding a year column to each dataset
nwdata2020["Year"]= 2020

# %%
#adding a year column to each dataset
nwdata2021["Year"]= 2021

# %% [markdown]
# Merging the data

# %%
combineddata = pd.concat([data2018, nwdata2019, nwdata2020,nwdata2021])
combineddata.sample(10)


