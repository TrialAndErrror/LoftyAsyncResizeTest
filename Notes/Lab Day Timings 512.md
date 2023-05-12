Lab Day Timings 5/12
========================

# Run 1
Running in blocking mode took 7.55 seconds (~0.13 minutes)
Running in async mode took 2.94 seconds (~0.05 minutes)
Running in multiprocessing mode took 8.05 seconds (~0.13 minutes)

## Notes

Something must be up with multiprocessing - going to take a look

# Run 2
 - branch labday-may12, 
 - commit 51388c373f3f1394102b027b889b741876717d56
 
Running in blocking mode took 7.55 seconds (~0.13 minutes)
Running in async mode took 2.45 seconds (~0.04 minutes)
Running in multiprocessing mode took 2.65 seconds (~0.04 minutes)

## Notes
Looks like using a multiprocessing pool did speed up the process back to async levels;
wonder if there's something in the looping that I did that was blocking.

[The site that I found the Pool instructions on](https://machinelearningmastery.com/multiprocessing-in-python/) mentioned that we use `apply_async()` when setting up the pool so that we don't block while adding the thread; I wonder if that would help with the original implementation. 

# Run 3 - Joblib
Running in blocking mode took 7.72 seconds (~0.13 minutes)
Running in async mode took 2.49 seconds (~0.04 minutes)
Running in multiprocessing mode took 3.64 seconds (~0.06 minutes)

## Notes
Here, we used Joblib to try and abstract away some of the multiprocessing details, but it looks like the added overhead slowed things down. I'm curious to see if increasing the number of files, or the size of the files, makes a difference. First, let's run all the multiprocessing methods at once to compare,

# Run 4 - All MP versions
Running in blocking mode took 7.60 seconds (~0.13 minutes)
Running in async mode took 7.92 seconds (~0.13 minutes)
Running in multiprocessing mode took 2.51 seconds (~0.04 minutes)
Running in multiprocessing-pool mode took 3.63 seconds (~0.06 minutes)
Running in multiprocessing-joblib mode took 2.48 seconds (~0.04 minutes)

## Notes
Did some more refactoring to make adding new options in later a bit easier, but otherwise largely unchanged. Looks like maybe joblib cleanup helped bring the timing down. Now i'm going to do 3 new runs; one with multiple iterations over these images to get averages; one with larger images; and one with more count of images.


# Run 5 - Averages
Running in blocking mode took 7.46 seconds (~0.12 minutes)
Running in async mode took 2.45 seconds (~0.04 minutes)
Running in multiprocessing mode took 7.86 seconds (~0.13 minutes)
Running in multiprocessing-pool mode took 2.86 seconds (~0.05 minutes)
Running in multiprocessing-joblib mode took 3.45 seconds (~0.06 minutes)


## Notes
Removed print statements and refactored to show averages across 10 rounds, for consistency.
Looks like my regular multiprocessing is still blocking, so it's good to use pool and joblib to avoid issues.

# Run 6 - 10x number of files
Running in blocking mode took 73.74 seconds (~1.23 minutes)
Running in async mode took 24.64 seconds (~0.41 minutes)
Running in multiprocessing mode took 81.92 seconds (~1.37 minutes)
Running in multiprocessing-pool mode took 34.20 seconds (~0.57 minutes)
Running in multiprocessing-joblib mode took 34.40 seconds (~0.57 minutes)


## Notes
To be expected, async was fastest; however, with the larger number of files, it seems that 
blocking mode averaged a bit faster. Overall the bad multiprocessing option came out as the worst, but the good ones
seemed to work pretty well. Async was still the fastest.
