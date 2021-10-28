#%%

%load_ext autoreload
%autoreload 2

# %%
from datetime import datetime
import os
import pandas as pd
# %%


import plotly.io as pio
import plotly.express as px
import plotly.offline as py

os.getcwd()
# %%
os.chdir(
    r"C:\Users\SLLau\SynologyDrive\AU\Analysis\21W44_NZ_Covid19_vacination_northland\testBook"
)

# %%
import modules


# %%
import modules.data_prep as dp

# %%
data = dp.MOH_data()
# %%
data.prep_step1_pull_data()
# %%
# data.prep_step_2_read_uptake_data(dp.DATE_WEEK_CURRENT,dp.DATE_WEEK_PRIOR)
data.prep_step_2_read_all_uptake_data()

# %%
data.prep_step_3_generate_report_data()

# %%
data.df_compare.dtypes
# %%
data.weekly_data_folders.keys()

# %%

fig = px.scatter(
    data.df_out,
    x="Age group",
    y="Population unvaccinated at week start",
    color="Ethnic group",
    facet_col="Gender",
    size="First dose administered Changed as Percent of unvaccinated Population",
    hover_data=[
        "Ethnic group",
        "Age group",
        "Population unvaccinated at week start",
        "Population",
        "First dose administered Changed",
        "First dose administered Changed as Percent of unvaccinated Population",
    ],
)
# %%
fig
# %%











# %%
fig = px.line(data.df_all_weeks.loc[data.df_all_weeks['Age group']=='12-15'], x="Week ending", y="Population unvaccinated at week start", color='Ethnic group',facet_col="Gender",facet_row="Age group")
# %%
fig
# %%
fig = px.line(data.df_all_weeks.loc[data.df_all_weeks['Ethnic group']=="European or Other"], x="Week ending", y="Population unvaccinated at week end", color='Age group',facet_col="Gender")
fig

# %%
fig = px.area(data.df_all_weeks_no_gender_age_category.query('["European or Other", "Maori"] in `Ethnic group`'
                    ).sort_values(["Week ending", "Age Category","Ethnic group"])
, 
        x="Week ending", y="Population unvaccinated at week end", color='Age Category',
        title="Total Maori and European unvaccinated at each Wednesday data release",
        markers=True,
        line_group="Ethnic group",
        # facet_col="Gender"
        )
fig.update_layout(
    yaxis={'title':'UnVaccinated Population'})

fig
# %%
fig = px.area(data.df_all_weeks_no_gender_age_category.loc[:], 
        x="Week ending", y="Population unvaccinated at week end", color='Age Category',
        facet_col="Ethnic group"
        )
fig.update_layout(
     yaxis={'title':'UnVaccinated Population'})

fig
# %%
fig = px.area(data.df_all_weeks_no_gender_age_category.query('["European or Other", "Maori"] in `Ethnic group`'), 
        x="Week ending", y="Population unvaccinated at week end", color='Age Category',
        title = "Unvaccinated European and Maori",
        markers=True,
        # hoveron="points+fills",       
        facet_col="Ethnic group"
        )
# fig.update_traces(mode="points+fills", hovertemplate=None)
fig.update_layout(
     yaxis={'title':'UnVaccinated Population'})
fig
# %%
ethnic_group="European or Other"
fig = px.bar(data.df_all_weeks_no_gender_age_category.loc[data.df_all_weeks_no_gender_age_category['Ethnic group']==ethnic_group],
    x="Week ending", 
    y="Population unvaccinated at week end", 
    title=f"{ethnic_group} -  unvaccinated remaining",
    color='Age Category',

    hover_data=[
        "Ethnic group",
        "Age Category",
        # "Population unvaccinated at week start",
        "Population unvaccinated at week end",
        "Population",
        "First dose administered_prior",
        "First dose administered Changed",
        "First dose administered Changed as Percent of unvaccinated Population",]
    )

# %%
fig





# %%
ethnic_group="European or Other"
fig = px.bar(data.df_all_weeks_no_gender.loc[data.df_all_weeks_no_gender['Ethnic group']==ethnic_group], 
    x="Week ending", 
    y="First dose administered Changed", 
    title=f"{ethnic_group} -  First dose received",
    color='Age Category',
    # facet_col="Gender",
    hover_data=[
        "Ethnic group",
        "Age Category",
        "Population unvaccinated at week start",
        "Population unvaccinated at week end",
        "Population",
        "First dose administered_prior",
        "First dose administered Changed",
        "First dose administered Changed as Percent of unvaccinated Population",
    ],)
# %%
fig
# %%
data.df_all_weeks['Age group'].unique()

# %%
data.df_all_weeks['Week ending'].unique()

# %%
data.df_all_weeks['Ethnic group'].unique()
# %%
data.df_all_weeks.loc[(data.df_all_weeks['Ethnic group']=="European or Other") 
    & (data.df_all_weeks['Week ending']==datetime.fromisoformat('2021-10-26')),['Population unvaccinated at week end']].sum()
# %%
data.df_all_weeks.loc[(data.df_all_weeks['Ethnic group']=="European or Other") & (data.df_all_weeks['Week ending']==datetime.fromisoformat('2021-10-26')),['First dose administered Changed']].sum()

# %%
data.df_all_weeks.loc[(data.df_all_weeks['Ethnic group']=="European or Other") & (data.df_all_weeks['Week ending']==datetime.fromisoformat('2021-10-19')),['First dose administered Changed']].sum()

# %%
data.df_all_weeks.loc[(data.df_all_weeks['Ethnic group']=="Maori") & (data.df_all_weeks['Week ending']==datetime.fromisoformat('2021-10-26')),['First dose administered Changed']].sum()

# %%
data.df_all_weeks.loc[(data.df_all_weeks['Ethnic group']=="Maori") & (data.df_all_weeks['Week ending']==datetime.fromisoformat('2021-10-19')),['First dose administered Changed']].sum()

# %%
data.df_all_weeks.loc[((data.df_all_weeks['Ethnic group']=="European or Other") 
            & (data.df_all_weeks['Week ending']==datetime.fromisoformat('2021-10-26'))
            ),['First dose administered']].sum()


# %%
data.df_all_weeks.loc[((data.df_all_weeks['Ethnic group']=="European or Other") 
            & (data.df_all_weeks['Week ending']==datetime.fromisoformat('2021-10-26'))
            & (data.df_all_weeks["First dose administered"]>data.df_all_weeks['Population'])
            ),['First dose administered Changed']].sum()









# # %%

# list_of_weeks = [week for week  in sorted(data.weekly_data_folders.keys())]
# comparison_sets=list(zip(list_of_weeks[1:],list_of_weeks[2:]))
# comparsion_sets_args=[{'date_week_current':t[1], 'date_week_prior':t[0]} for t in comparison_sets]
# comparsion_sets_args

# # %%
# # %%

# data.df_all_weeks = None
# # %%
# for cs in comparsion_sets_args:
#     data.prep_step_2_read_uptake_data(**cs)
#     if data.df_all_weeks is None:
#         data.df_all_weeks = data.df_compare.loc[:,data.df_uptake_keys+data.output_fields].copy(deep=True)
#     else:
#         data.df_all_weeks=pd.concat([data.df_all_weeks, data.df_compare.loc[:,data.df_uptake_keys+data.output_fields]], axis=0,ignore_index=True)

# # %%
# len(data.df_all_weeks)
# # %%
# data.df_all_weeks

# # %%
# list(data.df_all_weeks['Age group'].unique())
# # %%
# age_major_group=[['12-15',
#  '16-19',],

#  ['20-24',
#  '25-29',
#  '30-34',
#  '35-39',],

#  ['40-44',
#  '45-49',
#  '50-54',
#  '55-59',
#  '60-64',
#  '65-69',],
#  ['70-74',
#  '75-79',
#  '80-84',
#  '85-89',
#  '90+']]

#  # %%
# from typing import List
# def minmax(l:List[int])->List[int]:
#     return [min(l),max(l)]
#  # %%

# age_groups_new={i: "-".join(minmax("-".join(l).split("-"))) for i,l in enumerate(age_major_group)}

#  # %%
# age_major_group_lookup={a:age_groups_new[i]  for i,l in enumerate(age_major_group) for a in l }
# age_major_group_lookup_reverse = {v:k for k,v in age_major_group_lookup.items()}
# # %%
# age_major_group_lookup
# # %%
# data.df_all_weeks['Age group major'] = data.df_all_weeks['Age group'].apply(age_major_group_lookup.get)
# # %%

# df_all_no_gender = data.df_all_weeks.loc[:,].groupby(by=[
#                     "DHB of residence",
#                     "Week ending",
#                     "Ethnic group",
#                     # "Gender",
#                     "Age group major",
#                 ]
#             ).sum()
        
# df_all_no_gender.reset_index(inplace=True)


# # %%

# # %%
# df_all_no_gender_no_age = data.df_all_weeks.loc[:,].groupby(by=[
#                     "DHB of residence",
#                     "Week ending",
#                     "Ethnic group",
#                     # "Gender",
#                     # "Age group",
#                 ]
#             ).sum()
        
# df_all_no_gender_no_age.reset_index(inplace=True)

# # %%
# df_all_no_gender_age_major = data.df_all_weeks.loc[:,].groupby(by=[
#                     "DHB of residence",
#                     "Week ending",
#                     "Ethnic group",
#                     # "Gender",
#                     "Age group major",
#                 ]
#             ).sum()
        
# df_all_no_gender_age_major.reset_index(inplace=True)