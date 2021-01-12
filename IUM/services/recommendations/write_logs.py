import json
from definitions import ROOT_DIR


def write_logs(data):
    with open(f'{ROOT_DIR}/logs/recommendations.json', mode="r+") as f:
        logs = json.load(f)
        recommendations = logs["recommendations"]
        recommendations.append(data)
        new_logs = {"recommendations": recommendations}

        f.seek(0)
        json.dump(new_logs, f)
    f.close()
