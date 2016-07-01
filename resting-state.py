from psychopy import core, visual, event, monitors, parallel, prefs
from psychopy import sound
# prefs.general['audioLib'] = ['pygame']


# Resting State Script
# Jan Freyberg (jan.freyberg@kcl.ac.uk)
# This script simply presents instructions, and sends triggers.

# Parameters for this script
trialnumber = 4  # how many trials there will be in total
trialduration = 60  # how long a trial is

# Triggers - the script will just cycle through these
triggers = [201, 202]  # i.e. for 2 triggers & 4 trials, pattern will be A B A B

# Set the screen parameters: (This is important!)
screen = monitors.Monitor('tobiix300')
screen.setSizePix([1920, 1080])
screen.setWidth(51)  # screen width in cm
screen.setDistance(60)  # distance from screen in cm

# Open the display window:
win = visual.Window([500, 500], allowGUI=True, monitor=screen,
                    units='deg', fullscr=False)

# Make a generic text stimulus for instructions
message = visual.TextStim(win, units='norm', pos=[0, 0], height=0.07,
                          alignVert='center', alignHoriz='center',
                          text='')

# Make a fixation cross
fixation = visual.GratingStim(win, tex='sqr', mask='cross', sf=0, size=0.3,
                              pos=[0, 0], color='black', autoDraw=False)

# Make a sound that will notify the user when the trial changes
beep = sound.Sound(value=400, secs=0.25)
beep.setVolume(0.4)

# Open the parallel port (default address(LPT1), all pins low)
outport = parallel.ParallelPort()
outport.setData(0)


# define a trigger function. change this depending on the system
def trigger(value=0):
    outport.setData(value)  # set pins high
    core.wait(0.003)  # wait for acquisition of trigger
    outport.setData(0)  # set pins low


# Define a function that takes a string and displays it, then waits to proceed
def instruct(displaystring):
    message.text = displaystring
    message.draw()
    win.flip()
    event.waitKeys(keyList=['space'])

# Give instructions:
instruct("Please relax for the next 4 minutes. Please alternate between "
         "keeping your eyes open for a minute and keeping your eyes "
         "closed for a minute (you can of course blink.) There will be "
         "a tone notifying you of when you need to switch from having "
         "your eyes open to closed, or vice versa.\n\n"
         "Press [space] to continue.")
instruct("When you hear the first tone, please start with your eyes "
         "open for one minute. Please try to focus your eyes on the "
         "fixation cross in the center of the screen.\n\nIf you have any "
         "questions, please ask now - if not, check if the experimenter "
         "is ready, and then press [space] to start.")

for seconds in range(5):
    message.text = ("Starting in " + str(5 - seconds) + " seconds.")
    message.draw()
    win.flip()
    core.wait(1)
win.flip()

# Some stuff to keep track of timing
trialClock = core.Clock()
trialClock.add(1)  # because we want to have time before the trial starts
win.callOnFlip(trialClock.reset)
t = trialClock.getTime()
# Go through trials!
for trials in range(trialnumber):
    # before the trial is supposed to start, wait with high precision
    while trialClock.getTime() < trials * trialduration:
        pass
    # announce the next trial and also flip the screen (no real reason)
    beep.play()
    trigger(triggers[trials % len(triggers)])
    win.flip()
    # step through trial duration (except for one second) in 1s chunks
    for seconds in range(int(trialduration - 1)):
        core.wait(1)
        # check if experiment was interrupted in last second
        if event.getKeys(keyList='escape'):
            trigger(99)
            raise KeyboardInterrupt("You interrupted the script manually!")
