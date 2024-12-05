import socket
import sys
import json

# Substitution Box
sBox=[0x9,0x4,0xa,0xb,0xd,0x1,0x8,0x5,
      0x6,0x2,0x0,0x3,0xc,0xe,0xf,0x7]

# Round Keys
w=[None]*6

# Function to multiply two polynomials in GF(2^4),i.e, x^4+x+1
def mult(p1,p2):
    p=0
    while p2:
        if p2 & 0b1:
            p^=p1
        p1<<=1
        if p1 & 0b10000:
            p1^= 0b11
        p2 >>=1
    return p & 0b1111

# Function to convert integer into state vector
def IntToVec(n):
    return [n>>12,(n>>4) & 0xf, (n>>8) & 0xf, n & 0xf]

# Function to convert state vector to integer
def VecToInt(n):
    return (n[0]<<12)+(n[2]<<8)+(n[1]<<4)+n[3]
 
# Adding two keys in GF(2^4)
def addKey(s1,s2):
    return [i^j for i,j in zip(s1,s2)]

# Function used as Nibble Substitution
def NibSub(sbox,s):
    return [sbox[e] for e in s]

# Function to shift rowws of state
def shiftRows(s):
    return [s[0],s[1],s[3],s[2]]

# Swapping each nibble and substituting it using s-box
def sub2Nib(b):
    return sBox[b >>4]+(sBox[b & 0x0f]<<4)

# To generate the keys for encryption and decryption
def keyExp(key):
    Rcon1,Rcon2 = 0b10000000, 0b00110000
    w[0]=(key & 0xff00) >> 8
    w[1]=key & 0x00ff
    w[2]=w[0]^Rcon1^sub2Nib(w[1])
    w[3]=w[2]^w[1]
    w[4]=w[2]^Rcon2^sub2Nib(w[3])
    w[5]=w[4]^w[3]

# Function to mix columns according to the encryption method
def mixCol(s):
    return [s[0] ^ mult(4,s[2]), s[1] ^ mult(4,s[3]), s[2]^mult(4,s[0]), s[3]^ mult(4,s[1])]

# Function to encrypt the plaintext
def encrypt(data,key):
    keyExp(key)
    state=IntToVec(((w[0]<<8)+w[1])^data)
    state=mixCol(shiftRows(NibSub(sBox,state)))
    state= addKey(IntToVec((w[2]<< 8)+w[3]),state)
    state= shiftRows(NibSub(sBox,state))
    return VecToInt(addKey(IntToVec( (w[4] << 8) + w[5]),state))
