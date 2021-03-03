# MindisCernStuff
This is to automate the job of Mindi so it does 100 things all at once

## Steps Neccesary
1. open param_card.dat
2. set the masses for Zd and MfD1
3. close the card
4. run: ./bin/generate_events
5. find the run number that was just created 
6. go to Events/run#
7. unzip unweighted_events.tar.gz 
8. rename the file according to the mass: MZD_XX_XX.lhe
9. once you have a full coloum make directory with the related runs 
10. zip it
11. copy it to my mac

## What is happening now

We did it! well mostly. Ideally it works, but more testing is required on Mehdi's machine. we need to update the documentation on AutoProduction.py, and this README needs to reflect proper csv input. maybe, in the future, implement a csv that isn't restricted to mzd and mfd1, but other variables? for now that is unnecessary.
