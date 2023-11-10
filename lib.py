from time import sleep

def get_user_id(file):
    '''try to get user id from file'''
    try:
        f = open(file, 'r')
        for line in f:
            user_id = line.split('=')[1].strip()
        f.close()
    
    except FileNotFoundError:
        user_id = None
    return user_id

def set_user_id(file, user_id):
    '''write userid into file'''
    f = open(file, 'a')
    f.write('uid='+str(user_id)+'\n')
    f.close()

def get_calories_norm(user):
    '''calculate caloriris norm per day'''
    basic = 10 * user['weight'] + 6.25 * user['height'] - 5 * user['age']

    if user['sex'] in 'мМmM':
        return str((basic + 5)  * user['activity'])[:-1]
    elif user['sex'] in 'жЖfF':
        return str((basic - 161) * user['activity'])[:-1]

def validate(what, expected):
    '''check what is expected type'''
    what = str(what)

    def isfloat(what):
        if what.startswith('-'):
            what = what[1:]
        parts = what.split('.')
        return len(parts) == 2 and parts[0].isnumeric() and parts[1].isnumeric()

    if expected == 'int':
        return what.isdigit()
    else:
        print('Здесь требуется число d')
        sleep(1)
    
    if expected == 'float':
        return isfloat(what)
    else:
        print('Здесь требуется число f')
        sleep(1)
    
    if expected == 'str':
        return what.isalpha() and len(what) > 3
    else:
        print('Слишком короткая строка')
        sleep(1)

   # if what in expected:
    #    return True
        
    return False

def get_value_from_input(promt, expected):
    value = None
    while True:
        value = input(promt + ': ')
        if validate(value, expected):
            break
    
    return value

    

