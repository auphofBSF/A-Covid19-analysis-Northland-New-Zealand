# A Covid19 analysis Northland, New-Zealand

A personal study of the Covid19 situation in Northland New Zealand, by a concerned resident in the form of a Jupyter Book

This study is based on publicly available data sources

The Github Pages published version of this can be found at https://auphofbsf.github.io/NZ-Covid19-Vaccine-Analysis-Northland 

# Accessing Github Data sources
Credentials are required,  obtain a Github PAT token to access the MOH Github Data
set it in an .env in the root folder such as:

```
GITHUB_TOKEN=ghp_xMBoiqG...............cfa4oZ6p45yiNy
```

For further info on Github Personal Access Tokens (PAT's) see: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token


# Install in dev environment.

Python 3.9.7 was used with the dependencies contained in `requirement.txt` .A  poetry environment was configured, (this will be added to this repo)
It was developed on a Windows 10 x64 machine

# Building

for current changes
```
jb build .
```

for complete rebuild
```
jb build . --all
```