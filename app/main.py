from app.gmail.reader import get_latest_emails


def main():

    print("\n====================================")
    print("       EMAIL WHATSAPP BOT")
    print("====================================\n")

    print("Fetching latest emails...\n")

    emails = get_latest_emails(max_results=5)

    if not emails:
        print("No emails found.")
        return

    for index, email in enumerate(emails, start=1):

        print("------------------------------------")
        print(f"Email #{index}")
        print("------------------------------------")

        print(f"From    : {email['sender']}")
        print(f"Subject : {email['subject']}")
        print(f"Date    : {email['date']}")

        print("\nBody:")
        print(email["body"][:500])

        print()


if __name__ == "__main__":
    main()