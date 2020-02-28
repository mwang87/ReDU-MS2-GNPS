# Welcome to ReDU

![](https://github.com/mwang87/ReDU-MS2-GNPS/workflows/production-integration/badge.svg)

## Reanalysis of Data User Interface

[ReDU](https://redu.ucsd.edu/) is a community-minded approach to find and reuse public data containing tandem MS data at the repository scale. ReDU is a launchpad for co- or re-analysis of public data via the Global Natural Product Social Molecular Networking Platform [(GNPS)](https://gnps.ucsd.edu/ProteoSAFe/static/gnps-splash.jsp). Our aim is to empower researchers to put their data in the context of public data as well as explore questions using public data at the repository scale.

**This is a community effort and everyone is encouraged to participate by submitting their own data and sample information [instructions](https://mwang87.github.io/ReDU-MS2-Documentation/HowtoContribute). The sharing of new applications (and code) which use ReDU is highly encouraged.**

## Testing Procedure

To get ReDU up and running on your local system, it should be as easy as

```
server-compose-interactive
```

## Updating ReDU Data Procedure

One of the key steps in ReDU is the updating of the database to include the latest identifications for files within ReDU. These are the following steps:

1. Download batch template for GNPS at ```/batchtemplate```
1. Run Batch Workflow for Spectral Library Search
1. Get the set of tasks as tsv and save to [here](https://github.com/mwang87/ReDU-MS2-GNPS/blob/refactor-read-me-for-developers/database/global_tasks.tsv). 
1. Remove database [here](https://github.com/mwang87/ReDU-MS2-GNPS/tree/refactor-read-me-for-developers/database)
1. Run XXX command to drop identifications table
1. Start ReDU back up and it will autopopulate

