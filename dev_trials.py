#%%

%load_ext autoreload
%autoreload 2

# %%
from datetime import datetime
import os
import pandas as pd
from math import log10,trunc,ceil
import inflect
inflector = inflect.engine()
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
# %%
import modules.data_viz1 as dv


# %%
dv.plot2(data.df_all_weeks_no_gender_age_category)

# %%
ethnic_group = "European or Other"
df = data.df_all_weeks_no_gender_age_category
# %%
df
# %%
fig = px.bar(
    df.loc[df["Ethnic group"] == ethnic_group],
    x="Week ending",
    y="First dose administered Changed",
    title=f"{ethnic_group} -  First Dose",
    color="Age Category",
    hover_data=[
        "Ethnic group",
        "Age Category",
        # "Population unvaccinated at week start",
        "Population unvaccinated at week end",
        "Population",
        "First dose administered_prior",
        "First dose administered Changed",
        "First dose administered Changed as Percent of unvaccinated Population",
    ],
)
fig
# %%
fig = px.bar(
    df.loc[df["Ethnic group"] == ethnic_group],
    x="Week ending",
    y="First dose administered",
    title=f"{ethnic_group} -  First Dose",
    color="Age Category",
    hover_data=[
        "Ethnic group",
        "Age Category",
        # "Population unvaccinated at week start",
        "Population unvaccinated at week end",
        "Population",
        "First dose administered_prior",
        "First dose administered Changed",
        "First dose administered Changed as Percent of unvaccinated Population",
    ],
)
fig
# %%
fig = px.bar(
    df.loc[df["Ethnic group"] == ethnic_group],
    x="Week ending",
    y="Second dose administered",
    title=f"{ethnic_group} -  Second Dose",
    color="Age Category",
    hover_data=[
        "Ethnic group",
        "Age Category",
        # "Population unvaccinated at week start",
        "Population unvaccinated at week end",
        "Population",
        "First dose administered_prior",
        "First dose administered Changed",
        "First dose administered Changed as Percent of unvaccinated Population",
    ],
)
fig
# %%
fig = px.bar(
    df.loc[df["Ethnic group"] == ethnic_group],
    x="Week ending",
    y="Population",
    title=f"{ethnic_group} -  Population",
    color="Age Category",
    hover_data=[
        "Ethnic group",
        "Age Category",
        # "Population unvaccinated at week start",
        "Population unvaccinated at week end",
        "Population",
        "First dose administered_prior",
        "First dose administered Changed",
        "First dose administered Changed as Percent of unvaccinated Population",
    ],
)
fig
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

import altair as alt 
# %%
chart1 = alt.Chart(data.df_all_weeks.query('`Age group`=="12-15" & `Gender`=="Male"')).mark_line().encode(
   x="Week ending",
   y="Population unvaccinated at week start",
   color="Ethnic group"
).properties(
   height=300, width=500
)
chart2 = alt.Chart(data.df_all_weeks.query('`Age group`=="12-15" & `Gender`=="Female"')).mark_line().encode(
   x="Week ending",
   y="Population unvaccinated at week start",
   color="Ethnic group"
).properties(
   height=300, width=500
)

# %%
chart1 | chart2




# %%
fig = px.line(data.df_all_weeks.loc[data.df_all_weeks['Age group']=='12-15'], x="Week ending", y="Population unvaccinated at week start", color='Ethnic group',facet_col="Gender",facet_row="Age group")
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
fig = px.area(data.df_all_weeks_no_gender_age_category.query('["European or Other", "Maori"] in `Ethnic group`'
                    )
                    # .sort_values(["Week ending", "Age Category","Ethnic group"])
        , 
        x="Week ending", y="Second dose administered", color='Age Category',
        title="Total Maori and European Second Dosed",
        markers=True,
        line_group="Ethnic group",
        # facet_col="Gender"
        )
fig.update_layout(
    yaxis={'title':'Second Dosed Population'})
fig
# %%
"""[summary]

"""
# %%
df = data.df_all_weeks_no_gender_age_category.query((
    '["European or Other", "Maori"] in `Ethnic group`'
    ' and `Age Category` == "12-19"'
    )
).sort_values(["Age Category", "Ethnic group"])
# %%
df = data.df_all_weeks_no_gender_age_category.query((
    '["European or Other", "Maori"] in `Ethnic group`'
    # ' and `Age Category` == "12-19"'
        # ' and ["12-19","20-39"] in `Age Category`'

    )
).sort_values(["Age Category", "Ethnic group"])

# %%
import plotly.graph_objects as go

# x=sorted(df['Week ending'].unique())
x=df['Week ending'].unique()
# %%
fig = None
fig = go.Figure()
fig.update_layout(autosize=True)

def fig_section(fig,ethnic_group,age_category,y_offset=0,section='',
    colors=['#FD3216','#00FE35','#6A76FC']):
    vac_status="None"


    def fig_section_trace(
        fig,df,ethnic_group,age_category,field='',status_text='',y_offset=0,y_multiplier=1,section='',
        color=None,showlegend=True,**kwargs):

        if showlegend:
            kwargs = {**kwargs, 
                      **dict(
                       legendgroup=section,
                       legendgrouptitle=dict(
                                text=f"{ethnic_group}{age_category}"
                        ),
                      )
            }
        # print(f"kwargs: {kwargs}")
        fig.add_trace(go.Scatter(
            name=f"{age_category} - {status_text}",
            x=x, 
            y=y_offset+df.query((
                f'["{ethnic_group}"] in `Ethnic group`'
                f'and ["{age_category}"] in `Age Category`'
                )
                )[field].astype('Int64')*y_multiplier,
            
            mode='lines',
            line=dict(width=0.5, 
                        color=color
            ),
            showlegend=showlegend,
            # fillcolor=colors[0],
            hoveron = 'points+fills', # select where hover is active
            text=f"{ethnic_group}<br>{age_category} - {status_text}",
            hoverinfo = 'text',

            # marker = dict(
            #     autocolorscale=False,
            #     cauto=False,
            #     color=colors[0]
            #             ),
            stackgroup=section,
            **kwargs
        ))

    config= dict(
        fig=fig,
        df=df,
        ethnic_group=ethnic_group,
        age_category=age_category,
        section=section,
        y_offset=0,
        y_multiplier=1,
        )
    if y_offset>0:
        fig_section_trace(
                    **(config | 
                        dict(
                            field='Population unvaccinated at week end',
                            y_offset=y_offset,
                            y_multiplier=0,
                            color=colors[0], 
                            showlegend=False,
                            fill='none',  
                            groupnorm=''                         
                        )
                    )

)
    trace_configs= [dict(
                            status_text="No Doses",
                            field='Population unvaccinated at week end',
                            color=colors[0], 
                            # - extra trace config
                            groupnorm='',

                            ),
                    dict(
                            status_text="First Dose",
                            field='First dose administered',
                            color=colors[1], 
                            # - extra trace config

                            ),
                    dict(
                            status_text="Second Dose",
                            field='Second dose administered',
                            y_multiplier=-1,
                            color=colors[2], 
                            # - extra trace config
                            )
                            ]
    for trace_config in trace_configs:
        fig_section_trace(**(config | trace_config))

    

ethnic_groups = df['Ethnic group'].unique()
age_categories = df['Age Category'].unique()
# age_categories = ["12-19"]
last_section_y_max=0
section_id=1
for i,age_category in enumerate(age_categories):
    for j,ethnic_group in enumerate(ethnic_groups):
        population=df.query((
                    f'["{ethnic_group}"] in `Ethnic group`'
                    f'and `Age Category` == "{age_category}"'
        ))['Population'].max()
        section = inflector.number_to_words(f'{section_id}')
        print(f"Debug: {last_section_y_max}, {section}, {age_category}, {ethnic_group}, {population}")
        fig_section(fig,ethnic_group=ethnic_group,age_category=age_category,
                    y_offset=last_section_y_max,
                    section=section,
                    # colors=['#AD3216','#F0FE35','#3A76FC'],
                    colors=['Red','Yellow','Green']
                    )
        fig.add_annotation(x=str(x[0]), y=last_section_y_max,
            # xref='paper',
            xanchor='left',
            text=f"{ethnic_group} - {age_category}",
            showarrow=False,
            xref="x",
            yref="y",
            # arrowhead=1,
            # # If axref is exactly the same as xref, then the text's position is
            # # absolute and specified in the same coordinates as xref.
            # axref="x",
            # # The same is the case for yref and ayref, but here the coordinates are data
            # # coordinates
            # ayref="y",
            yshift=+10,
            xshift=100,
            align="left"
            )
        last_section_y_max=last_section_y_max+population
        section_id += 1


def xaxis_ceiling(val):
    ceiling_limiter=trunc(log10(last_section_y_max))-1
    return ceil(last_section_y_max/10**ceiling_limiter)*10**ceiling_limiter

fig.update_layout(
    title = 'Vaccination Status',
    height=1000,
    showlegend=True,
    # xaxis=dict(
    #     autorange=True,
    #     type='date',
    # )
    xaxis = dict(
        tickmode = 'array',
        tickvals = x,
        ticktext = [pd.Timestamp(e).to_pydatetime().strftime('%b %d<br>(%a)') for e in x]
    ),
    # xaxis_tickformat = '%d %B (%a)<br>%Y',
    yaxis=dict(
        type='linear',
        range=[0, xaxis_ceiling(last_section_y_max)],
        ticksuffix=''))

fig
#%%
# fig.add_trace(go.Scatter(
#     x=x, y=[100, 100, 100, 100],
#     mode='lines',
#     line=dict(width=0.5, color='rgb(131, 90, 241)'),
#     stackgroup='one'
# ))

fig.update_layout(
    showlegend=True,
    xaxis=dict(
        autorange=True,
        type='date',
    ),
    yaxis=dict(
        type='linear',
        range=[0, 200000],
        ticksuffix=''))

fig


# %%

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