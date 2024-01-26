import aiosqlite

async def update_user_in_db(user_id, login):
    async with aiosqlite.connect("users.db") as db:
        await db.execute(
            "UPDATE users SET login = ? WHERE user_id = ?", (login, user_id)
        )
        await db.commit()