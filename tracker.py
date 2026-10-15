import os
import requests

GROUP_ID = 5211428
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
USER_ID_TO_PING = os.environ.get("USER_ID_TO_PING")
STATE_FILE = "last_count.txt"

def get_saved_count():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            try:
                return int(f.read().strip())
            except ValueError:
                return None
    return None

def save_count(count):
    with open(STATE_FILE, "w") as f:
        f.write(str(count))

def main():
    url = f"https://groups.roblox.com/v1/groups/{GROUP_ID}"
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        print(f"API Error: {response.status_code}")
        return

    data = response.json()
    current_count = data.get("memberCount", 0)
    group_name = data.get("name", "Onett's Testing Group")
    last_count = get_saved_count()

    print(f"Current count: {current_count}, Last saved count: {last_count}")

    if last_count is not None and current_count > last_count:
        diff = current_count - last_count
        msg = {
            "content": f"<@{USER_ID_TO_PING}> 🚨 **NEW MEMBER JOINED!** 🚨\n**{group_name}** went from **{last_count}** to **{current_count}** members (+{diff}). Onett might be accepting requests right now!"
        }
        requests.post(DISCORD_WEBHOOK_URL, json=msg)

    save_count(current_count)

if __name__ == "__main__":
    main()
