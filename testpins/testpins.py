import time

import RPi.GPIO as GPIO


in_pins = [0, 1, 2, 3, 4, 5, 6, 7, 8]
in_pins += [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
clk_pin = 25

GPIO.setmode(GPIO.BCM)
print(f"seting up pin {clk_pin} as clock")
GPIO.setup(clk_pin, GPIO.OUT, initial=GPIO.LOW)
for p in in_pins:
    print(f"seting up pin {p} as input")
    GPIO.setup(p, GPIO.IN, pull_up_down=GPIO.PUD_OFF)


def toggle_clock():
    GPIO.output(clk_pin, 1)
    GPIO.output(clk_pin, 0)


def pin_states():
    states = {}
    for p in in_pins:
        states[p] = GPIO.input(p)
    return states


def format_pin_states(s):
    return ''.join(['*' if s[p] else '_' for p in in_pins])


def test_all_pins():
    high_fails = {}
    low_fails = {}
    # all GPIO should start low
    if any(pin_states().values()):
        print("all pins did not start low")
        low_fails['pre'] = True
    #assert not any(pin_states().values()), "all pins did not start low"
    for p in in_pins:
        print(f"toggling clock for pin {p}")
        toggle_clock()
        s = pin_states()
        print(format_pin_states(s))
        if s[p] == 0:
            print(f"expected {p} to be high and was low")
            high_fails[p] = True
        #assert s[p], f"expected {p} to be high and was low"
        for o in in_pins:
            if o == p:
                continue
            if s[o] == 1:
                print(f"expect {o} to be low and was high")
                low_fails[p] = low_fails.get(p, []) + [o, ]
            #assert s[o] == 0, f"expect {o} to be low and was high"

    # and should end low
    toggle_clock()
    if any(pin_states().values()):
        print("all pins did not end low")
        low_fails['post'] = True
    #assert not any(pin_states().values()), "all pins did not end low"
    return high_fails, low_fails

#toggle_clock()
#print(format_pin_states(pin_states()))
print(test_all_pins())
