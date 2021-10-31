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
from typing import List

import locale

locale.setlocale(locale.LC_NUMERIC, "")

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


def is_string_series(s: pd.Series):
    if isinstance(s.dtype, pd.StringDtype):
        # The series was explicitly created as a string series (Pandas>=1.0.0)
        return True
    elif s.dtype == "object":
        # Object series, check each value
        return all((v is None) or isinstance(v, str) for v in s)
    else:
        return False


class MOH_data:
    def prep_step1_pull_data(self):

        # TODO , if does not exist
        # Repo.clone_from(repo.clone_url, DATA_MOH)

        # create list of commits then print some of them to stdout
        # Repo object used to interact with Git repositories
        self.local_moh_repo = Repo(DATA_MOH)
        results = self.local_moh_repo.remotes.origin.pull()
        assert not any(
            [FetchInfoFlags.ERROR in FetchInfoFlags(fetch.flags) for fetch in results]
        ), "Error in last pull"
        # check that the repository loaded correctly
        if not self.local_moh_repo.bare:
            print("Repo at {} successfully loaded.".format(DATA_MOH))
            # print_repository_info(self.local_moh_repo)

            commits = list(
                self.local_moh_repo.iter_commits(self.local_moh_repo.active_branch)
            )[:COMMITS_TO_PRINT]
            # for commit in commits:
            #     print_commit_data(commit)
            #     pass
            commit_oi = commits[0]
            repo_last_commit = f"{commit_oi.authored_datetime} {str(commit_oi.hexsha)[0:8]} {commit_oi.summary}"
            glue("Northland MOH data last commit", repo_last_commit, display=False)

        # build lists of IO (Items of Interest)
        self.weekly_data_folders = {
            i: Path(DATA_MOH) / "vaccine-data" / i
            for i in os.listdir(Path(DATA_MOH) / "vaccine-data")
            if re.match(r"\d{4}-\d{2}-\d{2}", i)
        }

    def _prep_step_2_read_a_week_uptake_data(
        self, date_week_current=DATE_WEEK_CURRENT, date_week_prior=DATE_WEEK_PRIOR
    ):
        data_files_oi = ["dhb_residence_uptake.csv"]

        # Get the current week and prior weeks data
        self.df_week_prior = pd.read_csv(
            self.weekly_data_folders[date_week_prior] / data_files_oi[0]
        )
        self.df_week_current = pd.read_csv(
            self.weekly_data_folders[date_week_current] / data_files_oi[0]
        )

        # clean series, convert any str to int
        series_to_check = [
            "Population",
            "First dose administered",
            "Second dose administered",
        ]

        def convert_series_atoi(df: pd.DataFrame, series_to_check):
            for serie in series_to_check:
                if is_string_series(df[serie]):
                    df[serie] = df[serie].apply(locale.atoi)

        convert_series_atoi(self.df_week_prior, series_to_check)
        convert_series_atoi(self.df_week_current, series_to_check)

        # Filter for Northland
        self.df_week_current = self.df_week_current.loc[
            self.df_week_current["DHB of residence"] == "Northland"
        ]
        self.df_week_prior = self.df_week_prior.loc[
            self.df_week_prior["DHB of residence"] == "Northland"
        ]

        # Identify current Total Eligable population
        data_current_eligable = self.df_week_current["Population"].sum()
        data_prior_eligable = self.df_week_prior["Population"].sum()
        glue(
            f"Northland Total Vaccine Eligible Population (current week)",
            data_current_eligable,
            display=False,
        )
        glue(
            f"Current Week",
            datetime.fromisoformat(date_week_current).strftime("%yW%V"),
            display=False,
        )
        glue(
            f"Northland Total Vaccine Eligible Population (prior week)",
            data_prior_eligable,
            display=False,
        )
        glue(
            f"Prior Week",
            datetime.fromisoformat(date_week_prior).strftime("%yW%V"),
            display=False,
        )

        # setup list of fields that are key
        self.df_uptake_keys = [
            "DHB of residence",
            "Ethnic group",
            "Age group",
            "Gender",
        ]

        # produce a dataframe that compares this week to last week (prior)
        self.df_compare = pd.merge(
            left=self.df_week_current,
            right=self.df_week_prior,
            on=self.df_uptake_keys,
            how="inner",
            validate="one_to_one",
            suffixes=("", "_prior"),
        )
        # self.df_compare.loc[:, self.df_uptake_keys + ["Population", "Population_prior"]]

        self.df_compare["Week ending"] = datetime.fromisoformat(date_week_current)

        # Calculate Population Changes
        # 1. Create the Change  fields

        self.df_compare["Population Changed"] = None
        self.df_compare["First dose administered Changed"] = None
        self.df_compare["Second dose administered Changed"] = None

        # Calculate changes
        def calc_changes(record):

            result = (
                record["Population"] - record["Population_prior"],
                record["First dose administered"]
                - record["First dose administered_prior"],
                record["Second dose administered"]
                - record["Second dose administered_prior"],
            )
            result = (e if e > 0 else 0 for e in result)
            return pd.Series(result)

        change_fields = [
            "Population Changed",
            "First dose administered Changed",
            "Second dose administered Changed",
        ]
        self.df_compare[change_fields] = self.df_compare.apply(calc_changes, axis=1)

        # Calculate Population Unvaccinated
        # 1. Create the Population unvaccinated  fields
        self.df_compare["Population unvaccinated at week start"] = 0

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
                    and unvaccinated_population
                    > record["First dose administered Changed"]
                )
                else record["First dose administered Changed"]
            )
            try:
                # TODO: reduce the division by zero errors
                result = 0 if unvaccinated_population==0 else round(
                    # Calculate percentage
                    (
                        record["First dose administered Changed"]
                        / unvaccinated_population
                        * 100
                    ),
                    3,
                )
            except Exception as e:
                result = 0 if unvaccinated_population <= 0 else None
                print(
                    f"********  result:{result}, Exception for rec:\n{record}, \nexception :{e}"
                )
            # print((unvaccinated_population, result))
            # assert False
            return pd.Series(
                (
                    unvaccinated_population,
                    unvaccinated_population - record["First dose administered Changed"],
                    result,
                )
            )

        change_fields = [
            "Population unvaccinated at week start",
            "Population unvaccinated at week end",
            "First dose administered Changed as Percent of unvaccinated Population",
        ]
        self.df_compare[change_fields] = self.df_compare.apply(
            calc_percentage_of_unvaccinated_population, axis=1
        )
        self.output_fields = [
            "Week ending",
            "Population",
            "Population_prior",
            "Population Changed",
            "Population unvaccinated at week start",
            "Population unvaccinated at week end",
            "First dose administered",
            "First dose administered_prior",
            "First dose administered Changed",
            "First dose administered Changed as Percent of unvaccinated Population",
            "Second dose administered",
            "Second dose administered_prior",
            "Second dose administered Changed",
        ]

    def prep_step_2_read_all_uptake_data(self):
        """Read in all available data and format appropriately"""
        # Generate a list of Weeks available to process
        list_of_weeks = [week for week in sorted(self.weekly_data_folders.keys())]
        # Construct a paramater set
        comparison_sets = list(zip(list_of_weeks[1:], list_of_weeks[2:]))
        comparsion_sets_args = [
            {"date_week_current": t[1], "date_week_prior": t[0]}
            for t in comparison_sets
        ]

        self.df_all_weeks = None
        for cs in comparsion_sets_args:
            self._prep_step_2_read_a_week_uptake_data(**cs)
            if self.df_all_weeks is None:
                self.df_all_weeks = self.df_compare.loc[
                    :, self.df_uptake_keys + self.output_fields
                ].copy(deep=True)
            else:
                self.df_all_weeks = pd.concat(
                    [
                        self.df_all_weeks,
                        self.df_compare.loc[
                            :, self.df_uptake_keys + self.output_fields
                        ],
                    ],
                    axis=0,
                    ignore_index=True,
                )

    def prep_step_3_generate_report_data(self):
        """Generate Data Sets for Reporting against"""

        # Generate a grouped `Age Group` called `Age Category`
        age_group_sets = [
            [
                "12-15",
                "16-19",
            ],
            [
                "20-24",
                "25-29",
                "30-34",
                "35-39",
            ],
            [
                "40-44",
                "45-49",
                "50-54",
                "55-59",
                "60-64",
                "65-69",
            ],
            ["70-74", "75-79", "80-84", "85-89", "90+"],
        ]

        def minmax(l: List[int]) -> List[int]:
            return [min(l), max(l)]

        age_category = {
            i: "-".join(minmax("-".join(l).split("-")))
            for i, l in enumerate(age_group_sets)
        }
        age_category_lookup = {
            a: age_category[i] for i, l in enumerate(age_group_sets) for a in l
        }
        age_category_lookup_lookup_reverse = {
            v: k for k, v in age_category_lookup.items()
        }
        self.df_all_weeks["Age Category"] = self.df_all_weeks["Age group"].apply(
            age_category_lookup.get
        )

        self.df_all_weeks_no_gender_age_category = (
            self.df_all_weeks.loc[
                :,
            ]
            .groupby(
                by=[
                    "DHB of residence",
                    "Week ending",
                    "Ethnic group",
                    # "Gender",
                    "Age Category",
                ]
            )
            .sum()
        )

        self.df_all_weeks_no_gender_age_category.reset_index(inplace=True)

        self.df_all_weeks_no_gender = (
            self.df_all_weeks.loc[
                :,
            ]
            .groupby(
                by=[
                    "DHB of residence",
                    "Week ending",
                    "Ethnic group",
                    # "Gender",
                    "Age Category",
                ]
            )
            .sum()
        )

        self.df_all_weeks_no_gender.reset_index(inplace=True)

        self.df_all_weeks_no_gender_no_age = (
            self.df_all_weeks.loc[
                :,
            ]
            .groupby(
                by=[
                    "DHB of residence",
                    "Week ending",
                    "Ethnic group",
                    # "Gender",
                    # "Age group",
                ]
            )
            .sum()
        )

        self.df_all_weeks_no_gender_no_age.reset_index(inplace=True)

        # Create the Output Dataframe
        output_fields = [
            "Week ending",
            "Population",
            "Population_prior",
            "Population Changed",
            "Population unvaccinated at week start",
            "First dose administered",
            "First dose administered_prior",
            "First dose administered Changed",
            "First dose administered Changed as Percent of unvaccinated Population",
            "Second dose administered",
            "Second dose administered_prior",
            "Second dose administered Changed",
        ]
        self.df_out = (
            self.df_compare.loc[:, self.df_uptake_keys + output_fields]
            .groupby(
                [
                    "DHB of residence",
                    "Week ending",
                    "Ethnic group",
                    "Gender",
                    "Age group",
                ]
            )
            .sum()
        )

        self.df_out.reset_index(inplace=True)

        # Calculate the unvaccinated and ratio of first dose to unvaccinated
