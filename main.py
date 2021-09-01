import asyncio
import time
from bleak import BleakScanner, BleakError, BleakClient
from helpers import int_to_hex, get_rgb_hex, get_brightness_hex
import re

start_time = time.time()
devicename = "ihoment_H6125_3299"
# mac = 'A4:C1:38:2F:32:99'
UUID_CONTROL_CHARACTERISTIC = '00010203-0405-0607-0809-0a0b0c0d2b11'


    

async def keepAlive(device):
    print("uh uh uh uh staying alive staying alive")

async def do_keepalive_every_2_seconds(device): 
    interval = 2 
    print("committing to keeping alive")

    while device.is_connected:
        print(round(time.time() - start_time, 1), "Starting periodic function")
        await asyncio.gather(
            asyncio.sleep(interval),
            keepAlive(device)
        )

async def sendPayload(device, payload):
    await device.write_gatt_char(UUID_CONTROL_CHARACTERISTIC, bytes(payload))


async def setBrightness(device, BRIGHTNESS):
    print(f"setting brightness to {BRIGHTNESS}")    
    
    payload = [ 0x33, 0x04, BRIGHTNESS, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, (0x33 ^ 0x04 ^ BRIGHTNESS) ] 
    await sendPayload(device, payload)


async def run():
    print("scanning")
    devices = await BleakScanner.discover(timeout=0.5) # small because im impatient 
    devicefound = False
    for d in devices:
        print(d.name)
        if d.name == devicename:
            print("Device found!")
            ble_address = d.address
            devicefound = True
    
    if (not devicefound):
        print("device didnt find :(")
        raise BleakError(f"A device with name {devicename} could not be found.")

    print("getting on with it!")
    
    device = await BleakScanner.find_device_by_address(ble_address, timeout=20.0)
    if not device:
        raise BleakError(f"A device with address {ble_address} could not be found.")

    try: 
        async with BleakClient(device) as device:
            timebefore = time.perf_counter()

            print(f"Connected?: {device.is_connected} ")
            # print("Starting keepalive")
            # asyncio.run(do_keepalive_every_2_seconds(device))
            
            print("done")
            bright = 0
            while (device.is_connected):
                bright = (bright + 1) % 0xFF
                await setBrightness(device, bright)
                time.sleep(0.1)

            print(f"Disconnected after {time.perf_counter() - timebefore}")
    except KeyboardInterrupt: 
        print("keyboard interrupt!")
        pass
    finally:
        print("disconnecting")
        await device.disconnect()
        print("goodbye!")

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())

if __name__ == '__main__':
    main()


