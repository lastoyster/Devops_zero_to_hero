import time 

def simulate_cpu_spike(duration=30,cpu_percent=80):
    print(f"Simulating CPU Spike at {cpu_percent}%...")
    start_time = time.time()
    
    target_percent = cpu_percent/100
    total_iterations  = int(target_percent * 5_000_000)
    
    for _ in range(total_iterations):
        result = 0
        for i in range(1,1001):
            result += i 
            
    elapsed_time = time.time() - start_time
    remaining_time = max(0,duration - elapsed_time) 
    time.sleep(remaining_time)  
    
    if __name__ == '__main__':
        simulate_cpu_spike(duration=30,cpu_percent=80)