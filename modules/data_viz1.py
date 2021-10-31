import plotly.io as pio
import plotly.express as px
import plotly.offline as py
import pandas as pd
import plotly.graph_objects as go
from math import log10, trunc, ceil
import inflect

inflector = inflect.engine()


def plot1(df: pd.DataFrame):
    fig = px.scatter(
        df,
        x="Age group",
        y="Population unvaccinated",
        color="Ethnic group",
        size="First dose administered Changed as Percent of unvaccinated Population",
        hover_data=[
            "Ethnic group",
            "Age group",
            "Population unvaccinated",
            "Population",
            "First dose administered Changed",
            "First dose administered Changed as Percent of unvaccinated Population",
        ],
    )

    return fig


# fig
# glue(
#     f"Plot1",
#     fig,
#     display=False,
# )


def plot2(df: pd.DataFrame):
    ethnic_group = "European or Other"
    fig = px.bar(
        df.loc[df["Ethnic group"] == ethnic_group],
        x="Week ending",
        y="Population unvaccinated at week end",
        title=f"{ethnic_group} -  unvaccinated remaining",
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
    return fig


def plot3(df: pd.DataFrame):
    fig = px.area(
        df.query('["European or Other", "Maori"] in `Ethnic group`').sort_values(
            ["Week ending", "Age Category", "Ethnic group"]
        ),
        x="Week ending",
        y="Population unvaccinated at week end",
        color="Age Category",
        title="Total Maori and European unvaccinated at each Wednesday data release",
        markers=True,
        line_group="Ethnic group",
        # facet_col="Gender"
    )
    fig.update_layout(yaxis={"title": "UnVaccinated Population"})

    return fig


def plot_overall_vaccination_status(df: pd.DataFrame):
    x = df["Week ending"].unique()
    fig = None
    fig = go.Figure()
    fig.update_layout(autosize=True)

    def fig_section(
        fig,
        ethnic_group,
        age_category,
        y_offset=0,
        section="",
        colors=["#FD3216", "#00FE35", "#6A76FC"],
    ):
        vac_status = "None"

        def fig_section_trace(
            fig,
            df,
            ethnic_group,
            age_category,
            field="",
            status_text="",
            y_offset=0,
            y_multiplier=1,
            section="",
            color=None,
            showlegend=True,
            **kwargs,
        ):

            if showlegend:
                kwargs = {
                    **kwargs,
                    **dict(
                        legendgroup=section,
                        legendgrouptitle=dict(text=f"{ethnic_group}{age_category}"),
                    ),
                }
            # print(f"kwargs: {kwargs}")
            fig.add_trace(
                go.Scatter(
                    name=f"{age_category} - {status_text}",
                    x=x,
                    y=y_offset
                    + df.query(
                        (
                            f'["{ethnic_group}"] in `Ethnic group`'
                            f'and ["{age_category}"] in `Age Category`'
                        )
                    )[field].astype("Int64")
                    * y_multiplier,
                    mode="lines",
                    line=dict(width=0.5, color=color),
                    showlegend=showlegend,
                    # fillcolor=colors[0],
                    hoveron="points+fills",  # select where hover is active
                    text=f"{ethnic_group}<br>{age_category} - {status_text}",
                    hoverinfo="text",
                    # marker = dict(
                    #     autocolorscale=False,
                    #     cauto=False,
                    #     color=colors[0]
                    #             ),
                    stackgroup=section,
                    **kwargs,
                )
            )

        config = dict(
            fig=fig,
            df=df,
            ethnic_group=ethnic_group,
            age_category=age_category,
            section=section,
            y_offset=0,
            y_multiplier=1,
        )
        if y_offset > 0:
            fig_section_trace(
                **(
                    config
                    | dict(
                        field="Population unvaccinated at week end",
                        y_offset=y_offset,
                        y_multiplier=0,
                        color=colors[0],
                        showlegend=False,
                        fill="none",
                        groupnorm="",
                    )
                )
            )
        trace_configs = [
            dict(
                status_text="No Doses",
                field="Population unvaccinated at week end",
                color=colors[0],
                # - extra trace config
                groupnorm="",
            ),
            dict(
                status_text="First Dose",
                field="First dose administered",
                color=colors[1],
                # - extra trace config
            ),
            dict(
                status_text="Second Dose",
                field="Second dose administered",
                y_multiplier=-1,
                color=colors[2],
                # - extra trace config
            ),
        ]
        for trace_config in trace_configs:
            fig_section_trace(**(config | trace_config))

    ethnic_groups = df["Ethnic group"].unique()
    age_categories = df["Age Category"].unique()
    # age_categories = ["12-19"]
    last_section_y_max = 0
    section_id = 1
    for i, age_category in enumerate(age_categories):
        for j, ethnic_group in enumerate(ethnic_groups):
            population = df.query(
                (
                    f'["{ethnic_group}"] in `Ethnic group`'
                    f'and `Age Category` == "{age_category}"'
                )
            )["Population"].max()
            section = inflector.number_to_words(f"{section_id}")
            # print(
            #     f"Debug: {last_section_y_max}, {section}, {age_category}, {ethnic_group}, {population}"
            # )
            fig_section(
                fig,
                ethnic_group=ethnic_group,
                age_category=age_category,
                y_offset=last_section_y_max,
                section=section,
                # colors=['#AD3216','#F0FE35','#3A76FC'],
                colors=["Red", "Yellow", "Green"],
            )
            fig.add_annotation(
                x=str(x[0]),
                y=last_section_y_max,
                # xref='paper',
                xanchor="left",
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
                align="left",
            )
            last_section_y_max = last_section_y_max + population
            section_id += 1

    def xaxis_ceiling(val):
        ceiling_limiter = trunc(log10(last_section_y_max)) - 1
        return ceil(last_section_y_max / 10 ** ceiling_limiter) * 10 ** ceiling_limiter

    fig.update_layout(
        title="Vaccination Status",
        height=1000,
        showlegend=True,
        # xaxis=dict(
        #     autorange=True,
        #     type='date',
        # )
        xaxis=dict(
            tickmode="array",
            tickvals=x,
            ticktext=[
                pd.Timestamp(e).to_pydatetime().strftime("%b %d<br>(%a)") for e in x
            ],
        ),
        # xaxis_tickformat = '%d %B (%a)<br>%Y',
        yaxis=dict(
            type="linear", range=[0, xaxis_ceiling(last_section_y_max)], ticksuffix=""
        ),
    )

    return fig
