class Messages:
    """
    Клас, що містить текст повідомлень, що надсилатимуться ботом.
    Назва атрибуту повинна збігатися з назвою колбеку, якому він відповідає
    (назва тексту повідомлення має збігатися з назвою колбеку, яке має
    надіслати даний текст повідомлення)
    """
    start = '''
Hey! Вітаємо у Futurium English School боті - твоєму помічнику на шляху у вивченні англійської💛
Щоб ми могли вам краще допомогти - підкажіть нам ваш статус у школі ⬇️.
'''

    student = 'Добре! Яке у вас питання?'

    payment = 'Звісно! Який у вас формат навчання?'

    format = 'За скільки занять ви хочете внести оплату?'

    auth = 'Введіть своє Ім`я та Прізвище у такому форматі українською мовою: Петро Петренко'

    guest = 'Клас! Будемо раді вам допомогти із вивченням англійської🤞 Що саме вам цікаво дізнатись про навчання?'

    price = 'На разі доступні такі варіанти ☝️'

    guest_solo = '''
Для тих, хто постійно на робочих зустрічах та хоче мати гнучкий графік та програму, побудовану саме під вас!
Теми: IT, Business, Blogging, Fashion etc.

Чому індивідуальне навчання?
1️⃣ Самостійно обираєте тривалість занять, за потреби можна міксувати час у різні дні
2️⃣ Разом із викладачем створюєте програму та обираєте матеріали, які будуть цікаві саме вам
3️⃣ Інтерактивне навчання та свій онлайн словник

💰3000 грн/8 занять
'''

    guest_duet = '''
Навчання із колегою, коханою людиною або друзями - це можливість круто та з користю провести час!

Чому навчання у парі?
1️⃣ Навчання із близькою людиною = подвійна мотивація
2️⃣ Персональний трекінг прогресу - ви матимите змогу відстежувати свій прогрес від самого початку курсу, що надасть змогу вам сфокусуватись саме на тих аспектах вивчення мови, які потрібні саме вам.
3️⃣ Інтерактивне навчання із використанням сучасних матеріалів. 

💰2200 грн/8 занять
'''

    guest_group = '''
Навчання у міні-групі - це можливість швидко подолати мовний бар'єр та розвочати говорити уже у перший місяць занять! Цікаво, доступно, інтерактивно🤩

Чому навчання у міні-групі?
1️⃣ Максимум комунікації на занятті - робота у групах, парах, презентації
2️⃣ Круте ком'юніті! Групове навчання - це не тільки можливість познайомитись із різними людьми, це також шалена мотивація та підтримка.
3️⃣ Інтерактивне навчання із використанням сучасних матеріалів. Ми міксуємо кембриджські/оскфордські матеріали із аутентичними відео та статтями, які не тільки підвищують ваш словниковий запас, але й розширюють ваш кругозір.

💰1950 грн/8 занять
'''

    guest_format = '''
Формат навчання залежить від ваших цілей, вашого рівня та ще низки факторів. 
У нас в школі ви можете обрати як індивідуальне навчання, так і навчання у парі або у міні групі. 
Про який формат навчання ви хотіли б дізнатись детальніше?'''

    auth_done = 'Раді Вас бачити, '
