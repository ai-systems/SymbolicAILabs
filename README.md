# Symoblic AI Labs 
## Steel Example
Original Code Obtained from: https://github.com/johntrimble/foil-python

To run the code you create a folder. In our case the folder `example/`. It has three files.
- `facts.ilp` : contains the facts
- `negative.ilp`: contains the negative examples
- `positive.ilp`: contains the positive examples

You can run the code by:
```
python src/ilp.py example
```

### Note
We have restricted the facts predicates to arity 1 and the iron producing predicates should adhere to the following rules:
```
Ferrite(x,y) -> Temperature(x),Carbon(y)
```

This is a code in progress. Please raise issues and suggestions to improve it
