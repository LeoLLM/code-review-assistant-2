#!/usr/bin/env python3
# Example code with various issues for code review practice

import os, sys, json, time, random
from datetime import datetime

# Global variable
password = "mySecretPassword123"  # Hard-coded credential

def calculate_sum(l):
    """
    Calculate the sum of a list of numbers
    """
    s = 0
    for i in range(len(l)):  # Inefficient iteration
        s = s + l[i]
    return s

def fetch_user_data(user_id):
    # SQL injection vulnerability
    query = "SELECT * FROM users WHERE id = " + user_id
    
    # Simulate database fetch
    print(f"Executing query: {query}")
    
    # No proper error handling
    user_data = {"id": user_id, "name": "Test User", "email": "test@example.com"}
    return user_data

class userManager:  # Non-standard class naming
    def __init__(self):
        self.users = []
    
    def add_user(self, user):
        self.users.append(user)
        print("User added successfully")  # Hardcoded print instead of logging
    
    # Inconsistent method naming convention
    def DeleteUser(self, user_id):
        for i, user in enumerate(self.users):
            if user["id"] == user_id:
                del self.users[i]
                return True
        return False

def process_data(data):
    # Nested loop with O(n²) complexity
    result = []
    for i in data:
        temp = []
        for j in data:
            temp.append(i * j)
        result.append(temp)
    
    # Commented out code
    # for item in result:
    #     print(item)
    
    return result

# Inconsistent indentation
def validate_input(input_str):
    if input_str:
      # No input validation
      return input_str
    else:
        return None

# Function that does multiple unrelated things
def save_and_process(data, filename):
    # Write data to file without proper checks
    with open(filename, "w") as f:
        f.write(json.dumps(data))
    
    # Process the data
    processed = []
    for item in data:
        processed.append(item * 2)
    
    # Update timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return {"processed_data": processed, "timestamp": current_time}

if __name__ == "__main__":
    # Unused variables
    max_count = 100
    data = [random.randint(1, 100) for _ in range(10)]
    
    um = userManager()
    um.add_user({"id": 1, "name": "John"})
    
    print(calculate_sum(data))
    print(fetch_user_data("1; DROP TABLE users;"))  # SQL injection attempt
    
    # No cleanup of resources