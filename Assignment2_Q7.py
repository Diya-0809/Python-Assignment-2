import json
from collections import defaultdict

def read_jsonl_stream(file_path):
    """Generator to yield JSON objects line by line."""
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                yield line

def transform_and_aggregate(file_path):
    stats = defaultdict(lambda: {'count': 0, 'min_temp': float('inf'), 'max_temp': float('-inf'), 'sum_temp': 0.0, 'corrupted': 0})

    for raw_line in read_jsonl_stream(file_path):
        try:
            data = json.loads(raw_line)
            dev_id = data.get("device_id")
            temp = float(data.get("temperature_c"))

            dev_stat = stats[dev_id]
            dev_stat['count'] += 1
            dev_stat['min_temp'] = min(dev_stat['min_temp'], temp)
            dev_stat['max_temp'] = max(dev_stat['max_temp'], temp)
            dev_stat['sum_temp'] += temp

        except (json.JSONDecodeError, ValueError, TypeError):
            # Attempt to extract device_id if available to increment corrupted count
            try:
                data = json.loads(raw_line)
                dev_id = data.get("device_id", "UNKNOWN")
            except:
                dev_id = "UNKNOWN"
            stats[dev_id]['corrupted'] += 1

    for dev_id in sorted(stats.keys()):
        s = stats[dev_id]
        if s['count'] > 0:
            avg_temp = s['sum_temp'] / s['count']
            print(f"{dev_id} count={s['count']} min={int(s['min_temp'])} max={int(s['max_temp'])} avg={avg_temp:.2f} corrupted={s['corrupted']}")

if __name__ == "__main__":
    # Create sample JSONL file
    with open("sensor_data.jsonl", "w") as f:
        f.write('{"device_id":"D1","temperature_c":30,"humidity":50}\n')
        f.write('{"device_id":"D1","temperature_c":"bac","humidity":45}\n')

    transform_and_aggregate("sensor_data.jsonl")
