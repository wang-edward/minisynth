from machine import I2C, Pin
import time

i2c = I2C(0, scl=Pin(38), sda=Pin(37), freq=400000)
ADDR = 0x20

# port 1 (rows) as inputs, pull-ups on
i2c.writeto_mem(ADDR, 0x07, b'\x1f')
i2c.writeto_mem(ADDR, 0x03, b'\x1f')

# port 0 (columns) as outputs
i2c.writeto_mem(ADDR, 0x06, b'\x00')

prev = [[False]*5 for _ in range(5)]

while True:
    for col in range(5):
        # drive one column low, rest high
        i2c.writeto_mem(ADDR, 0x02, bytes([~(1 << col) & 0x1f]))

        rows = i2c.readfrom_mem(ADDR, 0x01, 1)[0] & 0x1f

        for row in range(5):
            pressed = not (rows & (1 << row))
            if pressed and not prev[row][col]:
                print(f"row={row} col={col}")
            prev[row][col] = pressed

    time.sleep_ms(10)
