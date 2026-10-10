import re
import sys
from collections import defaultdict

def extract_email_intelligence(file_path):
    # Matches username with letters, digits, +, ., _, - and domain ending in .com, .edu, .org
    email_pattern = re.compile(r'\b([a-zA-Z0-9+._-]+@([a-zA-Z0-9.-]+\.(?:com|edu|org)))\b', re.IGNORECASE)
    
    domain_users = defaultdict(set)
    domain_min_email = {}

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                matches = email_pattern.findall(line)
                for full_email, domain in matches:
                    full_email_lower = full_email.lower()
                    domain_lower = domain.lower()
                    
                    user = full_email_lower.split('@')[0]
                    domain_users[domain_lower].add(user)
                    
                    if domain_lower not in domain_min_email:
                        domain_min_email[domain_lower] = full_email_lower
                    else:
                        domain_min_email[domain_lower] = min(domain_min_email[domain_lower], full_email_lower)

        for domain in sorted(domain_users.keys()):
            user_count = len(domain_users[domain])
            smallest_email = domain_min_email[domain]
            print(f"{domain} {user_count} {smallest_email}")

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        extract_email_intelligence(sys.argv[1])
    else:
        # Self-contained sample test execution
        test_file = "sample_emails.txt"
        with open(test_file, "w") as f:
            f.write("Contact b+1@adit.edu, root@@bad.com, test-user@x.org and b+1@adit.edu")
        extract_email_intelligence(test_file)
