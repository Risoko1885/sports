# fetch_api_football_data.py
import requests
import datetime
import json

# === НАСТРОЙКИ ===
API_KEY = "0986bfd3b0ea4900794f791df18c5645"
BASE_URL = "https://v3.football.api-sports.io"
HEADERS = {"x-apisports-key": API_KEY}

# Сегодняшняя дата в формате YYYY-MM-DD
TODAY = datetime.datetime.utcnow().strftime("%Y-%m-%d")

def get_fixtures(date):
    url = f"{BASE_URL}/fixtures"
    params = {"date": date}
    resp = requests.get(url, headers=HEADERS, params=params)
    return resp.json().get("response", [])

def get_fixture_stats(fixture_id):
    stats = {}
    for section in ["statistics", "events", "lineups"]:
        url = f"{BASE_URL}/fixtures/{section}"
        resp = requests.get(url, headers=HEADERS, params={"fixture": fixture_id})
        stats[section] = resp.json().get("response", [])
    return stats

def send_to_emelya(payload):
    url = "https://emelya.api/v1/upload/match-data"  # пример: реальный URL добавим позже
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    return response.status_code == 200

def main():
    print(f"Сбор матчей за {TODAY}...")
    fixtures = get_fixtures(TODAY)
    all_data = []

    for fx in fixtures:
        fixture_id = fx["fixture"]["id"]
        match_info = {
            "fixture_id": fixture_id,
            "teams": fx["teams"],
            "league": fx["league"],
            "date": fx["fixture"]["date"]
        }
        stats = get_fixture_stats(fixture_id)
        match_info.update(stats)
        all_data.append(match_info)

    print(f"Матчей собрано: {len(all_data)}")

    # Отправка в Эмелю
    if send_to_emelya(all_data):
        print("✅ Данные успешно отправлены")
    else:
        print("❌ Ошибка отправки данных")

if __name__ == "__main__":
    main()
