import pandas as pd
import numpy as np
import re

import ssl
ssl._create_default_https_context = ssl._create_unverified_context      #Ignore les erreurs de certificats(temporaire)

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


#Lien 1 - List_of_countries_by_GDP_(nominal)_per_capita
url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)_per_capita"
tables = pd.read_html(url)
df = tables[1]                                            #Table voulu
col = df[('United Nations[7]','Estimate')]                #Colonne voulue
col = pd.to_numeric(col, errors = 'coerce')               #Converti en numérique afin de faire calculs
avg = col.mean()
med = col.median()
max = col.max()
mod = col.mode()
min = col.min()
var = col.var()
bin = (col.copy()).apply(lambda x: 1 if x > med else 0)   #Crée une copie binaire de la colonne

#*****Faute dans le doc, pas de Average download speed (Mbit/s) (Ookla)
#Lien 2 - List_of_countries_by_Internet_connection_speeds
url2 = "https://en.wikipedia.org/wiki/List_of_countries_by_Internet_connection_speeds"
tables2 = pd.read_html(url2)
df2 = tables2[1]                                          #Table voulu
col2 = df2[('Mediandownloadspeed(Mbit/s)(Ookla)[1]')]     #Colonne voulue
avg2 = col2.mean()
med2 = col2.median()
max2 = col2.max()
mod2 = col2.mode()
min2 = col2.min()
var2 = col2.var()
bin2 = (col2.copy()).apply(lambda x: 1 if x > med2 else 0)


#Lien 3 - List_of_countries_by_alcohol_consumption_per_capita
url3 = "https://en.wikipedia.org/wiki/List_of_countries_by_alcohol_consumption_per_capita"
tables3 = pd.read_html(url3)
df3 = tables3[1]                                          #Table voulu
col3 = df3[('2016[8]')]                                   #Colonne voulue
col3 = pd.to_numeric(col3, errors = 'coerce')             
avg3 = col3.mean()
med3 = col3.median()
max3 = col3.max()
mod3 = col3.mode()
min3 = col3.min()
var3 = col3.var()
bin3 = (col3.copy()).apply(lambda x: 1 if x > med3 else 0)

#Lien 4 - List_of_countries_by_intentional_homicide_rate
url4 = "https://en.wikipedia.org/wiki/List_of_countries_by_intentional_homicide_rate"
tables4 = pd.read_html(url4)
df4 = tables4[1]                                          #Table voulu
col4 = df4[('Rate')]                                      #Colonne voulue
col4 = pd.to_numeric(col4, errors = 'coerce')     
avg4 = col4.mean()
med4 = col4.median()
max4 = col4.max()
mod4 = col4.mode()
min4 = col4.min()
var4 = col4.var()
bin4 = (col4.copy()).apply(lambda x: 1 if x > med4 else 0)

#Lien 5 - List_of_countries_with_highest_military_expenditures
url5 = "https://en.wikipedia.org/wiki/List_of_countries_with_highest_military_expenditures"
tables5 = pd.read_html(url5)
df5 = tables5[1]                                          #Table voulu
col5 = df5[('% of GDP')]                                  #Colonne voulue
col5 = pd.to_numeric(col5, errors = 'coerce') 
avg5 = col5.mean()
med5 = col5.median()
max5 = col5.max()
mod5 = col5.mode()
min5 = col5.min()
var5 = col5.var()
bin5 = (col5.copy()).apply(lambda x: 1 if x > med5 else 0)

#Lien 6 - List_of_countries_by_Human_Development_Index
url6 = "https://en.wikipedia.org/wiki/List_of_countries_by_Human_Development_Index"
tables6 = pd.read_html(url6)
df6 = tables6[2]                                          #Table voulu
col6 = df6[('2019')]                                      #Colonne voulue
col6 = pd.to_numeric(col6, errors = 'coerce')
avg6 = col6.mean()
med6 = col6.median()
max6 = col6.max()
mod6 = col6.mode()
min6 = col6.min()
var6 = col6.var()
bin6 = (col6.copy()).apply(lambda x: 1 if x > med6 else 0)

#Lien 7 - Democracy_Index
url7 = "https://en.wikipedia.org/wiki/Democracy_Index"
tables7 = pd.read_html(url7)
df7 = tables7[5]                                          #Table voulu
col7 = df7[('2020')]                                      #Colonne voulue
col7 = pd.to_numeric(col7, errors = 'coerce')
avg7 = col7.mean()
med7 = col7.median()
max7 = col7.max()
mod7 = col7.mode()
min7 = col7.min()
var7 = col7.var()
bin7 = (col7.copy()).apply(lambda x: 1 if x > med7 else 0)

#Lien 8 - List_of_countries_by_tertiary_education_attainment
url8 = "https://en.wikipedia.org/wiki/List_of_countries_by_tertiary_education_attainment"
tables8 = pd.read_html(url8)
df8 = tables8[2]                                          #Table voulu
col8 = df8.loc[:, (slice(None), '2 years')]               #Colonne voulue est situé dans un multiindex
col8 = col8.iloc[:, 0]                                    #Colonne voulue
col8 = pd.to_numeric(col8, errors = 'coerce')
avg8 = col8.mean()
med8 = col8.median()
max8 = col8.max()
mod8 = col8.mode()
min8 = col8.min()
var8 = col8.var()
bin8 = (col8.copy()).apply(lambda x: 1 if x > med8 else 0)

#Lien 9 - Importance_of_religion_by_country
url9 = "https://en.wikipedia.org/wiki/Importance_of_religion_by_country"
tables9 = pd.read_html(url9)
df9 = tables9[5]                                          #Table voulu
col9 = df9[('Yes, important[1]')]                         #Colonne voulu
col9 = col9.str.rstrip("%").astype(float)                 #Enlève les %
avg9 = col9.mean()
med9 = col9.median()
max9 = col9.max()
mod9 = col9.mode()
min9 = col9.min()
var9 = col9.var()
bin9 = (col9.copy()).apply(lambda x: 1 if x > med9 else 0)

#Lien 10 - Christianity_by_country
url10 = "https://en.wikipedia.org/wiki/Christianity_by_country"
tables10 = pd.read_html(url10)
df10 = tables10[7]                                          #Table voulu
col10 = df10[('% Christian')]                               #Colonne voulue
col10 = col10.astype(str).apply(removeGarbage)
col10 = pd.to_numeric(col10, errors = 'coerce')
avg10 = col10.mean()
med10 = col10.median()
max10 = col10.max()
mod10 = col10.mode()
min10 = col10.min()
var10 = col10.var()
bin10 = (col10.copy()).apply(lambda x: 1 if x > med10 else 0)

#Lien 11 - Islam_by_country
url11 = "https://en.wikipedia.org/wiki/Islam_by_country"
tables11 = pd.read_html(url11)
df11 = tables11[7]                                          #Table voulu
col11 = df11[('Muslim percentage of total population')]     #Colonne voulue
col11 = col11.astype(str).apply(removeGarbage)              #Données contaminées, alors on applique la fonction removeGarbage
col11 = pd.to_numeric(col11, errors = 'coerce')     
avg11 = col11.mean()
med11 = col11.median()
max11 = col11.max()
mod11 = col11.mode()
min11 = col11.min()
var11 = col11.var()
bin11 = (col11.copy()).apply(lambda x: 1 if x > med11 else 0)

#Lien 12 - Buddhism_by_country
url12 = "https://en.wikipedia.org/wiki/Buddhism_by_country"
tables12 = pd.read_html(url12)
df12 = tables12[0]                                          #Table voulu
col12 = df12.loc[:, (slice(None), '% Buddhist')]            #Colonne voulue est situé dans un multiindex
col12 = col12.iloc[:, 1]                                    #Colonne voulue
col12 = col12.astype(str).apply(removeGarbage)              #Données contaminées, alors on applique la fonction removeGarbage
col12 = pd.to_numeric(col12, errors = 'coerce')
avg12 = col12.mean()
med12 = col12.median()
max12 = col12.max()
mod12 = col12.mode()
min12 = col12.min()
var12 = col12.var()
bin12 = (col12.copy()).apply(lambda x: 1 if x > med12 else 0)

#Lien 13 - Jewish_population_by_country
url13 = "https://en.wikipedia.org/wiki/Jewish_population_by_country"
tables13 = pd.read_html(url13)
df13 = tables13[36]                                         #Table voulu
col13 = df13.loc[:, (slice(None), 'pct')]                   #Colonne voulue est situé dans un multiindex
col13 = col13.iloc[:, 0]                                    #Colonne voulue
col13 = pd.to_numeric(col13, errors = 'coerce')     
avg13 = col13.mean()
med13 = col13.median()
max13 = col13.max()
mod13 = col13.mode()
min13 = col13.min()
var13 = col13.var()
bin13 = (col13.copy()).apply(lambda x: 1 if x > med13 else 0)

#***Faute dans le doc, pas de Under-five mortality (deaths/1,000 live births) – 2019 estimates
#Lien 14 - List_of_countries_by_infant_and_under-five_mortality_rates
url14 = "https://en.wikipedia.org/wiki/List_of_countries_by_infant_and_under-five_mortality_rates"
tables14 = pd.read_html(url14)
df14 = tables14[0]                                                          #Table voulu
col14 = df14[('2020 mortality rate, under-5 (per 1000 live births)')]       #Colonne voulue
col14 = pd.to_numeric(col14, errors = 'coerce')             
avg14 = col14.mean()
med14 = col14.median()
max14 = col14.max()
mod14 = col14.mode()
min14 = col14.min()
var14 = col14.var()
bin14 = (col14.copy()).apply(lambda x: 1 if x > med14 else 0)

#Lien 15 - Age_of_criminal_responsibility
url15 = "https://en.wikipedia.org/wiki/Age_of_criminal_responsibility"
tables15 = pd.read_html(url15)
df15 = tables15[2]                                          #Table voulu
col15 = df15[('Age (reduced)[a]')]                          #Colonne voulu
col15 = col15.astype(str).apply(removeGarbage)              #Données contaminées, alors on applique la fonction removeGarbage
col15 = pd.to_numeric(col15, errors = 'coerce')     
avg15 = col15.mean()
med15 = col15.median()
max15 = col15.max()
mod15 = col15.mode()
min15 = col15.min()
var15 = col15.var()
bin15 = (col15.copy()).apply(lambda x: 1 if x > med15 else 0)

#Lien 16 - List_of_countries_by_minimum_wage
url16 = "https://en.wikipedia.org/wiki/List_of_countries_by_minimum_wage"
tables16 = pd.read_html(url16)
df16 = tables16[1]                                          #Table voulu
col16 = df16.loc[:, (slice(None), 'Nominal (US$)[6]')]      #Colonne voulue est situé dans un multiindex
col16 = col16.iloc[:, 0]                                    #Colonne voulue
avg16 = col16.mean()
med16 = col16.median()
max16 = col16.max()
mod16 = col16.mode()
min16 = col16.min()
var16 = col16.var()
bin16 = (col16.copy()).apply(lambda x: 1 if x > med16 else 0)

#Lien 17 - List_of_countries_by_external_debt
url17 = "https://en.wikipedia.org/wiki/List_of_countries_by_external_debt"
tables17 = pd.read_html(url17)
df17 = tables17[0]                                          #Table voulu
col17 = df17[('% of GDP')]                                  #Colonne voulu
avg17 = col17.mean()
med17 = col17.median()
max17 = col17.max()
mod17 = col17.mode()
min17 = col17.min()
var17 = col17.var()
bin17 = (col17.copy()).apply(lambda x: 1 if x > med17 else 0)

#Lien 18 - List_of_countries_by_income_equality
url18 = "https://en.wikipedia.org/wiki/List_of_countries_by_income_equality"
tables18 = pd.read_html(url18)
df18 = tables18[1]                                          #Table voulu
col18 = df18[(('World Bank Gini[5][6]','%'))]               #Colonne voulue
avg18 = col18.mean()
med18 = col18.median()
max18 = col18.max()
mod18 = col18.mode()
min18 = col18.min()
var18 = col18.var()
bin18 = (col18.copy()).apply(lambda x: 1 if x > med18 else 0)

#Lien 19 - List_of_countries_by_total_health_expenditure_per_capita
url19 = "https://en.wikipedia.org/wiki/List_of_countries_by_total_health_expenditure_per_capita"
tables19 = pd.read_html(url19)
df19 = tables19[1]                                          #Table voulu
col19 = df19[('2018')]                                      #Colonne voulue
avg19 = col19.mean()
med19 = col19.median()
max19 = col19.max()
mod19 = col19.mode()
min19 = col19.min()
var19 = col19.var()
bin19 = (col19.copy()).apply(lambda x: 1 if x > med19 else 0)

#Lien 20 - List_of_countries_by_suicide_rate
url20 = "https://en.wikipedia.org/wiki/List_of_countries_by_suicide_rate"
tables20 = pd.read_html(url20)
df20 = tables20[1]                                          #Table voulu
col20 = df20[('All')]                                       #Colonne voulue
avg20 = col20.mean()
med20 = col20.median()
max20 = col20.max()
mod20 = col20.mode()
min20 = col20.min()
var20 = col20.var()
bin20 = (col20.copy()).apply(lambda x: 1 if x > med20 else 0)

#***Pas de Table 2019 List by the World Bank, 2019.
#Lien 21 - List_of_sovereign_states_and_dependencies_by_total_fertility_rate
url21 = "https://en.wikipedia.org/wiki/List_of_sovereign_states_and_dependencies_by_total_fertility_rate"
tables21 = pd.read_html(url21)
df21 = tables21[4]                                              #Table voulu
col21 = df21[('Fertility rate in 2019 (births/woman)')][:210]   #Les valeurs importantes s'arrêtent à la Corée du Sude(row:210)
col21 = pd.to_numeric(col21, errors = 'coerce')    
avg21 = col21.mean()
med21 = col21.median()
max21 = col21.max()
mod21 = col21.mode()
min21 = col21.min()
var21 = col21.var()
bin21 = (col21.copy()).apply(lambda x: 1 if x > med21 else 0)

#***Pas de table Prevalence of current tobacco use among persons aged 15 years and older, 2000.
#Lien 22 - Tobacco_consumption_by_country
url22 = "https://en.wikipedia.org/wiki/Tobacco_consumption_by_country"
tables22 = pd.read_html(url22)
df22 = tables22[0]                                          #Table voulu
col22 = df22[('Cigarettes')]                                #Colonne voulue
col22 = pd.to_numeric(col22, errors = 'coerce')             
avg22 = col22.mean()
med22 = col22.median()
max22 = col22.max()
mod22 = col22.mode()
min22 = col22.min()
var22 = col22.var()
bin22 = (col22.copy()).apply(lambda x: 1 if x > med22 else 0)

#Lien 23 - List_of_countries_by_obesity_rate
url23 = "https://en.wikipedia.org/wiki/List_of_countries_by_obesity_rate"
tables23 = pd.read_html(url23)
df23 = tables23[1]                                          #Table voulu
col23 = df23[('Obesity rate (%)')]                          #Colonne voulu
avg23 = col23.mean()
med23 = col23.median()
max23 = col23.max()
mod23 = col23.mode()
min23 = col23.min()
var23 = col23.var()
bin23 = (col23.copy()).apply(lambda x: 1 if x > med23 else 0)

#Lien 24 - List_of_countries_by_number_of_Internet_users
url24 = "https://en.wikipedia.org/wiki/List_of_countries_by_number_of_Internet_users"
tables24 = pd.read_html(url24)
df24 = tables24[5]                                          #Table voulu
col24 = df24[('Pct')]                                       #Colonne voulu
col24 = col24.astype(str).apply(removeGarbage)
col24 = pd.to_numeric(col24, errors = 'coerce')
avg24 = col24.mean()
med24 = col24.median()
max24 = col24.max()
mod24 = col24.mode()
min24 = col24.min()
var24 = col24.var()
bin24 = (col24.copy()).apply(lambda x: 1 if x > med24 else 0)

#Lien 25 - List_of_sovereign_states_and_dependencies_by_total_fertility_rate
url25 = "https://en.wikipedia.org/wiki/List_of_countries_by_median_age"
tables25 = pd.read_html(url25)
df25 = tables25[0]                                                  #Table voulu
col25 = df25[('Median ages in years','2020 medians', 'Combined')]   #Colonne voulu
col25 = pd.to_numeric(col25, errors = 'coerce')
avg25 = col25.mean()
med25 = col25.median()
max25 = col25.max()
mod25 = col25.mode()
min25 = col25.min()
var25 = col25.var()
bin25 = (col25.copy()).apply(lambda x: 1 if x > med25 else 0)

#Lien 26 - List_of_countries_by_economic_freedom
url26 = "https://en.wikipedia.org/wiki/List_of_countries_by_economic_freedom"
tables26 = pd.read_html(url26)
df26 = tables26[1]                                      #Table voulu
col26 = df26[('Score')]                                 #Colonne voulue
col26 = pd.to_numeric(col26, errors = 'coerce')   
avg26 = col26.mean()
med26 = col26.median()
max26 = col26.max()
mod26 = col26.mode()
min26 = col26.min()
var26 = col26.var()
bin26 = (col26.copy()).apply(lambda x: 1 if x > med26 else 0)

#***Pas de table per capita 2017
#Lien 27 - List_of_countries_by_oil_production
url27 = "https://en.wikipedia.org/wiki/List_of_countries_by_oil_production"
tables27 = pd.read_html(url27)
df27 = tables27[1]                                          #Table voulu
col27 = df27[('Oil production April 2022 (bbl/day)[1]')]    #Colonne voulue
col27 = pd.to_numeric(col27, errors = 'coerce')
avg27 = col27.mean()
med27 = col27.median()
max27 = col27.max()
mod27 = col27.mode()
min27 = col27.min()
var27 = col27.var()
bin27 = (col27.copy()).apply(lambda x: 1 if x > med27 else 0)

#Lien 28 - List_of_countries_by_population_growth_rate
url28 = "https://en.wikipedia.org/wiki/List_of_countries_by_population_growth_rate"
tables28 = pd.read_html(url28)
df28 = tables28[0]                                      #Table voulu
col28 = df28[('UN[5] 2015–20', 'Unnamed: 6_level_1')]   #Colonne voulue
col28 = pd.to_numeric(col28, errors = 'coerce')
avg28 = col28.mean()
med28 = col28.median()
max28 = col28.max()
mod28 = col28.mode()
min28 = col28.min()
var28 = col28.var()
bin28 = (col28.copy()).apply(lambda x: 1 if x > med28 else 0)

#Lien 29 - List_of_countries_by_life_expectancy
url29 = "https://en.wikipedia.org/wiki/List_of_countries_by_life_expectancy"
tables29 = pd.read_html(url29)
df29 = tables29[3]                                      #Table voulu
col29 = df29[('Life expectancy at birth', 'All')]       #Colonne voulu
col29 = pd.to_numeric(col29, errors = 'coerce')   
avg29 = col29.mean()
med29 = col29.median()
max29 = col29.max()
mod29 = col29.mode()
min29 = col29.min()
var29 = col29.var()
bin29 = (col29.copy()).apply(lambda x: 1 if x > med29 else 0)

#Lien 30 - List_of_countries_by_meat_consumption
url30 = "https://en.wikipedia.org/wiki/List_of_countries_by_meat_consumption"
tables30 = pd.read_html(url30)
df30 = tables30[1]                                      #Table voulu
col30 = df30[('kg/person (2002)[9][note 1]')]           #Colonne voulu
col30 = pd.to_numeric(col30, errors = 'coerce') 
avg30 = col30.mean()
med30 = col30.median()
max30 = col30.max()
mod30 = col30.mode()
min30 = col30.min()
var30 = col30.var()
bin30 = (col30.copy()).apply(lambda x: 1 if x > med30 else 0)

#Lien 31 - List_of_countries_by_incarceration_rate
url31 = "https://en.wikipedia.org/wiki/List_of_countries_by_incarceration_rate"
tables31 = pd.read_html(url31)
df31  = tables31[0]                                     #Table voulu
col31 = df31[('Rates per 100,000[2]')]                  #Colonne voulue
col31 = pd.to_numeric(col31, errors = 'coerce')
avg31 = col31.mean()
med31 = col31.median()
max31 = col31.max()
mod31 = col31.mode()
min31 = col31.min()
var31 = col31.var()
bin31 = (col31.copy()).apply(lambda x: 1 if x > med31 else 0)

#Lien 32 - List_of_countries_by_literacy_rate
url32 = "https://en.wikipedia.org/wiki/List_of_countries_by_literacy_rate"
tables32 = pd.read_html(url32)
df32 = tables32[1]                                      #Table voulu
col32 = df32[('Elderly (65+)',    'Rate')]              #Colonne voulue
col32 = pd.to_numeric(col32, errors = 'coerce')
avg32 = col32.mean()
med32 = col32.median()
max32 = col32.max()
mod32 = col32.mode()
min32 = col32.min()
var32 = col32.var()
bin32 = (col32.copy()).apply(lambda x: 1 if x > med32 else 0)

#Lien 33 - List_of_countries_by_age_at_first_marriage
url33 = "https://en.wikipedia.org/wiki/List_of_countries_by_age_at_first_marriage"
tables33 = pd.read_html(url33)
df1 = tables33[0]                                     #Table voulu: Africa
df2 = tables33[1]                                     #Table voulu: Americas
df3 = tables33[2]                                     #Table voulu: Asia
df4 = tables33[3]                                     #Table voulu: Europe
df5 = tables33[4]                                     #Table voulu: Oceania
col33 = pd.concat([df1['Women'], df2['Women'], df3['Women'], df4['Women'], df5['Women']])     #Concaténation des tables
col33 = col33.reset_index(drop=True)                                                            #Reset des index
col33 = pd.to_numeric(col33, errors = 'coerce')
avg33 = col33.mean()
med33 = col33.median()
max33 = col33.max()
mod33 = col33.mode()
min33 = col33.min()
var33 = col33.var()
bin33 = (col33.copy()).apply(lambda x: 1 if x > med33 else 0)

#Lien 34 - List_of_countries_by_spending_on_education_(%25_of_GDP)
url34 = "https://en.wikipedia.org/wiki/List_of_countries_by_spending_on_education_(%25_of_GDP)"
tables34 = pd.read_html(url34)
df34 = tables34[0]                                      #Table voulu
col34 = df34[('Expenditure on education (% of GDP)')]   #Colonne voulue
col34 = pd.to_numeric(col34, errors = 'coerce')
avg34 = col34.mean()
med34 = col34.median()
max34 = col34.max()
mod34 = col34.mode()
min34 = col34.min()
var34 = col34.var()
bin34 = (col34.copy()).apply(lambda x: 1 if x > med34 else 0)

#***Homeless per 10 000********
#Lien 35 - List_of_countries_by_homeless_population
url35 = "https://en.wikipedia.org/wiki/List_of_countries_by_homeless_population"
tables35 = pd.read_html(url35)
df35 = tables35[0]                                      #Table voulu
col35 = df35[('Homeless per 10k')]                      #Colonne voulue
col35 = pd.to_numeric(col35, errors = 'coerce')
avg35 = col35.mean()
med35 = col35.median()
max35 = col35.max()
mod35 = col35.mode()
min35 = col35.min()
var35 = col35.var()
bin35 = (col35.copy()).apply(lambda x: 1 if x > med35 else 0)

#Lien 36 - List_of_countries_by_milk_consumption_per_capita
url36 = "https://en.wikipedia.org/wiki/List_of_countries_by_milk_consumption_per_capita"
tables36 = pd.read_html(url36)
df36 = tables36[0]                                            #Table voulu
col36 = df36[('Milk consumption 2013 (kg/capita/yr) [1]')]    #Colonne voulue
col36 = pd.to_numeric(col36, errors = 'coerce')
avg36 = col36.mean()
med36 = col36.median()
max36 = col36.max()
mod36 = col36.mode()
min36 = col36.min()
var36 = col36.var()
bin36 = (col36.copy()).apply(lambda x: 1 if x > med36 else 0)

#Lien 37 - List_of_countries_by_number_of_scientific_and_technical_journal_articles
url37 = "https://en.wikipedia.org/wiki/List_of_countries_by_number_of_scientific_and_technical_journal_articles"
tables37 = pd.read_html(url37)
df37 = tables37[0]                                                  #Table voulu
col37 = df37[('Scientific publications per capita (per million)')]  #Colonne voulue
col37 = pd.to_numeric(col37, errors = 'coerce')
avg37 = col37.mean()
med37 = col37.median()
max37 = col37.max()
mod37 = col37.mode()
min37 = col37.min()
var37 = col37.var()
bin37 = (col37.copy()).apply(lambda x: 1 if x > med37 else 0)

#Lien 38 - Books_published_per_country_per_year
url38 = "https://en.wikipedia.org/wiki/Books_published_per_country_per_year"
tables38 = pd.read_html(url38)
df38 = tables38[0]                                  #Table voulu
col38 = df38[('Titles')]                            #Colonne voulu
col38 = pd.to_numeric(col38, errors = 'coerce')
avg38 = col38.mean()
med38 = col38.median()
max38 = col38.max()
mod38 = col38.mode()
min38 = col38.min()
var38 = col38.var()
bin38 = (col38.copy()).apply(lambda x: 1 if x > med38 else 0)


#Lien 39 - List_of_countries_by_food_energy_intake
url39 = "https://en.wikipedia.org/wiki/List_of_countries_by_food_energy_intake"
tables39 = pd.read_html(url39)
df39 = tables39[0]                                                                          #Table voulu
col39 = df39[('Average daily dietary energy consumption per capita[8]', 'kilocalories')]    #Colonne voulue
col39 = pd.to_numeric(col39, errors = 'coerce')
avg39 = col39.mean()
med39 = col39.median()
max39 = col39.max()
mod39 = col39.mode()
min39 = col39.min()
var39 = col39.var()
bin39 = (col39.copy()).apply(lambda x: 1 if x > med39 else 0)

#Lien 40 - List_of_countries_by_average_yearly_temperature
url40 = "https://en.wikipedia.org/wiki/List_of_countries_by_average_yearly_temperature"
tables40 = pd.read_html(url40)
df40 = tables40[0]                                                  #Table voulu
col40 = df40[('Average yearly temperature (1961–1990 Celsius)')]    #Colonne voulue
col40 = pd.to_numeric(col40, errors = 'coerce')
avg40 = col40.mean()
med40 = col40.median()
max40 = col40.max()
mod40 = col40.mode()
min40 = col40.min()
var40 = col40.var()
bin40 = (col40.copy()).apply(lambda x: 1 if x > med40 else 0)

