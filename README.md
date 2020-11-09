## Pink Programming Workshop -- Nov 15, 2020
In this repository, you will find all necessary resources you will need for the
workshop. Keen observers will also note that there is a script, as well as
finished solutions for all steps the workshop in here as well. You're not
expected to read this before the workshop, and we will not follow it to the
letter, but if you find it helpful to skim it in advance or follow along during
the event, you are of course very welcome to. 

I will most likely try to keep this repository up and unmodified for as long as
possible after the event, but if you want to keep this material, you should
create your own copy using the "Fork" button in the top left hand side of the
repository web page.

## Setup instructions
In preparation for the workshop, you will need access to a computer with a
working Python executable and package manager installed. In addition, you will
need to install the `pika` package using that package manager.

For users of the Microsoft Windows operating system: There is a section
dedicated to you, specifically about how to use some of the tools that are more
prevalent on Unices. Skip ahead to that now if you'll be using Windows.

If you have not done this previously, this is what you will need to do:
  1. First, go to [this
    link](https://www.anaconda.com/products/individual#Downloads) and download
    the Anaconda software distribution installer for your operating system.
    - If you are on a linux-based operating system (including the Windows
      Subsystem for Linux), you can probably find it in your package manager's
      repository under `conda` or `anaconda`. On most distributions, you can
      install `python` (and possibly `python-pip`) instead, and then skip to
      the final step.
  2. Run the downloaded installer, following the recommended settings.
  3. Open a new terminal window and run the `conda` command in it. This should
    print a long-ish message to your terminal window.
  4. Run the command `conda activate` in your terminal window. On most systems,
    this will cause something like `(base)` to appear after you type a command.
  5. Run `pip install pika`. This will install the package we're going to use to
    send data during the workshop.

Finally, you will need a text editor. Any editor that can handle plain text
files will work, but most people prefer one made specifically for editing code.
At the workshop, we will be using Visual Studio Code (note that this is not the
same as Visual Studio). You can install VSCode at
[https://code.visualstudio.com/download](https://code.visualstudio.com/download).
We will not be using any features specific to any editor, so if you feel more
comfortable using something else, by all means stick to it.

## Getting a proper terminal on Microsoft Windows
During the setup process and the workshop, we will be using (and building)
terminal-based interfaces. The Windows terminal ecosystem is fragmented and
slightly obscure, so the Anaconda distribution ships with its own program for
opening a new terminal window inside its environment. By default (in the test
install I did) step 2. above will install a program called "Anaconda Prompt
(anaconda3)".  This is the application you want to run in order to open a
terminal window for the rest of the setup and during the workshop.

## Trouble? Questions? Confused?
Reach out to me or another mentor on the participants' Slack as a first resort
(cuts down on question repetition), or if you are for some reason unable, send
me an email at renee.gyllenvaan@gmail.com -- I try to be as prompt as possible.
