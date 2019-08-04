# N-BodySimulator


My Final Project in Object-Oriented Programming at SUNY Geneseo Spring of 2019. This project simulates gravitational interactions between n numbers of bodies via python. Currently the code has examples for 3,4 and 5 body systems however the code can easily be extended to handle more or less. If one were to extend the code to handle more bodies beware of a confusing bug in numpy that isn't allowing values to be stored in a numpy array. I had to work around this issue by using variables such as c,d, and e to act as temporary storage and that fixed this issue. You would have to modify or add these temporary variables if you wanted a different number of bodies other than 3,4 or 5.

To run the simulation make sure you have the libraries such as vpython, numpy ect. and simply alter the initial position, velocity, and acceleration vectors.
