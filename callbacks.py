from messages import Messages


class CallbackInfo:
    """
    Клас, що містить інформацію про колбек
    msg - повідомлення, що надсилатиметься, коли користувач натиснув інлайн-кнопку
    btn_name - назва кнопки, натискання на яку і викликає даний колбек (міститься у 'попередньому' колбеці)
    next_calls - інлайн-кнопки, що виведуться разом з msg
    back_opt - колбек кнопки '< Назад', що виведеться разом з msg
    url - посилання, яке може містити інлайн-кнопка
    """
    def __init__(self, msg='⬇️', btn_name=None, next_calls=None, back_opt=None, url=None):
        self.msg = msg
        self.btn_name = btn_name
        self.next_calls = next_calls
        self.back_opt = back_opt
        self.url = url


# Словник з усіма колбеками
msgs = Messages()
callback_info = {
    '/start': CallbackInfo(msg=msgs.start,
                           next_calls=('student', 'guest')
                           ),
        'student': CallbackInfo(msg=msgs.student,
                                btn_name='Студент🎓',
                                next_calls=('feedback', 'auth'),
                                back_opt='/start',
                                ),
        'feedback': CallbackInfo(btn_name='Анонімний відгук про навчання📝',
                                 url='www.google.com',
                                 back_opt='student',
                                 ),
        'auth': CallbackInfo(msg=msgs.auth,
                             btn_name='Заняття 📚',
                             back_opt='student',
                             ),
        'auth_done': CallbackInfo(msg=msgs.auth_done,
                                  next_calls=('payment', 'remains'),
                                  back_opt='student',
                                  ),
            'payment': CallbackInfo(msg=msgs.payment,
                                    btn_name='Оплата навчання💰',
                                    next_calls=('solo', 'duet', 'group'),
                                    back_opt='auth_done',
                                    ),
                'solo': CallbackInfo(btn_name='Індивідуальний',
                                     back_opt='auth_done',
                                     ),
                'duet': CallbackInfo(btn_name='У парі',
                                     back_opt='auth_done',
                                     ),
                'group': CallbackInfo(btn_name='У групі',
                                      back_opt='auth_done',
                                      ),
            'remains': CallbackInfo(btn_name='Лишилось занять 📚',
                                    back_opt='auth_done',
                                    ),
        'guest': CallbackInfo(msg=msgs.guest,
                              btn_name='Хочу навчатись!🤓',
                              next_calls=('price', 'guest_format', 'test_level'),
                              back_opt='/start',
                              ),
            'price': CallbackInfo(msg=msgs.price,
                                  btn_name='Ціна навчання',
                                  next_calls=('more_prices',),
                                  back_opt='guest',
                                  ),
                'more_prices': CallbackInfo(msg=msgs.price,
                                            btn_name='Далі >',
                                            next_calls=('more_prices',),
                                            back_opt='guest',
                                            ),
            'guest_format': CallbackInfo(msg=msgs.guest_format,
                                         btn_name='Формат навчання',
                                         next_calls=('guest_solo', 'guest_duet', 'guest_group'),
                                         back_opt='guest',
                                         ),
                'guest_solo': CallbackInfo(msg=msgs.guest_solo,
                                           btn_name='Індивідуальний',
                                           next_calls=('trial',),
                                           back_opt='guest_format',
                                           ),
                'guest_duet': CallbackInfo(msg=msgs.guest_duet,
                                           btn_name='У парі',
                                           next_calls=('trial',),
                                           back_opt='guest_format',
                                           ),
                'guest_group': CallbackInfo(msg=msgs.guest_group,
                                            btn_name='У групі',
                                            next_calls=('trial',),
                                            back_opt='guest_format',
                                            ),
                    'trial': CallbackInfo(btn_name='Записатись на пробне заняття✍️',
                                          url='www.google.com',  # змінити на введення даних, а не посилання
                                          back_opt='guest_format',
                                          ),
            'test_level': CallbackInfo(btn_name='Дізнатись свій рівень англійської',
                                       back_opt='guest',
                                       ),
                 }
