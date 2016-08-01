# EEG Resting State
Resting state scripts for many projects.

These scripts by default run through 4 trials, and send two triggers alternating (101 and 102). Changes between trials (by default 60 seconds long) are signalled with beeps. You can edit any of the parameters at the top of the script.

If you change the design of the study make sure to also update the text you are presenting to the participants as instructions!

### Dependencies

For the Matlab version, you need the [Psychtoolbox](www.psychtoolbox.org)

For python, you need:
- Python 2.7.x
- Psychopy (`pip install psychopy`, but check the dependencies at [psychopy](psychopy.org)
- 

Jan Freyberg (jan.freyberg [at] kcl.ac.uk)
