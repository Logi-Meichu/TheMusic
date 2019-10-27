import websocket
import psutil
import json
import uuid
import time
from json import JSONEncoder
from uuid import UUID
from museScore_handler import *
JSONEncoder_olddefault = JSONEncoder.default

# special encoding for supporting UUID in json payload
def JSONEncoder_newdefault(self, o):
    if isinstance(o, UUID): return str(o)
    return JSONEncoder_olddefault(self, o)

JSONEncoder.default = JSONEncoder_newdefault

last_msg = []
duration = 5
eps = 0
sessionId = 0
tool = 0
def on_message(ws, message):
    global last_msg, duration, tool
    message = json.loads(message)
    print(message)
    if message['message_type'] == 'crown_turn_event' :
        if message['task_options']['current_tool']  == 'NoInput':
            if message['task_options']['current_tool_option'] == 'Pitch' :
                # set_edit_mode(1)
                if int(message['ratchet_delta']) > eps :
                    press_key(38) # up arrow
                elif int(message['ratchet_delta']) < -eps :
                    press_key(40) # down arrow
            elif message['task_options']['current_tool_option'] == 'Rewind' :
                if int(message['ratchet_delta']) > eps :
                    press_key(39) # right arrow
                elif int(message['ratchet_delta']) < -eps :
                    press_key(37) # left arrow
            else :
                # set_edit_mode(0)
                if int(message['ratchet_delta']) > eps and duration < 7:
                    duration += 1
                elif int(message['ratchet_delta']) < -eps and duration > 1:
                    duration -= 1
                print(duration)
                press_key(48 + duration)
        else :
            set_edit_mode(0)
            if message['task_options']['current_tool_option'] == 'Trans' :
                if int(message['ratchet_delta']) > eps :
                    press_key([[107]])
                elif int(message['ratchet_delta']) < -eps :
                    press_key([[109]]) 
            elif message['task_options']['current_tool_option'] == 'Tone' :
                press_key(121)
                press_key([9 for i in range(17)])
                if int(message['ratchet_delta']) > eps :
                    press_key([38]) # right arrow 2 : 50
                elif int(message['ratchet_delta']) < -eps :
                    press_key([40]) # left arrow  1 : 49
                press_key(121)

        last_msg.append(message)
        message = []

    elif message['message_type'] == 'crown_touch_event':
        message['time_stamp'] = time.time()
        print('touch', message['touch_state'])
        if message['touch_state'] == 0 and len(last_msg) > 0 and last_msg[-1]['message_type'] == 'crown_touch_event' and last_msg[-1]['touch_state'] == 1:
            if message['time_stamp'] - last_msg[-1]['time_stamp'] >= 0.5:
                tool = 1 - tool
                if tool == 1 :
                    change_tool(ws, "Input")
                    print("CHANGEMODE Input")
                else :
                    change_tool(ws, "NoInput")
                    print("CHANGEMODE NoInput")
        last_msg.append(message)
        message = []
    elif message['message_type'] == "register_ack" :
        global sessionId
        sessionId = message['session_id']
        change_tool(ws, "NoInput")

def change_tool(ws, name) :
    global sessionId
    connectMessage = {
        "message_type": "tool_change",
        "session_id": sessionId,
        "tool_id": name
    }
    regMsg = json.dumps(connectMessage)
    ws.send(regMsg.encode('utf8'))

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    uid = "6202f2fb-834c-4393-a95f-f5051171e3ec"
    
    pid = -1
    pids = psutil.pids()
    for pid_element in pids:
        if psutil.Process(pid_element).name() == 'MuseScore3.exe':
            pid = pid_element
            break

    connectMessage = {
        "message_type": "register",
        "plugin_guid": uid,
        "PID": pid,
        "execName": "MuseScore3.exe",
        "application_version": "1.0"
    }
    regMsg =  json.dumps(connectMessage)
    ws.send(regMsg.encode('utf8'))

if __name__ == "__main__":
    set_edit_mode(1)
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://127.0.0.1:10134",  on_open = on_open, on_message = on_message, on_error = on_error, on_close = on_close)
    ws.run_forever()