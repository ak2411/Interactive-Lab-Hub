# Chatterboxes
[![Watch the video](https://user-images.githubusercontent.com/1128669/135009222-111fe522-e6ba-46ad-b6dc-d1633d21129c.png)](https://www.youtube.com/embed/Q8FWzLMobx0?start=19)

In this lab, we want you to design interaction with a speech-enabled device--something that listens and talks to you. This device can do anything *but* control lights (since we already did that in Lab 1).  First, we want you first to storyboard what you imagine the conversational interaction to be like. Then, you will use wizarding techniques to elicit examples of what people might say, ask, or respond.  We then want you to use the examples collected from at least two other people to inform the redesign of the device.

We will focus on **audio** as the main modality for interaction to start; these general techniques can be extended to **video**, **haptics** or other interactive mechanisms in the second part of the Lab.

## Prep for Part 1: Get the Latest Content and Pick up Additional Parts 

### Pick up Additional Parts

As mentioned during the class, we ordered additional mini microphone for Lab 3. Also, a new part that has finally arrived is encoder! Please remember to pick them up from the TA.

### Get the Latest Content

As always, pull updates from the class Interactive-Lab-Hub to both your Pi and your own GitHub repo. As we discussed in the class, there are 2 ways you can do so:

**\[recommended\]**Option 1: On the Pi, `cd` to your `Interactive-Lab-Hub`, pull the updates from upstream (class lab-hub) and push the updates back to your own GitHub repo. You will need the *personal access token* for this.

```
pi@ixe00:~$ cd Interactive-Lab-Hub
pi@ixe00:~/Interactive-Lab-Hub $ git pull upstream Fall2021
pi@ixe00:~/Interactive-Lab-Hub $ git add .
pi@ixe00:~/Interactive-Lab-Hub $ git commit -m "get lab3 updates"
pi@ixe00:~/Interactive-Lab-Hub $ git push
```

Option 2: On your your own GitHub repo, [create pull request](https://github.com/FAR-Lab/Developing-and-Designing-Interactive-Devices/blob/2021Fall/readings/Submitting%20Labs.md) to get updates from the class Interactive-Lab-Hub. After you have latest updates online, go on your Pi, `cd` to your `Interactive-Lab-Hub` and use `git pull` to get updates from your own GitHub repo.

## Part 1.
### Text to Speech 

In this part of lab, we are going to start peeking into the world of audio on your Pi! 

We will be using a USB microphone, and the speaker on your webcamera. (Originally we intended to use the microphone on the web camera, but it does not seem to work on Linux.) In the home directory of your Pi, there is a folder called `text2speech` containing several shell scripts. `cd` to the folder and list out all the files by `ls`:

```
pi@ixe00:~/text2speech $ ls
Download        festival_demo.sh  GoogleTTS_demo.sh  pico2text_demo.sh
espeak_demo.sh  flite_demo.sh     lookdave.wav
```

You can run these shell files by typing `./filename`, for example, typing `./espeak_demo.sh` and see what happens. Take some time to look at each script and see how it works. You can see a script by typing `cat filename`. For instance:

```
pi@ixe00:~/text2speech $ cat festival_demo.sh 
#from: https://elinux.org/RPi_Text_to_Speech_(Speech_Synthesis)#Festival_Text_to_Speech

echo "Just what do you think you're doing, Dave?" | festival --tts
```

Now, you might wonder what exactly is a `.sh` file? Typically, a `.sh` file is a shell script which you can execute in a terminal. The example files we offer here are for you to figure out the ways to play with audio on your Pi!

You can also play audio files directly with `aplay filename`. Try typing `aplay lookdave.wav`.

\*\***Write your own shell file to use your favorite of these TTS engines to have your Pi greet you by name.**\*\*
(This shell file should be saved to your own repo for this lab.)

Bonus: If this topic is very exciting to you, you can try out this new TTS system we recently learned about: https://github.com/rhasspy/larynx

### Speech to Text

Now examine the `speech2text` folder. We are using a speech recognition engine, [Vosk](https://alphacephei.com/vosk/), which is made by researchers at Carnegie Mellon University. Vosk is amazing because it is an offline speech recognition engine; that is, all the processing for the speech recognition is happening onboard the Raspberry Pi. 

In particular, look at `test_words.py` and make sure you understand how the vocab is defined. Then try `./vosk_demo_mic.sh`

One thing you might need to pay attention to is the audio input setting of Pi. Since you are plugging the USB cable of your webcam to your Pi at the same time to act as speaker, the default input might be set to the webcam microphone, which will not be working for recording.

\*\***Write your own shell file that verbally asks for a numerical based input (such as a phone number, zipcode, number of pets, etc) and records the answer the respondent provides.**\*\*

Bonus Activity:

If you are really excited about Speech to Text, you can try out [Mozilla DeepSpeech](https://github.com/mozilla/DeepSpeech) and [voice2json](http://voice2json.org/install.html)
There is an included [dspeech](./dspeech) demo  on the Pi. If you're interested in trying it out, we suggest you create a seperarate virutal environment for it . Create a new Python virtual environment by typing the following commands.

```
pi@ixe00:~ $ virtualenv dspeechexercise
pi@ixe00:~ $ source dspeechexercise/bin/activate
(dspeechexercise) pi@ixe00:~ $ 
```

### Serving Pages

In Lab 1, we served a webpage with flask. In this lab, you may find it useful to serve a webpage for the controller on a remote device. Here is a simple example of a webserver.

```
pi@ixe00:~/Interactive-Lab-Hub/Lab 3 $ python server.py
 * Serving Flask app "server" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 162-573-883
```
From a remote browser on the same network, check to make sure your webserver is working by going to `http://<YourPiIPAddress>:5000`. You should be able to see "Hello World" on the webpage.

### Storyboard

Storyboard and/or use a Verplank diagram to design a speech-enabled device. (Stuck? Make a device that talks for dogs. If that is too stupid, find an application that is better than that.) Write out what you imagine the dialogue to be. Use cards, post-its, or whatever method helps you develop alternatives or group responses. 

**Teammates: Grace Le and Evan Lin**
We were interested in creating a speech-enabled device that isn't an _assistant_. We felt like voice assistants or just our smartphones in general are too kind - they would remind us to do the dishes, but would let it go if we don't do so; they would ask us to sleep, or set off screentime limits, but would let us continue to use our phone if we wanted to. Sometimes, what people need may not be nudges but forced compliance. 

**Enter:** the Tiger Parent! Essentially a speech-enabled habit builder in the form factor of a **picture frame**. It is relentless in keeping you accountable, and comes with a variety of classic tiger parenting phrases such as: "When I was your age...", "After all I have done for you", etc. You can even maximize its effect by putting a picture of someone who really motivates you. The characterization of the VA as a tiger parent opens up interesting design choices, such as never giving up when asking you to complete your task, sweetly understanding what you need, like cut fruit, through contextual clues, requiring you to formulate a valid reason for postponing a task, and giving you encouragement when you need it.

As a team, we came up with 3 different scenarios of where the tiger parent can be useful, and envision the different types of dialogue/responses it can provide depending on context.

**SCENARIO 1: WAKING YOU UP**


![IMG_5228](https://user-images.githubusercontent.com/18011694/135945336-2e62ccec-aa22-4143-a4d5-7efe3f905f10.JPG)


**SCENARIO 2: REMINDING YOU TO DO YOUR ASSIGNMENTS**


![IMG_5230](https://user-images.githubusercontent.com/18011694/135945351-dacb98fa-1d19-4c05-b1c0-f63ecb38ad06.JPG)


**SCENARIO 3: TELLING YOU TO GO TO SLEEP**


![IMG_5229](https://user-images.githubusercontent.com/18011694/135945342-9786dfdd-21b4-4356-8a53-95a3d1061005.JPG)


**The tiger parent's key features are:**
1. Relentless in ensuring you do what you said you would do (i.e. will not stop until you specify when you want to delay the task to)
2. Reminding you of motivational phrases when you're unmotivated
3. Rewards you when you do a good job with verbal affirmation
4. When you feel down, it will switch modes and be encouraging

**Below is the initial ideation of potential speech-enabled devices**
![Initial Ideation](https://user-images.githubusercontent.com/18011694/135939506-55067667-8617-4b0d-849f-72a4e1362914.JPG)

### Acting out the dialogue

Find a partner, and *without sharing the script with your partner* try out the dialogue you've designed, where you (as the device designer) act as the device you are designing.  Please record this interaction (for example, using Zoom's record feature).

I partnered with Shengnan Han for this section. The dialogue was similar to what we scripted, but the live dialogue also opened up new responses and prompts. For example, when we simulated the waking up situation, Shengnan asked for a 60 minute extention, but the class will start before that. This was actually an important point for the tiger parent to consider and ensure that the extension was feasible. It also elicited more common phrases that the tiger parent could potentially say. 

**Videos:**


https://user-images.githubusercontent.com/18011694/135946498-abf13bf0-0ea3-42f9-9805-48ad2917e3fe.mp4


https://user-images.githubusercontent.com/18011694/135946743-0b449c8f-aa6c-47cb-9ca7-1bc2c15078d0.mp4



https://user-images.githubusercontent.com/18011694/135947041-212f7ff0-0bfe-405f-bf26-5d1510a02cdc.mp4




### Wizarding with the Pi (optional)
In the [demo directory](./demo), you will find an example Wizard of Oz project. In that project, you can see how audio and sensor data is streamed from the Pi to a wizard controller that runs in the browser.  You may use this demo code as a template. By running the `app.py` script, you can see how audio and sensor data (Adafruit MPU-6050 6-DoF Accel and Gyro Sensor) is streamed from the Pi to a wizard controller that runs in the browser `http://<YouPiIPAddress>:5000`. You can control what the system says from the controller as well!

\*\***Describe if the dialogue seemed different than what you imagined, or when acted out, when it was wizarded, and how.**\*\*

# Lab 3 Part 2

For Part 2, you will redesign the interaction with the speech-enabled device using the data collected, as well as feedback from part 1.

## Prep for Part 2

1. What are concrete things that could use improvement in the design of your device? For example: wording, timing, anticipation of misunderstandings...
   - How the system will figure out what the user needs it to do
   - Customizability of the voice so its tailored to the user
   - Wording and phrases related to the culture of the person
   - How the system will react to a change in the environment, e.g. friends sleeping over or if it's a holiday 
   - How much of the nagging will make the user more stressed than before? Can we set settings? How do we balance between pushing the user whilst not pushing too hard? --> perhaps use peer accountability where you assign a friend to validate changes you want to make to the device like asking it to stop reminding you to do something

2. What are other modes of interaction _beyond speech_ that you might also use to clarify how to interact?
   - Reducing dependence on speech as an output modality by including non-verbal cues: 
      - Giving "the glare" by adding a laser to continuously follow the user's hand if they aren't responding
   - Adding light to show if the system is listening, processing, or off
   - Motion to show if its listening, processing or off
   - Motion for it to point
   - Facial expressions! To show its responses. For example if the user successfully does something, it will show a happy animation
   - Motion to just nudge the user to do their work, to call for attention, to express its "emotions"

3. Make a new storyboard, diagram and/or script based on these reflections.
   - 

## Prototype your system

The system should:
* use the Raspberry Pi 
* use one or more sensors
* require participants to speak to it. 

*Document how the system works*

*Include videos or screencaptures of both the system and the controller.*

## Test the system
Try to get at least two people to interact with your system. (Ideally, you would inform them that there is a wizard _after_ the interaction, but we recognize that can be hard.)

Answer the following:

### What worked well about the system and what didn't?
\*\**your answer here*\*\*

### What worked well about the controller and what didn't?

\*\**your answer here*\*\*

### What lessons can you take away from the WoZ interactions for designing a more autonomous version of the system?

\*\**your answer here*\*\*


### How could you use your system to create a dataset of interaction? What other sensing modalities would make sense to capture?

\*\**your answer here*\*\*

