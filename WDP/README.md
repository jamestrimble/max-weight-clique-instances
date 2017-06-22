# Winner Determination Problem Instances

The graphs in this directory are derived from winner determination problem instances from Lau, H.C., Goh, Y.G.: [_An intelligent brokering system to support multi-agent web-
based 4th-party logistics._](http://dx.doi.org/10.1109/TAI.2002.1180800) In: 14th IEEE International Conference on Tools with
Artificial Intelligence (ICTAI) 2002, 4-6 November 2002, Washington, DC, USA. p.
154. IEEE Computer Society (2002)

We include the first ten instances from each family, with vertices randomly permuted.

The bids in the original WDP instances are given to three decimal places.  We
used Java's `BigDecimal` class to multiply these by 1000 and convert them
precisely to integers.  Note that some previously-published work appears to
have converted the bids using a floating-point representation.  This explains
the very small differences between the maximum-weight cliques for our instances
and some published results.
