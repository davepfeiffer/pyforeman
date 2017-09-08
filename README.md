# Notice

This project is under construction and untested. The work in here will not have
a high level of polish or documentation. The project will likely see some
improvement and the documentation will come once the core features are settled.

# Overview

Foreman is an extremely simple python3 package for writing or generating build/test scripts.

It also uses a cute construction site analogy for building programs.

# Motivation

For one of my classes I am not allowed to use Makefiles, only Bash or BAT scripts. Because I don't feel like actually writing bash/BAT scripts by hand, I'm writing this project as a framework to make it look like I did.

# Structure

The project structure consists of the following elements:

- Blueprints

- Builders

- The Foreman

- The Inspector

## Blueprints

These are the dependancy structure of your project

## Builders

Builders are where all the work happens. They build blueprints.

The builders are llambda functions to be written by the package user.

Their signature is:

`environment -> name -> materials -> product`

The environment is the set of all available resources.

The name is blueprint's . . .

## The Foreman

The foreman contains the functions to generate your scripts

## The Inspector

The inspector will contain the functions to build/run your tests
