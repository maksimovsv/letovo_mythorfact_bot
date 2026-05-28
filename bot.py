import telebot 
from telebot import types 
import time 
import os

API_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(API_TOKEN)  
 
quiz_data = [ 
    { 
        'question': 'Обучение в школе «Летово» проводится 5 дней в неделю', 
        'answer': False, 
        'description': 'В школе Летово учебная неделя состоит из шести дней, при этом занятия в субботу начинаются в 9:00. А с понедельника по пятницу - в 8:30' 
    }, 
    { 
        'question': 'Обязательный недельный минимум физической активности в школе «Летово» составляет шесть часов.', 
        'answer': True, 
        'description': 'В Летово еженедельно требуется не менее шести часов занятий спортом, из которых два часа составляют обязательная физическая культура, два часа — обязательные игровые виды спорта, а еще два часа можно выбрать самостоятельно. Доступные варианты включают футбол, баскетбол, волейбол, теннис, плавание, чирлидинг, историческое фехтование, акробатику, фитнес и бокс…' 
    }, 
    { 
        'question': 'В школе «Летово» организовано только трехразовое питание.', 
        'answer': False, 
        'description': 'В Летово организовано пятиразовое питание, включающее завтрак, обед, полдник, ужин и сонник. На завтрак предоставляется шесть различных блюд, а также овощи и каши. В меню обеда и ужина на выбор предлагаются два вида салатов, пять видов овощей, три различных гарнира, основное блюдо (мясо, птица или рыба) и три вида супов. К каждому приему пищи предоставляются три различных напитка.' 
    }, 
    { 
        'question': 'Помимо обязательных английского и русского языков, студентам доступен для изучения один из двух дополнительных иностранных языков.', 
        'answer': False, 
        'description': 'В Летово учащиеся могут изучать три языка, из которых русский и английский являются обязательными, а третий можно выбрать из следующих: немецкий, французский, испанский или китайский. Также существуют «внеакадемы» — дополнительные занятия по выбору после обязательных уроков, на которых можно изучить иврит, японский, старорусский и многие другие языки.' 
    }, 
    { 
        'question': 'В школе «Летово» действует десятибалльная система оценивания знаний.', 
        'answer': False, 
        'description': 'В Летово организована 8ми балльная система оценивания. Для каждой оценки установлены критерии, обеспечивающие независимость оценки знаний учащихся.' 
    }, 
    { 
        'question': 'Спортивная инфраструктура позволяет трансформировать большой зал в три отдельные площадки.', 
        'answer': True, 
        'description': 'В Летово имеется один малый спортивный зал, зал единоборств, зал аэробики, бассейн, тренажерный зал, а также один большой спортивный зал, который можно разделить на три отдельных секции. Кроме того, на прилегающей территории расположено футбольное поле, где в теплый период года могут проводиться занятия физической культурой.' 
    }, 
    { 
        'question': 'Кампус школы «Летово» оснащен системой подземных переходов между корпусами.', 
        'answer': True, 
        'description': 'В Летово действительно существуют подземные переходы, соединяющие жилые дома и школу, что позволяет учащимся в суровых погодных условиях быстро добраться до учебного заведения, не подвергая свое здоровье риску.' 
    }, 
    { 
        'question': 'В школе «Летово» представлено всего восемь устоявшихся профильных направлений обучения.', 
        'answer': True, 
        'description': 'В Летово присутствует система ИУПов (индивидуальные учебные планы), что предоставляет ученикам выбор профиля из следующих предметов — математика, физика, информатика, экономика, химия, биология, иностранные языки, география, история, искусство, общество и литература. Но в Летово уже есть и готовые профильные направления — МатЭк, ФизМат, МатIT, МатITML (machine learning), ХимФиз, ХимБио, БиоХим, БиоIT, ФилОбщ, ФилИн, СоцЭк, СоцГео, ГеоИст, ФилArts, СоцГум.' 
    }, 
    { 
        'question': 'Прием в школу «Летово» осуществляется исключительно для детей, проживающих в близлежащих районах.', 
        'answer': False,'description': 'В Летово учатся подростки со всей России и не только. Для этого проводятся дистанционные экзамены, а на территории школы есть пансион, в котором ученики живут от каникул до каникул или в течение учебной недели.' 
    } 
] 
 
user_states = {} 
 
@bot.message_handler(commands=['start']) 
def start_quiz(message): 
    user_id = message.from_user.id 
    user_states[user_id] = {'current_index': 0, 'score': 0} 
 
    bot.send_message( 
        message.chat.id, 
        "🎓 *Викторина «Летово: Миф или Реальность»*\n\n" 
        "Проверьте свои знания об одной из ведущих школ страны. " 
        "Отвечайте «Правда» или «Миф» на каждое утверждение.\n\n" 
        "Начнем!", 
        parse_mode="Markdown" 
    ) 
    send_question(message.chat.id, user_id) 
 
def send_question(chat_id, user_id): 
    user_data = user_states.get(user_id) 
    if not user_data: 
        return 
 
    current_index = user_data['current_index'] 
 
    if current_index >= len(quiz_data): 
        finish_quiz(chat_id, user_id) 
        return 
 
    question_data = quiz_data[current_index] 
    question_text = question_data['question'] 
 
    markup = types.InlineKeyboardMarkup(row_width=2) 
    btn_true = types.InlineKeyboardButton("✅ Правда", callback_data=f"answer_True_{current_index}") 
    btn_false = types.InlineKeyboardButton("❌ Миф", callback_data=f"answer_False_{current_index}") 
    markup.add(btn_true, btn_false) 
 
    caption = f"*Вопрос {current_index + 1}/{len(quiz_data)}*\n\n{question_text}" 
 
    bot.send_message( 
        chat_id, 
        caption, 
        parse_mode="Markdown", 
        reply_markup=markup 
    ) 
 
@bot.callback_query_handler(func=lambda call: call.data.startswith('answer_')) 
def handle_answer(call): 
    user_id = call.from_user.id 
    chat_id = call.message.chat.id 
    message_id = call.message.message_id 
 
    _, user_answer_str, question_index_str = call.data.split('_') 
    user_answer = (user_answer_str == 'True') 
    question_index = int(question_index_str) 
 
    user_data = user_states.get(user_id) 
    if not user_data: 
        bot.answer_callback_query(call.id, "Сессия устарела. Нажмите /start, чтобы начать заново.") 
        return 
 
    if user_data['current_index'] != question_index: 
        bot.answer_callback_query(call.id, "Этот вопрос уже был отвечен.", show_alert=False) 
        return 
 
    correct_answer = quiz_data[question_index]['answer'] 
    description = quiz_data[question_index]['description'] 
    is_correct = (user_answer == correct_answer) 
 
    if is_correct: 
        user_data['score'] += 1 
        result_text = "✅ Великолепно! Это действительно так." 
    else: 
        if correct_answer: 
            result_text = "❌ Неверно. Это утверждение является *Правдой*." 
        else: 
            result_text = "❌ Неверно. Это утверждение — *Миф*." 
 
    user_data['current_index'] += 1 
 
    new_text = call.message.text + f"\n\n➡️ {result_text}" 
 
    try: 
        bot.edit_message_text( 
            chat_id=chat_id, 
            message_id=message_id, 
            text=new_text, 
            parse_mode="Markdown", 
            reply_markup=None 
        ) 
    except Exception as e: 
        print(f"Ошибка редактирования: {e}") 
 
    bot.send_message( 
        chat_id, 
        description 
    ) 
 
    time.sleep(1.5) 
    send_question(chat_id, user_id) 
    bot.answer_callback_query(call.id) 
 
def finish_quiz(chat_id, user_id): 
    user_data = user_states.pop(user_id, None) 
    if not user_data: 
        return 
 
    score = user_data['score'] 
    total = len(quiz_data) 
 
    if score == total: 
        emoji = "🏆" 
        comment = "Вы — настоящий знаток «Летово»! Ни один миф не ввел вас в заблуждение." 
    elif score >= total * 0.7: 
        emoji = "🥈" 
        comment = "Великолепный результат! Вы отлично осведомлены о жизни школы." 
    elif score >= total * 0.5: 
        emoji = "📚" 
        comment = "Неплохо! Вы знаете многое, но некоторые факты еще ждут своего открытия." 
    else: 
        emoji = "🔍"
        comment = "Благодарим за участие! Теперь вы знаете немного больше о «Летово»." 
 
    final_message = ( 
        f"{emoji} *Викторина завершена!* {emoji}\n\n" 
        f"Правильных ответов: *{score} из {total}*\n\n" 
        f"{comment}\n\n" 
        f"Желаем успехов в поступлении и учебе в «Летово»!" 
    ) 
 
    bot.send_message(chat_id, final_message, parse_mode="Markdown") 
    bot.send_message(chat_id, "Нажмите /start, чтобы попробовать свои силы снова.", reply_markup=types.ReplyKeyboardRemove()) 

if __name__ == '__main__':
    print("Бот запущен...")
    bot.infinity_polling(skip_pending=True)
