---
title: "Fortran_Tales = .gone_wrong."
date: 2023-11-06
draft: false
author: "Masuda"
math: true
tags:
  - Fortran
  - BracU
  - Numerical analysis
image: /images/crying.png
description: "Sharing some tales and code snippets form my Fortran classes at my University"
toc: 
---


## <u>Lab 1 (Pascal Triangle)</u>
Bad bad. It was bad. It was soooo bad that I don't even remember anyth from Lab 1, except "Hello world"? Here's a [<span style="color:#00B5E2">link</span>](https://fortran-lang.org/learn/quickstart/) to a nice introductory tutorial on Fortran if you too got unlucky enough in your undergrad life.

And then we were given an home task to ouput a Pascal Triangle (using Binomial coefficients):
```f90 
program pascal
    implicit none
    integer::i,j,c
    do i=1,7
        c = 1
        do j=1,i
            write(*, "(I10)", advance="no") c
            c = (c * (i - j)) / j
        end do
        write(*,*)
    end do
end program
```
Output:
```
    1
    1         1
    1         2         1
    1         3         3         1
    1         4         6         4         1
    1         5        10        10         5         1
    1         6        15        20        15         6         1
```
</br>

## <u>Lab 2 (Arrays)</u>
Lab 1 seemed fun and easy. Not bad. So, in lab 2 I was pretty chilled and ate cake in the first 1 hour of the class. And then the tisar gave us a classwork. This task would have taken me much less than what I took if I weren't high on suger (normal cake suger).

Question: (i don't remember the exact one. It was sth like) Given an array, check all its subarrays. If their sum is 0, print 0, or 1 otherwise.
<!-- ```f90 {.myclass linenos=table,linenostart=1,linenos=false} -->
```f90
program array
    implicit none
    integer :: arr1(7) = [1,3,2,-5,-3,1,5]
    integer :: i, j, res
    do i = 1, 7
        do j = i, 7
            res = sub_arr(arr1, i, j)
            if( res == 0 ) then
                write(*,*) 0
            else
                write(*,*) 1
            end if
        end do
    end do
contains
    function sub_arr(arr1, m, n) result(sum)
        implicit none
        integer :: a, m, n, sum, arr1(7)
        sum = 0
        do a = m, n
            sum = sum + arr1(a)
        end do
    end function sub_arr
end program
```
</br>

## <u>Lab 3 (Eular Method)</u>
Solve the 2nd Order ODE with h=0.1 and t range [0,2]:
$$ \frac{d^2x}{dt^2} + 25x = 0 , \ \ \  x(0)=1, \ \ \  x^′(0)=0$$
Convert this to a system of two 1st order ODE:
$$x^′=z , \ \ \ z^′=-25x , \ \ \   x(0)=1, \ \ \  z(0)=0$$
Code:
```f90
program euler
    implicit none
    real :: t(100), x(100), z(100), e(100)
    real :: a=0.0, b=2.0, x0=1.0, z0=0.0, h=0.1 ![a,b]
    real :: f, g, act !functions
    integer :: i, n
    n = (b - a)/h
    x(1) = x0
    z(1) = z0
    e(1) = 0.0
    do i = 1, n + 1
       t(i) = a + (i - 1)*h 
    end do
 
    do i = 1, n
        x(i + 1) = x(i) + h*f(t(i), x(i), z(i)) ! x soln
        z(i + 1) = z(i) + h*g(t(i), x(i), z(i)) ! next z
        e(i + 1) = abs(x(i + 1) - act(t(i + 1))) ! error
    end do
    
    write (*, *)"      t_i        |       y_i        |     actual_i     |     error_i"
    write (*, *)"========================================================================"
    do i = 1, n + 1
       write (*, *) t(i),'|', x(i),'|', act(t(i)),'|', e(i)
    end do
 end program euler

 ! x'=z=f(t,x,z)
 function f(t, x, z)
    implicit none
    real :: f, t, x, z
    f = z 
 end function f

! z'=-25x=g(t,x,z)
 function g(t, x, z)
    implicit none
    real :: g, t, x, z
    g = -25 * x   
 end function g
 
 ! actual solution func of the IVP (to get error)
 function act(t)
    implicit none
    real :: act, t
    act = cos(5*t)
 end function act
 ```
 Output:
 ```
        t_i        |       y_i        |     actual_i     |     error_i
 ========================================================================
   0.00000000     |   1.00000000     |   1.00000000     |   0.00000000    
  0.100000001     |   1.00000000     |  0.877582550     |  0.122417450    
  0.200000003     |  0.750000000     |  0.540302277     |  0.209697723    
  0.300000012     |  0.250000000     |   7.07371980E-02 |  0.179262802    
  0.400000006     | -0.437500000     | -0.416146845     |   2.13531554E-02
  0.500000000     |  -1.18750000     | -0.801143587     |  0.386356413    
  0.600000024     |  -1.82812500     | -0.989992499     |  0.838132501    
  0.699999988     |  -2.17187500     | -0.936456680     |   1.23541832    
  0.800000012     |  -2.05859375     | -0.653643608     |   1.40495014    
  0.900000036     |  -1.40234375     | -0.210795805     |   1.19154799    
   1.00000000     | -0.231445312     |  0.283662200     |  0.515107512    
   1.10000002     |   1.29003906     |  0.708669782     |  0.581369281    
   1.20000005     |   2.86938477     |  0.960170269     |   1.90921450    
   1.30000007     |   4.12622070     |  0.976587534     |   3.14963317    
   1.39999998     |   4.66571045     |  0.753902256     |   3.91180825    
   1.50000000     |   4.17364502     |  0.346635312     |   3.82700968    
   1.60000002     |   2.51515198     | -0.145500034     |   2.66065192    
   1.70000005     | -0.186752319     | -0.602011919     |  0.415259600
   1.80000007     |  -3.51744461     | -0.911130250     |   2.60631442
   1.89999998     |  -6.80144882     | -0.997172177     |   5.80427647
   2.00000000     |  -9.20609188     | -0.839071512     |   8.36702061
```

For Modified Eular method, it's the same code except for, replace the `do` loop where the main iteration is going, with this (don't forget to initiate the added variables):

 ```f90
do i = 1, n
    x_intm = x(i) + h * f(t(i), x(i), z(i))
    z_intm = z(i) + h * g(t(i), x(i), z(i))
    x(i + 1) = x(i) + (h/2) * (f(t(i), x(i), z(i)) + f(t(i+1), x_intm, z_intm))
    z(i + 1) = z(i) + (h/2) * (g(t(i), x(i), z(i)) + g(t(i+1), x_intm, z_intm))
end do
 ```
</br>

## <u>Lab 4 (Runge Kutta 4 Method)</u>
Just replace the iteration block with:
```f90
do i = 1, n
    k1_x = h*f(t(i), x(i), z(i))
    k1_z = h*g(t(i), x(i), z(i))
    k2_x = h*f(t(i) + (h/2), x(i) + (k1_x/2), z(i) + (k1_z/2))
    k2_z = h*g(t(i) + (h/2), x(i) + (k1_x/2), z(i) + (k1_z/2))
    k3_x = h*f(t(i) + (h/2), x(i) + (k2_x/2), z(i) + (k2_z/2))
    k3_z = h*g(t(i) + (h/2), x(i) + (k2_x/2), z(i) + (k2_z/2))
    k4_x = h*f(t(i) + h, x(i) + k3_x, z(i) + k3_z)
    k4_z = h*g(t(i) + h, x(i) + k3_x, z(i) + k3_z)

    x(i + 1) = x(i) + (k1_x + 2*k2_x + 2*k3_x + k4_x)/6
    z(i + 1) = z(i) + (k1_z + 2*k2_z + 2*k3_z + k4_z)/6
end do
```
A funny thing happened here. My friend also did the code and had very different answers and we were sooo confused. And then we found the culprit:
```f90 
x(i + 1) = x(i) + (k1_x + 2*k2_x + 2*k3_x + k4_x)/6
! Output:  2.00000000  | -0.839878798  | -0.839071512  |  8.07285309E-04
```
```f90 
x(i + 1) = x(i) + (1/6)*(k1_x + 2*k2_x + 2*k3_x + k4_x)
! Output:  2.00000000  |  1.00000000   | -0.839071512  |  1.83907151
```
See the difference? XDDD The entire y_i row became 1 for this. Have fun.

</br>

## <u>Midterm (3rd oder ODE) </u>
Solve this 3rd order differential equation with Modified Eular and RK4:
$$\frac{d^3y}{dx^3}-\frac{d^2y}{dx^2}\sin(x)+2\frac{dy}{dx} − xy = \cos(x)$$
$$ y(0) = 1,\ \ \   y^′(0) = −2, \ \ \   y^{′′}(0) = 3$$

Convert this into a system of three 1st order ODEs:
$$ y^′ = p$$
$$ p^′ = q$$
$$ q^′ = q\cdot \sin(x) - 2p +xy + \cos(x)$$
$$ y(0) = 1,\ \ \  p(0) = −2, \ \ \   q(0) = 3$$
And then use the methods above and alter some things to fit the 3 equations. Byeee.


<br>

<br>

<h4> <p style="text-align: center;">----------The End----------</p> <h4>
