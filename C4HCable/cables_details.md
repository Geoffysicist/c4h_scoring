
Cable order:

[pl2303 usb rs232 to 3.5mm serial cable for replacing rs232 db9 to 3.5mm jack adapter for intel galileo board console cable](https://www.aliexpress.com/item/620194122.html?spm=a2g0s.12269583.0.0.72162fc3iMfEH5)

Note Farmtek uses the bloody old RS232 protocol not TTL

Modes:
The Farmtek Polaris console can send the data to the computer in 2 modes:

 - normal mode: RS232 protocol at 1200 baud. Two data packets are sent.  The first is the time followed by the flag '(M)' eg.
 ```
   11.53 (M)
 ```
 Note: the length og this string is 11 characters with 4 characters before the decimal point and there is no EOL. The second is the name of the round and the number of faults also with no EOL eg.
 ```
 Round 1 Faults    0.00
 ```
 - continuous mode: RS232 protocol at 9600 baud. A continuous stream 7 characters long indicating the time.
 ```
  14.409
 ```