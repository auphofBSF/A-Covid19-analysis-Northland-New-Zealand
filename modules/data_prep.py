from myst_nb import glue

DATE_WEEK_CURRENT = "2021-10-19"
DATE_WEEK_PRIOR = "2021-10-26"
DATA_MOH = "../data_moh_nz"
from github import Github
import os, re
from pathlib import Path
from pprint import pprint
from git import Repo
import enum
import pandas as pd
from datetime import datetime

token = os.getenv("GITHUB_TOKEN", "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")
g = Github(token)
repo = g.get_repo("minhealthnz/nz-covid-data")


class FetchInfoFlags(enum.IntFlag):
    (
        NEW_TAG,
        NEW_HEAD,
        HEAD_UPTODATE,
        TAG_UPDATE,
        REJECTED,
        FORCED_UPDATE,
        FAST_FORWARD,
        ERROR,
    ) = [1 << x for x in range(8)]


# TODO , if does not exist
# Repo.clone_from(repo.clone_url, DATA_MOH)


# create list of commits then print some of them to stdout
# Repo object used to interact with Git repositories
local_moh_repo = Repo(DATA_MOH)
COMMITS_TO_PRINT = 5


def print_commit_data(commit):
    print("-----")
    print(str(commit.hexsha))
    print(f'"{commit.summary}" by {commit.author.name} ({commit.author.email})')
    print(str(commit.authored_datetime))
    print(str(f"count: {commit.count()} and size: {commit.size}"))


def print_repository_info(repo):
    print(generate_repository_info(repo))
    # print(f"Repository description: {repo.description}")
    # print(f"Repository active branch is {repo.active_branch}")

    # for remote in repo.remotes:
    #     print(f'Remote named "{remote}" with URL "{remote.url}"')

    # print(f"Last commit for repository is {str(repo.head.commit.hexsha)}.")


def generate_repository_info(repo):
    return (
        f"Repository description: {repo.description}\n"
        f"Repository active branch is {repo.active_branch}\n"
        f"Last commit for repository is {str(repo.head.commit.hexsha)}\n"
    ) + "".join(
        [
            f'    Remote named "{remote}" with URL "{remote.url}\n"'
            for remote in repo.remotes
        ]
    )


results = local_moh_repo.remotes.origin.pull()
assert not any(
    [FetchInfoFlags.ERROR in FetchInfoFlags(fetch.flags) for fetch in results]
), "Error in last pull"
# check that the repository loaded correctly
if not local_moh_repo.bare:
    print("Repo at {} successfully loaded.".format(DATA_MOH))
    # print_repository_info(local_moh_repo)

    commits = list(local_moh_repo.iter_commits(local_moh_repo.active_branch))[
        :COMMITS_TO_PRINT
    ]
    # for commit in commits:
    #     print_commit_data(commit)
    #     pass
    commit_oi = commits[0]
    repo_last_commit = f"{commit_oi.authored_datetime} {str(commit_oi.hexsha)[0:8]} {commit_oi.summary}"
    glue("Northland MOH data last commit", repo_last_commit, display=False)


# build lists of IO (Items of Interest)
weekly_data_folders = {
    i: Path(DATA_MOH) / "vaccine-data" / i
    for i in os.listdir(Path(DATA_MOH) / "vaccine-data")
    if re.match(r"\d{4}-\d{2}-\d{2}", i)
}
data_files_oi = ["dhb_residence_uptake.csv"]


# Get the current week and prior weeks data
df_week_prior = pd.read_csv(weekly_data_folders[DATE_WEEK_CURRENT] / data_files_oi[0])
df_week_current = pd.read_csv(weekly_data_folders[DATE_WEEK_PRIOR] / data_files_oi[0])

# Filter for Northland
df_week_current = df_week_current.loc[
    df_week_current["DHB of residence"] == "Northland"
]
df_week_prior = df_week_prior.loc[df_week_prior["DHB of residence"] == "Northland"]


# Identify current Total Eligable population
data_current_eligable = df_week_current["Population"].sum()
data_prior_eligable = df_week_prior["Population"].sum()
glue(
    f"Northland Total Vaccine Eligible Population (current week)",
    data_current_eligable,
    display=False,
)
glue(
    f"Current Week",
    datetime.fromisoformat(DATE_WEEK_CURRENT).strftime("%yW%V"),
    display=False,
)
glue(
    f"Northland Total Vaccine Eligible Population (prior week)",
    data_prior_eligable,
    display=False,
)
glue(
    f"Prior Week",
    datetime.fromisoformat(DATE_WEEK_PRIOR).strftime("%yW%V"),
    display=False,
)


# setup list of fields that are key
keys = ["DHB of residence", "Ethnic group", "Age group", "Gender"]


# produce a dataframe that compares this week to last week (prior)
df_compare = pd.merge(
    left=df_week_current,
    right=df_week_prior,
    on=keys,
    how="inner",
    validate="one_to_one",
    suffixes=("", "_prior"),
)
df_compare.loc[:, keys + ["Population", "Population_prior"]]


# Calculate Population Changes
# 1. Create the Change  fields

df_compare["Population Changed"] = None
df_compare["First dose administered Changed"] = None
df_compare["Second dose administered Changed"] = None


# Calculate changes
def calc_changes(record):

    result = (
        record["Population"] - record["Population_prior"],
        record["First dose administered"] - record["First dose administered_prior"],
        record["Second dose administered"] - record["Second dose administered_prior"],
    )
    result = (e if e > 0 else 0 for e in result)
    return pd.Series(result)


change_fields = [
    "Population Changed",
    "First dose administered Changed",
    "Second dose administered Changed",
]
df_compare[change_fields] = df_compare.apply(calc_changes, axis=1)


# Create the Output Dataframe
output_fields = [
    "Population",
    "Population_prior",
    "Population Changed",
    "First dose administered",
    "First dose administered_prior",
    "First dose administered Changed",
    "Second dose administered",
    "Second dose administered_prior",
    "Second dose administered Changed",
]
df_out = (
    df_compare.loc[:, keys + output_fields]
    .groupby(["DHB of residence", "Ethnic group", "Age group"])
    .sum()
)

df_out.reset_index(inplace=True)


# Calculate the unvaccinated and ratio of first dose to unvaccinated
df_out["Population unvaccinated"] = 0


def calc_percentage_of_unvaccinated_population(record):
    # print(type(record["Population"]))
    unvaccinated_population = (
        record["Population"] - record["First dose administered_prior"]
    )

    # print(unvaccinated_population)
    # Correct for case of population is less than vacninated
    # If so then assume that the change is the unvaccinated
    unvaccinated_population = (
        unvaccinated_population
        if (
            unvaccinated_population >= 0
            and unvaccinated_population > record["First dose administered Changed"]
        )
        else record["First dose administered Changed"]
    )
    try:
        result = round(
            # Calculate percentage
            (record["First dose administered Changed"] / unvaccinated_population * 100),
            3,
        )
    except Exception as e:
        result = 0 if unvaccinated_population <= 0 else None
        print(
            f"********  result:{result}, Exception for rec:\n{record}, \nexception :{e}"
        )
    # print((unvaccinated_population, result))
    # assert False
    return pd.Series((unvaccinated_population, result))


changed_fields = [
    "Population unvaccinated",
    "First dose administered Changed as Percent of unvaccinated Population",
]
df_out[changed_fields] = df_out.apply(
    calc_percentage_of_unvaccinated_population, axis=1
)
import plotly.io as pio
import plotly.express as px
import plotly.offline as py


fig = px.scatter(
    df_out,
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
# fig
# glue(
#     f"Plot1",
#     fig,
#     display=False,
# )
