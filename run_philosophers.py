from philosopher import philosopher

def start_dining():
    
    for i in range(5):  
        philosopher.delay(i)
        print(f"Started philosopher {i} task") 

if __name__ == "__main__":
    start_dining()
