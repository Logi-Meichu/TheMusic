import win32gui
import win32con
import win32api
import math

edit_mode = 0

# def read_file() :
# 	press_key([[16, 17, 49]])
	
# 	data = []
# 	with open(filename, "r") as file :
# 		while True :
# 			section = []
# 			tmp = file.readline().split(' ')
# 			print(tmp)
# 			if len(tmp[0]) == 0 :
# 				break
# 			for element in tmp :
# 				section.append(element)
# 			data.append(section)
# 	return data

# def head_type_converter(head_string) : # format [num1]/[num2]
# 	if head_string[0] == '1' :
# 		return int(math.log(64 / int(head_string[2:]), 2)) + 1 + 48 # calculate log2(num2)
# 	return [int(math.log(64 / int(head_string[2:]), 2)) + 2 + 48, 110] # 附點音符


# def map_data_to_screen(data) :
# 	for section in data :
# 		for index in range(0, len(section), 2) :
# 			# 音符種類
# 			press_key(head_type_converter(section[index]))
# 			# 音調
# 			press_key(67)
# 			section[index + 1] = int(section[index + 1])
# 			if section[index + 1] == -1 :
# 				press_key(48)
# 			elif section[index + 1] >= 72 :  # 72 是高音 Do
# 				press_key([38 for i in range(section[index + 1] - 72)])
# 			else :
# 				press_key([40 for i in range(72 - section[index + 1])])
# 	return data

def press_key(key_list) :
	if type(key_list) != list :
		win32api.keybd_event(key_list, 0 , 0 ,0)
		win32api.keybd_event(key_list, 0, win32con.KEYEVENTF_KEYUP, 0)
	else :
		for key in key_list :
			if type(key) == list :
				for key_element in key :
					win32api.keybd_event(key_element, 0 , 0 ,0)
				for key_element in key :
					win32api.keybd_event(key_element, 0, win32con.KEYEVENTF_KEYUP, 0)
			else :
				win32api.keybd_event(key, 0 , 0 ,0)
				win32api.keybd_event(key, 0, win32con.KEYEVENTF_KEYUP, 0)

def set_foreground_window() :
	win = win32gui.FindWindow(None, 'MuseScore 3.3 Release Candidate 2: 未命名')
	if win == 0 :
		win = win32gui.FindWindow(None, 'MuseScore 3.3 Release Candidate 2: 未命名*')
	if win == 0 :
		print(window_name + " GG")
	win32gui.SetForegroundWindow(win)

def set_edit_mode(val) :
	global edit_mode
	if edit_mode != val :
		press_key(78) # 'N'
		edit_mode = val	

def list_all_window() :
	# show window list
	windows_list = []
	win32gui.EnumWindows(lambda window, windows_list: windows_list.append(window), windows_list)
	for win in windows_list :
		print(win32gui.GetWindowText(win))
