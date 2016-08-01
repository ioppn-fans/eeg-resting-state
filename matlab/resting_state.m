%% A Resting State Script

% Variables
trialnumber = 4; % how many trials to run through
trialduration = 60; % trial duration in seconds

% Triggers
triggers = [101, 102]; % what triggers you want to use
triggers = repmat(triggers, 1, trialnumber/numel(triggers));

% Backgroundcolor
bgcolor = 127.5;

try
    InitializePsychSound;
    pa = PsychPortAudio('Open', [], [], [], [], [], 256);
    bp400 = PsychPortAudio('CreateBuffer', pa, [MakeBeep(400, 0.2); MakeBeep(400, 0.2)]);
    PsychPortAudio('FillBuffer', pa, bp400);
catch sounderr
    sca;
    rethrow(sounderr);
end

% Configure the Parallel Port
try
    % config_io;
    address = hex2dec('D010');
    outp(address, 0); % set all parport pins low
catch ioerr
    sca;
    disp('IO Error. Is config_io installed and is it the right version?');
    rethrow(ioerr);
end

KbName('UnifyKeyNames');
esc_key = KbName('Escape');

% Open the screen
try
    scr = Screen('OpenWindow', 2, bgcolor);
    HideCursor;
catch screenerr
    sca;
    rethrow(screenerr);
end

try
    % Instruct the participant:
    DrawFormattedText(scr, ['From the first beep, keep your eyes open for a minute.'...
                            'After a minute you will hear a second beep, indicating '...
                            'you should close your eyes for one minute. This will '...
                            'continue to alternate for 4 minutes.\n\nPlease try and '...
                            'restrict blinking during the eye open intervals. Press '...
                            'any key to start.'], 'center', 'center', 0, 40, [], [], 1.5);
    Screen('Flip', scr);
    KbStrokeWait;

    % Give a 5 Second countdown:
    for lapsedTime = 1:5
    DrawFormattedText(scr, ['Starting in ' num2str(6-lapsedTime) ' seconds'], 'center', 'center', 0);
    Screen('Flip', scr);
    WaitSecs(1);
    end

    % Draw the fixation cross
    DrawFormattedText(scr, '+', 'center', 'center', 0);
    Screen('Flip', scr);

    % Priority(1); % NB Priority works differently on Windows, OSX and Linux
    %              % Priority(1) is highest priority on Windows machines


    % Cycle through trials:
    t = GetSecs + 1; % Add one sec to give an additional 1 sec waiting
    for trial = 1:trialnumber
        % Before the trial, wait with high precision
        while GetSecs < t
            WaitSecs(0.001); % Wait one millisecond
        end
        % Start the trial:
        outp(address, triggers(trial)); % Send the trigger
        PsychPortAudio('Start', pa); % Produce the beep

        t = GetSecs + trialduration; % Set start time for next trial

        % Wait for the next trial by waiting in 1second steps:
        for waitTime = 1:trialduration-5
            % Wait one sec & also check keyboard:
            [~, keys] = KbWait([], [], GetSecs+1);
            % If escape key was pressed:
            if keys(esc_key)
                error('You manually interrupted the script.');
            end
        end
    end

catch experimenterr
    sca;
    rethrow(experimenterr)
end

% Finish: Beep twice, close everything
PsychPortAudio('Start', pa);
WaitSecs(0.5);
PsychPortAudio('Start', pa);
sca;
