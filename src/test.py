from datetime import datetime, timezone
dt = datetime.now(timezone.utc)

print(dt.strftime("%Y-%m-%d %H:%M:%S"))
# print(datetime.strptime(str(datetime.now(timezone.utc)), "%Y-%m-%dT%H:%M:%S.%f"))

