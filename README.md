# Calculating Functional Flow Metrics

Lauren Chew, with CM flow data from Jon Cohen, supervised by Jon Herman

## About
Calculator for ecologically relevant flow characteristics known as functional flows, which includes timing, duration, and magnitude of seasonal hydrologic events. Currently working with inflow data from Folsom reservoir but will be expanded to be  a multi-reservoir simulation model. The aim is to determine the additional influence of water management on ecologically relevant flow metrics, as well as the potential to modify system operations to maintain functional flows while meeting other operating objectives such as water supply, flood control, and electricity generation. This analysis provides support for modifying future reservoir operation rules to reduce damage to downstream habitat, as well as an understanding of the relative influence of climate change on key components of the flow regime in northern California.

Adapted code from https://github.com/leogoesger/func-flow by Sarah Yarnell and Noelle Patterson
Additional documentation https://eflow.gitbook.io/ffc-readme/ 
## Usage

**Required Libraries:** Numpy, Pandas and ScyPi

**Input File:** FOL_in.csv

**Running Code:** Each script is run individually and outputs results into csv. Only the Annual and PeakMag scripts run properly. The WetSeason script runs but I have not been able to extract the correct data. SpringRec and DrySeason scripts are not functioning.
