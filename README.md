# Introduction

Tracery Builder makes managing Tracery projects easier by allowing you to easily separate text productions into separate files. The first release is compatible with most Tracery files (no saving data yet!).

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

The first requires Tracery Builder, since it's missing some references. Note that #planet# and #event:celestial# aren't found in that file. Just run:

    > tbuild star_system.json star_system_out.json
    
and Tracery Builder will produce the following output file:

```json   
star_system_out.json

{
  "origin": ["#star#", "#planet#", "#events:celestial#"],
  "star": ["a big star", "a little star"],
  "planet": ["a big planet", "a little planet"],
  "events:celestial": ["cosmic shower", "moon explosion"]
}
```

# TODO

* preserve data saves
