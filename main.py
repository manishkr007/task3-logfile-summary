import re
from collections import defaultdict

# Regular expression to match the fields of a line in log file
fields_pattern = re.compile( r'^(?P<pod_name>\S+)\s+'
                            r'(?P<container_name>\S+)\s+'
                            r'(?P<ip_address>\S+)\s+'
                            r'-\s+-\s+'
                            r'(?P<timestamp>\[[^\]]+\])\s+'
                            r'"(?P<method>\S+)\s+(?P<request_path>\S+)\s+(?P<http_version>\S+)"\s+'
                            r'(?P<response_code>\d{3})\s+'
                            r'(?P<bytes_sent>\S+)\s+'
                            r'"(?P<website>[^"]*)"\s+'
                            r'"(?P<user_browser>[^"]*)"\s+'
                            r'(?P<can_be_skipped1>\S+)\s+'
                            r'(?P<can_be_skipped2>\S+)\s+'
                            r'\[(?P<backend_service>[^\]]*)\]\s+'
                            r'\[(?P<empty_field>)?\]\s+'
                            r'(?P<service_ip>\S+)\s+'
                            r'(?P<can_be_skipped4>\S+)\s+'
                            r'(?P<can_be_skipped5>\S+)\s+'
                            r'(?P<final_response_code>\d{3})\s+'
                            r'(?P<trace_id>\S+)$'
)

# analyze_logfile function reads the log file, processes each line and returns a summary of the data
def analyze_logfile(logfile_path):

    # Initialize a dictionary to store the count, sum and a set for unique paths
    requests_per_pod = defaultdict(int)
    response_code_summary = defaultdict(int)
    bytes_per_pod  = defaultdict(int)
    unique_request_paths = set()

    # Open the log file
    with open(logfile_path, 'r') as file:
        logfile_data = file.readlines()

    # Process each line in the log file after stripping whitespace
    for line in logfile_data:
        refined_line = line.strip()
        
        if not refined_line:
            continue

        # Match the line with the regex pattern
        match = fields_pattern.match(refined_line)
        if match:
            data = match.groupdict()
            pod_name = data['pod_name']
            response_code = data['response_code']
            request_path = data['request_path']
            
            # Remove the trailing number from the request path, it might be restored again if needed
            request_path_generic = re.sub(r'/\d+$', '', request_path)

            # bytes_sent is a string, convert it to int, if it is '-' set it to 0
            try:
                bytes_sent_string = data['bytes_sent']
                if bytes_sent_string == '-':
                    bytes_sent = 0
                else:
                    bytes_sent = int(bytes_sent_string)
            except ValueError:
                print(f"Warning: Could not get bytes_sent {bytes_sent} in line: {line}")
                bytes_sent = 0
            
            # Update the dictionaries and set
            requests_per_pod[pod_name] += 1
            response_code_summary[response_code] += 1
            bytes_per_pod[pod_name] += bytes_sent
            unique_request_paths.add(request_path_generic)

        else:
            print(f"Warning: Line did not match regex: {line}")
            continue

    return requests_per_pod, response_code_summary, bytes_per_pod, unique_request_paths

# Write the summarized results to a file
def summary_in_file(requests_per_pod, response_code_summary, bytes_per_pod, unique_request_paths):
    with open('analysis_results.txt', 'w') as f:
        f.write("Log File Analysis Results :-\n\n")
        
        f.write("Total requests per pod:\n")
        for pod, count in requests_per_pod.items():
            f.write(f"{pod}: {count}\n")

        f.write("\nResponse code summary:\n")
        for code, count in response_code_summary.items():
            f.write(f"{code}: {count}\n")

        f.write("\nTotal bytes sent per pod:\n")
        for pod, bytes_sent in bytes_per_pod.items():
            f.write(f"{pod}: {bytes_sent}\n")

        f.write("\nUnique request paths:\n")
        for path in sorted(unique_request_paths):
            f.write(f"{path}\n")

def main():
    # Define the path to the log file
    log_file_path = 'fp-sre-challenge.log'

    # Get the analysis results
    requests_per_pod, response_code_summary, bytes_per_pod, unique_request_paths = analyze_logfile(log_file_path)

    # Write the summary to a file
    summary_in_file(requests_per_pod, response_code_summary, bytes_per_pod, unique_request_paths)
    
    print("Summarized results have been written to file 'analysis_results.txt'")

if __name__ == "__main__":
    main()