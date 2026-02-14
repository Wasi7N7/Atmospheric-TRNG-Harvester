import serial
import time
import sys

# --- CONFIGURATION ---
SERIAL_PORT = 'COM4'     
BAUD_RATE = 115200        
OUTPUT_FILE = "quantum_data.txt"
TARGET_BITS = 1000000     # The goal: 1 Million Bits

# --- MAIN CODE ---
def main():
    print(f"--- WASI'S QUANTUM HARVESTER ---")
    print(f"Connecting to {SERIAL_PORT}...")
    print(f"Target: {TARGET_BITS} bits")
    print(f"Saving to: {OUTPUT_FILE}")
    print("-" * 30)

    try:
       
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2) 
        
        total_bits = 0
        start_time = time.time()

       
        with open(OUTPUT_FILE, "w") as f:
            while total_bits < TARGET_BITS:
                if ser.in_waiting > 0:
                   
                    raw_data = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
                    
                    # Filter: Keep ONLY '0' and '1' characters
                    clean_bits = "".join([c for c in raw_data if c in '01'])
                    
                    if clean_bits:
                        f.write(clean_bits)
                        f.flush() # Force save to disk immediately
                        total_bits += len(clean_bits)
                        
                        # Calculate progress
                        percent = (total_bits / TARGET_BITS) * 100
                        elapsed = int(time.time() - start_time)
                        
                        # Update the counter on the SAME line (no scrolling spam)
                        sys.stdout.write(f"\r[STATUS] Bits Saved: {total_bits:,} / {TARGET_BITS:,} ({percent:.2f}%) | Time: {elapsed}s")
                        sys.stdout.flush()

        print(f"\n\n--- MISSION COMPLETE ---")
        print(f"Successfully harvested {total_bits} bits.")
        print(f"File saved: {OUTPUT_FILE}")

    except serial.SerialException:
        print(f"\n[ERROR] Could not open {SERIAL_PORT}. Is the Arduino IDE Serial Monitor open? Close it!")
    except KeyboardInterrupt:
        print(f"\n[STOPPED] User stopped the script. Data saved so far.")
    except Exception as e:
        print(f"\n[ERROR] Something went wrong: {e}")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()

if __name__ == "__main__":
    main()