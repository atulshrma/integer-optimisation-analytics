# integer-optimisation-analytics

This repo builds a simple FastAPI webserver exposing 2 algorithms for solving an integer optimisation problem.

### Part I: Optimization Algorithms
Assume a function $f(x)=x^2$. Assume a set of $K$ lists, $X_{1},X_{2},...X_{K}$, where each list $X_{i}$ has $N_{i}$ elements. So, the lists do not necessarily have the same lengths. The function that needs to be maximized is $R = (\sum_{k}f(x_{k}))\mod M$, where each $x_{i}$ is one element picked from list $X_{i}$. For this assignment you can assume that all the elements from the lists are larger or equal to $1$ or smaller or equal to $10^9$. That is, $1 <= x_{i,k} <= 10^9$.

To give an example, assume that we have a 3 lists: `([5, 4], [7, 8, 9], [5, 7, 8, 9, 10])`, and that $M=40$. Then the maximum value of $R$ is 37, and is achieved by choosing 4 from the first list, 9 from the second and 10 from the third list: $37=(4^2+9^2+10^2)\mod 40$.

### Part II: Application
This is a FastAPI webserver that implements the functionalities developed in Part I.

You can run the application locally using the provided Dockerfile using the commands
```sh
$ docker built -t interger-optimisation .
$ docker run -p 80:80 integer-optimisation
```

To view the API documentation navigate to http://127.0.0.1/docs in your browser.
