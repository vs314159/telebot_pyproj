from messages import Messages


class CallbackInfo:
    def __init__(self, msg='⬇️', btn_name=None, next_calls=None, back_opt=None, url=None):
        self.msg = msg
        self.btn_name = btn_name
        self.next_calls = next_calls
        self.back_opt = back_opt
        self.url = url


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
            'price': CallbackInfo(btn_name='Ціна навчання',
                                  back_opt='guest',
                                 ),
            'guest_format': CallbackInfo(msg=msgs.guest_format,
                                         btn_name='Формат навчання',
                                         next_calls=('guest_solo', 'guest_duet', 'guest_group'),
                                         back_opt='guest',
                                        ),
                'guest_solo': CallbackInfo(msg=msgs.guest_solo,
                                           btn_name='Індивідуальний',
                                           back_opt='guest_format',
                                           ),
                'guest_duet': CallbackInfo(msg=msgs.guest_duet,
                                           btn_name='У парі',
                                           back_opt='guest_format',
                                           ),
                'guest_group': CallbackInfo(msg=msgs.guest_group,
                                            btn_name='У групі',
                                            back_opt='guest_format',
                                            ),
            'test_level': CallbackInfo(btn_name='Дізнатись свій рівень англійської',
                                       back_opt='guest',
                                       ),
                 }
