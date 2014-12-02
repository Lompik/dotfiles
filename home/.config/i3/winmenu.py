#!/usr/bin/env dmenu
# python script to jump to windows in i3.
#
# using ziberna's i3-py library: https://github.com/ziberna/i3-py
# depends: dmenu (vertical patch), i3.
# released by joepd under WTFPLv2-license:
# http://sam.zoy.org/wtfpl/COPYING
#
# edited by Jure Ziberna for i3-py's examples section

import i3
import subprocess

def i3clients():
    """
    Returns a dictionary of key-value pairs of a window text and window id.
    Each window text is of format "[workspace] window title (instance number)"
    """
    clients = {}
    ws = i3.get_workspaces()
    for ws_num in range(0, len(ws)):
        workspace = i3.filter(name=ws[ws_num]['name'])
        if not workspace:
            continue
        # pdb.set_trace()
        workspace = workspace[0]
        windows = i3.filter(workspace, nodes=[])
        instances = {}
        # Adds windows and their ids to the clients dictionary
        for window in windows:
            # pdb.set_trace()
            win_str = '[%s] %s' % (workspace['name'], " > ".
                                   join([window.get('window_properties', {"1": ""}).
                                         get('class', ""), window['name']])) #  "-".join(window['window_properties'].values()))
            # Appends an instance number if other instances are present
            if win_str in instances:
                instances[win_str] += 1
                win_str = '%s (%d)' % (win_str, instances[win_str])
            else:
                instances[win_str] = 1
            clients[win_str] = window['id']
        floating_wins = i3.filter(workspace['floating_nodes'], nodes=[])
        if floating_wins[0] != {'nodes': []}:
            for window in floating_wins:
                # pdb.set_trace()
                win_str = '[%s] ~~ %s' % (workspace['name'],
                                          " > ".join([window.get('window_properties', {"1": ""}).
                                                      get('class', ""), window['name']])) # "-".join(window['window_properties'].values()))
                # Appends an instance number if other instances are present
                if win_str in instances:
                    instances[win_str] += 1
                    win_str = '%s (%d)' % (win_str, instances[win_str])
                else:
                    instances[win_str] = 1
                clients[win_str] = window['id']
    return clients

def win_menu(clients, l=10):
    """
    Displays a window menu using dmenu. Returns window id.
    """
    dmenu = subprocess.Popen(['/usr/bin/dmenu', '-i', '-l', str(l), '-fn', "xft:Droid Sans:bold:pixelsize=20:antialias=true:hinting=slight"],
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE)
    menu_str = '\n'.join(sorted(clients.keys()))
    # Popen.communicate returns a tuple stdout, stderr
    win_str = dmenu.communicate(menu_str.encode('utf-8'))[0].decode('utf-8').rstrip()
    return clients.get(win_str, None)

if __name__ == '__main__':
    clients = i3clients()
    win_id = win_menu(clients)
    if win_id:
        i3.focus(con_id=win_id)

