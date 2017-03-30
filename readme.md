# ApiRepl

## What it is
If you want API data copied to your database, the workers should fetch for you elastically.

## Setup
### Database Requirement
use schema.sql to create a database, and load it with the types of information you need
### Subclass BaseWorker
see samples/usage.py for an example.
Create an api method and save method for your workflow by subclassing BaseWorker.

## Functionality (requirements)
* Splits update task into pieces
* Prioritizes pieces
* Can be paused and resumed
* Can scale across hosts easily using DB
* Good test coverage (soon :) )

## Usage
See Sample folder
