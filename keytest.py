"""
Test keyboard latency. The method is to track the key press time in
milliseconds between KEYDOWN and KEYUP. A histogram of key down times
should show "picket fencing" for keyboards with slow scans. The slow
scan could be due to slow USB polling and/or slow key matrix
scanning and debouncing. SPOILER: Some gaming keyboard have slow
scans.
"""
import array
import pygame
from pygame.locals import *

pygame.init()
SCREEN = pygame.display.set_mode((320, 240))
pygame.display.set_caption("Poll Test")

# Show one line status on the console every TIME_TICKS milliseconds
TIME_TICKS = 1000

KEY_ARRAY = array.array('B', [0] * 256)

# Key down start time in ticks. Indexed by key scan code
KEY_DOWN_ARRAY = array.array('L', [0] * 256)

# Key down delta time in ticks. Indexed by key_delta_count
KEY_DELTA_ARRAY = array.array('L', [0] * 60 * TIME_TICKS)

# Key event delta time in ticks
KEY_EVENT_ARRAY = array.array('L', [0] * 60 * TIME_TICKS)

def show_histo(f, count, rawdata):
    """ Write a histogram to a file """
    histogram = array.array('L', [0]*256)
    for ticks in range(0, count):
        if rawdata[ticks] > 255:
            histogram[255] += 1
        else:
            histogram[rawdata[ticks]] += 1
    for counts in range(0, 256):
        f.write('%3d ' % (counts))
        for i in range(0, histogram[counts]):
            f.write('*')
        f.write('\n')

def show_all_histos(key_delta_count, key_event_count):
    """ Write key press and key event histograms to a file """
    with open('./histograms.txt', 'w') as f:
        f.write('Histogram of key down times in milliseconds\n')
        show_histo(f, key_delta_count, KEY_DELTA_ARRAY)
        f.write('\nHistogram of time between key events in milliseconds\n')
        show_histo(f, key_event_count, KEY_EVENT_ARRAY)

def main():
    """ pygame event loop in here """
    key_delta_count = 0
    key_event_count = 0
    last_event_ticks = pygame.time.get_ticks()
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
                show_all_histos(key_delta_count, key_event_count)
                print('')
                print('See histograms.txt')
                return
            elif event.type == pygame.VIDEOEXPOSE:
                pygame.display.update()
            elif event.type == KEYDOWN:
                KEY_EVENT_ARRAY[key_event_count] = pygame.time.get_ticks() - last_event_ticks
                key_event_count += 1
                if key_event_count > 500:
                    show_all_histos(key_delta_count, key_event_count)
                    return
                last_event_ticks = pygame.time.get_ticks()
                z_down += 1
                z_down_now += 1
                KEY_ARRAY[event.scancode] += 1
                KEY_DOWN_ARRAY[event.scancode] = pygame.time.get_ticks()
            elif event.type == KEYUP:
                KEY_EVENT_ARRAY[key_event_count] = pygame.time.get_ticks() - last_event_ticks
                key_event_count += 1
                last_event_ticks = pygame.time.get_ticks()
                z_down_now -= 1
                if KEY_ARRAY[event.scancode] > 0:
                    KEY_ARRAY[event.scancode] -= 1
                    KEY_DELTA_ARRAY[key_delta_count] = pygame.time.get_ticks() - KEY_DOWN_ARRAY[event.scancode]
                    key_delta_count += 1
            elif event.type == pygame.USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, TIME_TICKS)
                print('Z =', z_down, '/second, down now =', z_down_now)
                z_down = 0

if __name__ == "__main__":
    main()
