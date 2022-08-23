HELP_MESSAGE = """ Hello, I'm util_bot, I can help you with many different things!
Send /help to see this message again.

Available commands (More commands can be found by just typing / and using auto-complete):
/help - show this message

/remind <text to remember> - set a timer to send <text> after a time you specify
Example of a valid time: 'in 1 day 1 month 1 hour'

/rand <start> <end> - choose a number between <start> and <end>

/pexels - fetch a random photo from Pexels

/pexels <search> - search for a photo on Pexels

/unsplash - fetch a random photo from Unsplash

/unsplash <search> - search for a photo on Unsplash

/lang - change the language of the bot (English or Arabic)
-------------------------------------------------
Store commands:
/mystore - show info you saved in the your store
/put <key> <value> - save <value> with key <key>
/get <key> - show the value saved with key <key>
/del <key> - delete the value saved with key <key>
-------------------------------------------------
This is it for now!
"""

HELP_MESSAGE_ARABIC = """
مرحباً! أنا بوت مساعد، أستطيع القيام بالعديد من المهام

الأوامر المتوفرة (يمكنك استخدام أوامر أخرى بالضغط على / واستخدام الإكمال التلقائي):
/help - عرض هذه الرسالة

/remind <النص الذي تريد أن أذكرك به> -
يمكنني تذكيرك بنص ما بعد وقت محدد أنت تحدده
مثال عن الوقت بالعربية
'خلال 1 شهر 1 يوم 1 ساعة'

/die - قم برمي نرد واحصل على نتيجة

/rand قم بالحصول على عدد عشوائي بين رقمين تدخلهم بعد الأمر بينهما مسافة

/pexels
قم بالحصول على صورة عشوائية من موقع Pexels
أو أدخل نصاً بعد الأمر للبحث عنه في الموقع

/unsplash
قم بالحصول على صورة عشوائية من موقع Unsplash
أو أدخل نصاً بعد الأمر للبحث عنه في الموقع

/lang - تغيير لغة البوت (الإنجليزية أو العربية)
-------------------------------------------------
أوامر تخزين البيانات الخاصة بك:
/mystore - عرض معلوماتك المحفوظة في مخزنك
/put - خزن قيمة معينة في المخزن (قم بوضع اسم وبعده قيمة)
/get - عرض القيمة المحفوظة في المخزن (قم بوضع اسم)
/del - حذف قيمة (قم بوضع اسم القيمة التي تريد حذفها)
-------------------------------------------------
هذا كل شيء حتى الآن!
"""

WOLFRAM_HELP="""These commands use the WolframAlpha API to answer different questions and solve equations.

The commands are:
/quick <question> - ask WolframAlpha any quick question.

/eq <equation> - solve an equation with step-by-step instructions.

/bool <expression> - solve a boolean expression.

/plot <function> - plot a one-dimensional function.

/3dplot <function> - plot a two-dimensional function.
"""

WOLFRAM_HELP_ARABIC="""هذه الأوامر تستخدم الAPI الخاص بWolframAlpha.

الأوامر المتوفرة:
/quick <question> - اسأل أي سؤال عام للإجابة عليه مثلاً عاصمة بلد ما
(البحث باللغة الإنجليزية فقط، الموقع لا يدعم اللغة العربية.)

/eq <equation> - حل معادلة رياضية ما.

/bool <expression> - حل تعبير بولياني أو منطقي.

/plot <function> - رسم تابع لمتحول واحد.

/3dplot <function> - رسم ثلاثي الأبعاد لتابع  لمتحولين.
"""