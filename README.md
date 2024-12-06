# INTRODUCTION TO CRYPTOGRAPHY PROJECT

## Project Description

This project is a simple, GUI-based application that allows users to send messages to one another that are encrypted for security during communication. Using a combination of symmetric and asymmetric encryption (more specifically, the AES cipher and RSA algorithm), the application allows users to send messages to one another that are encrypted and decrypted using a shared key.

## Requirements

The project requires the following libraries to be installed:
- `PyCryptodome`
- `Tkinter`

## How to Use

To run the application, simply run the *main.py* file with either "server" or "client" as an argument. The server will need to be running before the client can connect to it. From there, the client can send messages to the server, which will then be decrypted and displayed in the server's window.
