---
title: "Tonelli's Algorithm"
date: 2023-03-26T13:48:28+06:00
draft: false
author: "Masuda"
tags:
  - Storytime
  - Mathematics
  - Number theory
  - Tonelli's Algorithm
math: true
image: /images/tonellishanks.jpg
description: "A story about one of my Number theory quizes where we had to solve a square root mod problem using the Tonelli's algorithm (Not Tonelli Shank Algorithm)"
---
```[If you are here just for the algorithms, skip to them from the "table of content"]```

## <u>Storytime</u>
<hr>

This week I had a quiz on Number theory and as always i waited till the last day before the quiz to start studying for it. Our teacher for some sadistic reason, uses the [<span style="color:blue">MIT lecture notes</span>](https://ocw.mit.edu/courses/18-781-theory-of-numbers-spring-2012/pages/lecture-notes/) as the main "textbook" and also covers two entire lectures in a day. Mind you, we are not students of MIT with the giga brains but, just some struggling students in a private university which is known as the place saturated with rich dumb kids who couldn't get a chance in public Universities. TwT

The 15 minute quiz syllabus had 4 lectures and so I knew the teacher was going to give only 1 math problem and none of the other topics had any big math-to-do except for the Tonelli's algorithm. So, that's where i need to  start.

10:00 am : Woke up and while still in bed, started going through the MIT lecture notes. Got distracted like a thousand times but still I would like to say that I did put a lot of 'time and effort' to try and understand this supplimentary text. I searched on google and found everything about some other Tonelli Shank algorithm and nothing about Tonelli's (I didn't go for the second page of google though). 

6:00 pm : whaaaaaaaaah??!! DId I just waste the entire half day trying to understand just one part of one single lecture?? I started to calculate what my grade would be if I fail this quiz and ran a trailer in my head of me grinding for the finals to make up for the coming loss.

8:00 pm : (obviously I don't remember the exact times). Anyways, I wasn't gonna give up just then. This number theory teacher is one of those grade destroying faculties who listens to no pleadings regarding marks (He's a sweet guy otherwise). So, I havvee to atleast try get some numbers in this quiz if I wanted to avoid any C,D,E,F,G in my gradesheet (sorry, I am indeed your typical nerd). 

9:00 pm : I started looking at the Tonelli Shank Algorithm from wikipedia and solved an example with it. It was pretty easy and I had fun solving it with two of my friends on an audio call. One of them assured me that we won't need the algorithm in the lecture notes. (Meanwhile my bestfriend was grinding on previous chapters from a book he bought 7 years ago and was having some emotional nostalgic moments with it...)

Next Day (8:00 am) : I confessed to sir that I didn't understand Tonelli's algorithm and asked him to help by showing him the problem that we solved last night with the not-tonilli's-algorithm. He said he can't help at the moment and apologised for it TwT. And then he handed out the quiz question. 

Quiz time : It was the saaaammmmeeeee QUESTION that I showed him like a min agooo. Me and the friends I studied with the night before looked at eachother and started laughing. Sir also laughed because he too was shocked when I showed him that practice problem earlier and tried his best not to react. Fortunately for us, sir allowed us to use the other algorithm.

Anyways... I'm bad at writing and worse at trying to make it entertaining. That was the "storytime"... (Btw, the mentioned bestfriend wasn't able to answer the quiz fully but he didn't seem that dissappointed after it. So, all is gut.)

Below I tried to summerise both the algorithms since I myself couldn't find the second one anywhere on the google search's first page.
<hr>

## <u>Tonelli Shank Algorithm</u>
$$x \equiv a \ (mod \ p)$$

First check if 'a' is quadratic residue of p. i.e. if we get 1 using the Legendre symbol:
$$\left( \frac{a}{p}\right)=1$$
If not, break your pencil coz you made a mistake literally on the first step. There is no way the teacher gave you an equation with no solution. Otherwise, continue.
Define s, some odd number q  and like:
> $$p-1=2^s.q$$

Find a quadratic non-residue of p (their Legendre symbol value would be -1), by manually checking integers starting from 2 and call it z. Then initiate this variables:
> $$M=s$$ 
$$c=z^q$$
$$ t=a^q $$
$$ R=a^{{(q+1)}/{2}}(mod\ p)$$
$$b=1$$

Now we move onto the iterative part:

> If  *t = 0* , return:
$$ x = 0$$
Else if *t = 1* , return:
$$ x=\pm R $$
Else: Find a smallest integer *i* by checking values from 1 to less than M, such that,
$$t^{2^i}\equiv 1\ (mod \ p)$$
Update the variables,
$$b=c^{2^{M-i-1}}$$
$$M=i$$
$$c=b^2$$
$$t=tb^2$$
$$R=Rb$$

After each iteration, the value of M will decrease until t becomes 1 and we end the loop by returning the value *x*.
(Btw, all the large value variables are modded with p).

That's the end of Tonelli Shank Algorithm.

<hr>

## <u>Tonelli's Algorithm</u>
$$x \equiv a \ (mod \ p)$$
Read the MIT lecture notes lecture 11 for context and proof. I am just summerising the steps here.

Similar to Tonelli shank, confirm that the equation has solutions by getting 1 from the legendre symbol of a mod p.

Find a interger *n* such that it is a quadratic non-residue of mod p and define s, q and c as,
> $$p-1=2^s.t$$
$$c=n^t$$
$$A=a \text{ and } b=1$$

$$\text{You can calculate } c^{-1} \text{  (mod p) too for later use.} $$
Now for the looping part of the algorithm. Starting from k = 1 to s (exclusive). For each iteration, check if:
> $$A^{{(p-1)}/{2^{k+1}}} \equiv 1 \ (mod \ p)$$
If yes: *continue loop (k increases by 1)* \
If no: *update as below and loop (k increases by 1)*
$$A=A(c^{-1})^{2^{k}} \text{ and } b=bc^{2^{k-1}}$$ 

Stop the iterations when A becomes 1. Our answer will be,
> $$x=\pm \ b \ (mod \ p)$$

If loop ended at k=s and A is not 1 yet, our answer will be,
> $$x=\pm \ bA^{(t+1)/2} \ (mod \ p)$$
<hr>

Thanks for reading. hehe. I'm probably the only one reading... coz these are basically my notes. Good night, me.
<h4> <p style="text-align: center;">----------The End----------</p> <h4>



