#!/usr/bin/env python
#coding:utf-8
"""
  Author:   mikewolfli<mikewolfli@163.com>
  Purpose: gui main frame
  Created: 2016/6/7
<<<<<<< HEAD
"""
from tkinter import *
from tkinter import simpledialog
from tkinter import font
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import filedialog
import tkinter.ttk as ttk

class mainframe(Frame):
    import_tab = None
    operat_tab = None
    proj_release_tab=None
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()  
        pg_db.connect()
        if not mbom_db.get_conn():
            mbom_db.connect()
                                    
    def createWidgets(self):
        self.ntbook = ttk.Notebook(self)
        
        self.tree = ttk.Treeview(self,columns=('col0'), displaycolumns=(), selectmode='browse')
        self.tree.column('#0', width=150)
        self.tree.column('col0',anchor='w')
        self.tree.heading('#0', text='')
        self.tree.heading('col0', text='')
        ysb = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        xsb = ttk.Scrollbar(self, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)
        self.tree.grid(row=0, column=0, sticky=NS)
        ysb.grid(row=0, column=1, sticky=NS)
        xsb.grid(row=1,column=0, sticky=EW)
        
        tree_root = self.tree.insert('','end', text='操作列表', open =True)
        for item in tree_items:
            self.tree.insert(tree_root, 'end', text=item, values=(-1), open=False)
        
        self.ntbook.grid(row=0, column=2, rowspan=2, sticky=NSEW)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
        self.ntbook.rowconfigure(0, weight=1)
        self.ntbook.columnconfigure(0, weight=1)
        self.st_msg = StringVar()
        self.status_bar = Label(self,textvariable=self.st_msg, anchor='w')
        self.status_bar.grid(row=2, column=0, columnspan=4, sticky=EW)

        self.tree.bind('<<TreeviewSelect>>',self.select_func)
        self.ntbook.bind('<<NotebookTabChanged>>', self.tab_changed)
                           
    def tab_changed(self, event):
        if not login_info['status']:
            return
        
        i_sel = int(self.ntbook.index(CURRENT))
        root = self.tree.get_children()
        if not root :
            return
        ch_items = self.tree.get_children(root)
        for item in ch_items:
            if i_sel == int(self.tree.item(item, 'values')[0]):
                self.tree.selection_set(item)
                return       
        
    def select_func(self,event):
        if not login_info['status']:
            return
        
        select = self.tree.selection()        
        if not select :
            return
        
        sel=select[0]
        i_per = int(self.tree.item(sel, 'values')[0])
        s_perm = login_info['perm']
                      
        i_sel = self.ntbook.index(END)
        
        if i_per==-1:
            nt_title=self.tree.item(sel, 'text')
            i_index=tree_items.index(nt_title)
            if i_index==0:
                if not self.import_tab and int(s_perm[i_index])>0:
                    self.import_tab = import_pane(self) 
                    self.ntbook.add(self.import_tab, text=nt_title, sticky=NSEW)
                    self.tree.set(sel, 'col0', i_sel)
                    self.ntbook.select(i_sel)
                else:
                    self.st_msg.set('没有权限')
                    return
            elif i_index==1:
                if not self.operat_tab and int(s_perm[i_index])>0:
                    self.operat_tab = mat_fin_pane(self)
                    self.ntbook.add(self.operat_tab, text=nt_title, sticky=NSEW) 
                    self.tree.set(sel, 'col0', i_sel)
                    self.ntbook.select(i_sel)
                else:
                    self.st_msg.set('没有权限')
                    return
            elif i_index==2:
                if not self.proj_release_tab and int(s_perm[i_index])>0:
                    self.proj_release_tab = proj_release_pane(self)
                    self.ntbook.add(self.proj_release_tab, text=nt_title, sticky=NSEW) 
                    self.tree.set(sel, 'col0', i_sel)
                    self.ntbook.select(i_sel)
                else:
                    self.st_msg.set('没有权限')
                    return 
        else:
            if int(s_perm[i_per]) <= 0:
                self.st_msg.set('没有权限')
                return
                
            self.ntbook.select(i_per)

        '''                       
        if i_per ==0:
            self.ntbook.add(self.import_tab)
        elif i_per ==1:
            self.ntbook.add(self.operat_tab)
        elif i_per ==2:
            self.ntbook.add(self.proj_release_tab)
            
        self.ntbook.select(i_per)  
'''        
    
        
class Application():
    def __init__(self, root):      
        main_frame = mainframe(root)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.grid(row=0, column=0, sticky=NSEW)
        LoginForm(main_frame, '用户登陆')
        #popup.attributes("-toolwindow",1)
        #popup.wm_attributes("-topmost",1)

        #for t in threads:
        #    t.join()
        
        root.protocol("WM_DELETE_WINDOW", self.quit_func)

    def quit_func(self):
        if pg_db.get_conn():
            pg_db.close()
            
        if mbom_db.get_conn() and login_info['status']:
            log_loger = login_log.update(logout_time = datetime.datetime.now(), log_status=False).where((login_log.employee==login_info['uid'])&(login_log.log_status==True))
            log_loger.execute()            
            mbom_db.close()
            
        root.destroy()
                
if __name__ == '__main__':   
    root=Tk() 
    #root.resizable(0, 0)
    root.wm_state('zoomed')
    root.title('非标物料处理')
    default_font = font.nametofont("TkDefaultFont")
    default_font.configure(size=10)  
    root.option_add("*Font", default_font)
    Application(root)
    root.geometry('800x600')
    root.mainloop()
=======
"""
>>>>>>> 18fac031555c51907340e5402da96bccf1f10d1e
