"""
סקריפט זרע לאכלוס מסד נתונים EmoBridge בנתוני בדיקה ריאליסטיים.
מוסיף רגשות, משתמשים, סשנים ומשחקים עם מגמת שיפור לאורך זמן.
הרץ מתוך תיקיית server: python seed.py
"""

import asyncio
import random
from datetime import datetime, timedelta

from sqlalchemy import text

from app.db import async_session, engine
from app.models import Base, Emotion, GameTrial, Image, LearningSession, User
from app.services.auth_service import get_password_hash

# ---------------------------------------------------------------------------
# נתוני רגשות: שם בעברית, אמוג'י, צבע Hex
# ---------------------------------------------------------------------------
EMOTIONS_DATA = [
    {"name": "שמחה",    "emoji": "😊", "color": "#FFD700"},
    {"name": "עצב",     "emoji": "😢", "color": "#4682B4"},
    {"name": "כעס",     "emoji": "😠", "color": "#DC143C"},
    {"name": "פחד",     "emoji": "😨", "color": "#8B008B"},
    {"name": "הפתעה",   "emoji": "😲", "color": "#FF8C00"},
    {"name": "גועל",    "emoji": "🤢", "color": "#556B2F"},
    {"name": "אהבה",    "emoji": "🥰", "color": "#FF69B4"},
    {"name": "בושה",    "emoji": "😳", "color": "#FF6347"},
    {"name": "גאווה",   "emoji": "😤", "color": "#20B2AA"},
    {"name": "שלווה",   "emoji": "😌", "color": "#98FB98"},
]

# ---------------------------------------------------------------------------
# נתוני משתמשים: שמות ישראליים, מיילים, סיסמה זהה לכולם לצורכי בדיקה
# ---------------------------------------------------------------------------
USERS_DATA = [
    {"username": "אבי כהן",    "email": "avi.cohen@example.com"},
    {"username": "שירה לוי",   "email": "shira.levi@example.com"},
    {"username": "מיכאל ברק",  "email": "michael.barak@example.com"},
    {"username": "נועה פרידמן","email": "noa.friedman@example.com"},
    {"username": "יונתן שפירא","email": "yonatan.shapira@example.com"},
]

DEFAULT_PASSWORD = "Password123!"

# ---------------------------------------------------------------------------
# קבועים לבניית מגמת שיפור
# ---------------------------------------------------------------------------
SESSIONS_PER_USER = 4          # מספר סשנים לכל משתמש
TRIALS_PER_SESSION = 8         # מספר ניסיונות בכל סשן
BASE_RESPONSE_TIME_MS = 5000   # זמן תגובה התחלתי (5 שניות)
RESPONSE_TIME_REDUCTION = 400  # הפחתת זמן תגובה בין סשנים (ms)
BASE_CORRECT_RATE = 0.35       # אחוז הצלחה ראשוני
CORRECT_RATE_STEP = 0.15       # שיפור באחוז ההצלחה בין סשנים

SCORE_CORRECT = 10
SCORE_WRONG = 0


async def clear_existing_data(session) -> None:
    """מחיקת כל הנתונים הקיימים לפני זריעה מחודשת.
    אין צורך ב-commit — הטרנזקציה מנוהלת על-ידי session.begin() ב-main."""
    await session.execute(text("DELETE FROM game_trials"))
    await session.execute(text("DELETE FROM learning_sessions"))
    await session.execute(text("DELETE FROM images"))
    await session.execute(text("DELETE FROM users"))
    await session.execute(text("DELETE FROM emotions"))


async def seed_emotions(session) -> list[Emotion]:
    """יצירת 10 רגשות בסיסיים עם שמות בעברית."""
    emotions = []
    for data in EMOTIONS_DATA:
        emotion = Emotion(
            name=data["name"],
            emoji=data["emoji"],
            color=data["color"],
        )
        session.add(emotion)
        emotions.append(emotion)
    await session.flush()
    print(f"  נוצרו {len(emotions)} רגשות.")
    return emotions


async def seed_images(session, emotions: list[Emotion]) -> list[Image]:
    """
    יצירת 3 תמונות לדוגמה לכל רגש.
    ה-URL מדמה תמונות placeholder עם מזהה הרגש.
    """
    images = []
    for emotion in emotions:
        for idx in range(1, 4):
            image = Image(
                url=f"https://placehold.co/400x400?text={emotion.name}_{idx}",
                emotion_id=emotion.id,
            )
            session.add(image)
            images.append(image)
    await session.flush()
    print(f"  נוצרו {len(images)} תמונות.")
    return images


def _get_images_for_emotion(images: list[Image], emotion_id: int) -> list[Image]:
    """מסנן תמונות השייכות לרגש מסוים."""
    return [img for img in images if img.emotion_id == emotion_id]


async def seed_users_with_sessions(
    session,
    emotions: list[Emotion],
    images: list[Image],
) -> None:
    """
    יצירת משתמשים עם LearningSessions ו-GameTrials.
    הנתונים מדמים מגמת שיפור: כל סשן מאוחר יותר מראה יותר תשובות נכונות
    וזמן תגובה קצר יותר.
    """
    hashed_pw = get_password_hash(DEFAULT_PASSWORD)

    for user_data in USERS_DATA:
        user = User(
            username=user_data["username"],
            email=user_data["email"],
            hashed_password=hashed_pw,
            created_at=datetime.utcnow() - timedelta(days=30),
        )
        session.add(user)
        await session.flush()

        session_start = datetime.utcnow() - timedelta(days=SESSIONS_PER_USER * 7)

        for session_idx in range(SESSIONS_PER_USER):
            # כל סשן מאוחר יותר → שיפור בביצועים
            correct_rate = min(BASE_CORRECT_RATE + session_idx * CORRECT_RATE_STEP, 0.95)
            avg_response_time = max(
                BASE_RESPONSE_TIME_MS - session_idx * RESPONSE_TIME_REDUCTION,
                800,
            )

            session_start_dt = session_start + timedelta(days=session_idx * 7)
            session_end_dt = session_start_dt + timedelta(minutes=random.randint(10, 25))

            learning_session = LearningSession(
                user_id=user.id,
                started_at=session_start_dt,
                ended_at=session_end_dt,
            )
            session.add(learning_session)
            await session.flush()

            for trial_idx in range(TRIALS_PER_SESSION):
                # בחירת רגש נכון ותמונה תואמת
                correct_emotion = random.choice(emotions)
                emotion_images = _get_images_for_emotion(images, correct_emotion.id)
                if not emotion_images:
                    continue
                chosen_image = random.choice(emotion_images)

                # קביעת תשובת המשתמש: מגמת שיפור לאורך הסשנים
                is_correct = random.random() < correct_rate
                if is_correct:
                    selected_emotion = correct_emotion
                else:
                    distractors = [e for e in emotions if e.id != correct_emotion.id]
                    selected_emotion = random.choice(distractors)

                # זמן תגובה עם שונות אקראית קטנה סביב הממוצע
                jitter = random.randint(-300, 300)
                response_time = max(300, avg_response_time + jitter)

                trial = GameTrial(
                    session_id=learning_session.id,
                    image_id=chosen_image.id,
                    correct_emotion_id=correct_emotion.id,
                    selected_emotion_id=selected_emotion.id,
                    is_correct=is_correct,
                    score=SCORE_CORRECT if is_correct else SCORE_WRONG,
                    response_time_ms=response_time,
                )
                session.add(trial)

        print(
            f"  נוצר משתמש '{user.username}' עם {SESSIONS_PER_USER} סשנים "
            f"× {TRIALS_PER_SESSION} ניסיונות."
        )

    await session.flush()


async def main() -> None:
    """נקודת הכניסה הראשית: יוצרת את כל טבלאות ה-DB ומאכלסת נתוני בדיקה."""
    print("=== EmoBridge Seed ===")
    print("משחזר סכמת DB (drop + create) כדי להבטיח עמודות עדכניות...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        async with session.begin():
            print("DB נקי — מדלג על מחיקה ידנית.")
            # לאחר drop_all + create_all הטבלאות ריקות; אין צורך ב-DELETE

            print("זורע רגשות...")
            emotions = await seed_emotions(session)

            print("זורע תמונות...")
            images = await seed_images(session, emotions)

            print("זורע משתמשים, סשנים וניסיונות...")
            await seed_users_with_sessions(session, emotions, images)

        print("\n=== Seed הושלם בהצלחה! ===")
        print(f"  רגשות: {len(EMOTIONS_DATA)}")
        print(f"  תמונות: {len(EMOTIONS_DATA) * 3}")
        print(f"  משתמשים: {len(USERS_DATA)}")
        print(f"  סשנים: {len(USERS_DATA) * SESSIONS_PER_USER}")
        print(
            f"  ניסיונות (מקסימום): "
            f"{len(USERS_DATA) * SESSIONS_PER_USER * TRIALS_PER_SESSION}"
        )
        print(f"\n  סיסמה לכל המשתמשים: {DEFAULT_PASSWORD}")


if __name__ == "__main__":
    asyncio.run(main())
