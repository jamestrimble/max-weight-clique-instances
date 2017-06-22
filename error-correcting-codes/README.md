# Error Correcting Codes Instances

These files encode instances from a problem in coding theory described in Section 4 of
Östergård, P.R.J.: _A new algorithm for the maximum-weight clique problem._ Nord. J. Comput. 8(4), 424–436 (2001).

Östergård's original instances are no longer readily available online.
(One of the instances can be found in the [Internet Archive](web.archive.org/web/20001004150639/http://www.tcs.hut.fi:80/~pat/graphs/11-4-4.gz).) We
have written a program to reproduce the instances, based on the description in the
paper.  We verified the correctness of our instances by checking that the
number of vertices and the weight of the optimal solution agree with the
values in the paper.

Our instance files, with vertices randomly shuffled, are in the
`instances-randomly-permuted` directory.  Our generator program (which does not
shuffle vertices) is in the `generate-error-correcting-code-instances`
directory.

