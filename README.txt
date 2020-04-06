
(The following is a DeTeX of Nathan's proposal .tex file,
for readability on the github page)


Public Images as Secure Group Messages

       Project Proposal

       COMP 5610 - Computer  Network Security I

       Spring 2020
       

        Cook, Charles

        charlescook@student.uml.edu
        
        Finegan, Conor

        conorfinegan@student.uml.edu
        
        Percival, Nathan

        nathanpercival@student.uml.edu
        
March 4, 2020






Concept
Sometimes there is a need to pass secret messages using insecure systems.   One common, but insecure system is the use of online message forums such as Reddit, 4chan, Twitter or Facebook.   These systems allow message to be shared easily but there is no system provided to allow direct, secure communication to a group via these public forums.   Most of these systems do allow the posting of images. This project will develop a process and proof of concept software to use images to send and received secured communications. 

For this project, it is assumed that there a group of people wishing to communicate securely and that they want to all be able to directly read the message without the need for each individual to have access to the a shared key.   Additionally, the key to decrypt any message should not be usable to decrypt any other message.  To accomplish this, the system will generate a unique key for each message in a repeatable way.   The system will also provide verification that the message was posted by the user who claims to be posting the message.
 
The system will use a server as the gateway for this information.  All communications with the server will use public keys that will be exchanged using a secure process outside the actual process of messaging.  The system will use RSA for the encryption of short message between clients and the server and will use AES to encrypt the message being sent.   In addtion, the use of RSA will allow for the message authentication.   Per message keys will be derived from a master group key, the same size as the AES key that will be permuted by the sender's public key, the timestamp of the message and the nonce value.


Proposed Component Design
Assume there is a sending user, , with RSA public key / Private key pair 

Assume there is a receiving user, , with RSA public key / Private key pair 

For each group, ,  there exist a unique master symmetric encryption exists  held by the security server.

For each group , the server has the public keys  for users authorized to access the group.

Let  be the message to be sent.

Encryption Operation (by user )

  Create a time-stamp  for the message.
  Create a nonce  for the message.
  Create key request 
  Encrypt Request using Private Key 
  Send Request  and  to Server
  Receive Response  for server
  Decrypt 
  Encrypt 
  Create encrypted version of user id, time-stamp, and nonce 
  Create image from  and 
  Post image


Decryption Operation (by user )

  Retrieve Image
  Decode image to  and 
  Using  from known source, 
  Verify given  matches the  found within  to ensure senders identity
  Create key request  to decrypt message
  Encrypt Request using Private Key 
  Send Request  and  to Server
  Receive Response  for server
  Decrypt 
  Decrypt 


Server Key Operation

  Verify user  belongs to Group 
  Decrypt request using  on server 
  Permute  using  and  to get  as the encryption key for this image. (using a combination XOR, shifts, etc)
  Encrypt 
  Send  to requesting system


Implementation Plans

  Complete as Proof of concept - do not worry about over the wire transmission.  
  Encryption / Decryption program passes message to server by command line call to server application
  Live implementation

   



