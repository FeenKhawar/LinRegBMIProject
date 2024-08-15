import pandas as pd
import matplotlib.pyplot as plt
import os

df = pd.read_csv("DatasetForLinearRegressionsOnBMI.csv")

if os.path.exists("BMI_Histogram.png"):
    print("BMI_Histogram.png already exists.")
else:
    fig, ax = plt.subplots()
    BMI = df["BMI"]
    BMI.hist(ax=ax, bins=75, density=True, edgecolor="black")
    plt.xlabel("BMI", fontsize=16, labelpad=15)
    plt.ylabel("Density", fontsize=16, labelpad=15)
    plt.title("BMI Histogram", fontsize=20, fontweight='bold', pad=30)
    plt.grid(False)
    plt.tight_layout()
    fig.savefig("BMI_Histogram.png")

if os.path.exists("UE_Histograms.png"):
    print("UE_Histograms.png already exists.")
else:
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    UE = df["unemployment rate"]
    ln_UE = df["ln(unemployment rate)"]
    UE.hist(ax=ax[0], bins=25, density=True, edgecolor="black")
    ax[0].set_xlabel("Unemployment Rates", fontsize=16, labelpad=15)
    ax[0].set_ylabel("Density", fontsize=16, labelpad=15)
    ax[0].set_title("Histogram of Unemployment Rates\nCollapsed by Year and State", fontsize=17, fontweight='bold', pad=30)
    ax[0].grid(False)
    ln_UE.hist(ax=ax[1], bins=25, density=True, edgecolor="black")
    ax[1].set_xlabel("Natural Log of Unemployment Rates", fontsize=16, labelpad=15)
    ax[1].set_ylabel("Density", fontsize=16, labelpad=15)
    ax[1].set_title("Histogram of Natural Log\nof Unemployment Rates\nCollapsed by Year and State", fontsize=17, fontweight='bold', pad=30)
    ax[1].grid(False)
    plt.tight_layout()
    fig.savefig("UE_Histograms.png") 

if os.path.exists("Mean_BMI_Year.png"):
    print("Mean_BMI_Year.png already exists.")
else:
    fig, ax = plt.subplots()
    mean_bmi_by_year = df.groupby("year")["BMI"].mean()
    mean_bmi_by_year.plot.bar(ax=ax)
    for i, (year, mean_bmi) in enumerate(mean_bmi_by_year.items()):
        ax.text(i, mean_bmi + 0.1, f'{mean_bmi:.2f}', ha='center', va='bottom')
    ax.set_ylim(0,32)
    plt.xticks(rotation=0)    
    plt.xlabel("Year", fontsize=16, labelpad=15)
    plt.ylabel("Mean BMI", fontsize=16, labelpad=15)
    plt.title("Mean BMI by Year", fontsize=20, fontweight='bold', pad=30)
    plt.tight_layout()
    fig.savefig("Mean_BMI_Year.png")

if os.path.exists("Mean_BMI_Education.png)"):
    print("Mean_BMI_Education.png already exists.")
else:
    fig, ax = plt.subplots()
    mean_bmi_by_education = df.groupby("education")["BMI"].mean()
    colors = ['goldenrod', 'teal', 'mediumseagreen', 'mediumorchid']
    bars = mean_bmi_by_education.plot.bar(ax=ax, color=colors)
    for i, (education, mean_bmi) in enumerate(mean_bmi_by_education.items()):
        ax.text(i, mean_bmi + 0.15, f'{mean_bmi:.2f}', ha='center', va='bottom', fontsize=10.0)
    ax.set_ylim(0,33)
    ax.set_xticks([])
    education_labels = [
        'Did Not Graduate High School',
        'Graduated High School',
        'Attended College or Technical School',
        'Graduated from College or Technical School']
    ax.legend(bars.patches, education_labels, loc='upper center', bbox_to_anchor=(0.5, -0.20), ncol=1, title="Education Level", fontsize=10, title_fontsize=12)
    plt.xlabel("Education Classification", fontsize=16, labelpad=10)
    plt.ylabel("Mean BMI", fontsize=16, labelpad=5)
    plt.title("Mean BMI by Education Classification", fontsize=20, fontweight='bold', pad=30)
    plt.tight_layout()
    fig.savefig("Mean_BMI_Education.png")

if os.path.exists("Mean_BMI_Race.png"):
    print("Mean_BMI_Race.png already exists.")
else:
    fig, ax = plt.subplots()
    mean_bmi_by_race = df.groupby("race")["BMI"].mean()
    colors = ['silver', 'dimgray', 'coral', 'peru', 'gold', 'forestgreen', 'cadetblue', 'sienna']
    bars = mean_bmi_by_race.plot.bar(ax=ax, color=colors)
    for i, (race, mean_bmi) in enumerate(mean_bmi_by_race.items()):
        ax.text(i, mean_bmi + 0.20, f'{mean_bmi:.2f}', ha='center', va='bottom', fontsize=10.0)
    ax.set_ylim(0,35)
    ax.set_xticks([])
    race_labels = [
        'White only, non-Hispanic',
        'Black only, non-Hispanic',
        'American Indian or Alaskan Native',
        'Asian only, non-Hispanic',
        'Native Hawaiian or other Pacific Islander',
        'Other race only, non-Hispanic',
        'Multiracial, non-Hispanic',
        'Hispanic']
    ax.legend(bars.patches, race_labels, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=1, title="Race Classification", fontsize=9, title_fontsize=11)
    plt.xlabel("Race", fontsize=16, labelpad=5)  
    plt.ylabel("Mean BMI", fontsize=16, labelpad=2.5)
    plt.title("Mean BMI by Race", fontsize=20, fontweight='bold', pad=30)
    plt.tight_layout()
    # plt.subplots_adjust(bottom=0.80)
    fig.savefig("Mean_BMI_Race.png")

if os.path.exists("Mean_BMI_Income.png"):
    print("Mean_BMI_Income.png already exists.")
else:
    fig, ax = plt.subplots()
    mean_bmi_by_income = df.groupby("income")["BMI"].mean()
    colors = ['maroon', 'orangered', 'darkgoldenrod', 'darkorange', 'gold', 'yellowgreen', 'deepskyblue', 'lightseagreen', 'teal', 'orchid', 'darkmagenta']
    bars = mean_bmi_by_income.plot.bar(ax=ax, color=colors)
    for i, (income, mean_bmi) in enumerate(mean_bmi_by_income.items()):
        ax.text(i, mean_bmi + 0.10, f'{mean_bmi:.2f}', ha='center', va='bottom', fontsize=7.5)
    ax.set_xticks([])
    income_labels = [
        'Less than $10,000',
        '$10,000 - $14,999',
        '$15,000 - $19,999',
        '$20,000 - $24,999',
        '$25,000 - $34,999',
        '$35,000 - $49,999',
        '$50,000 - $74,999',
        '$75,000 - $99,999',
        '$100,000 - $149,999',
        '$150,000 - $199,999',
        'More than $200,000']
    ax.legend(bars.patches, income_labels, loc='center left', bbox_to_anchor=(1, 0.5), ncol=1, title="Race Classification", fontsize=9, title_fontsize=11)
    plt.xlabel("Income Level", fontsize=16, labelpad=15)
    plt.ylabel("Mean BMI", fontsize=16, labelpad=5)
    plt.title("Mean BMI by Income Level", fontsize=20, fontweight='bold', pad=30)
    plt.tight_layout()
    fig.savefig("Mean_BMI_Income.png")

if os.path.exists("Boxplots_ln(UE).png"):
    print("Boxplots_ln(UE).png already exists.")
else:
    fig, ax = plt.subplots()
    ln_UE_by_year = []
    unique_years = df['year'].unique()
    for year in unique_years:
        year_data = df[df['year'] == year]
        ln_UE_values = year_data["ln(unemployment rate)"].values
        ln_UE_by_year.append(ln_UE_values)
    ax.boxplot(ln_UE_by_year)
    ax.set_xticklabels(unique_years)
    plt.xlabel("Year", fontsize=16, labelpad=15) 
    plt.ylabel("Natural Log of Unemployment Rate", fontsize=16, labelpad=15)
    plt.title("Box Plots of the Natural Log of the\nUnemployment Rates of States by Year", fontsize=18, fontweight='bold', pad=30)
    plt.tight_layout()
    fig.savefig("Boxplots_ln(UE).png")

if os.path.exists("Scatter_Income_BMI.png"):
    print("Scatter_Income_BMI.png already exists.")
else:
    fig, ax = plt.subplots()
    income = df['income']
    BMI = df['BMI']
    ax.scatter(income, BMI, s=10)
    plt.xlabel("Income Classification", fontsize=16, labelpad=15)  
    plt.ylabel("BMI", fontsize=16, labelpad=5)
    plt.title("Scatterplot of BMI\nby Income Classification", fontsize=20, fontweight='bold', pad=30)
    plt.tight_layout()
    fig.savefig("Scatter_Income_BMI.png")

if os.path.exists("Scatter_UE_BMI.png"):
    print("Scatter_UE_BMI.png already exists.")
else:
    fig, ax = plt.subplots()
    UE = df['unemployment rate']
    BMI = df['BMI']
    ax.scatter(UE, BMI, s=5)
    plt.xlabel("Unemployment Rate", fontsize=16, labelpad=15)  
    plt.ylabel("BMI", fontsize=16, labelpad=5)
    plt.title("Scatterplot of BMI\nby Unemployment Rate", fontsize=20, fontweight='bold', pad=30)
    plt.tight_layout()
    fig.savefig("Scatter_UE_BMI.png")