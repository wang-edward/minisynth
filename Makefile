PORT ?= /dev/cu.usbmodem*

# erases entire flash, removes micropython interpreter
erase:
	uv run esptool --chip esp32s3 --port $(PORT) erase-flash

# writes micropython firmware to board
flash:
	uv run esptool --chip esp32s3 --port $(PORT) --baud 460800 write-flash 0 firmware/*.bin

# copies src/* to boards filesystem
upload:
	uv run mpremote connect $(PORT) cp -r src/ :

repl:
	uv run mpremote connect $(PORT) repl

# reboot
reset:
	uv run mpremote connect $(PORT) reset

# simple way to ping to check board is connected
chip-id:
	uv run esptool --chip esp32s3 --port $(PORT) chip-id

# runs main.py without copying files over
run:
	uv run mpremote connect $(PORT) run src/main.py
