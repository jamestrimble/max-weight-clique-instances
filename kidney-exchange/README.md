# Kidney Exchange Instances

We derived these instances from the first 100 of John Dickerson's
[kidney exchange instances](http://www.preflib.org/data/matching/kidney/)
on PrefLib.  Dickerson's code for generating these instances is
[available on GitHub](https://github.com/JohnDickerson/KidneyExchange/blob/master/src/edu/cmu/cs/dickerson/kpd/structure/generator/SaidmanPoolGenerator.java).  
This is based on the generator described in
S. L. Saidman, Alvin Roth, Tayfun Sonmez, Utku Unver, Frank Delmonico:
_Increasing the Opportunity of Live Kidney Donation by Matching for Two and Three Way Exchanges,_
**Transplantation**, Volume 81, Number 5, March 15, 2006.

The instances in the `kidney_mwc` directory can be re-created by
downloading http://www.preflib.org/data/matching/kidney/kidney.zip
into the scripts directory, and running `convert.sh`.  The instances
in the `kidney_mwc-randomly-permuted` directory are the same instances
with the vertices in random order; these are the instances we used in
the paper.

