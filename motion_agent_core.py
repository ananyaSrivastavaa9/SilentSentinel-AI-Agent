import time
import random

# In a real phone, gravity sits at 1.0G (9.8 m/s²). 
# A violent fall causes a massive spike (impact) followed by absolute stillness.
FALL_IMPACT_THRESHOLD = 3.5  # G-force spike indicating a hard crash/impact
STILLNESS_THRESHOLD = 0.1    # Almost 0 movement indicating unconsciousness
SUSTAINED_STILLNESS_SECS = 4 # How many seconds of stillness to confirm crisis

# Global state link for our agent architecture
MOTION_PANIC_FLAG = False

print("🛡️ [SILENT SENTINEL] Motion Security Simulation Layer initializing...")

def generate_mock_accelerometer_data(scenario="normal"):
    """Generates realistic G-force numbers based on human activity"""
    if scenario == "normal":
        # Normal walking/sitting causes slight fluctuations around 1.0G
        return random.uniform(0.9, 1.2)
    elif scenario == "impact":
        # A hard fall or crash creates a violent peak force spike
        return random.uniform(3.6, 5.0)
    elif scenario == "stillness":
        # Complete lack of movement after a fall
        return random.uniform(0.0, 0.05)

def run_motion_monitor():
    global MOTION_PANIC_FLAG
    print("🏃‍♂️ Ingesting motion telemetry. Simulating normal daily movement...")
    
    timeline = []
    # Build a 12-second test timeline: 4s normal walking, 1s violent impact, 7s stillness
    for _ in range(4): timeline.append("normal")
    timeline.append("impact")
    for _ in range(7): timeline.append("stillness")
    
    stillness_counter = 0
    
    for state in timeline:
        g_force = generate_mock_accelerometer_data(state)
        print(f"📊 Accelerometer Telemetry: {g_force:.2f} G | Current Activity State: {state.upper()}")
        time.sleep(1) # Read telemetry every 1 second
        
        # --- CRISIS DETECTION REASONING ---
        # 1. Check for the massive impact spike
        if g_force > FALL_IMPACT_THRESHOLD and not MOTION_PANIC_FLAG:
            print(f"💥 [WARNING] High-G Impact Detected ({g_force:.2f}G)! Monitoring for user response...")
            MOTION_PANIC_FLAG = "monitoring"
            continue
            
        # 2. If an impact occurred, check if the user stops moving completely
        if MOTION_PANIC_FLAG == "monitoring":
            if g_force < STILLNESS_THRESHOLD:
                stillness_counter += 1
                print(f"⏳ Post-Impact Stillness Confirmed: {stillness_counter}/{SUSTAINED_STILLNESS_SECS} seconds.")
            else:
                # If they move normally, reset the panic state (False Alarm)
                print("🔄 User movement detected post-impact. Resetting security threshold.")
                MOTION_PANIC_FLAG = False
                stillness_counter = 0
                
            # 3. If they are still for too long, lock down and trip the flag
            if stillness_counter >= SUSTAINED_STILLNESS_SECS:
                MOTION_PANIC_FLAG = True
                print("\n🚨 [CRITICAL MOTION TRIGGER] Abnormal Behavioral State Confirmed!")
                print("↳ Logic: High-G impact followed by prolonged structural stillness.")
                print(f"⚡ Global Motion Status: {MOTION_PANIC_FLAG} -> Halting stream.")
                break

if __name__ == "__main__":
    run_motion_monitor()