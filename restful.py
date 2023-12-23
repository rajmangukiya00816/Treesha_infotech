#!/usr/bin/env python3
import argparse
import requests
import json
import csv
from typing import Optional

class RestfulClient:
    BASE_URL = "https://jsonplaceholder.typicode.com"

    def __init__(self, method: str, endpoint: str, data: Optional[str], output: Optional[str]):
        self.method = method
        self.endpoint = endpoint
        self.data = data
        self.output = output

    def send_request(self):
        url = f"{self.BASE_URL}{self.endpoint}"
        headers = {"Content-Type": "application/json"}

        if self.method == "get":
            response = requests.get(url)
        elif self.method == "post":
            data = json.loads(self.data) if self.data else None
            response = requests.post(url, json=data, headers=headers)
        else:
            raise ValueError("Invalid method. Use 'get' or 'post'.")

        self.handle_response(response)

    def handle_response(self, response):
        print(f"HTTP Status Code: {response.status_code}")

        if response.status_code // 100 == 2:  # Check if status code is 2xx
            if self.output:
                self.save_response(response)
            else:
                print(response.json())
        else:
            print(f"Error: {response.text}")
            exit(1)

    def save_response(self, response):
        if self.output.endswith(".json"):
            with open(self.output, "w") as json_file:
                json.dump(response.json(), json_file, indent=2)
        elif self.output.endswith(".csv"):
            with open(self.output, "w", newline="") as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(response.json()[0].keys())
                for item in response.json():
                    csv_writer.writerow(item.values())
        else:
            raise ValueError("Invalid output file format. Use '.json' or '.csv'.")

def main():
    parser = argparse.ArgumentParser(description="Simple command-line REST client for JSONPlaceholder.")
    parser.add_argument("method", choices=["get", "post"], help="Request method")
    parser.add_argument("endpoint", help="Request endpoint URI fragment")
    parser.add_argument("-d", "--data", help="Data to send with request")
    parser.add_argument("-o", "--output", help="Output to .json or .csv file (default: dump to stdout)")

    args = parser.parse_args()
    restful_client = RestfulClient(args.method, args.endpoint, args.data, args.output)
    restful_client.send_request()

if __name__ == "__main__":
    main()
