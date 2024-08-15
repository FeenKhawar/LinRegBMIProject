import pandas as pd
import statsmodels.api as sm

# Load the dataset
df1 = pd.read_csv('DatasetForLinearRegressionsOnBMI.csv')

summary_of_lnUE = df1["ln(unemployment rate)"].describe()
print("Information on 'ln(unemployment rate)' variable:\n")
print(summary_of_lnUE)
print()
summary_of_UE = df1["unemployment rate"].describe()
print("Information on 'unemployment rate' variable:\n")
print(summary_of_UE)
print()
summary_of_BMI = df1["BMI"].describe()
print("Information on 'BMI' variable:\n")
print(summary_of_BMI)
print()

# For quick linear regression of just ln(unemployment rate):

# Ensure all data is numeric
for col in df1.columns:
    df1[col] = pd.to_numeric(df1[col], errors='coerce')

# Convert boolean columns to integers
for col in df1.select_dtypes(include=['bool']).columns:
    df1[col] = df1[col].astype(int)

# Define the independent and dependent variables
X = df1.drop(columns=['BMI', 'state code', 'unemployment rate', 'height (in)', 'weight (Ib)', 'income', 'race', 'education', 'sex', 'year', 'state'])
y = df1['BMI']

# Add a constant to the model
X = sm.add_constant(X)

# Fit the model
model = sm.OLS(y, X).fit()

# Print the summary
print("Linear Regression of just ln(unemployment rate) and BMI:")
print(model.summary())

# Predict on the same dataset
y_pred = model.predict(X)

# For alternate regression (which excludes the unemployment rate altogether)

df2 = pd.read_csv('DatasetForLinearRegressionsOnBMI.csv')

# Convert relevant object types to categorical
df2['state'] = df2['state'].astype('category')
df2['year'] = df2['year'].astype('category')
df2['sex'] = df2['sex'].astype('category')
df2['income'] = df2['income'].astype('category')
df2['race'] = df2['race'].astype('category')
df2['education'] = df2['education'].astype('category')

# Create dummy variables for fixed effects
df2 = pd.get_dummies(df2, columns=['state', 'year', 'sex', 'income', 'race', 'education'], drop_first=True)

# Ensure all data is numeric
for col in df2.columns:
    df2[col] = pd.to_numeric(df2[col], errors='coerce')

# Convert boolean columns to integers
for col in df2.select_dtypes(include=['bool']).columns:
    df2[col] = df2[col].astype(int)

# Define the independent and dependent variables
X = df2.drop(columns=['BMI', 'state code', 'unemployment rate', 'ln(unemployment rate)', 'height (in)', 'weight (Ib)'])
y = df2['BMI']

# Add a constant to the model
X = sm.add_constant(X)

# Fit the model
model = sm.OLS(y, X).fit()

# Print the summary
print("Alternate Linear Regression where unemployment rates are entirely excluded:")
print(model.summary())

# Predict on the same dataset
y_pred = model.predict(X)

# For main regression:

# Load the dataset
df3 = pd.read_csv('DatasetForLinearRegressionsOnBMI.csv')

# Convert relevant object types to categorical
df3['state'] = df3['state'].astype('category')
df3['year'] = df3['year'].astype('category')
df3['sex'] = df3['sex'].astype('category')
df3['income'] = df3['income'].astype('category')
df3['race'] = df3['race'].astype('category')
df3['education'] = df3['education'].astype('category')

# Create dummy variables for fixed effects
df3 = pd.get_dummies(df3, columns=['state', 'year', 'sex', 'income', 'race', 'education'], drop_first=True)

# Ensure all data is numeric
for col in df3.columns:
    df3[col] = pd.to_numeric(df3[col], errors='coerce')

# Convert boolean columns to integers
for col in df3.select_dtypes(include=['bool']).columns:
    df3[col] = df3[col].astype(int)

# Define the independent and dependent variables
X = df3.drop(columns=['BMI', 'state code', 'unemployment rate', 'height (in)', 'weight (Ib)'])
y = df3['BMI']

# Add a constant to the model
X = sm.add_constant(X)

# Fit the model
model = sm.OLS(y, X).fit()

# Print the summary
print("Main Linear Regression for this project:")
print(model.summary())

# Predict on the same dataset
y_pred = model.predict(X)

print("Linear Regression output above is the main linear regression of the project.")
print("In regards to the extremely low R^2 value, please see page 15 of my paper, 'BMIProjectPaper.pdf,' for a full explanation.")