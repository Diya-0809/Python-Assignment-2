import sys
from collections import deque, defaultdict

def parse_time_to_minutes(time_str):
    h, m = map(int, time_str.split(':'))
    return h * 60 + m

def detect_anomalies():
    lines = sys.stdin.read().splitlines()
    if not lines:
        return

    first_line = lines[0].strip().split()
    X, T = int(first_line[0]), int(first_line[1])
    n = int(lines[1].strip())

    user_failures = defaultdict(deque) # user -> deque of (timestamp_min, ip)
    suspicious_users = {}

    for line in lines[2:2+n]:
        parts = line.strip().split()
        if len(parts) < 4:
            continue
        
        t_str, user, ip, status = parts[0], parts[1], parts[2], parts[3]
        t_min = parse_time_to_minutes(t_str)

        failures = user_failures[user]

        # Purge failures outside the T-minute sliding window
        while failures and failures[0][0] < t_min - T:
            failures.popleft()

        if status == "FAIL":
            failures.append((t_min, ip))
        elif status == "SUCCESS":
            # Check conditions: >= X failures in window, and success from a DIFFERENT IP
            if len(failures) >= X:
                recent_ips = {fail_ip for _, fail_ip in failures}
                if ip not in recent_ips or len(recent_ips) > 1 or (len(recent_ips) == 1 and ip not in recent_ips):
                    if user not in suspicious_users:
                        suspicious_users[user] = t_str

    for user in sorted(suspicious_users.keys()):
        print(f"{user} {suspicious_users[user]}")

if __name__ == "__main__":
    detect_anomalies()
