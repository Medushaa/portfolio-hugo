---
title: "RSA implementation in Python and Rust"
date: 2025-05-16
draft: false
author: "Masuda"
math: true
tags:
  - Number Theory
  - Computer Science
  - Cryptography
  - RSA
  - Rust
  - Mathematics
  - Euclidean Algorithm
  - Extended Euclidean Algorithm
  - Right to Left binary exponentiation method
# image: /images/crying.png
description: "Explaining the Maths behind RSA encyption and decryption by implementing it in Python and Rust"
toc: false
---

RSA is an ancient Public-key encryption algorithm used to safely pass secret message from sender to receiver without the risk of anyone else having unauthorized access to the content of the message. It makes use of 2 asymmetric keys: **Public key** that is shared with everyone to encrypt a message and **Private key** that is kept secret to the user to decrypt messages addressed to him.

The key generation step starts by randomly picking two prime numbers p and q. And then calculate these next integers from it:
$$ n = p \times q $$
$$ r = (p - 1)(q -1)$$
$$ e = \text{a value relatively prime to }r$$
$$ d = e^{-1}\ (\text{mod }\ r)$$

Public key: (n, e), Private key: (n, d)

Encryption of the message (`msg` is an integer) with the public key, gives the ciphertext (`ct`). Decryption with the private key, gives the message back. The proof for why it works is left as an exercise for the reader.

$$ ct = \text{msg}^e\ (\text{mod }\ r) $$
$$ \text{msg} = ct^d\ (\text{mod }\ r) $$

For it to work, n has to be larger than `msg`. Otherwise the number will be wrapped, giving a wrong decrypted message.


# RSA implementation in Python
First I used Python because it'll be easier. Just put the equations as is, and done! 

Starting with a user generating his key pair, before any transactions are initiated addressed to him:
```Python
def generate_rsa_keys(): 
    p = sympy.randprime(300, 10000)
    q = sympy.randprime(300, 10000)
    n = p * q  
    r = (p - 1) * (q - 1) 
    for i in range(3, r):
        if gcd(i, r) == 1: 
            e = i
            break
    d = pow(e, -1, r) 

    return n, e, d
```
The public key `(n, e)` is made public to everyone. A sender will use this to encrypt each letter in the message with the above equations. Once received, only the the owner of this key will be able to decrypt the letters with his private key `(n, d)` and concat them to reform the message.

```Python
def rsa_encrypt(n: int, e: int, txt: str): #by sender 
    ct = [pow(ord(c), e, n) for c in txt] #list for each letter
    print(f"Encrypted ciphertext: {ct}")
    return ct

def rsa_decrypt(n: int, d: int, ct: int): #by receiver
    mes = ''.join(chr(pow(c, d, n)) for c in ct)
    print(f"Decrypted message: {mes}")
    return mes
```
Example:
```Python
n, e, d = generate_rsa_keys()
ct = rsa_encrypt(n, e, "meow") #list
rsa_decrypt(n, d, ct)
```
Output:
```
Private key (n,e) = (46684657,7)                                  
Public key (n,d) = (46684657, 26668903)
Encrypted ciphertext: [7027600, 26231322, 8679471, 30302896]
Decrypted message: meow
```
Doneeeee!

# RSA implementation in Rust
The above was pretty slow despite the key size being extremely small. Also we directly used the built-in functions like `pow`, `gcd` and `randprime`, which hide important algorithms that we could explore.

So, lets do all that in Rust.

### GCD using Euclidean Algorithm
GCD or the **Greatest Common Divisor** of two integers, `gcd(a, b)` can be calculated using a very cool simple algorithm called the **Euclidean Algorithm**. The steps are:
1. If `a > b`, switch `a` and `b`
2. If `a = 0`, return `b`
3. Since `a > 0`, write `b = a * q + r`,  with 0 ≤ r < a. (This `r` is basically `r = b % a`). Replace `(a, b)` with `(r, a)` and repeat. 

Implementing this in Rust:
```Rust
fn gcd(mut a: u64, mut b: u64) -> u64 {
    assert!(a != 0 && b != 0); //terminates if n or m is 0
    while b != 0 {
        if b < a { //swap
            let t = b; 
            b = a;
            a = t;
        }
        b = b % a;
    }
    a 
}
```


### Extended Euclidean Algorithm
**Extended Euclidean Algorithm** can efficiently find even the coefficients of the gcd diaphantine equation: `ax + by = gcd(a, b)`.


It can be used to calculate the multiplicative inverse: $$a^{-1} \ \ (\text{mod}\ \ m)$$

<div style="text-align: center;">
  <img src="\images\extended-eucleadian-algo.png" alt="image description" style="max-width: 55%; height: auto; margin-bottom: 1rem;">
</div>

where, `q` is the quotient of dividing `r` with `r'`, (`q = r // r'`),
and the next `r'` value is the reminder, (`r - q * r'`).

If `t < 0` , do `t = t + n`.

Return `t'` , when `r' = 1` .

Implementing this in Rust:
```Rust
fn mod_inverse(a: u64, m: u64) -> u64 {
    let (mut t, mut new_t) = (0_i64, 1_i64);
    let (mut r, mut new_r) = (m as i64, a as i64);

    while new_r != 0 {
        let q = r / new_r;
        let temp_t = t - q * new_t;
        let temp_r = r - q * new_r;
        t = new_t;
        new_t = temp_t;
        r = new_r;
        new_r = temp_r;
    }
    if r > 1 { return 0 }; // No inverse
    if t < 0 { t += m as i64 };

    t as u64
}
```

### Checking Prime
This code simply brute forces dividing the number with every number from 2 to it's square. If any of them is divisible, the number is not a prime.
```Rust
fn is_prime(num: u64) -> bool {
    if num <= 1 {
        return false; 
    }
    for i in 2..=(num as f64).sqrt() as u64 {
        if num % i == 0 {
            return false; // divisible
        }
    }   
    true 
}
```
This is extremely inefficient if the number becomes huge, which is required for RSA. Hence, the real RSA uses probabilistic tests for this.

### Algorithm for Modular Exponents
To efficiently calulate `(num^exp % modulus)`, I used the **Right to Left binary exponentiation method**, which works by considering the binary representation of the exponent (`exp`).
1. Start by setting the answer to 1 and reducing num to `num % modulus`.
2. Iterate through each bit of exp from right to left by right shifting it (i.e. divide by 2). If the current bit is 1, update: `ans = (ans * num) % modulus`. In every iteration, square the num, i.e. `(num * num) % modulus`.
3. Repeat until all bits of `exp` has been iterated through.
```Rust
fn modular_exponent(mut num:u64 ,mut exp:u64 , modulus:u64) -> u64{
    let mut ans = 1;
    if exp <= 0 { return 1; }
    loop {
        if exp == 1 { return (ans * num) % modulus; }
        if exp & 1 == 0 { //binary check for if exp is even
            num = (num * num) % modulus;
            exp >>= 1; //right shift to next bit. exp=exp>>1
            continue;
        }
        else {
            ans = (ans * num) % modulus;
            exp -= 1;
        }
    }
}
```

### Generating the two keys
Similar to our implementation with Python, we'll randomly pick the two prime numbers p and q, and then calculate n, r, e (public key) and d (private key) using the above algorithms.
```Rust
fn generate_rsa_keys() -> Keys {
    let mut rng = rand::thread_rng();
    let mut p: u64;
    let mut q: u64;
    loop { 
        p = rng.gen_range(300..10000);
        if is_prime(p) {
            break;
        }
    }
    loop {
        q = rng.gen_range(300..10000);
        if is_prime(q) {
            break;
        }
    }
    let n: u64 = p * q; //biger than msg
    let r: u64 = (p - 1) * (q - 1);
    let mut e: u64 = 3;
    for i in 3..r {
        if gcd(i, r) == 1 {
            e = i;
            break;
        }
    }
    let d = mod_inverse(e, r); 

    Keys { n: (n), e: (e), d: (d) }
}
```

### Encryprtion and Decryption
The sender can now use the receiver's public key to encrypt a message (`txt`) into a list of encrypted numbers representing each letter in the message.
```Rust
fn rsa_encrypt(n: u64, e: u64, txt: String) -> Vec<u64> {
    let mut ct = Vec::new();
    for l in txt.chars() { 
        ct.push(modular_exponent((l as u8) as u64, e, n));
    }
    println!("Encrypted message: {:?}", ct);
    ct
}
```

Once the receiver, receives this encrypted message, they will try to decrypt it with their private key and retrive the original message. A small helper function was used to convert the u64 to u8 ascii, before making it a char.

```Rust
fn convert_u64_to_u8(x: u64) -> u8 {
    if x <= u8::MAX as u64 { //is it bigger than u8?
        x as u8
    } else {
        panic!("u64 to u8 failed");
    }
}

fn rsa_decrypt(n: u64, d: u64, ct: Vec<u64>) -> String {
    let mut msg: Vec<char> = Vec::new();
    for i in ct {
        let ascii = modular_exponent(i, d, n);
        msg.push(convert_u64_to_u8(ascii) as char);
    }
    msg.iter().collect()
}
```

## Summary
This was a very silly way of implementing the RSA with u64 since it can be super easily broken. Rust's BigInt type instead of u64 could have been a better fit, also having built-in support for the algorithms being used. Regardless, I wanted to do it to get away with using simple naive algorithms like `is_prime(num)`.

Here is the github link with the code for this: [[<span style="color:#00B5E2">link</span>]](https://github.com/Medushaa/RSA-in-u64-Rust)