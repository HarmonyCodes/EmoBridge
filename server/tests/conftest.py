import os

# הגדרת משתני סביבה לפני ייבוא האפליקציה.
# Settings דורש ערכים אלו כשדות חובה, ובלעדיהם ייבוא app נכשל.
# setdefault שומר על ערכים שהוגדרו מבחוץ (למשל ב-CI).
_TEST_ENV = {
    "DB_USER": "test_user",
    "DB_PASSWORD": "test_password",
    "DB_HOST": "localhost",
    "DB_PORT": "5432",
    "DB_NAME": "emobridge_test",
    "SECRET_KEY": "test-secret-key-not-used-in-production",
}

for key, value in _TEST_ENV.items():
    os.environ.setdefault(key, value)
