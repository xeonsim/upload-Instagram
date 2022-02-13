import tkinter
import subprocess
from tkinter import *
from tkinter import filedialog
import os
import sys
import autoit
import pickle
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as ExpectedConditions
from selenium.webdriver.support.ui import Select



root = Tk()
root.geometry('500x400')
root.title("Upload Instagram")
input_save_list = ["Posts folder :", 0, 0, 0, 0, 0, 0, 0, 0, 0]
main_directory = os.path.join(sys.path[0])
waittime = BooleanVar()
waittime.set(False)



def open_chrome_profile():
    subprocess.Popen(
        [
            "start",
            "chrome",
            "--remote-debugging-port=8989",
            "--user-data-dir=" + main_directory + "/chrome_profile",
        ],
        shell=True,
    )


def save_file_path():
    return os.path.join(sys.path[0], "Save_file.cloud") 

# ask for directory on clicking button, changes button name.
def upload_folder_input():
    global upload_path
    upload_path = filedialog.askdirectory()
    Name_change_img_folder_button(upload_path)

def upload_folder_input2():
    global upload_path2
    upload_path2 = filedialog.askdirectory()
    Name_change_img_folder_button2(upload_path2)

def Name_change_img_folder_button(upload_folder_input):
    upload_folder_input_button["text"] = upload_folder_input

def Name_change_img_folder_button2(upload_folder_input2):
    upload_folder_input_button2["text"] = upload_folder_input2

class InputField:
    def __init__(self, label, row_io, column_io, pos, master=root):
        self.master = master
        self.input_field = Entry(self.master)
        self.input_field.label = Label(master, text=label)
        self.input_field.label.grid(row=row_io, column=column_io)
        self.input_field.grid(row=row_io, column=column_io + 1)
        try:
            with open(save_file_path(), "rb") as infile:
                new_dict = pickle.load(infile)
                self.insert_text(new_dict[pos])
        except FileNotFoundError:
            pass

    def insert_text(self, text):
        self.input_field.delete(0, "end")
        self.input_field.insert(0, text)

    def save_inputs(self, pos):
        input_save_list.insert(pos, self.input_field.get())
        with open(save_file_path(), "wb") as outfile:
            pickle.dump(input_save_list, outfile)

###input objects###
start_num_input = InputField("Start Number:", 1, 0, 2)
end_num_input = InputField("End Number:", 2, 0, 3)
title = InputField("hashtags:", 3, 0, 4)
description = InputField("Description:", 4, 0, 5)
file_format = InputField("Posts Image Format:", 5, 0, 6)
post_num= InputField("Posts number:", 6, 0, 7)
ad_post_num= InputField("Ad Posts number:", 7, 0, 8)
waittime_num= InputField("waiting time:",8, 0, 9)



###save inputs###
def save():
    input_save_list.insert(0, upload_path)
    input_save_list.insert(1, upload_path2)
    print(input_save_list)
    start_num_input.save_inputs(2)
    end_num_input.save_inputs(3)
    title.save_inputs(4)
    description.save_inputs(5)
    file_format.save_inputs(6)
    post_num.save_inputs(7)
    ad_post_num.save_inputs(8)
    waittime_num.save_inputs(9)
    
  
   

# _____MAIN_CODE_____
def main_program_loop():
    ###START###
    project_path = main_directory
    file_path = upload_path
    ad_file_path = upload_path2
    Instagram_link = "https://www.instagram.com/"
    start_num = int(start_num_input.input_field.get())
    end_num = int(end_num_input.input_field.get())
    loop_title = title.input_field.get()
    loop_file_format = file_format.input_field.get()
    loop_description = description.input_field.get()
    loop_post_num=post_num.input_field.get()
    loop_ad_post_num=ad_post_num.input_field.get()
    sum=int(loop_ad_post_num)+int(loop_post_num)
    loop_wait=int(waittime_num.input_field.get())
    print(sum)
    if sum > 10:
        print("posts sum should not be over 10")
        raise Exception
         

    ##chromeoptions
    opt = Options()
    opt.add_experimental_option("debuggerAddress", "localhost:8989")
    driver = webdriver.Chrome(
        executable_path=project_path + "/chromedriver.exe",
        chrome_options=opt,
    )
    wait = WebDriverWait(driver, 60)

    ###wait for methods
    def wait_xpath(code):
        wait.until(ExpectedConditions.presence_of_element_located((By.XPATH, code)))

    n=0
    while end_num >= start_num:
        print("Start uploading Posts"+str(start_num))
       
        #refreshing instagram website once
        if n==0:
            driver.get(Instagram_link)
            time.sleep(3)
        
        #clicking uploadind post icon
        wait_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[3]/div/button')
        additem = driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[3]/div/button')
        additem.click()
        time.sleep(1)     
       
        #clicking add picture icon
        wait_xpath('/html/body/div[8]/div[2]/div/div/div/div[2]/div[1]/div/div/div[2]/div/button')
        im=driver.find_element_by_xpath('/html/body/div[8]/div[2]/div/div/div/div[2]/div[1]/div/div/div[2]/div/button')
        im.click()
        
        #sending file
        handle = "[CLASS:#32770; TITLE:Open]"        
        autoit.win_wait_active("Open", 10)
        path=os.path.abspath(file_path + "\\" + str(start_num) + "." + loop_file_format)
        print("uploading"+path)
        autoit.control_focus(handle,'Edit1')
        autoit.send(path,mode=0)
        autoit.control_click(handle, "Button1")
        time.sleep(1)
        start_num=start_num+1
        
        #adding post
        if int(loop_post_num)>1:
            #clicking add more post icon
            wait_xpath('/html/body/div[6]/div[2]/div/div/div/div[2]/div[1]/div/div/div/div[3]/div/div[2]/div/button')
            additem=driver.find_element_by_xpath("/html/body/div[6]/div[2]/div/div/div/div[2]/div[1]/div/div/div/div[3]/div/div[2]/div/button")
            additem.click()
            
            #adding more files
            for i in range(1,int(loop_post_num)):
                wait_xpath("/html/body/div[6]/div[2]/div/div/div/div[2]/div[1]/div/div/div/div[3]/div/div[1]/div/div/div/div[2]/div")
                additem=driver.find_element_by_xpath("/html/body/div[6]/div[2]/div/div/div/div[2]/div[1]/div/div/div/div[3]/div/div[1]/div/div/div/div[2]/div")
                additem.click()
                handle = "[CLASS:#32770; TITLE:Open]"
                path=os.path.abspath(file_path + "\\" + str(start_num) + "." + loop_file_format)
                print(path)        
                autoit.win_wait_active("Open", 10)
                autoit.control_focus(handle,'Edit1')
                autoit.send(path,mode=0)
                autoit.control_click(handle, "Button1")
                time.sleep(1)
                start_num=start_num+1
        
        #adding ad post
        if int(loop_ad_post_num)>0:
            #adding more files
            for i in range(0,int(loop_ad_post_num)):
                wait_xpath("/html/body/div[6]/div[2]/div/div/div/div[2]/div[1]/div/div/div/div[3]/div/div[1]/div/div/div/div[2]/div")
                additem=driver.find_element_by_xpath("/html/body/div[6]/div[2]/div/div/div/div[2]/div[1]/div/div/div/div[3]/div/div[1]/div/div/div/div[2]/div")
                additem.click()
                handle = "[CLASS:#32770; TITLE:Open]"        
                autoit.win_wait_active("Open", 10)
                path=os.path.abspath(ad_file_path + "\\" + str(i+1) + "." + loop_file_format)
                print(path)
                autoit.control_focus(handle,'Edit1')
                autoit.send(path,mode=0)
                autoit.control_click(handle, "Button1")
                time.sleep(1)

        #clicking next step
        wait_xpath('/html/body/div[6]/div[2]/div/div/div/div[1]/div/div/div[2]/div/button')
        additem = driver.find_element_by_xpath('/html/body/div[6]/div[2]/div/div/div/div[1]/div/div/div[2]/div/button')
        additem.click()
        time.sleep(3)
        
        #clicking next step
        wait_xpath('/html/body/div[6]/div[2]/div/div/div/div[1]/div/div/div[2]/div/button')
        additem = driver.find_element_by_xpath('/html/body/div[6]/div[2]/div/div/div/div[1]/div/div/div[2]/div/button')
        additem.click()
        time.sleep(2)
        
        #typing hashtags
        wait_xpath("/html/body/div[6]/div[2]/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/textarea")
        hashtag = driver.find_element_by_xpath('/html/body/div[6]/div[2]/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/textarea')
        hashtag.send_keys(loop_title) 
        time.sleep(2)

        #typing descriptions
        wait_xpath("html/body/div[6]/div[2]/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/textarea")
        desc = driver.find_element_by_xpath('/html/body/div[6]/div[2]/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/textarea')
        desc.send_keys(" "+loop_description)
        time.sleep(2)

        #clicking share icon
        wait_xpath('/html/body/div[6]/div[2]/div/div/div/div[1]/div/div/div[2]/div/button')
        additem = driver.find_element_by_xpath('/html/body/div[6]/div[2]/div/div/div/div[1]/div/div/div[2]/div/button')
        additem.click()
        time.sleep(6)

        #exiting uploading page to upload more
        wait_xpath('/html/body/div[6]/div[1]/button')
        additem = driver.find_element_by_xpath('/html/body/div[6]/div[1]/button')
        additem.click()
        print('Post uploading completed!')
        n=n+1

        #sleeping to avoid being found as a bot
        if waittime.get():
            time.sleep(loop_wait)

#####BUTTON ZONE#######
button_save = tkinter.Button(root, width=20, text="Save Form", command=save) 
button_save.grid(row=24, column=1)
button_start = tkinter.Button(root, width=20, bg="green", fg="white", text="Start", command=main_program_loop)
button_start.grid(row=25, column=1)
open_browser = tkinter.Button(root, width=20,  text="Open Chrome Browser", command=open_chrome_profile)
open_browser.grid(row=23, column=1)
Waittime = tkinter.Checkbutton(root, text="set waiting time", var=waittime)
Waittime.grid(row=19, column=1)
upload_folder_input_button = tkinter.Button(root, width=20, text="Add Posts Upload Folder", command=upload_folder_input)
upload_folder_input_button.grid(row=21, column=1)
upload_folder_input_button2 = tkinter.Button(root, width=20, text="Add Ad Posts Upload Folder", command=upload_folder_input2)
upload_folder_input_button2.grid(row=22, column=1)
try:
    with open(save_file_path(), "rb") as infile:
        new_dict = pickle.load(infile)
        global upload_path
        global upload_path2
        Name_change_img_folder_button(new_dict[0])
        Name_change_img_folder_button2(new_dict[1])
        upload_path = new_dict[0]
        upload_path2 = new_dict[1]
except FileNotFoundError:
    pass
#####BUTTON ZONE END#######
root.mainloop()
