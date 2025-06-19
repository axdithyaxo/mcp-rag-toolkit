import subprocess

def print_cron_jobs():
    try:
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True, check=True)
        lines = result.stdout.strip().split('\n')
        if not lines:
            print("❌ No cron jobs found.")
            return

        print("📅 Current Cron Jobs:\n")
        for line in lines:
            if not line.strip().startswith("#") and "update_index_cron.sh" in line:
                print(f"🕓 {line}")
    except subprocess.CalledProcessError as e:
        print("⚠️ Failed to read crontab:", e)

if __name__ == "__main__":
    print_cron_jobs()