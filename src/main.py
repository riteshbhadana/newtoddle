from process_data import detect_churn
from notifier import send_email_alert

def run():
    churned = detect_churn()

    print(f"Total churned users: {len(churned)}")

    for _, row in churned.head(5).iterrows():
        msg = f"User {row['person_id']} moved to non-Toddle school {row['new_school']}"
        print(msg)
        # Uncomment below to send emails
        # send_email_alert(msg)

if __name__ == "__main__":
    run()