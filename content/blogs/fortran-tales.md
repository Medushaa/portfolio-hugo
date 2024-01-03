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
Lab 1 seemed fun and easy. Not bad. So, in lab 2 I was pretty chilled and ate cake in the first 1 hour of the class. And then the tisar gave us a classwork. This task would have taken me much less than what I took if I weren't high on sugar (normal cake sugar).

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

## <u>Lab 3 (Euler Method)</u>
Euler Method formula for 1st Order ODE:
$$ \frac{dy}{dx}=f(x,y), \ \ \ y(x_0)=y_0$$
$$\text{Iterate: }\ \ \hat{y}_{i+1}=y_i+h\cdot f(x_i,y_i)$$

Our task was to solve a 2nd Order ODE with h=0.1 and t range [0,2]:
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
        t_i       |       y_i        |     actual_i     |     error_i
 ========================================================================
   0.00000000     |   1.00000000     |  1.000000000     |  0.000000000    
   0.10000001     |   1.00000000     |  0.877582550     |  0.122417450    
   0.20000003     |   0.75000000     |  0.540302277     |  0.209697723    
    ...
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
The general formula for Modified Eular Method for 1st Order ODE:

$$ \frac{dy}{dx}=f(x,y), \ \ \ y(x_0)=y_0$$

$$ y_{i+1}=y_i+h\cdot f(x_i,y_i)$$

$$ y_{i+1}=y_i + \frac{h}{2}(f(x_i,y_i)+f(x_{i+1},y_{i+1})) $$

The last two lines are iterated to get each approximated point in the solution curve.


</br>

## <u>Lab 4 (Runge Kutta 4 Method)</u>
The general formula for 4th order Runge Kutta method for 1st Order ODE:

$$ K_1=h\cdot f(x_i,y_i) $$

$$ K_2=h\cdot f \left( x_i + \frac{h}{2}, \ y_i+\frac{K_1}{2}\right)  $$

$$ K_3=h\cdot f \left( x_i + \frac{h}{2}, \ y_i+\frac{K_2}{2}\right)  $$

$$ K_4=h\cdot f \left( x_i + h, \ y_i+K_3\right)  $$

$$ y_{i+1}=y_i+ \frac{1}{6} (K_1+2K_2 +2K_3 +K_4)  $$

For the RK4 code on the same 2nd order ODE that we solved in Lab 3, we'll just replace the iteration block with:
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
Question: Solve this 3rd order differential equation with Modified Eular and RK4:
$$\frac{d^3y}{dx^3}-\frac{d^2y}{dx^2}\sin(x)+2\frac{dy}{dx} − xy = \cos(x)$$
$$ y(0) = 1,\ \ \   y^′(0) = −2, \ \ \   y^{′′}(0) = 3$$

First convert this into a system of three 1st order ODEs:
$$ y^′ = p$$
$$ p^′ = q$$
$$ q^′ = q\cdot \sin(x) - 2p +xy + \cos(x)$$
$$ y(0) = 1,\ \ \  p(0) = −2, \ \ \   q(0) = 3$$
And then use the methods above and alter some things to fit the 3 equations. Byeee.


<br>

<br>

<h4> <p style="text-align: center;">----------The End----------</p> <h4>
