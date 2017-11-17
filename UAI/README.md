# UAI Competition 2014 Instances

These files encode the WCSP instances converted from max-a-posteriori (MAP) problem on UAI
Competition 2014 PR and MMAP benchmark instances. They are the constraint composite graphs (CCGs) of
these WCSP instances.

The original UAI instances is at http://www.hlt.utdallas.edu/~vgogate/uai14-competition/index.html

These instances are produced according to

    Hong Xu, Sven Koenig, and T. K. Satish Kumar. A constraint composite graph-based ILP encoding of the
    Boolean weighted CSP. In Proceedings of the 23rd International Conference on Principles and Practice
    of Constraint Programming (CP), 630–638. 2017. doi:10.1007/978-3-319-66158-2_40.

    Hong Xu, T. K. Satish Kumar, and Sven Koenig. The Nemhauser-Trotter reduction and lifted message
    passing for the weighted CSP. In Proceedings of the 14th International Conference on Integration of
    Artificial Intelligence and Operations Research Techniques in Constraint Programming (CPAIOR),
    387–402. 2017. doi:10.1007/978-3-319-59776-8_31.

    T. K. Satish Kumar. A Framework for Hybrid Tractability Results in Boolean Weighted Constraint
    Satisfaction Problems. Proceedings of the 14th International Conference on Principles and Practice
    of Constraint Programming (CP), 282–297. 2008. doi:10.1007/978-3-540-85958-1_19

Please note that you should compute the maximum weighted cliques on the complement of these
instances (connecting/disconnecting two vertices if they are nonadjacent/adjacent). In other words,
you should compute the minimum weighted vertex covers on these instances.
