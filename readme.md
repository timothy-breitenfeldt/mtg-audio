### Description

This project is an accessible audio based Magic the Gathering application, providing a comprehensive search engine, and at the moment single player battlefield for playing with other people. This application is driven by screen reader output, and requires that the user is using a screen reader for optimal experience.

This application has only been tested on Windows and Mac. It might work on Linux, but will not support Linux officially unless requests dictate otherwise.

#### Screen Readers

This application uses accessible_output2 for cross platform screen reader output. Tested screen readers are:

Windows:

- JAWS
- NVDA

Mac:

- Voiceover

Other screen readers might work with it since there are others that are supported by accessible_output2, but these are the only screen readers that have been tested.

#### Development Environment

MTG Audio uses python 3 with the following third party libraries that can be installed via pip:

- accessible_output2
- wxpython
- pyinstaller
- wget
