from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()

@router.callback_query(F.data.startswith("duration_"))
async def duration_callback(callback: CallbackQuery):

    duration = callback.data.split("_")[1]

    await callback.message.edit_text(
        f"✅ Clip Duration Selected: {duration} seconds\n\n"
        "Now select number of clips:\n"
        "3 • 5 • 10"
    )

    await callback.answer()
