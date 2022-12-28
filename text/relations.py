from collections import namedtuple


relations = dict()
relations['/start'] = ('student', 'guest')
relations['student'] = ('feedback', 'payment', 'remains')
relations['payment'] = ('solo', 'duet', 'group')
#relations['remains'] = ('name_student',)
relations['guest'] = ('price', 'guest_format', 'test_level')
relations['guest_format'] = ('guest_solo', 'guest_duet', 'guest_group')


start_message = '''
Hey! Вітаємо у Futurium English School боті - твоєму помічнику на шляху у вивченні англійської💛
Щоб ми могли вам краще допомогти - підкажіть нам ваш статус у школі ⬇️.
'''
student_message = 'Добре! Яке у вас питання?'
payment_message = 'Звісно! Який у вас формат навчання?'
format_message = 'За скільки занять ви хочете внести оплату?'
remains_message = 'Введіть своє Імя та Прізвище у такому форматі українською мовою: Петро Петренко'
guest_message = 'Клас! Будемо раді вам допомогти із вивченням англійської🤞 Що саме вам цікаво дізнатись про навчання?'
guest_solo_message = '''
Для тих, хто постійно на робочих зустрічах та хоче мати гнучкий графік та програму, побудовану саме під вас!
Теми: IT, Business, Blogging, Fashion etc.

Чому індивідуальне навчання?
1️⃣ Самостійно обираєте тривалість занять, за потреби можна міксувати час у різні дні
2️⃣ Разом із викладачем створюєте програму та обираєте матеріали, які будуть цікаві саме вам
3️⃣ Інтерактивне навчання та свій онлайн словник

💰3000 грн/8 занять
'''
guest_duet_message = '''
Навчання із колегою, коханою людиною або друзями - це можливість круто та з користю провести час!

Чому навчання у парі?
1️⃣ Навчання із близькою людиною = подвійна мотивація
2️⃣ Персональний трекінг прогресу - ви матимите змогу відстежувати свій прогрес від самого початку курсу, що надасть змогу вам сфокусуватись саме на тих аспектах вивчення мови, які потрібні саме вам.
3️⃣ Інтерактивне навчання із використанням сучасних матеріалів. 

💰2200 грн/8 занять
'''
guest_group_message ='''
Навчання у міні-групі - це можливість швидко подолати мовний бар'єр та розвочати говорити уже у перший місяць занять! Цікаво, доступно, інтерактивно🤩

Чому навчання у міні-групі?
1️⃣ Максимум комунікації на занятті - робота у групах, парах, презентації
2️⃣ Круте ком'юніті! Групове навчання - це не тільки можливість познайомитись із різними людьми, це також шалена мотивація та підтримка.
3️⃣ Інтерактивне навчання із використанням сучасних матеріалів. Ми міксуємо кембриджські/оскфордські матеріали із аутентичними відео та статтями, які не тільки підвищують ваш словниковий запас, але й розширюють ваш кругозір.

💰1950 грн/8 занять
'''
guest_format_message = '''
Формат навчання залежить від ваших цілей, вашого рівня та ще низки факторів. 
У нас в школі ви можете обрати як індивідуальне навчання, так і навчання у парі або у міні групі. 
Про який формат навчання ви хотіли б дізнатись детальніше?'''



info_template = namedtuple('Info', 'btn_name message')
info_dict = {'/start': info_template('/start', start_message),
                'student': info_template('Студент🎓', student_message),
                    'payment': info_template('Хочу оплатити навчання💰', payment_message),
                        'solo': info_template('Індивідуальне', format_message),
                        'duet': info_template('У парі', format_message),
                        'group': info_template('У групі', format_message),
                    'feedback': info_template('Хочу залишити анонімний відгук про навчання📝', ''),
                    'remains': info_template('Хочу дізнатись кількість занять, які у мене залишились📚', remains_message),
             'guest': info_template('Хочу навчатись!🤓', guest_message),
                'price': info_template('Ціна навчання', ''),
                'guest_format': info_template('Формат навчання', guest_format_message),
                    'guest_solo': info_template('Індивідуальне', guest_solo_message),
                    'guest_duet': info_template('У парі', guest_duet_message),
                    'guest_group': info_template('У групі', guest_group_message),
                'test_level': info_template('Хочу дізнатись свій рівень англійської', ''),
             }