#LASO Bill Fetch

Engine to get bills from different APIs for different States.

# Database Tables
## In App DB
* state : Contains apimethod and options for api use (relevant paramaters)
* fetchlog : Results of each fetch

# Fetch DB
Different schema for internals of the fetch tool.


# Functionality (requirements)
* Splits update task into pieces
* Prioritizes pieces
* Can be paused and resumed
* Updates relevant app data
* Can scale across hosts easily using DB
* Good test coverage

# Usage
(todo)
