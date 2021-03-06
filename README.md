# Keyboard and Gamepad Scan Rates

## Keyboard
Keyboard scan rate is the the lower of the USB polling rate and the key
hardware scan rate. keytest.py attempts to determine the keyboard scan rate
by showing a histogram of hundreds of key press times measured in milliseconds.
For an 8 ms/125 Hz keyboard, the histogram shows sharp spikes at multiples of
8 ms.

SPOILER: The histogram for my DK61E shows 24 ms/42 HZ scan rate!

Name            |Key switch |USB VID:PID|USB Speed, Mbits/s |USB bInterval, ms  |Scan rate, ms, Hz|Comments
----------------|-----------|-----------|-------------------|-------------------|-----------------|--------
Logitech iTouch |membrane   |046d:c30a  |1.5                |32                 |8, 125           |Membrane keyboard
Logitech Int 350|membrane   |046d:c313  |1.5                |10                 |16, 62.5         |Slow membrane keyboard
FL ESports GT87S|mechanical |040b:0a67  |12                 |1                  |5, 200           |Slightly faster
Gigabyte K83    |mechanical |04d9:a06b  |12                 |1                  |3, 333           |Best so far
Dierya DK61E    |optical    |1ea7:0077  |12                 |1                  |24, 42           |Whaaaaa?

All tests were done on computers running Ubuntu 18.04. Two keyboards were
tested on a Win10 PC with similar results.

The Logitech iTouch keyboard specifies bInterval 32 but the histogram shows 8
ms scan rate. The other Logitech keyboard specifies bInterval of 10 but the
histogram shows 16 ms scan rate. Baffling.

The Gigabyte K83 does not show picket fencing so I gave it scan rate of 1 ms.
The keyboard is scannning fast enough the histogram shows no picket fencing.
Perhaps the scan rate should be 3 ms because there are small peaks at 3 ms
intervals. UPDATE: Using a higher resolution timer and doubling the number of
key presses makes the 3 ms scan rate clear. Thanks to DeltaEpsilon on the
Etterna Discord for the tip.

The Dierya DK61E has Gateron optical switches but it has the slowest scan rate.
I suspect the keyboard LED animation is slowing down the keyboard scan but this
is only speculation. Too bad the keyboard firmware is not open source.

The keytest.py program produces a histogram of key press times in milliseconds.
Keyboards with slow scan rates have key press times that are multiples of the
scan rate. For example, in the Logitech_iTouch directory the histogram is in
notes.txt. The left column is the key press time in milliseconds starting from
0 to 255. The number of '\*' on each line shows the number of keypresses.

For example, the following shows 1 key press of 39 ms, 11 of 40 ms, 25 of
48 ms, and 2 of 49 ms. Histogram picket fence refers to the alternating spaces
and peaks. The 8 ms spacing indicates key presses are reported in multiples of
8 ms which is a common USB polling rate for USB low speed HID devices. Timing
is based on a 1 ms counter so the results are +/- 1 ms.

```
 39 *
 40 ***********
 41
 42
 43
 44
 45
 46
 47
 48 *************************
 49 **
```

Install pygame and Python3. This should work on Linux, Windows, and Mac but
has only been tested on Linux and Windows.

https://www.pygame.org/wiki/GettingStarted

Run the key test like this.

```
$ python3 keytest.py
```

If you want higher resolution timing for fast scan keyboards, use this.

```
$ python3 keytest.py --bin=1
```

This produces histograms with 0.1 millisecond bins. The histograms are
ten times longer but this is required if the key scan rate is close to 1 ms.
For example, the 3 ms scan rate of the Gigabyte K83 is clearer using this
option.

The --bin options refers to the histogram bin size. The default is bin size=10
for 10 * 0.1 millisecond (1 ms) bins. Use bin size = 1 for 0.1 millisecond
bins.

Be sure to close all other programs to get the most accurate timing. In
particular, do not run games, web browsers, video players, or anything that
uses lots of CPU to get the clearest histograms.

Once a second the program prints a status line to show it is alive. It creates
an small black window which MUST have the focus. Put 8-10 fingers on the
keyboard then bang away like a drunken monkey for about 20 seconds or until the
program exits. Close the small window or go back to the terminal window and
press ^C or the Pause key to stop the program. The histograms are in a file
named histograms.txt.

Older versions of the program produces a histogram of key press times. The
current version also includes a histogram of time between key events (up or
down). This is a cross check on the first histogram since I had a hard time
believing the results for the DK61E. The second histogram is sometime more
useful because the scan time is clearer. If the first is murky, take a look
at the second one.

How does this program differ from
http://blog.seethis.link/scan-rate-estimator/?  The scan-rate-estimator shows
the best case (shortest) key press time. This program shows histograms for
hundreds of key presses. The histograms better characterize the keyboard
behavior during real world use such as gaming.

## Gamepad

The program joytest.py is similar to keytest.py but measures the time between
joystick/gamepad events.

WARNING: The gamepads were tested on Ubuntu 18.04 so may behave differently in
their respective consoles. There have been many revisions of gamepads over the
year so some may behave differently.

The Sony DS4 and Nintendo Switch compatible HoriPad shows clear lines at 4 ms
intervals.

The Xbox One controllers shows clear lines at 8 ms intervals but much smaller
lines in between at 4 ms. Not sure what is happening here.

## References

References to sources that measure keyboard lag/scan rate. There are an
unlimited number of threads on this topic but just a few people are providing
evidence.

### Keyboard polling rate matters, here's why | osu! & Etterna

Excellent explanation why key scan rate matters. Keyboards with very low scan
rates affect all gamers, not just elite rhythm gamers.

https://www.youtube.com/watch?v=heZVmr9fyng

### Scan Rate Estimator

Interesting but very short key presses can be produced by flicking dozens of
of times.

http://blog.seethis.link/scan-rate-estimator/

### Keyboard Input Lag 125, 250, 500, 1000Hz USB vs. PS/2

https://www.youtube.com/watch?v=eEswl6kZq5k

### Keyboard Latency

https://danluu.com/keyboard-latency/

