# -*- coding:utf-8 -*-
from flask import Flask, request, render_template, redirect, url_for, session , send_from_directory
from flask_socketio import SocketIO, emit, join_room, leave_room
from models.executeSqlite3 import executeSelectOne, executeSelectAll, executeSQL
from functools import wraps
from models.user_manager import UserManager
from models.user_friend_manager import UserRelationManager
from flask_mail import Mail, Message
import os

# створюємо головний об'єкт сайту класу Flask
app = Flask(__name__)
# добавляємо секретний ключ для сайту щоб шифрувати дані сессії
# при кожнаму сапуску фласку буде генечитись новий рандомний ключ з 24 символів
# app.secret_key = os.urandom(24)

app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True


socketio = SocketIO(app)
socketio.init_app(app)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

app.secret_key = '125'


app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=587,
	MAIL_USE_TLS=True,
	MAIL_USERNAME = 'hardanchukvasia@gmail.com',
	MAIL_PASSWORD = '123456789o'
	)
mail = Mail(app)

#app.config['MAIL_SERVER'] = 'smtp.gmail.com'
#app.config['MAIL_PORT'] = 587
#app.config['MAIL_USE_TLS'] = True

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'username' in session:
            if UserManager.load_models.get(session['username'], None):
                return f(*args, **kwargs)
        return redirect(url_for('login'))
    return wrap

@app.route("/email")
@login_required
def email():
    print('Hello Sender!')
    if request.method == 'POST':
        user = UserManager()
        values = user.getModelFromForm(request.form)
        message = values.object.descr
        #recipient = values.object.nickname
        #print(recipient)
        msg = Message(message,
            sender="nikita.ogranchuk@gmail.com",
            recipients=["hardanchukvasia@gmail.com"])
        mail.send(msg)
        return('ok')
    #else:
     #   return('/ok')



# описуємо логін роут
# вказуємо що доступні методи "GET" і "POST"
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        # якщо метод пост дістаємо дані з форми і звіряємо чи є такий користвач в базі данних
        # якшо є то в дану сесію добавляєм ключ username
        # і перекидаємо користувача на домашню сторінку
        user = UserManager()
        if user.loginUser(request.form):
            print('hey')
            addToSession(user)
            return redirect(url_for('home'))

    return render_template('login.html')

# описуємо роут для вилогінення
# сіда зможуть попадати тільки GET запроси
@app.route('/logout')
@login_required
def logout():
    user = session.get('username', None)
    if user:
        # якщо в сесії є username тоді видаляємо його
        del session['username']
    return redirect(url_for('login'))

@app.route('/add_friend', methods=["GET","POST"])
@login_required
def add_friend():
    if request.method == 'POST':
        user = UserManager()
        user_nickname = session['username']
        if user.SelectUser(user_nickname):
            user_id = user.object.id
        friend_id = request.form['friend_id']
        func_type = request.form['func_type']
        func_type = int(func_type)
        print(type(func_type))
        print('kjgjgjgjf')
        friend = UserRelationManager()
        isfriend = friend.isFriend(user_id,friend_id)
        print(isfriend)
        print('Vasya privet')
        if isfriend == True:
            print('func_type')
            print(func_type)
            print("it's working")
            if func_type == 1: # Block
                print('You are blocking a friend.')
                if user_id and friend_id:
                    friend.blockFriend(user_id , friend_id)
                    return redirect(url_for('home'))
            elif func_type == 2: #Delete
                print('You are deliting a friend.')
                print('hallo mein freinde.')
                if user_id and friend_id:
                    friend.delFriend(user_id , friend_id)
                    return redirect(url_for('home'))
            elif func_type == 3: # AddFriend
                sender = user.ifsender()
                print('Hallo.')
                if sender == True:
                    print('you are sender')
                    return("You are Sender You can't accept it.")
                else:
                    if user_id and friend_id:
                        print('You are adding a friend.')
                        friend.addFriend(user_id , friend_id)
                        return redirect(url_for('home'))
        else:
            print('hey chuvak')
            if user_id and friend_id:
                sender = 0
                print('hey good man')
                friend.addFriend(user_id , friend_id,sender)
                print(friend.addFriend(user_id , friend_id,sender))
                return redirect(url_for('home'))
    else:
        return  redirect(url_for('home'))

@app.route('/find_friend', methods = ["GET","POST"])
@login_required
def find_friend():
    if request.method == 'GET':
        user_nickname = session['username']
        user = UserManager()
        if user.SelectUser(user_nickname):
            user_id = user.object.id
        friend_nickname = request.args['friend_nickname']
        friend = UserManager()
        if friend.SelectUser(friend_nickname):
            friend_id = friend.object.id
        friend = UserRelationManager()
        if user_id and friend_id:
            IsItYourFriend = friend.isFriend(user_id , friend_id)
            if IsItYourFriend == True:
                return redirect(url_for('nickname', nickname = friend_nickname))
            elif friend_nickname == None:
                return redirect(url_for('home'))
            else:
                #context = {'Error': []}
               # context['Error:'].append("you don't have friend with that nickname")
                render_template('find_friend error.html')
                return("you do not have friends with this nickname")

#@app.route('/delete_friend', methods=["GET","POST"])
#@login_required
#def delete_friend():
#    if request.method == 'POST':
#        user_nickname = session['username']
#        user = UserManager()
#        if user.SelectUser(user_nickname):
#            user_id = user.object.id
#        friend_id = request.form['friend_id']
#        friend = UserRelationManager()
#        if user_id and friend_id:
#            friend.delFriend(user_id , friend_id)
#            return('ok')
#        return('!ok')
#    else:
#        render_template('home.html')

#@app.route('/block_friend', methods=["GET","POST"])
#@login_required
#def block_friend():
#    if request.method == 'POST':
#        user_nickname = session['username']
#        user = UserManager()
#        if user.SelectUser(user_nickname):
#            user_id = user.object.id
#        friend_id = request.form['friend_id']
#        friend = UserRelationManager()
#        if user_id and friend_id:
#            friend.blockFriend(user_id , friend_id)
#            return redirect(url_for('home'))
#        return('!ok')
#    else:
#        render_template('home.html')

@app.route('/friends_view',methods = ["GET","POST"])
@login_required
def friends_view():
    context = {}
    if session.get('username', None):
        user = UserManager.load_models[session['username']]
        context['user'] = user
        context['loginUser'] = user
    friends_list = {}
    user_nickname = session['username']
    user = UserManager()
    if user.SelectUser(user_nickname):
        user_id = user.object.id
    friend = UserRelationManager()
    print('hey man')
    friend.getFriends(user_id)
    friends = []
    friends_request = []
    friend_nickname = UserManager()
    print(type(friend.object))
    print(friend.object)
    if isinstance(friend.object,list):
        for i in friend.object:
            print('hey friend')
            print(i)
            friend_id = i.user2
            friend_nickname.get_user(friend_id)
            if i.block == 2 or i.block == 1:
                friends_request.append(friend_nickname.object.nickname)
            else:
                friends.append(friend_nickname.object.nickname)
    elif friend.object == None:
        return('YOU ARE ALONE.')
    else:
        print('friends')
        print(friend.object)
        if isinstance(friend.object,None):
            return ('YOU ARE ALONE.')
        friend_id = friend.object.user2
        print(type(friend_id))
        print(friend_id)
        friend_nickname.get_user(friend_id)
        if friend.object.block == 2 or friend.object.block == 1:
            friends_request.append(friend_nickname.object.nickname)
        else:
            friends.append(friend_nickname.object.nickname)
    context['friends_list'] = friends
    context['friends_request_list'] = friends_request
    return render_template('home.html', context = context)

@app.route('/<nickname>',methods=["GET","POST"])
@login_required
def nickname(nickname):
    context = {}
    if session.get('username', None):
        user = UserManager.load_models[session['username']]
        context['loginUser'] = user

    if request.method == "POST":
        nickname = request.form.get('nickname')

    selectUser = UserManager()
    selectUser.select().And([('nickname','=',nickname)]).run()
    context['user'] = selectUser

    return render_template('home.html', context=context)

# описуємо домашній роут
# сіда зможуть попадати тільки GET запроси
@app.route('/')
@login_required
def home():
    context = {}
    if session.get('username', None):
        user = UserManager.load_models[session['username']]
        # якщо в сесії є username тоді дістаємо його дані
        # добавляємо їх в словник для передачі в html форму
        context['user'] = user
        context['loginUser'] = user
    return render_template('home.html', context=context)

def addToSession(user):
    session['username'] = user.object.nickname

@app.route('/edit', methods=["GET", "POST"])
@login_required
def edit():
    nickname = session['username']
    context = {}
    user = UserManager()
    if user.SelectUser(nickname):
            context['user'] = user
    if request.method == 'POST':
        user = user.getModelFromForm(request.form)
        print('Hallo!')
        print(user)
        if user.save():
            print('Hallo!2')
            context['user'] = user
            return redirect(url_for('home'))
    return render_template('edit.html', context=context)

@app.route('/registration',methods = ["POST"])
def registation():
    context = {'Error': []}
    if session['username']:
        return redirect(url_for('registr_group'))
    else:
        if session.get('username') and request.method == 'GET':
            nickname = session.get('username')
            user = UserManager()
            user.SelectUser(nickname)
            context['user'] = user
            return render_template('registration.html', context=context)
        if request.method == 'POST':
            user = UserManager().getModelFromForm(request.form)
            if user.check_user():
                context['Error'].append('wrong nickname or email')
            if not user.object.password:
                context['Error'].append('incorrect password')
            if context['Error']:
                return render_template('registration.html', context=context)
            if user.save():
                UserManager.load_models[user.object.nickname] = user
                addToSession(user)
                return redirect(url_for('home'))

            context['Error'].append('incorrect data')
        return render_template('registr.html', context=context)

@app.route('/registration', methods=["GET", "POST"])
def registration():
    context = {'Error': []}
    if session.get('username') and request.method == 'GET':
        nickname = session.get('username')
        user = UserManager()
        user.SelectUser(nickname)
        context['user'] = user
        return render_template('registr.html', context=context)
    if request.method == 'POST':
        user = UserManager().getModelFromForm(request.form)
        if user.check_user():
            context['Error'].append('wrong nickname or email')
        if not user.object.password:
            context['Error'].append('incorrect password')
        if context['Error']:
            return render_template('registration.html', context=context)
        if user.save():
            UserManager.load_models[user.object.nickname] = user
            addToSession(user)
            return redirect(url_for('home'))

        context['Error'].append('incorrect data')
    return render_template('registr.html', context=context)

@app.route('/registr_group', methods=["GET", "POST"])
def registr_group():
    context = {'Error': []}
    if request.method == 'POST':
        user = UserManager().getModelFromForm(request.form)
        print(user.object.nickname)
        if user.check_user():
            context['Error'].append('wrong Name or email')
        if context['Error']:
            return render_template('registration.html', context=context)
        if user.save_group:
            print("ok")
            return redirect(url_for('home'))

        context['Error'].append('incorrect data')
    return render_template('registration.html', context=context)

@app.route("/upload_files")
def index():
    return render_template('upload.html')

#@app.route("/upload", methods=['POST'])
#def upload():
 #   target = os.path.join(APP_ROOT, 'images/')
 #   print(target)
 #   if not os.path.isdir(target):
 #       os.mkdir(target)

#    for file in request.files.getlist("file"):
 #       print(file)
  #      filename = file.filename
   #     destination = "/".join([target, filename])
    #    print(destination)
     #   print(filename)
      #  file.save(destination)

   # return render_template("complete.html" , image_name = filename)

@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images" , filename)

@app.route('/chat')
def chat():
    """Chat room. The user's name and room must be stored in
    the session."""
    session['name'] = session['username']
    session['room'] = 'test room'
    name = session.get('name', '')
    room = session.get('room', '')
    if not (name or room):
        return redirect(url_for('.index'))
    return render_template('chat.html', name=name, room=room)


@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    join_room(room)
    print(session.get('name'))
    emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    print(session.get('name'))
    emit('message', {'msg': session.get('name') + ':' + message['msg']}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)

if __name__ == '__main__':
    socketio.run(app)
