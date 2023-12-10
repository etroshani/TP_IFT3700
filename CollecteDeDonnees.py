import pandas as pd
import numpy as np
import re

import ssl
ssl._create_default_https_context = ssl._create_unverified_context      #Ignore les erreurs de certificats(temporaire)

#Enlève les *, (...), [...], NaN de la colonne "Country/Territory" qui sera l'index
def indexClean(content):
    content = content.dropna()
    content = content.str.replace(r'\*', '', regex=True).str.strip()
    content = content.apply(lambda x: re.sub(r'\[.*?\]', '', x).strip())
    content = content.apply(lambda x: re.sub(r'\(.*?\)', '', x).strip())

    return content

#La fonction removeGarbage sert à enlever les charactères non nécessaires ainsi que calcule les médianes nécessaires dans les
#données des tables en question
def removeGarbage(content):
    newCol = re.sub(r'\[.*?\]', '', content).strip()                #Efface les [] et les charactères à l'intérieur
    newCol = re.sub(r'\(.*?\)', '', newCol).strip()                 #Efface les () et les charactères à l'intérieur
    newCol = newCol.replace("%", '')                                #Efface les %
    newCol = newCol.replace("<", '')                                #Efface les <
    newCol = newCol.replace(">", '')                                #Efface les >

    values = re.findall(r'\d+(?:\.\d+)?', newCol)                   #Crée une liste contenant les valeurs trouvées dans les string
    if '/' in newCol:
        sides = newCol.split('/')
        medians = []
        for side in sides:                                          #On isole chaque côté du / afin de trouver les médianes
            sideValues = re.findall(r'\d+(?:\.\d+)?', side)
            sideValues = [float(val) for val in sideValues if val]
            if len(sideValues) >= 2:                                #Lorsque 2 valeurs ou plus sont retrouvés dans un bord, on fait la médiane(Exemple le 4-6 dans 4-6/3.14)
                medians.append(np.median(sideValues))
            elif len(sideValues) == 1:                              #Lorsque c'est une seule valeur d'un bord. (Exemple le 3.14 dans 3.14/4-6)
                medians.append(sideValues[0])
        return np.median(np.array(medians))                         #Une fois les médianes des 2 bords ont été trouvés, on calcule la médiane des 2 bords

    elif ('/' not in newCol) and len(values) >= 2:                  #Lorsque au moins 2 valeurs sont trouvées et qu'on ne retrouve pas de / dans le string
        medians = []
        for i in range(0, len(values), 2):
            #Médiane des 2 valeurs conjointes
            median = np.median([float(values[i]), float(values[i+1])])
            medians.append(median)
        return np.median(np.array(medians))
    elif len(values) == 1:                                          #On retourne la valeur telle quelle lorsqu'elle est seule
        return values[0]
    return np.nan                                                   #On retourne NaN lorsque ca ne respecte aucune des conditions


def valeurs(colonne):
    avg = colonne.mean()
    med = colonne.median()
    max = colonne.max()
    min = colonne.min()
    var = colonne.var()
    mod = colonne.mode()
    return avg, med, max, min, var, mod


#Lien 1 - List_of_countries_by_GDP_(nominal)_per_capita
url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)_per_capita"
tables = pd.read_html(url)
df = tables[1][[('Country/Territory', 'Country/Territory'), ('United Nations[7]','Estimate')]]
df.columns = [''.join(col).strip() for col in df.columns.values]
df.columns = ['Country/Territory', 'GDP_per_capita United Nations Estimate']
df['Country/Territory'] = indexClean(df['Country/Territory'])
df = df.set_index('Country/Territory')
df['GDP_per_capita United Nations Estimate'] = pd.to_numeric(df["GDP_per_capita United Nations Estimate"], errors='coerce')
df = df[df.index.notna()]                   #Enlève les rows de valeurs NaN dans la colonne de noms de pays
colValeurs = valeurs(df['GDP_per_capita United Nations Estimate'])
bin = (df['GDP_per_capita United Nations Estimate'].copy()).apply(lambda x: 1 if x > colValeurs[1] else 0)   #Crée une copie binaire de la colonne


#*****Faute dans le doc, pas de Average download speed (Mbit/s) (Ookla)
#Lien 2 - List_of_countries_by_Internet_connection_speeds
url2 = "https://en.wikipedia.org/wiki/List_of_countries_by_Internet_connection_speeds"
tables2 = pd.read_html(url2)
df2 = tables2[1]                                          #Table voulu
df2 = df2[['Country/Territory', 'Mediandownloadspeed(Mbit/s)(Ookla)[1]']]  # Keeping only the specified columns
df2 = df2.set_index('Country/Territory')  # Setting 'Country/Territory' as the index
colValeurs2 = valeurs(df2['Mediandownloadspeed(Mbit/s)(Ookla)[1]'])
bin2 = (df2['Mediandownloadspeed(Mbit/s)(Ookla)[1]'].copy()).apply(lambda x: 1 if x > colValeurs2[1] else 0)
dfFinal = pd.merge(df, df2, left_index=True, right_index=True, how='outer')

#Lien 3 - List_of_countries_by_alcohol_consumption_per_capita
url3 = "https://en.wikipedia.org/wiki/List_of_countries_by_alcohol_consumption_per_capita"
tables3 = pd.read_html(url3)
df3 = tables3[1][['Country', '2016[8]']]                                  #Colonne voulue
df3.columns = ['Country/Territory', 'Alcohol consumption per capita, 2016']
df3['Country/Territory'] = indexClean(df3['Country/Territory'])
df3 = df3.set_index('Country/Territory')
df3['Alcohol consumption per capita, 2016'] = pd.to_numeric(df3['Alcohol consumption per capita, 2016'], errors = 'coerce')             
colValeurs3 = valeurs(df3['Alcohol consumption per capita, 2016'])
bin3 = (df3['Alcohol consumption per capita, 2016'].copy()).apply(lambda x: 1 if x > colValeurs3[1] else 0)
dfFinal = pd.merge(dfFinal, df3, left_index=True, right_index=True, how='outer')

#Lien 4 - List_of_countries_by_intentional_homicide_rate
url4 = "https://en.wikipedia.org/wiki/List_of_countries_by_intentional_homicide_rate"
tables4 = pd.read_html(url4)
df4 = tables4[1][['Location', 'Rate']]                                      #Colonne voulue
df4.columns = ['Country/Territory', 'Rate of intentional homicide']
df4['Country/Territory'] = df4['Country/Territory'].str.replace(r'\*', '', regex=True).str.strip()          #On n'applique pas la fonction indexClean car on veut séparer la région de kurdistan en Iraq, et les régions dans le UK
df4 = df4.set_index('Country/Territory')
df4["Rate of intentional homicide"] = pd.to_numeric(df4["Rate of intentional homicide"], errors = 'coerce')     
colValeurs4 = valeurs(df4["Rate of intentional homicide"])
bin4 = (df4["Rate of intentional homicide"].copy()).apply(lambda x: 1 if x > colValeurs4[1] else 0)
dfFinal = pd.merge(dfFinal, df4, left_index=True, right_index=True, how='outer')


#Lien 5 - List_of_countries_with_highest_military_expenditures
url5 = "https://en.wikipedia.org/wiki/List_of_countries_with_highest_military_expenditures"
tables5 = pd.read_html(url5)
df5 = tables5[1][['Country', '% of GDP']]                                      #Colonne voulue
df5.columns = ['Country/Territory', 'Highest military expenditures, % of GDP']
df5['Country/Territory'] = indexClean(df5['Country/Territory'])
df5 = df5.set_index('Country/Territory')
df5['Highest military expenditures, % of GDP'] = pd.to_numeric(df5['Highest military expenditures, % of GDP'], errors = 'coerce') 
colValeurs5 = valeurs(df5['Highest military expenditures, % of GDP'])
bin5 = (df5['Highest military expenditures, % of GDP'].copy()).apply(lambda x: 1 if x > colValeurs5[1] else 0)
dfFinal = pd.merge(dfFinal, df5, left_index=True, right_index=True, how='outer')


#Pas de colonne pour l'année 2019, seulement 2021(2022 report)
#Lien 6 - List_of_countries_by_Human_Development_Index
url6 = "https://en.wikipedia.org/wiki/List_of_countries_by_Human_Development_Index"
tables6 = pd.read_html(url6)
hdiColumns = [col for col in tables6[1].columns if col[0] == 'HDI']
col6 = hdiColumns[0]
df6 = tables6[1][[('Nation',                                 'Nation'), col6]]
df6.columns = [''.join(col).strip() for col in df6.columns.values]
df6.columns = ['Country/Territory', 'Human Development Index, 2021']
df6 = df6.set_index('Country/Territory')
df6['Human Development Index, 2021'] = pd.to_numeric(df6['Human Development Index, 2021'], errors = 'coerce') 
colValeurs6 = valeurs(df6['Human Development Index, 2021'])
bin6 = (df6['Human Development Index, 2021'].copy()).apply(lambda x: 1 if x > colValeurs6[1] else 0)
dfFinal = pd.merge(dfFinal, df6, left_index=True, right_index=True, how='outer')


#Lien 7 - Democracy_Index
url7 = "https://en.wikipedia.org/wiki/Democracy_Index"
tables7 = pd.read_html(url7)
df7 = tables7[5][['Country', '2020']]
df7.columns = ['Country/Territory', 'Democracy Index, 2020']
df7 = df7.set_index('Country/Territory')
df7['Democracy Index, 2020'] = pd.to_numeric(df7['Democracy Index, 2020'], errors = 'coerce') 
colValeurs7 = valeurs(df7['Democracy Index, 2020'])
bin7 = (df7['Democracy Index, 2020'].copy()).apply(lambda x: 1 if x > colValeurs7[1] else 0)
dfFinal = pd.merge(dfFinal, df7, left_index=True, right_index=True, how='outer')



#Lien 8 - List_of_countries_by_tertiary_education_attainment
url8 = "https://en.wikipedia.org/wiki/List_of_countries_by_tertiary_education_attainment"
tables8 = pd.read_html(url8)
df8 = tables8[2]                                          #Table voulu
col8 = [col for col in tables8[2].columns if col[1] == '2 years']
df8 = tables8[2][[('Country','Country'), col8[0]]]
df8.columns = [''.join(col).strip() for col in df8.columns.values]
df8.columns = ['Country/Territory', 'Tertiary education attainment, 2 years']
df8 = df8.set_index('Country/Territory')
df8['Tertiary education attainment, 2 years'] = pd.to_numeric(df8['Tertiary education attainment, 2 years'], errors = 'coerce') 
colValeurs8 = valeurs(df8['Tertiary education attainment, 2 years'])
bin8 = (df8['Tertiary education attainment, 2 years'].copy()).apply(lambda x: 1 if x > colValeurs8[1] else 0)
dfFinal = pd.merge(dfFinal, df8, left_index=True, right_index=True, how='outer')



#Lien 9 - Importance_of_religion_by_country
url9 = "https://en.wikipedia.org/wiki/Importance_of_religion_by_country"
tables9 = pd.read_html(url9)
df9 = tables9[5][['Country/district', 'Yes, important[1]']]
df9.columns = ['Country/Territory', 'Importance of religion by country, %']
df9 = df9.set_index('Country/Territory')
df9['Importance of religion by country, %'] = df9['Importance of religion by country, %'].str.rstrip("%").astype(float)                 #Enlève les %
df9['Importance of religion by country, %'] = pd.to_numeric(df9['Importance of religion by country, %'], errors = 'coerce') 
colValeurs9 = valeurs(df9['Importance of religion by country, %'])
bin9 = (df9['Importance of religion by country, %'].copy()).apply(lambda x: 1 if x > colValeurs9[1] else 0)
dfFinal = pd.merge(dfFinal, df9, left_index=True, right_index=True, how='outer')


#Lien 10 - Christianity_by_country
url10 = "https://en.wikipedia.org/wiki/Christianity_by_country"
tables10 = pd.read_html(url10)
df10 = tables10[7]                                          #Table voulu
df10 = tables10[7][['Country or entity', '% Christian']]
df10.columns = ['Country/Territory', 'Christianity by country, %']
df10['Christianity by country, %'] = df10['Christianity by country, %'].astype(str).apply(removeGarbage)
df10['Country/Territory'] = indexClean(df10['Country/Territory'])
df10 = df10.set_index('Country/Territory')
df10['Christianity by country, %'] = pd.to_numeric(df10['Christianity by country, %'], errors = 'coerce') 
colValeurs10 = valeurs(df10['Christianity by country, %'])
bin10 = (df10['Christianity by country, %'].copy()).apply(lambda x: 1 if x > colValeurs10[1] else 0)
dfFinal = pd.merge(dfFinal, df10, left_index=True, right_index=True, how='outer')



#Lien 11 - Islam_by_country
url11 = "https://en.wikipedia.org/wiki/Islam_by_country"
tables11 = pd.read_html(url11)
df11 = tables11[7]                                          #Table voulu
df11 = tables11[7][['Country/Region', 'Muslim percentage of total population']]
df11.columns = ['Country/Territory', 'Islam by country, %']
df11['Islam by country, %'] = df11['Islam by country, %'].astype(str).apply(removeGarbage)
df11['Country/Territory'] = indexClean(df11['Country/Territory'])
df11 = df11.set_index('Country/Territory')
df11['Islam by country, %'] = pd.to_numeric(df11['Islam by country, %'], errors = 'coerce') 
colValeurs11 = valeurs(df11['Islam by country, %'])
bin11 = (df11['Islam by country, %'].copy()).apply(lambda x: 1 if x > colValeurs11[1] else 0)
dfFinal = pd.merge(dfFinal, df11, left_index=True, right_index=True, how='outer')


#Lien 12 - Buddhism_by_country
url12 = "https://en.wikipedia.org/wiki/Buddhism_by_country"
tables12 = pd.read_html(url12)
df12 = tables12[0]                                          #Table voulu
df12 = df12[[('Country/Territory', 'Country/Territory'), ('Pew estimates (2010)[1]','% Buddhist')]]
df12.columns = [''.join(col).strip() for col in df12.columns.values]
df12.columns = ['Country/Territory', 'Buddhism by country (Pew estimates 2010), % Buddhist']
df12['Buddhism by country (Pew estimates 2010), % Buddhist'] = df12['Buddhism by country (Pew estimates 2010), % Buddhist'].astype(str).apply(removeGarbage)
df12['Country/Territory'] = indexClean(df12['Country/Territory'])
df12 = df12.set_index('Country/Territory')
df12['Buddhism by country (Pew estimates 2010), % Buddhist'] = pd.to_numeric(df12['Buddhism by country (Pew estimates 2010), % Buddhist'], errors = 'coerce') 
colValeurs12 = valeurs(df12['Buddhism by country (Pew estimates 2010), % Buddhist'])
bin12 = (df12['Buddhism by country (Pew estimates 2010), % Buddhist'].copy()).apply(lambda x: 1 if x > colValeurs12[1] else 0)
dfFinal = pd.merge(dfFinal, df12, left_index=True, right_index=True, how='outer')


#Lien 13 - Jewish_population_by_country
url13 = "https://en.wikipedia.org/wiki/Jewish_population_by_country"
tables13 = pd.read_html(url13)
df13 = tables13[36]                                         #Table voulu
df13 = df13[[('Countries','Countries'), ('Core population','pct')]]
df13.columns = [''.join(col).strip() for col in df13.columns.values]
df13.columns = ['Country/Territory', 'Jewish population by country, %']
df13['Country/Territory'] = indexClean(df13['Country/Territory'])
df13 = df13.set_index('Country/Territory')
df13['Jewish population by country, %'] = pd.to_numeric(df13['Jewish population by country, %'], errors = 'coerce') 
colValeurs13 = valeurs(df13['Jewish population by country, %'])
bin13 = (df13['Jewish population by country, %'].copy()).apply(lambda x: 1 if x > colValeurs13[1] else 0)
dfFinal = pd.merge(dfFinal, df13, left_index=True, right_index=True, how='outer')


#***Faute dans le doc, pas de Under-five mortality (deaths/1,000 live births) – 2019 estimates
#Lien 14 - List_of_countries_by_infant_and_under-five_mortality_rates
url14 = "https://en.wikipedia.org/wiki/List_of_countries_by_infant_and_under-five_mortality_rates"
tables14 = pd.read_html(url14)
df14 = tables14[0]                                                          #Table voulu
df14 = df14[['Location', '2020 mortality rate, under-5 (per 1000 live births)']]
df14.columns = ['Country/Territory', 'Infant and under-five mortality rates']
df14['Country/Territory'] = indexClean(df14['Country/Territory'])
df14 = df14.set_index('Country/Territory')
df14['Infant and under-five mortality rates'] = pd.to_numeric(df14['Infant and under-five mortality rates'], errors = 'coerce') 
colValeurs14 = valeurs(df14['Infant and under-five mortality rates'])
bin14 = (df14['Infant and under-five mortality rates'].copy()).apply(lambda x: 1 if x > colValeurs14[1] else 0)
dfFinal = pd.merge(dfFinal, df14, left_index=True, right_index=True, how='outer')


#Lien 15 - Age_of_criminal_responsibility
url15 = "https://en.wikipedia.org/wiki/Age_of_criminal_responsibility"
tables15 = pd.read_html(url15)
df15 = tables15[2]                                          #Table voulu
df15 = df15[['Country', 'Age (reduced)[a]']]
df15.columns = ['Country/Territory', 'Age of criminal responsibility']
df15['Country/Territory'] = indexClean(df15['Country/Territory'])
df15 = df15.set_index('Country/Territory')
df15['Age of criminal responsibility'] = pd.to_numeric(df15['Age of criminal responsibility'], errors = 'coerce') 
colValeurs15 = valeurs(df15['Age of criminal responsibility'])
bin15 = (df15['Age of criminal responsibility'].copy()).apply(lambda x: 1 if x > colValeurs15[1] else 0)
dfFinal = pd.merge(dfFinal, df15, left_index=True, right_index=True, how='outer')

#Lien 16 - List_of_countries_by_minimum_wage
url16 = "https://en.wikipedia.org/wiki/List_of_countries_by_minimum_wage"
tables16 = pd.read_html(url16)
df16 = tables16[1]                                          #Table voulu
df16 = df16[[('Country','Country'), ('Annual','Nominal (US$)[6]')]]
df16.columns = [''.join(col).strip() for col in df16.columns.values]
df16.columns = ['Country/Territory', 'Countries by minimum wage']
df16 = df16.drop(df16.index[0])
df16 = df16.set_index('Country/Territory')
df16['Countries by minimum wage'] = pd.to_numeric(df16['Countries by minimum wage'], errors = 'coerce') 
colValeurs16 = valeurs(df16['Countries by minimum wage'])
bin16 = (df16['Countries by minimum wage'].copy()).apply(lambda x: 1 if x > colValeurs16[1] else 0)
dfFinal = pd.merge(dfFinal, df16, left_index=True, right_index=True, how='outer')

#Lien 17 - List_of_countries_by_external_debt
url17 = "https://en.wikipedia.org/wiki/List_of_countries_by_external_debt"
tables17 = pd.read_html(url17)
df17 = tables17[0]                                          #Table voulu
df17 = df17[['Country/Region', '% of GDP']]
df17.columns = ['Country/Territory', 'Countries by external debt, % of GDP']
df17['Country/Territory'] = indexClean(df17['Country/Territory'])
df17 = df17.set_index('Country/Territory')
df17['Countries by external debt, % of GDP'] = pd.to_numeric(df17['Countries by external debt, % of GDP'], errors = 'coerce') 
colValeurs17 = valeurs(df17['Countries by external debt, % of GDP'])
bin17 = (df17['Countries by external debt, % of GDP'].copy()).apply(lambda x: 1 if x > colValeurs17[1] else 0)
dfFinal = pd.merge(dfFinal, df17, left_index=True, right_index=True, how='outer')

#Lien 18 - List_of_countries_by_income_equality
url18 = "https://en.wikipedia.org/wiki/List_of_countries_by_income_equality"
tables18 = pd.read_html(url18)
df18 = tables18[1]                                          #Table voulu
df18 = df18[[('Country','Country'), ('World Bank Gini[5][6]','%')]]
df18.columns = [''.join(col).strip() for col in df18.columns.values]
df18.columns = ['Country/Territory', 'Countries by income equlity, %']
df18 = df18.drop(df18.index[0])
df18 = df18.set_index('Country/Territory')
df18['Countries by income equlity, %'] = pd.to_numeric(df18['Countries by income equlity, %'], errors = 'coerce') 
colValeurs18 = valeurs(df18['Countries by income equlity, %'])
bin18 = (df18['Countries by income equlity, %'].copy()).apply(lambda x: 1 if x > colValeurs18[1] else 0)
dfFinal = pd.merge(dfFinal, df18, left_index=True, right_index=True, how='outer')

#Lien 19 - List_of_countries_by_total_health_expenditure_per_capita
url19 = "https://en.wikipedia.org/wiki/List_of_countries_by_total_health_expenditure_per_capita"
tables19 = pd.read_html(url19)
df19 = tables19[1]                                          #Table voulu
df19 = df19[['Location', '2018']]
df19.columns = ['Country/Territory', 'Countries by total health expenditure per capita, 2018']
df19['Country/Territory'] = indexClean(df19['Country/Territory'])
df19 = df19.set_index('Country/Territory')
df19['Countries by total health expenditure per capita, 2018'] = pd.to_numeric(df19['Countries by total health expenditure per capita, 2018'], errors = 'coerce') 
colValeurs19 = valeurs(df19['Countries by total health expenditure per capita, 2018'])
bin19 = (df19['Countries by total health expenditure per capita, 2018'].copy()).apply(lambda x: 1 if x > colValeurs19[1] else 0)
dfFinal = pd.merge(dfFinal, df19, left_index=True, right_index=True, how='outer')

#Lien 20 - List_of_countries_by_suicide_rate
url20 = "https://en.wikipedia.org/wiki/List_of_countries_by_suicide_rate"
tables20 = pd.read_html(url20)
df20 = tables20[1]                                          #Table voulu
df20 = df20[['Country', 'All']]
df20.columns = ['Country/Territory', 'Countries by suicide rate']
df20['Country/Territory'] = indexClean(df20['Country/Territory'])
df20 = df20.set_index('Country/Territory')
df20['Countries by suicide rate'] = pd.to_numeric(df20['Countries by suicide rate'], errors = 'coerce') 
colValeurs20 = valeurs(df20['Countries by suicide rate'])
bin20 = (df20['Countries by suicide rate'].copy()).apply(lambda x: 1 if x > colValeurs20[1] else 0)
dfFinal = pd.merge(dfFinal, df20, left_index=True, right_index=True, how='outer')

#***Pas de Table 2019 List by the World Bank, 2019.
#Lien 21 - List_of_sovereign_states_and_dependencies_by_total_fertility_rate
url21 = "https://en.wikipedia.org/wiki/List_of_sovereign_states_and_dependencies_by_total_fertility_rate"
tables21 = pd.read_html(url21)
df21 = tables21[4]                                              #Table voulu
df21 = df21[['Country', 'Fertility rate in 2019 (births/woman)']][:210]   #Les valeurs importantes s'arrêtent à la Corée du Sude(row:210)
df21.columns = ['Country/Territory', 'Sovereign states and dependencies by fertility rate in 2019 (births/woman)']
df21['Country/Territory'] = indexClean(df21['Country/Territory'])
df21 = df21.set_index('Country/Territory')
df21['Sovereign states and dependencies by fertility rate in 2019 (births/woman)'] = pd.to_numeric(df21['Sovereign states and dependencies by fertility rate in 2019 (births/woman)'], errors = 'coerce') 
colValeurs21 = valeurs(df21['Sovereign states and dependencies by fertility rate in 2019 (births/woman)'])
bin21 = (df21['Sovereign states and dependencies by fertility rate in 2019 (births/woman)'].copy()).apply(lambda x: 1 if x > colValeurs21[1] else 0)
dfFinal = pd.merge(dfFinal, df21, left_index=True, right_index=True, how='outer')

#***Pas de table Prevalence of current tobacco use among persons aged 15 years and older, 2000.
#Lien 22 - Tobacco_consumption_by_country
url22 = "https://en.wikipedia.org/wiki/Tobacco_consumption_by_country"
tables22 = pd.read_html(url22)
df22 = tables22[0]                                          #Table voulu
df22 = df22[['Country', 'Cigarettes']]
df22.columns = ['Country/Territory', 'Tobacco_consumption_by_country']
df22['Country/Territory'] = indexClean(df22['Country/Territory'])
df22 = df22.set_index('Country/Territory')
df22['Tobacco_consumption_by_country'] = pd.to_numeric(df22['Tobacco_consumption_by_country'], errors = 'coerce') 
colValeurs22 = valeurs(df22['Tobacco_consumption_by_country'])
bin22 = (df22['Tobacco_consumption_by_country'].copy()).apply(lambda x: 1 if x > colValeurs22[1] else 0)
dfFinal = pd.merge(dfFinal, df22, left_index=True, right_index=True, how='outer')

#Lien 23 - List_of_countries_by_obesity_rate
url23 = "https://en.wikipedia.org/wiki/List_of_countries_by_obesity_rate"
tables23 = pd.read_html(url23)
df23 = tables23[1]                                          #Table voulu
df23 = df23[['Country', 'Obesity rate (%)']]
df23.columns = ['Country/Territory', 'Countries by obesity rate, %']
df23 = df23.set_index('Country/Territory')
df23['Countries by obesity rate, %'] = pd.to_numeric(df23['Countries by obesity rate, %'], errors = 'coerce') 
colValeurs23 = valeurs(df23['Countries by obesity rate, %'])
bin23 = (df23['Countries by obesity rate, %'].copy()).apply(lambda x: 1 if x > colValeurs23[1] else 0)
dfFinal = pd.merge(dfFinal, df23, left_index=True, right_index=True, how='outer')

#Lien 24 - List_of_countries_by_number_of_Internet_users
url24 = "https://en.wikipedia.org/wiki/List_of_countries_by_number_of_Internet_users"
tables24 = pd.read_html(url24)
df24 = tables24[5]                                          #Table voulu
df24 = df24[['Country or area', 'Pct']]
df24.columns = ['Country/Territory', 'Countries by number of internet users, %']
df24['Countries by number of internet users, %'] = df24['Countries by number of internet users, %'].astype(str).apply(removeGarbage)
df24['Country/Territory'] = indexClean(df24['Country/Territory'])
df24 = df24.set_index('Country/Territory')
df24['Countries by number of internet users, %'] = pd.to_numeric(df24['Countries by number of internet users, %'], errors = 'coerce') 
colValeurs24 = valeurs(df24['Countries by number of internet users, %'])
bin24 = (df24['Countries by number of internet users, %'].copy()).apply(lambda x: 1 if x > colValeurs24[1] else 0)
dfFinal = pd.merge(dfFinal, df24, left_index=True, right_index=True, how='outer')

#Lien 25 - List_of_countries_by_median_age
url25 = "https://en.wikipedia.org/wiki/List_of_countries_by_median_age"
tables25 = pd.read_html(url25)
df25 = tables25[0]                                                  #Table voulu
df25 = df25[[('Country/Territory', 'Country/Territory', 'Country/Territory'), ('Median ages in years','2020 medians', 'Combined')]]
df25.columns = [''.join(col).strip() for col in df25.columns.values]
df25.columns = ['Country/Territory', 'Countries by median age']
df25['Country/Territory'] = df25['Country/Territory'].replace('Palestine (West Bank)', 'West Bank')         #On identifie la region spécifique de West Bank en Palestine
df25['Country/Territory'] = df25['Country/Territory'].replace('Palestine (Gaza Strip)', 'Gaza Strip')       #On identifie la region spécifique de Gaza en Palestine
df25['Country/Territory'] = indexClean(df25['Country/Territory'])
df25 = df25.set_index('Country/Territory')
df25['Countries by median age'] = pd.to_numeric(df25['Countries by median age'], errors = 'coerce') 
colValeurs25 = valeurs(df25['Countries by median age'])
bin25 = (df25['Countries by median age'].copy()).apply(lambda x: 1 if x > colValeurs25[1] else 0)
dfFinal = pd.merge(dfFinal, df25, left_index=True, right_index=True, how='outer')

#Lien 26 - List_of_countries_by_economic_freedom
url26 = "https://en.wikipedia.org/wiki/List_of_countries_by_economic_freedom"
tables26 = pd.read_html(url26)
df26 = tables26[1]                                      #Table voulu
df26 = df26[['Country', 'Score']]
df26.columns = ['Country/Territory', 'Countries by economic freedom']
df26 = df26.set_index('Country/Territory')
df26['Countries by economic freedom'] = pd.to_numeric(df26['Countries by economic freedom'], errors = 'coerce') 
colValeurs26 = valeurs(df26['Countries by economic freedom'])
bin26 = (df26['Countries by economic freedom'].copy()).apply(lambda x: 1 if x > colValeurs26[1] else 0)
dfFinal = pd.merge(dfFinal, df26, left_index=True, right_index=True, how='outer')

#***Pas de table per capita 2017
#Lien 27 - List_of_countries_by_oil_production
url27 = "https://en.wikipedia.org/wiki/List_of_countries_by_oil_production"
tables27 = pd.read_html(url27)
df27 = tables27[1]                                          #Table voulu
df27 = df27[['Country', 'Oil production April 2022 (bbl/day)[1]']]
df27.columns = ['Country/Territory', 'Countries by oil production']
df27['Country/Territory'] = indexClean(df27['Country/Territory'])
df27 = df27.set_index('Country/Territory')
df27['Countries by oil production'] = pd.to_numeric(df27['Countries by oil production'], errors = 'coerce') 
colValeurs27 = valeurs(df27['Countries by oil production'])
bin27 = (df27['Countries by oil production'].copy()).apply(lambda x: 1 if x > colValeurs27[1] else 0)
dfFinal = pd.merge(dfFinal, df27, left_index=True, right_index=True, how='outer')

#Lien 28 - List_of_countries_by_population_growth_rate
url28 = "https://en.wikipedia.org/wiki/List_of_countries_by_population_growth_rate"
tables28 = pd.read_html(url28)
df28 = tables28[0]                                      #Table voulu
df28 = df28[[('Country (or territory)', 'Unnamed: 0_level_1'), ('UN[5] 2015–20', 'Unnamed: 6_level_1')]]
df28.columns = [''.join(col).strip() for col in df28.columns.values]
df28.columns = ['Country/Territory', 'Countries by population growth rate']
df28['Country/Territory'] = indexClean(df28['Country/Territory'])
df28 = df28.set_index('Country/Territory')
df28 = df28.drop(df28.index[0])
df28['Countries by population growth rate'] = pd.to_numeric(df28['Countries by population growth rate'], errors = 'coerce') 
colValeurs28 = valeurs(df28['Countries by population growth rate'])
bin28 = (df28['Countries by population growth rate'].copy()).apply(lambda x: 1 if x > colValeurs28[1] else 0)
dfFinal = pd.merge(dfFinal, df28, left_index=True, right_index=True, how='outer')

#Lien 29 - List_of_countries_by_life_expectancy
url29 = "https://en.wikipedia.org/wiki/List_of_countries_by_life_expectancy"
tables29 = pd.read_html(url29)
df29 = tables29[3]                                      #Table voulu
df29 = df29[[('Countries', 'Countries'), ('Life expectancy at birth', 'All')]]
df29.columns = [''.join(col).strip() for col in df29.columns.values]
df29.columns = ['Country/Territory', 'Countries by life expectancy']
df29['Country/Territory'] = indexClean(df29['Country/Territory'])
df29 = df29.drop(df29.index[0])
df29 = df29.set_index('Country/Territory')
df29['Countries by life expectancy'] = pd.to_numeric(df29['Countries by life expectancy'], errors = 'coerce') 
colValeurs29 = valeurs(df29['Countries by life expectancy'])
bin29 = (df29['Countries by life expectancy'].copy()).apply(lambda x: 1 if x > colValeurs29[1] else 0)
dfFinal = pd.merge(dfFinal, df29, left_index=True, right_index=True, how='outer')

#Lien 30 - List_of_countries_by_meat_consumption
url30 = "https://en.wikipedia.org/wiki/List_of_countries_by_meat_consumption"
tables30 = pd.read_html(url30)
df30 = tables30[1]                                      #Table voulu
df30 = df30[['Country/Dependency', 'kg/person (2002)[9][note 1]']]
df30.columns = ['Country/Territory', 'Countries by meat consumption, kg/person']
df30 = df30.set_index('Country/Territory')
df30['Countries by meat consumption, kg/person'] = pd.to_numeric(df30['Countries by meat consumption, kg/person'], errors = 'coerce') 
colValeurs30 = valeurs(df30['Countries by meat consumption, kg/person'])
bin30 = (df30['Countries by meat consumption, kg/person'].copy()).apply(lambda x: 1 if x > colValeurs30[1] else 0)
dfFinal = pd.merge(dfFinal, df30, left_index=True, right_index=True, how='outer')

#Lien 31 - List_of_countries_by_incarceration_rate
url31 = "https://en.wikipedia.org/wiki/List_of_countries_by_incarceration_rate"
tables31 = pd.read_html(url31)
df31  = tables31[0]                                     #Table voulu
df31 = df31[['Location', 'Rates per 100,000[2]']]
df31.columns = ['Country/Territory', 'Countries by incarceration rate, rates per 100 000']
df31['Country/Territory'] = indexClean(df31['Country/Territory'])
df31 = df31.drop(df31.index[0])
df31 = df31.set_index('Country/Territory')
df31['Countries by incarceration rate, rates per 100 000'] = pd.to_numeric(df31['Countries by incarceration rate, rates per 100 000'], errors = 'coerce') 
colValeurs31 = valeurs(df31['Countries by incarceration rate, rates per 100 000'])
bin31 = (df31['Countries by incarceration rate, rates per 100 000'].copy()).apply(lambda x: 1 if x > colValeurs31[1] else 0)
dfFinal = pd.merge(dfFinal, df31, left_index=True, right_index=True, how='outer')

#Lien 32 - List_of_countries_by_literacy_rate
url32 = "https://en.wikipedia.org/wiki/List_of_countries_by_literacy_rate"
tables32 = pd.read_html(url32)
df32 = tables32[1]                                      #Table voulu
df32 = df32[[('Country', 'Country'), ('Elderly (65+)','Rate')]]
df32.columns = [''.join(col).strip() for col in df32.columns.values]
df32.columns = ['Country/Territory', 'Countries by literacy rate']
df32['Country/Territory'] = indexClean(df32['Country/Territory'])
df32 = df32.set_index('Country/Territory')
df32['Countries by literacy rate'] = pd.to_numeric(df32['Countries by literacy rate'], errors = 'coerce') 
colValeurs32 = valeurs(df32['Countries by literacy rate'])
bin32 = (df32['Countries by literacy rate'].copy()).apply(lambda x: 1 if x > colValeurs32[1] else 0)
dfFinal = pd.merge(dfFinal, df32, left_index=True, right_index=True, how='outer')

#Lien 33 - List_of_countries_by_age_at_first_marriage
url33 = "https://en.wikipedia.org/wiki/List_of_countries_by_age_at_first_marriage"
tables33 = pd.read_html(url33)
df33_1 = tables33[0]                                     #Table voulu: Africa
df33_2 = tables33[1]                                     #Table voulu: Americas
df33_3 = tables33[2]                                     #Table voulu: Asia
df33_4 = tables33[3]                                     #Table voulu: Europe
df33_5 = tables33[4]                                     #Table voulu: Oceania
#Concaténation des tables
df33 = pd.concat([df33_1[['Country', 'Women']], df33_2[['Country', 'Women']], df33_3[['Country', 'Women']], df33_4[['Country', 'Women']], df33_5[['Country', 'Women']]]) 
df33.columns = ['Country/Territory', 'Countries by age at first marriage, women']
df33['Country/Territory'] = indexClean(df33['Country/Territory'])
df33 = df33.set_index('Country/Territory')
df33['Countries by age at first marriage, women'] = pd.to_numeric(df33['Countries by age at first marriage, women'], errors = 'coerce') 
colValeurs33 = valeurs(df33['Countries by age at first marriage, women'])
bin33 = (df33['Countries by age at first marriage, women'].copy()).apply(lambda x: 1 if x > colValeurs33[1] else 0)
dfFinal = pd.merge(dfFinal, df33, left_index=True, right_index=True, how='outer')

#Lien 34 - List_of_countries_by_spending_on_education_(%25_of_GDP)
url34 = "https://en.wikipedia.org/wiki/List_of_countries_by_spending_on_education_(%25_of_GDP)"
tables34 = pd.read_html(url34)
df34 = tables34[0]                                      #Table voulu
df34 = df34[['Country or subnational area', 'Expenditure on education (% of GDP)']]
df34.columns = ['Country/Territory', 'Countries by spending on education, % of GDP']
df34 = df34.set_index('Country/Territory')
df34['Countries by spending on education, % of GDP'] = pd.to_numeric(df34['Countries by spending on education, % of GDP'], errors = 'coerce') 
colValeurs34 = valeurs(df34['Countries by spending on education, % of GDP'])
bin34 = (df34['Countries by spending on education, % of GDP'].copy()).apply(lambda x: 1 if x > colValeurs34[1] else 0)
dfFinal = pd.merge(dfFinal, df34, left_index=True, right_index=True, how='outer')

#***Homeless per 10 000********
#Lien 35 - List_of_countries_by_homeless_population
url35 = "https://en.wikipedia.org/wiki/List_of_countries_by_homeless_population"
tables35 = pd.read_html(url35)
df35 = tables35[0]                                      #Table voulu
df35 = df35[['Country', 'Homeless per 10k']]
df35.columns = ['Country/Territory', 'Countries by homeless population, per 10k']
df35 = df35.set_index('Country/Territory')
df35['Countries by homeless population, per 10k'] = pd.to_numeric(df35['Countries by homeless population, per 10k'], errors = 'coerce') 
colValeurs35 = valeurs(df35['Countries by homeless population, per 10k'])
bin35 = (df35['Countries by homeless population, per 10k'].copy()).apply(lambda x: 1 if x > colValeurs35[1] else 0)
dfFinal = pd.merge(dfFinal, df35, left_index=True, right_index=True, how='outer')

#Lien 36 - List_of_countries_by_milk_consumption_per_capita
url36 = "https://en.wikipedia.org/wiki/List_of_countries_by_milk_consumption_per_capita"
tables36 = pd.read_html(url36)
df36 = tables36[0]                                            #Table voulu
df36 = df36[['Country', 'Milk consumption 2013 (kg/capita/yr) [1]']]
df36.columns = ['Country/Territory', 'Countries by milk consumption per capita, kg/capita/year, 2013']
df36 = df36.set_index('Country/Territory')
df36['Countries by milk consumption per capita, kg/capita/year, 2013'] = pd.to_numeric(df36['Countries by milk consumption per capita, kg/capita/year, 2013'], errors = 'coerce') 
colValeurs36 = valeurs(df36['Countries by milk consumption per capita, kg/capita/year, 2013'])
bin36 = (df36['Countries by milk consumption per capita, kg/capita/year, 2013'].copy()).apply(lambda x: 1 if x > colValeurs36[1] else 0)
dfFinal = pd.merge(dfFinal, df36, left_index=True, right_index=True, how='outer')

#Lien 37 - List_of_countries_by_number_of_scientific_and_technical_journal_articles
url37 = "https://en.wikipedia.org/wiki/List_of_countries_by_number_of_scientific_and_technical_journal_articles"
tables37 = pd.read_html(url37)
df37 = tables37[0]                                                  #Table voulu
df37 = df37[['Country', 'Scientific publications per capita (per million)']]
df37.columns = ['Country/Territory', 'Countries by number of scientific and technical journal articles, per million']
df37 = df37.set_index('Country/Territory')
df37['Countries by number of scientific and technical journal articles, per million'] = pd.to_numeric(df37['Countries by number of scientific and technical journal articles, per million'], errors = 'coerce') 
colValeurs37 = valeurs(df37['Countries by number of scientific and technical journal articles, per million'])
bin37 = (df37['Countries by number of scientific and technical journal articles, per million'].copy()).apply(lambda x: 1 if x > colValeurs37[1] else 0)
dfFinal = pd.merge(dfFinal, df37, left_index=True, right_index=True, how='outer')

#Lien 38 - Books_published_per_country_per_year
url38 = "https://en.wikipedia.org/wiki/Books_published_per_country_per_year"
tables38 = pd.read_html(url38)
df38 = tables38[0]                                  #Table voulu
df38 = df38[['Country', 'Titles']]
df38.columns = ['Country/Territory', 'Countries by books published per year']
df38 = df38.set_index('Country/Territory')
df38['Countries by books published per year'] = pd.to_numeric(df38['Countries by books published per year'], errors = 'coerce') 
colValeurs38 = valeurs(df38['Countries by books published per year'])
bin38 = (df38['Countries by books published per year'].copy()).apply(lambda x: 1 if x > colValeurs38[1] else 0)
dfFinal = pd.merge(dfFinal, df38, left_index=True, right_index=True, how='outer')

#Lien 39 - List_of_countries_by_food_energy_intake
url39 = "https://en.wikipedia.org/wiki/List_of_countries_by_food_energy_intake"
tables39 = pd.read_html(url39)
df39 = tables39[0]                                                                          #Table voulu
df39 = df39[[('Country', 'Country'), ('Average daily dietary energy consumption per capita[8]', 'kilocalories')]]
df39.columns = [''.join(col).strip() for col in df39.columns.values]
df39.columns = ['Country/Territory', 'Countries by food energy intake, kilocalories']
df39['Country/Territory'] = indexClean(df39['Country/Territory'])
df39 = df39.set_index('Country/Territory')
df39['Countries by food energy intake, kilocalories'] = pd.to_numeric(df39['Countries by food energy intake, kilocalories'], errors = 'coerce') 
colValeurs39 = valeurs(df39['Countries by food energy intake, kilocalories'])
bin39 = (df39['Countries by food energy intake, kilocalories'].copy()).apply(lambda x: 1 if x > colValeurs39[1] else 0)
dfFinal = pd.merge(dfFinal, df39, left_index=True, right_index=True, how='outer')


#Lien 40 - List_of_countries_by_average_yearly_temperature
url40 = "https://en.wikipedia.org/wiki/List_of_countries_by_average_yearly_temperature"
tables40 = pd.read_html(url40)
df40 = tables40[0]                                                  #Table voulu
df40 = df40[['Country', 'Average yearly temperature (1961–1990 Celsius)']]
df40.columns = ['Country/Territory', 'Countries by average yearly temperature, 1961–1990 Celsius']
df40['Country/Territory'] = indexClean(df40['Country/Territory'])
df40 = df40.set_index('Country/Territory')
df40['Countries by average yearly temperature, 1961–1990 Celsius'] = pd.to_numeric(df40['Countries by average yearly temperature, 1961–1990 Celsius'], errors = 'coerce') 
colValeurs40 = valeurs(df40['Countries by average yearly temperature, 1961–1990 Celsius'])
bin40 = (df40['Countries by average yearly temperature, 1961–1990 Celsius'].copy()).apply(lambda x: 1 if x > colValeurs40[1] else 0)
dfFinal = pd.merge(dfFinal, df40, left_index=True, right_index=True, how='outer')



##   Nettoyage final de la table    ##
dfFinal = dfFinal.drop('Population replacement', axis=0)
dfFinal = dfFinal.drop('World total', axis=0)
dfFinal = dfFinal.drop('World', axis=0)
dfFinal = dfFinal.drop('Total', axis=0)
dfFinal = dfFinal.drop('Global', axis=0)
dfFinal = dfFinal.drop('Asia', axis=0)
dfFinal = dfFinal.drop('Americas', axis=0)
dfFinal = dfFinal.drop('Africa', axis=0)
dfFinal = dfFinal.drop('Europe', axis=0)
dfFinal = dfFinal.drop('European Union', axis=0)
dfFinal = dfFinal.drop('French Southern and Antarctic Lands', axis=0)
dfFinal = dfFinal.drop('Latin America and the Caribbean', axis=0)
dfFinal = dfFinal.drop('Middle East-North Africa', axis=0)
dfFinal = dfFinal.drop('North America', axis=0)
dfFinal = dfFinal.drop('Oceania', axis=0)
dfFinal = dfFinal.drop('South-East Asia', axis=0)
dfFinal = dfFinal.drop('Western Pacific', axis=0)
dfFinal = dfFinal.drop('Eastern Mediterranean', axis=0)
dfFinal = dfFinal.drop('British Indian Ocean Territory', axis=0)
dfFinal = dfFinal.drop('Cocos  Islands', axis=0)
dfFinal = dfFinal.drop('Holy See', axis=0)
dfFinal = dfFinal.drop('Iraq (Kurdistan Region)', axis=0)
dfFinal = dfFinal.drop('Iraq. Central Iraq', axis=0)
dfFinal = dfFinal.drop('Mainland China', axis=0)
dfFinal = dfFinal.drop('Pitcairn Islands', axis=0)
dfFinal = dfFinal.drop('Republika Srpska', axis=0)
dfFinal = dfFinal.drop('Saint Barthelemy', axis=0)
dfFinal = dfFinal.drop('Somaliland', axis=0)
dfFinal = dfFinal.drop('Svalbard and Jan Mayen', axis=0)
dfFinal = dfFinal.drop('United Kingdom  (Great Britain and Northern Ireland)', axis=0)


# Nettoyage de Democratic Republic of Congo
combinedData = dfFinal.loc[["Democratic Republic of Congo","Congo", "Congo DR", "Congo, Democratic Republic of", "Congo, Republic of", "DR Congo", "Democratic Republic of the Congo", "Republic of Congo", "Republic of the Congo"]].ffill().iloc[-1]
dfFinal.loc["Democratic Republic of Congo"] = combinedData
dfFinal.drop(index=["Congo", "Congo DR", "Congo, Democratic Republic of", "Congo, Republic of", "DR Congo", "Democratic Republic of the Congo", "Republic of Congo", "Republic of the Congo"], inplace=True)

# Nettoyage de Czech Republic
dfFinal.loc['Czech Republic'] = dfFinal.loc['Czech Republic'].fillna(dfFinal.loc['Czechia'])
dfFinal.drop(index='Czechia', inplace=True)

# Nettoyage de Sao Tome and Principe
dfFinal.loc['Sao Tome and Principe'] = dfFinal.loc['Sao Tome and Principe'].fillna(dfFinal.loc['São Tomé and Príncipe'])
dfFinal.drop(index='São Tomé and Príncipe', inplace=True)

# Nettoyage de Eswatini
dfFinal.loc['Eswatini'] = dfFinal.loc['Eswatini'].fillna(dfFinal.loc['Swaziland'])
dfFinal.drop(index='Swaziland', inplace=True)

# Nettoyage de North Macedonia
dfFinal.loc['North Macedonia'] = dfFinal.loc['North Macedonia'].fillna(dfFinal.loc['Macedonia'])
dfFinal.drop(index='Macedonia', inplace=True)

# Nettoyage de Kyrgyzstan
dfFinal.loc['Kyrgyzstan'] = dfFinal.loc['Kyrgyzstan'].fillna(dfFinal.loc['Kyrgyz Republic'])
dfFinal.drop(index='Kyrgyz Republic', inplace=True)

# Nettoyage de Cabo Verde
dfFinal.loc['Cabo Verde'] = dfFinal.loc['Cabo Verde'].fillna(dfFinal.loc['Cape Verde'])
dfFinal.drop(index='Cape Verde', inplace=True)

# Nettoyage de United Kingdom  (England and Wales)
dfFinal.loc['United Kingdom  (England and Wales)'] = dfFinal.loc['United Kingdom  (England and Wales)'].fillna(dfFinal.loc['England and Wales'])
dfFinal.drop(index='England and Wales', inplace=True)

# Nettoyage de Brunei
dfFinal.loc['Brunei'] = dfFinal.loc['Brunei'].fillna(dfFinal.loc['Brunei Darussalam'])
dfFinal.drop(index='Brunei Darussalam', inplace=True)

# Nettoyage de Palestine
dfFinal.loc['Palestine'] = dfFinal.loc['Palestine'].fillna(dfFinal.loc['State of Palestine'])
dfFinal.drop(index='State of Palestine', inplace=True)

# Nettoyage de Curacao
dfFinal.loc['Curacao'] = dfFinal.loc['Curacao'].fillna(dfFinal.loc['Curaçao'])
dfFinal.drop(index='Curaçao', inplace=True)

# Nettoyage de Côte d'Ivoire
dfFinal.loc["Côte d'Ivoire"] = dfFinal.loc["Côte d'Ivoire"].fillna(dfFinal.loc["Cote d'Ivoire"])
dfFinal.drop(index="Cote d'Ivoire", inplace=True)

# Nettoyage de Dominican Republic
dfFinal.loc["Dominican Republic"] = dfFinal.loc["Dominican Republic"].fillna(dfFinal.loc["Dominica"])
dfFinal.drop(index="Dominica", inplace=True)

# Nettoyage de Bosnia and Herzegovina
dfFinal.loc["Bosnia and Herzegovina"] = dfFinal.loc["Bosnia and Herzegovina"].fillna(dfFinal.loc["Federation of Bosnia and Herzegovina"])
dfFinal.drop(index="Federation of Bosnia and Herzegovina", inplace=True)

# Nettoyage de Guinea-Bissau
dfFinal.loc["Guinea-Bissau"] = dfFinal.loc["Guinea-Bissau"].fillna(dfFinal.loc["Guinea Bissau"])
dfFinal.drop(index="Guinea Bissau", inplace=True)

# Nettoyage de Hong Kong
dfFinal.loc["Hong Kong"] = dfFinal.loc["Hong Kong"].fillna(dfFinal.loc["Hong Kong, China"])
dfFinal.drop(index="Hong Kong, China", inplace=True)

# Nettoyage de Micronesia
combinedData = dfFinal.loc[["Micronesia", "Micronesia, Federated States of", "Federated States of Micronesia"]].ffill().iloc[-1]
dfFinal.loc["Micronesia"] = combinedData
dfFinal.drop(index=["Micronesia, Federated States of", "Federated States of Micronesia"], inplace=True)

# Nettoyage de Reunion
dfFinal.loc["Reunion"] = dfFinal.loc["Reunion"].fillna(dfFinal.loc["Réunion"])
dfFinal.drop(index="Réunion", inplace=True)

# Nettoyage de Saint Helena
combinedData = dfFinal.loc[["Saint Helena", "Saint Helena, Ascension and Tristan da Cunha", "Saint Helena, Ascension, and Tristan da Cunha"]].ffill().iloc[-1]
dfFinal.loc["Saint Helena"] = combinedData
dfFinal.drop(index=["Saint Helena, Ascension and Tristan da Cunha", "Saint Helena, Ascension, and Tristan da Cunha"], inplace=True)

# Nettoyage de Bahamas
dfFinal.loc["Bahamas"] = dfFinal.loc["Bahamas"].fillna(dfFinal.loc["The Bahamas"])
dfFinal.drop(index="The Bahamas", inplace=True)

# Nettoyage de Gambia
dfFinal.loc["Gambia"] = dfFinal.loc["Gambia"].fillna(dfFinal.loc["The Gambia"])
dfFinal.drop(index="The Gambia", inplace=True)

# Nettoyage de Trinidad & Tobago
dfFinal.loc["Trinidad & Tobago"] = dfFinal.loc["Trinidad & Tobago"].fillna(dfFinal.loc["Trinidad and Tobago"])
dfFinal.drop(index="Trinidad and Tobago", inplace=True)

# Nettoyage de US Virgin Islands
combinedData = dfFinal.loc[["US Virgin Islands", "U.S. Virgin Islands", "United States Virgin Islands", "Virgin Islands"]].ffill().iloc[-1]
dfFinal.loc["US Virgin Islands"] = combinedData
dfFinal.drop(index=["U.S. Virgin Islands", "United States Virgin Islands", "Virgin Islands"], inplace=True)

# Nettoyage de United States
dfFinal.loc["United States"] = dfFinal.loc["United States"].fillna(dfFinal.loc["United States of America"])
dfFinal.drop(index="United States of America", inplace=True)

# Nettoyage de Vatican City
dfFinal.loc["Vatican City"] = dfFinal.loc["Vatican City"].fillna(dfFinal.loc["Vatican City State"])
dfFinal.drop(index="Vatican City State", inplace=True)

# Nettoyage de Vietnam
dfFinal.loc["Vietnam"] = dfFinal.loc["Vietnam"].fillna(dfFinal.loc["Viet Nam"])
dfFinal.drop(index="Viet Nam", inplace=True)

# Nettoyage de North Korea
dfFinal.loc["North Korea"] = dfFinal.loc["North Korea"].fillna(dfFinal.loc["Korea, North"])
dfFinal.drop(index="Korea, North", inplace=True)

# Nettoyage de South Korea
dfFinal.loc["South Korea"] = dfFinal.loc["South Korea"].fillna(dfFinal.loc["Korea, South"])
dfFinal.drop(index="Korea, South", inplace=True)

# Nettoyage de Macao
combinedData = dfFinal.loc[["Macao", "Macau", "Macau, China"]].ffill().iloc[-1]
dfFinal.loc["Macao"] = combinedData
dfFinal.drop(index=["Macau", "Macau, China"], inplace=True)

# Nettoyage de Chine
combinedData = dfFinal.loc[["China", "People's Republic of China", "Republic of China"]].ffill().iloc[-1]
dfFinal.loc["China"] = combinedData
dfFinal.drop(index=["People's Republic of China", "Republic of China"], inplace=True)

dfFinal = dfFinal.dropna(how='all')                     #Enlève tous les rows qui ne contiennent aucune valeur

csvFinal = dfFinal.to_csv("Collecte_Donnees_Nettoyees_test2.csv")
