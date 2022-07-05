import PySimpleGUI as sg

skyb = {'size':(4,1), 'font':('FC Lamoon',30),'button_color':("white","#56CBDB")}
skyb2 = {'size':(9,1), 'font':('FC Lamoon',30),'button_color':("white","#56CBDB")}
bblu = {'size':(4,1), 'font':('FC Lamoon',30),'button_color':("white","#1E2435")}

layout = [
	[sg.Text('PyCalculator',size=(50,3),justification='right', background_color='#262834',text_color='white',font=('FC Lamoon',14,'bold'))],
	[	sg.Text('=',text_color='#56CBDB',background_color='#262834',font=('FC Lamoon',50)),
		sg.Text('0.000',size=(50,1),justification='right',text_color='white',background_color='#262834',font=('FC Lamoon',40,'bold'),key = "-DISPLAY-")],
    [sg.HSep()],    
	[sg.Button('C',**skyb), sg.Button('CE',**skyb), sg.Button('%',**skyb), sg.Button("/",**skyb)],
    [sg.Button('7',**bblu), sg.Button('8',**bblu), sg.Button('9',**bblu), sg.Button("x",**skyb)],
    [sg.Button('4',**bblu), sg.Button('5',**bblu), sg.Button('6',**bblu), sg.Button("-",**skyb)],
    [sg.Button('1',**bblu), sg.Button('2',**bblu), sg.Button('3',**bblu),sg.Button("+",**skyb)],    
    [sg.Button('0',**bblu), sg.Button('.',**bblu), sg.Button('=',**skyb2, bind_return_key=True)]	
]

window = sg.Window('PyCalculator_V.00',background_color='#262834',layout = layout,size=(380, 570))

var: dict = {'front':[], 'back':[], 'decimal':False, 'x_val':0.0, 'y_val':0.0, 'result':0.0, 'operator':''}

def format_number() -> float:
    return float(''.join(var['front']).replace(',','') + '.' + ''.join(var['back']))


def update_display(display_value: str):
    try:
        window['-DISPLAY-'].update(value='{:,.3f}'.format(display_value))
    except:
        window['-DISPLAY-'].update(value=display_value)

def number_click(event: str):
    global var
    if var['decimal']:
        var['back'].append(event)
    else:
        var['front'].append(event)
    update_display(format_number())

def clear_click():
    global var
    var['front'].clear()
    var['back'].clear()
    var['decimal'] = False

def operator_click(event: str):
    global var
    var['operator'] = event
    try:
        var['x_val'] = format_number()
    except:
        var['x_val'] = var['result']
    clear_click()

def calculate_click():
    global var
    try:
        var['y_val'] = format_number()
    except ValueError:
        var['x_val'] = var['result']
    try:
        var['result'] = eval(str(var['x_val']) + var['operator'] + str(var['y_val']))
        update_display(var['result'])
        clear_click()    
    except:
        update_display("ERROR! DIV/0")
        clear_click()       

while True:
    event, values = window.read()
    if event == 'x':
        event = '*'
    #print(event)

    if event is None:
        break
    if event in ['0','1','2','3','4','5','6','7','8','9']:
        number_click(event)
    if event in ['Escape:27','C','CE']:
        clear_click()
        update_display(0.0)
        var['result'] = 0.0
    if event in ['+','-','*','/']:
        operator_click(event)
    if event == '=':
        calculate_click()
    if event == '.':
        var['decimal'] = True
    if event == '%':
        update_display(var['result'] / 100.0)