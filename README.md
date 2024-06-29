# Avia

This a project fro tracking avia tickets using aviasales.com [API](https://api.travelpayouts.com/aviasales/v3/prices_for_dates).

## Algorithm

1. /scripts/run_main.sh is run with this schedule "0 02,08,14,20 * * *"
2. This bash script calls another bash script /scripts/run.sh using the given list of origin:destination pairs (/cong/iata*_.txt)
3. /scripts/run.sh calls python script /scripts/main.py with a given arguments.
4. /scripts/main.py requests API day by day from TODAY till TODAY+365.
5. The resulting files are saved to /files/data. Files are tab separated.
6. Logs are saved to /logs and /logs/runs
