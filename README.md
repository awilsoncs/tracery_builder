# Introduction

Tiny Tracery Compiler (TTC) is a JSON preprocessor that makes developing Tracery projects easier.

Let's look at a few json files.
  
```json
star_system.json

{
   "origin": ["#star#", "#planet#", "#events:celestial#"],
   "star": ["a big star", "a little star"]
}

planet.json

{
   "origin": ["a big planet", "a little planet"]
}

events.json

{
    "celestial": ["cosmic shower", "moon explosion"]
}
```

The first requires TTC, since it's missing some references. Note that #planet# and #event:celestial# aren't found in that file. Just run:

    > ttc star_system.json star_system_out.json
    
and TTC will produce the following output file:

```json   
star_system_out.json

{
  "origin": ["#star#", "#planet#", "#events:celestial#"],
  "star": ["a big star", "a little star"],
  "planet": ["a big planet", "a little planet"],
  "events:celestial": ["cosmic shower", "moon explosion"]
}
```

# Extension Macros
Some things are a real pain to write in bare JSON. TTC provides some convenience methods to make these tasks easier.

## Production Weights
While not a proper macro, TTC will perform the following transformation:
```json
input:
{
    "origin": [
      [5, "highly weighted item"],
      [2, "medium weighted item"],
      "unweighted item"
    ]
}

output:
{
  "origin": [
    "highly weighted item",
    "highly weighted item",
    "highly weighted item",
    "highly weighted item",
    "highly weighted item",
    "medium weighted item",
    "medium weighted item",
    "unweighted item"
  ]
}

```

## Dice Rolls
The ! operator tells TTC that the following is a macro to expand. In this case, !dice allows the generator to properly simulate a dice roll (given in NdS notation).

```json
input:
{
    "origin": "#dice(2d4)#"
}

output:
{
    "origin": ["#basic_test:dice(2d4#"],
    "basic_test": ["#basic_test:dice(2d4)#"],
    "basic_test:dice(2d4)": [
        "2",
        "3",
        "4",
        "5",
        "3",
        "4",
        "5",
        "6",
        "4",
        "5",
        "6",
        "7",
        "5",
        "6",
        "7",
        "8"
    ]
}
```