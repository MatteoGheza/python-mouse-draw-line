import mouse
import PySimpleGUI as sg
import time

def get_focus():
    global window
    window.TKroot.focus_force()

def lost_focus():
    global window
    window.minimize()

layout = [  [sg.Text('Disegna una linea utilizzando il mouse', size=(60, 1), font=("Helvetica"))],
            [sg.Text('Durata realizzazione linea'), sg.Slider(range=(1,5), default_value=1, orientation='horizontal', key='duration')],
            [sg.Button('Modalità automatica', key='auto_mode')],
            [sg.HorizontalSeparator()],
            [sg.Text('Impostazioni avanzate')],
            [sg.CBox('Blocca movimenti asse x', key='x_lock')],
            [sg.CBox('Blocca movimenti asse y', key='y_lock')],
            [sg.Text('Iterazioni per disegno'), sg.Slider(range=(1,5), default_value=1, orientation='horizontal', key='iterations')],
            [sg.CBox('Disegna automaticamente quando il punto finale viene selezionato', key='do_not_require_button_press', default=True)],
            [sg.Button('Imposta punto iniziale', key='get_initial_position'), sg.Button('Imposta punto finale', key='get_final_position')],
            [sg.Button('Disegna', key='draw')] ]

window = sg.Window('Disegna linee con il mouse', layout)

mouse_initial_position = (0, 0)
mouse_final_position = (0, 0)   

def update_initial_position():
    global mouse_initial_position
    mouse_initial_position = mouse.get_position()

def update_final_position():
    global mouse_final_position, values, event
    mouse_final_position = mouse.get_position()
    if values['x_lock']:
        mouse_final_position = (mouse_initial_position[0], mouse_final_position[1])
    elif values['y_lock']:
        mouse_final_position = (mouse_final_position[0], mouse_initial_position[1])
    if values['do_not_require_button_press']:
        if event == 'auto_mode':
            print(mouse_initial_position, mouse_final_position)
            if -40 <= mouse_initial_position[0] - mouse_final_position[0] <= 40 and not values['x_lock']:
                mouse_final_position = (mouse_initial_position[0], mouse_final_position[1])
            elif -40 <= mouse_initial_position[1] - mouse_final_position[1] <= 40 and not values['y_lock']:
                mouse_final_position = (mouse_final_position[0], mouse_initial_position[1])
        draw()

def get_initial_position():
    global mouse_initial_position
    print("callback call to get_initial_position()")
    update_initial_position()
    mouse.unhook_all()

def get_final_position():
    global mouse_final_position, values
    print("callback call to get_final_position()")
    update_final_position()
    mouse.unhook_all()

def auto_mode_callback():
    global mouse_initial_position, mouse_final_position
    print("callback call to auto_mode_callback()")
    if mouse_initial_position == (0, 0):
        update_initial_position()
    else:
        update_final_position()
        mouse.unhook_all()

def draw():
    global mouse_initial_position, mouse_final_position
    if mouse_initial_position != (0, 0) and mouse_final_position != (0, 0):
        for i in range(0, int(values['iterations'])):
            mouse.move(mouse_initial_position[0], mouse_initial_position[1])
            print(mouse_initial_position, mouse_final_position)
            mouse.drag(mouse_initial_position[0], mouse_initial_position[1], mouse_final_position[0], mouse_final_position[1], absolute=True, duration=float(values['duration']))
    else:
        sg.popup('Non hai ancora selezionato i punti iniziale e finale')

while True:
    global event, values
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == '__TIMEOUT__' or event == 'Cancel':
        break

    if event == 'auto_mode' or event == 'get_initial_position' or event == 'get_final_position' or event == 'draw':
        lost_focus()

    if event == 'auto_mode':
        mouse_initial_position = (0, 0)
        mouse_final_position = (0, 0)
        mouse.on_click(auto_mode_callback)
    if event == 'get_initial_position':
        mouse.on_click(get_initial_position)
    elif event == 'get_final_position':
        mouse.on_click(get_final_position)
    elif event == 'draw':
        draw()

    print(event, values)

window.close()
