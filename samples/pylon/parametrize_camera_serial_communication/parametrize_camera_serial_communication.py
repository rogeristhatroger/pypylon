#!/usr/bin/env python3
"""\
Demonstrate UART (asynchronous serial communication) through a camera.

This sample shows how to configure the camera's built-in UART module and
transmit/receive data. By default it operates in loopback mode, where the
camera's serial TX output is wired internally to the RX input, so no
external device is needed.

Set LOOPBACK to False to route communication through the camera's physical
GPIO lines (e.g. Line2 for TX, Line3 for RX on ace 2 Pro cameras). In that
case a UART device must be connected to those lines.

UART serial communication is available on some camera models, for example
ace 2 Pro. Cameras without BslSerialReceive/BslSerialTransmit nodes will
cause this sample to print a message and exit cleanly.
"""
import sys
import time
from pypylon import pylon

LOOPBACK = True

exit_code = 0


def serial_transmit(camera, data):
    """Transmit a bytes-like object over the camera's UART.

    Workflow:
      1. Write the data to BslSerialTransferBuffer (for GigE, write multiples of 4 bytes).
      2. Write the real (not the padded) length in bytes to BslSerialTransferLength.
      3. Execute BslSerialTransmit.
      4. Wait for BslSerialTxFifoEmpty to become true before further transmissions.
      5. Repeat until all data has been transmitted.
    """
    max_tx_size = camera.BslSerialTransferBuffer.Length
    offset = 0

    while offset < len(data):
        chunk = data[offset : offset + max_tx_size]
        transfer_length = len(chunk)

        # Pad to a multiple of 4 bytes for GigE compatibility.
        padded_length = transfer_length + (-transfer_length % 4)
        padded_chunk = bytes(chunk) + b"\x00" * (padded_length - transfer_length)

        camera.BslSerialTransferBuffer.Set(padded_chunk)
        camera.BslSerialTransferLength.Value = transfer_length

        camera.BslSerialTransmit.Execute()
        offset += transfer_length

        # Wait for the TX FIFO to drain (poll at 1 ms intervals, up to 100 ms).
        for _ in range(100):
            if camera.BslSerialTxFifoEmpty.Value:
                break
            time.sleep(0.001)

        # Overflow status is updated by the transmit command.
        if camera.BslSerialTxFifoOverflow.Value:
            print("WARNING: Serial transmit overflow!")


def serial_receive(camera):
    """Receive all pending data from the camera's UART and return as bytes.

    Workflow:
      1. Execute BslSerialReceive.
      2. Check flags: BslSerialRxFifoOverflow, BslSerialRxParityError, BslSerialRxStopBitError.
      3. Read BslSerialTransferLength to obtain the length of received data.
      4. Read that many bytes from BslSerialTransferBuffer (for GigE, read multiples of 4 bytes).
      5. Repeat if BslSerialTransferLength was not 0.
    """
    received = bytearray()

    while True:
        camera.BslSerialReceive.Execute()

        # If overflow is set, data was lost!
        if camera.BslSerialRxFifoOverflow.Value:
            print("WARNING: Receive overflow detected!")
        # If parity error is set, data may be incorrect!
        if camera.BslSerialRxParityError.Value:
            print("WARNING: Parity error in received data stream detected!")
        # If stop bit error is set, data may be incorrect!
        # This bit is also normally set when a break condition occurred.
        if camera.BslSerialRxStopBitError.Value:
            print("WARNING: Stop bit error in received data stream detected!")

        transfer_length = camera.BslSerialTransferLength.Value
        if transfer_length == 0:
            break

        # GigE cameras require reading multiples of 4 bytes.
        padded_length = transfer_length + (-transfer_length % 4)
        buf = camera.BslSerialTransferBuffer.Get(padded_length)
        received.extend(buf[:transfer_length])

    return bytes(received)


try:
    with pylon.InstantCamera(pylon.FirstFound) as camera:
        print("Using device:", camera.DeviceInfo.ModelName)
        print()

        # Check for UART support.
        if not (
            camera.BslSerialReceive.IsWritable()
            and camera.BslSerialTransmit.IsWritable()
        ):
            print("The device doesn't support asynchronous serial communication.")
            sys.exit(0)

        # --- Configure I/O ---
        if LOOPBACK:
            print("Configure loopback for serial communication...", end="")
            camera.BslSerialRxSource.Value = "SerialTx"
            print("done")
        else:
            print("Configure GPIO lines for serial communication...")
            # On ace 2 cameras, lines 2 and 3 are GPIO lines.
            # Do not use the opto-coupled input for UART communications!

            # Use line 2 as TX (Output).
            camera.LineSelector.Value = "Line2"
            camera.LineMode.Value = "Output"
            camera.LineSource.Value = "SerialTx"

            # Use line 3 as RX (Input).
            camera.LineSelector.Value = "Line3"
            camera.LineMode.Value = "Input"

            camera.BslSerialRxSource.Value = "Line3"
            print("done")

        # --- Configure UART: 115200 baud, 8 data bits, no parity, 1 stop bit ---
        print("Configure UART to 115200 8N1...", end="")
        camera.BslSerialBaudRate.Value = "Baud115200"
        camera.BslSerialNumberOfDataBits.Value = "Bits8"
        camera.BslSerialParity.Value = "None"
        camera.BslSerialNumberOfStopBits.Value = "Bits1"
        print("done")

        # --- Transmit data ---
        message = "For documentation, see: https://docs.baslerweb.com/serial-communication"
        print(f"Transmit: '{message}'")
        serial_transmit(camera, message.encode())
        print("Transmit: done!")

        # --- Receive data ---
        print("Receive: Starting...")
        if LOOPBACK:
            print(
                "Note: In loopback mode, the message is too long for the "
                "receive FIFO and an overflow message will appear!"
            )
            print("Note: The received message seen here will be truncated!")

        received_data = serial_receive(camera)
        print(f"Receive: '{received_data.decode(errors='replace')}'")

        # --- Demonstrate break condition ---
        print("Receive break:", camera.BslSerialRxBreak.Value)
        camera.BslSerialRxBreakReset.Execute()

        print("Set break condition...", end="")
        camera.BslSerialTxBreak.Value = True
        time.sleep(0.010)
        camera.BslSerialTxBreak.Value = False
        print("done!")

        print("Receive break:", camera.BslSerialRxBreak.Value)
        camera.BslSerialRxBreakReset.Execute()

        # After a break, the receive FIFO contains errors, so flush it.
        print("Note: After a break condition framing error flags will probably be set!")
        serial_receive(camera)

except Exception as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)
