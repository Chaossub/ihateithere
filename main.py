from handlers import (
    moderation,
    federation,
    summon,
    fun,
    welcome,
    help_cmd,
    test  # ✅ this is required
)

# Register handlers
moderation.register(app)
federation.register(app)
summon.register(app)
fun.register(app)
welcome.register(app)
help_cmd.register(app)
test.register(app)  # ✅ register the test handler

