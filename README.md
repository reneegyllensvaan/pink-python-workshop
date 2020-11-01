## Setup instructions
In preparation for the workshop, you will need access to a computer with a
working Python executable and package manager installed. In addition, you will
need to install the `pika` package using that package manager.

If you have not done this previously, this is what you will need to do:
  - First, go to [this
    link](https://www.anaconda.com/products/individual#Downloads) and download
    the Anaconda software distribution installer for your operating system.
    - If you are on a linux-based operating system (including the Windows
      Subsystem for Linux), you can probably find it in your package manager's
      repository under `conda` or `anaconda`. On most distributions, you can
      install `python` (and possibly `python-pip`) instead, and then skip to
      the final step.
  - Run the downloaded installer, following the recommended settings.
  - Open a new terminal window and run the `conda` command in it. This should
    print a long-ish message to your terminal window.
  - Run the command `conda activate` in your terminal window. On most systems,
    this will cause something like `(base)` to appear after you type a command.
  - Run `pip install pika`. This will install the package we're going to use to
    send data during the workshop.

Finally, you will need a text editor to edit source code with. At the workshop,
we are going to use Visual Studio Code (this is not the same as Visual Studio).
You can install VSCode at
[https://code.visualstudio.com/download](https://code.visualstudio.com/download).
The workshop will be editor-independent, if you feel more comfortable with
another editor you are very welcome to use it.

### Troubleshooting
FIXME:
  - Add some links for Windows:
    - How to check and set `$PATH`
    - Look up which shells are pre-installed and which one is easiest to use,
      also if conda provides a terminal wrapper. Check if this is a potential
      solution to path issues
  - For OS X:
    - Add some troubleshooting steps for what happens if the conda installer
      isn't appending to people's zshrc/bashrc to set the environment conf.
    - Maybe add steps to debug path issues, or at least how to call the shell
      environment hook yourself.

