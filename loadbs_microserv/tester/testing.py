import requests
import time

def perform_get_requests(endpoint, k):
    start_time = time.time() 
    for i in range(k):
        try:
            response = requests.get(endpoint)
            if response.status_code == 200:
                print(f"Request {i + 1}: Success - Status Code {response.status_code} {response.json()}")
            else:
                print(f"Request {i + 1}: Failed - Status Code {response.status_code}")
        except requests.RequestException as e:
            print(f"Request {i + 1}: Error - {e}")

    end_time = time.time() 
    
    total_time = end_time - start_time
    print(f"\nTotal time taken for {k} requests: {total_time:.2f} seconds")
    return total_time

if __name__ == "__main__":
    endpoint_url = "http://127.0.0.1:8000"
    choice = 'y'
    while choice == 'y':
        k = int(input("Enter the K : "))
        perform_get_requests(endpoint_url, k)
        choice = input("Do you want to continue?")

