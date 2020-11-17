"""
Test keyboard latency. The method is to track the key press time in
milliseconds between KEYDOWN and KEYUP. A histogram of key down times
should show "picket fencing" for keyboards with slow scans. The slow
scan could be due to slow USB polling and/or slow key matrix
scanning and debouncing. SPOILER: Some gaming keyboard have slow
scans.

This differs from pytest.py by using a higher resolution timer. This
is useful for keyboard with faster scan rates. The number of key presses
required has doubled. The number of the left in the histogram is now
0.1 milliseconds. For example, 160 = 16.0 milliseconds.

Using this on slow keyboards produces histograms with lots blank
areas between peaks so pytest.py has been left unchanged.

Thanks to DeltaEpsilon on Etterna Discord for the suggestion to use
time.perf_timer().

"""
import sys
import array
import time
import getopt
import pygame
from pygame.locals import *

pygame.init()
SCREEN = pygame.display.set_mode((320, 240))
pygame.display.set_caption("Poll Test")

# Program shows histograms and exits after these many events
KEY_EVENT_LIMIT = 1000

# Show one line status on the console every TIME_TICKS milliseconds
TIME_TICKS = 1000

# Key event delta time in float seconds
KEY_EVENT_ARRAY = array.array('f', [0] * 60 * TIME_TICKS)

def show_histo(f, count, rawdata, bin_size):
    """ Write a histogram to a file """
    num_bins = int(2560 / bin_size)
    last_bin = num_bins - 1
    histogram = array.array('L', [0]*num_bins)
    for ticks in range(0, count):
        bin_index = round(rawdata[ticks]*10000/bin_size)
        if bin_index > last_bin:
            histogram[last_bin] += 1
        else:
            histogram[bin_index] += 1
    for counts in range(0, num_bins):
        f.write('%3d ' % (counts))
        for i in range(0, histogram[counts]):
            f.write('*')
        f.write('\n')

def show_all_histos(key_event_count, bin_size):
    """ Write key press and key event histograms to a file """
    with open('./histograms.txt', 'w') as f:
        f.write('\nHistogram of time between joystick events in ' + str(round(0.1*bin_size, 1)) + ' milliseconds\n')
        show_histo(f, key_event_count, KEY_EVENT_ARRAY, bin_size)

def main():
    """ pygame event loop in here """
    try:
        opts, args = getopt.getopt(sys.argv[1:], "b", ["bin="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err) # will print something like "option -a not recognized"
        sys.exit(2)
    bin_size = 10
    for o, a in opts:
        if o in ("-b", "--bin"):
            bin_size = int(a)
            if (bin_size <= 0):
                bin_size = 1
        else:
            assert False, "unhandled option"

    for i in range(pygame.joystick.get_count()):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        # Get the name from the OS for the controller/joystick.
        name = joystick.get_name()
        print("Joystick name: {}".format(name))

    key_event_count = 0
    last_event_ticks = time.perf_counter()
    pygame.display.update()
    pygame.time.set_timer(pygame.USEREVENT, TIME_TICKS)
    z_down = 0
    z_down_now = 0
    print('\nPress keys with 8-10 fingers as fast as possible for about 10 seconds.')
    print('Press the Pause key to exit. Or keep going until the program exits.')
    print('See histograms.txt for the results.\n')
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_PAUSE):
                show_all_histos(key_event_count, bin_size)
                print('')
                print('See histograms.txt')
                return
            elif event.type == pygame.VIDEOEXPOSE:
                pygame.display.update()
            elif event.type == pygame.JOYBUTTONDOWN:
                KEY_EVENT_ARRAY[key_event_count] = time.perf_counter() - last_event_ticks
                key_event_count += 1
                if key_event_count > KEY_EVENT_LIMIT:
                    show_all_histos(key_event_count, bin_size)
                    return
                last_event_ticks = time.perf_counter()
                z_down += 1
                z_down_now += 1
            elif event.type == pygame.JOYBUTTONUP:
                KEY_EVENT_ARRAY[key_event_count] = time.perf_counter() - last_event_ticks
                key_event_count += 1
                last_event_ticks = time.perf_counter()
                z_down_now -= 1
            elif event.type == pygame.JOYAXISMOTION or event.type == pygame.JOYHATMOTION:
                KEY_EVENT_ARRAY[key_event_count] = time.perf_counter() - last_event_ticks
                key_event_count += 1
                last_event_ticks = time.perf_counter()
            elif event.type == pygame.USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, TIME_TICKS)
                print('Z =', z_down, '/second, down now =', z_down_now)
                z_down = 0

if __name__ == "__main__":
    main()
    pygame.quit()
