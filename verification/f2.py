import time
from parse import parse
from interface import window
from verification.reference import VERIFICATION


def verify_contains(strings, attempts):
    def tries(strings):
        screen = window.get_window()
        for s in strings:
            if not screen or s not in screen:
                return False
        return True

    for i in range(attempts):
        if tries(strings):
            return True

    return False


def verify(points, attempts=1):
    def tries(points):
        screen = parse.process_scene(window.get_window())
        for p in points:
            try:
                if not p['target'] in screen[p['location'][0]][p['location'][1]:]:
                    return False
            except:
                return False
        return True

    for i in range(attempts):
        if tries(points):
            return True

    return False


def verify_system(system):
    return verify(VERIFICATION['system'][system], 10)


def get_window_info(targets):
    total = []
    w = parse.process_scene(window.get_window())

    for target in (targets):
        i = 0
        for line in w:
            if target in line:
                total.append({'target': target, 'location': (i, line.index(target))})
            i += 1

    #print(total)
    return total


def is_system_open(tries=25):
    for i in range(tries):
        key_phrase = VERIFICATION['f2_window']['any']
        open_windows = window.get_matching_handles(key_phrase)
        if len(open_windows) > 0:
            return True
        else:
            time.sleep(.2)


def info_based_on(old, new):
    a = []
    for o in old:
        a.append(o['target'])
    a.extend(new)
    get_window_info(a)


def is_new_screen(old_screen, attempts=0):
    if old_screen == '':
        return True

    if attempts > 50:
        return False

    old_screen = parse.process_scene(old_screen)[6:-4]
    new_screen = parse.process_scene(window.get_window())[6:-4]

    if old_screen == new_screen:
        return is_new_screen(old_screen, attempts + 1)
    return True


def get_updated_locations(p):
    new_targets = []
    for t in p:
        new_targets.append(t['target'])
    return get_window_info(new_targets)



def compare(p):
    print('------------------------------------')
    print(p)
    print(get_updated_locations(p))

    return get_updated_locations(p) == p


# window_data = VERIFICATION['screens']['text_login_menu_2']
# get_window_info(['║       1)   Toronto                    ║', '© Uniware Computer Systems BV'])


# old = VERIFICATION['screens']['main_menu-maintenance_data']
# new = ['Pricelist type','Pricelists']

# info_based_on(old, new)

if __name__ == '__main__':
    #text = 'stock_per_location-flowers-location-price_level'
    targets = ['Date    :','Input purchases']
    #get_window_info(text, targets)
    #a = compare([{'target': 'Inkooporder', 'location': (19, 97)}, {'target': 'Art. info', 'location': (5, 98)},
                 #{'target': 'VBN', 'location': (8, 97)},
                 #{'target': 'Intern partijnummer  : 639545', 'location': (18, 97)}])
    #print(a)
    get_window_info(targets)
    print(get_window_info(targets))
