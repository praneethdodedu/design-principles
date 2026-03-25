"""
Separation of Concerns (SoC)
============================
Each class/module should have ONE responsibility and handle ONE concern.
Don't mix data management, persistence, presentation, and business logic in one class.
"""

import os
from datetime import datetime


# ============================================================================
# BAD APPROACH - Violates Separation of Concerns
# ============================================================================
# This class does TOO MUCH: manages entries, saves to file, loads from file,
# formats output, and sends emails. All concerns mixed together!

class JournalBad:
    """
    This class violates SoC!
    It handles: data, persistence, formatting, and notifications.
    """
    
    def __init__(self):
        self.entries = []
        self.count = 0

    def add_entry(self, text):
        self.count += 1
        self.entries.append(f"{self.count}: {text}")

    def remove_entry(self, index):
        del self.entries[index]

    # BAD: Persistence concern mixed with data management
    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            f.write('\n'.join(self.entries))

    def load_from_file(self, filename):
        with open(filename, 'r') as f:
            self.entries = f.read().split('\n')

    # BAD: Formatting concern mixed in
    def format_as_html(self):
        html = "<html><body><ul>"
        for entry in self.entries:
            html += f"<li>{entry}</li>"
        html += "</ul></body></html>"
        return html

    # BAD: Notification concern mixed in
    def send_email_notification(self, email):
        print(f"Sending journal to {email}...")  # Imagine email logic here


# ============================================================================
# GOOD APPROACH - Proper Separation of Concerns
# ============================================================================

# Concern 1: Data Management (Core Domain)
class Journal:
    """
    Single responsibility: Manage journal entries.
    Does NOT know about files, formatting, or notifications.
    """
    
    def __init__(self):
        self.entries = []
        self.count = 0

    def add_entry(self, text):
        self.count += 1
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.entries.append(f"{self.count}. [{timestamp}] {text}")

    def remove_entry(self, index):
        if 0 <= index < len(self.entries):
            del self.entries[index]
            # Re-number entries
            for i, entry in enumerate(self.entries):
                parts = entry.split('. ', 1)
                if len(parts) > 1:
                    self.entries[i] = f"{i + 1}. {parts[1]}"
            self.count = len(self.entries)

    def __str__(self):
        return '\n'.join(self.entries)

    def __len__(self):
        return len(self.entries)

    def __iter__(self):
        return iter(self.entries)


# Concern 2: Persistence
class PersistenceManager:
    """
    Single responsibility: Save and load data to/from files.
    Works with ANY object that has entries, not just Journal.
    """
    
    @staticmethod
    def save_to_file(journal, filename):
        with open(filename, 'w') as f:
            f.write(str(journal))
        print(f"  Saved {len(journal)} entries to '{filename}'")

    @staticmethod
    def load_from_file(filename):
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File '{filename}' not found")
        
        journal = Journal()
        with open(filename, 'r') as f:
            lines = f.read().strip().split('\n')
            for line in lines:
                if line:
                    # Extract text after the timestamp
                    parts = line.split('] ', 1)
                    if len(parts) > 1:
                        journal.add_entry(parts[1])
                    else:
                        journal.add_entry(line)
        return journal


# Concern 3: Formatting / Presentation
class JournalFormatter:
    """
    Single responsibility: Format journal for different outputs.
    """
    
    @staticmethod
    def to_plain_text(journal):
        return str(journal)

    @staticmethod
    def to_html(journal):
        html_lines = [
            "<!DOCTYPE html>",
            "<html>",
            "<head><title>My Journal</title></head>",
            "<body>",
            "<h1>Journal Entries</h1>",
            "<ul>"
        ]
        for entry in journal:
            html_lines.append(f"  <li>{entry}</li>")
        html_lines.extend(["</ul>", "</body>", "</html>"])
        return '\n'.join(html_lines)

    @staticmethod
    def to_markdown(journal):
        md_lines = ["# Journal Entries", ""]
        for entry in journal:
            md_lines.append(f"- {entry}")
        return '\n'.join(md_lines)

    @staticmethod
    def to_json(journal):
        import json
        return json.dumps({
            "entries": list(journal),
            "count": len(journal)
        }, indent=2)


# Concern 4: Notifications
class NotificationService:
    """
    Single responsibility: Handle notifications.
    """
    
    @staticmethod
    def send_email(recipient, subject, body):
        # In real code, this would use smtplib or an email service
        print(f"  Email sent to: {recipient}")
        print(f"  Subject: {subject}")
        print(f"  Body preview: {body[:50]}...")

    @staticmethod
    def send_sms(phone_number, message):
        # In real code, this would use Twilio or similar
        print(f"  SMS sent to: {phone_number}")
        print(f"  Message: {message[:50]}...")


# Concern 5: Statistics / Analytics
class JournalAnalytics:
    """
    Single responsibility: Analyze journal data.
    """
    
    @staticmethod
    def word_count(journal):
        total = 0
        for entry in journal:
            # Skip the number and timestamp prefix
            parts = entry.split('] ', 1)
            if len(parts) > 1:
                total += len(parts[1].split())
        return total

    @staticmethod
    def entry_count(journal):
        return len(journal)

    @staticmethod
    def average_words_per_entry(journal):
        count = len(journal)
        if count == 0:
            return 0
        return JournalAnalytics.word_count(journal) / count


# ============================================================================
# Demo / Usage
# ============================================================================

def main():
    print("=" * 60)
    print("SEPARATION OF CONCERNS DEMONSTRATION")
    print("=" * 60)

    # Create journal (Concern 1: Data Management)
    print("\n1. Creating journal and adding entries...")
    journal = Journal()
    journal.add_entry("I started learning design patterns today")
    journal.add_entry("Separation of Concerns makes code cleaner")
    journal.add_entry("Each class should have one responsibility")
    
    print(f"\nJournal contents:\n{journal}")

    # Save to file (Concern 2: Persistence)
    print("\n" + "-" * 40)
    print("2. Saving to file (Persistence concern)...")
    filename = "my_journal.txt"
    PersistenceManager.save_to_file(journal, filename)

    # Format differently (Concern 3: Formatting)
    print("\n" + "-" * 40)
    print("3. Format as HTML (Formatting concern):")
    print(JournalFormatter.to_html(journal))

    print("\n" + "-" * 40)
    print("4. Format as Markdown:")
    print(JournalFormatter.to_markdown(journal))

    print("\n" + "-" * 40)
    print("5. Format as JSON:")
    print(JournalFormatter.to_json(journal))

    # Analytics (Concern 5: Analytics)
    print("\n" + "-" * 40)
    print("6. Analytics (Analytics concern):")
    print(f"  Total entries: {JournalAnalytics.entry_count(journal)}")
    print(f"  Total words: {JournalAnalytics.word_count(journal)}")
    print(f"  Avg words/entry: {JournalAnalytics.average_words_per_entry(journal):.1f}")

    # Notifications (Concern 4: Notifications)
    print("\n" + "-" * 40)
    print("7. Send notification (Notification concern):")
    NotificationService.send_email(
        "user@example.com",
        "Your Journal Backup",
        str(journal)
    )

    # Load from file
    print("\n" + "-" * 40)
    print("8. Load from file (Persistence concern):")
    loaded_journal = PersistenceManager.load_from_file(filename)
    print(f"  Loaded {len(loaded_journal)} entries")

    # Cleanup
    if os.path.exists(filename):
        os.remove(filename)

    print("\n" + "=" * 60)
    print("KEY TAKEAWAY:")
    print("=" * 60)
    print("""
Each class has ONE concern:
- Journal         → Manages entry data
- PersistenceManager → Handles file I/O
- JournalFormatter   → Formats output
- NotificationService → Sends notifications
- JournalAnalytics   → Analyzes data

Benefits:
1. Easier to test (mock one concern at a time)
2. Easier to change (swap file storage for database)
3. Easier to reuse (PersistenceManager works with any data)
4. Easier to understand (each class is focused)
""")


if __name__ == "__main__":
    main()
