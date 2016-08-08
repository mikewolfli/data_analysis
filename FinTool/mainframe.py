#!/usr/bin/env python
#coding:utf-8
'''
  Author:   mikewolfli<mikewolfli@163.com>
  Purpose: gui main frame
  Created: 2016/6/7
'''
from tkinter import *
from tkinter import simpledialog
from tkinter import font
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import filedialog
from constant import *
import tkinter.ttk as ttk
#import platform
import logging 


class TextHandler(logging.Handler):
    """This class allows you to log to a Tkinter Text or ScrolledText widget"""
    def __init__(self, text):
        # run the regular Handler __init__
        logging.Handler.__init__(self)
        # Store a reference to the Text it will log to
        self.text = text

    def emit(self, record):
        self.formatter = logging.Formatter('%(asctime)s-%(levelname)s : %(message)s')
        msg = self.format(record)
        def append():
            self.text.configure(state='normal')          
            self.text.insert(END, msg+"\n")
            self.text.configure(state='disabled')
            # Autoscroll to the bottom
            self.text.yview(END)
        # This is necessary because we can't modify the Text from other threads
        self.text.after(0, append)# Scroll to the bottom
        
logger = logging.getLogger()

class data_syc_pane(Frame):
    pass

class history_pane(Frame):
    pass

class run_chart_pane(Frame):
    pass

class data_analysis_pane(Frame):
    pass

class mainframe(Frame):
    data_syc_tab = None
    his_data_tab = None
    run_chart_tab =None
    data_analysis_tab = None
    
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()  
                                    
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
        self.tree.grid(row=0, column=0, rowspan=3,sticky=NS)
        ysb.grid(row=0, column=1, sticky=NS)
        xsb.grid(row=4,column=0, sticky=EW)
        
        tree_root = self.tree.insert('','end', text='操作列表', open =True)
        for item in tree_items:
            self.tree.insert(tree_root, 'end', text=item, values=(-1), open=False)
        
        self.ntbook.grid(row=0, column=2, rowspan=2, sticky=NSEW)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
        self.ntbook.rowconfigure(0, weight=1)
        self.ntbook.columnconfigure(0, weight=1)
        
        self.log_text=scrolledtext.ScrolledText(self, state='disabled')
        self.log_text.config(font=('TkFixedFont', 10, 'normal'))
        self.log_text.grid(row=3, column=2, rowspan=2, sticky=EW)
              
        # Create textLogger
        text_handler = TextHandler(self.log_text)        
        # Add the handler to logger
        
        logger.addHandler(text_handler)
        logger.setLevel(logging.INFO) 
        
        self.tree.bind('<<TreeviewSelect>>',self.select_func)
        self.ntbook.bind('<<NotebookTabChanged>>', self.tab_changed)
                           
    def tab_changed(self, event):
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
        select = self.tree.selection()        
        if not select :
            return
        
        sel=select[0]
        i_per = int(self.tree.item(sel, 'values')[0])
                      
        i_sel = self.ntbook.index(END)
        
        if i_per==-1:
            nt_title=self.tree.item(sel, 'text')
            i_index=tree_items.index(nt_title)
            if i_index==0:
                if not self.data_syc_tab:
                    self.data_syc_tab = data_syc_pane(self) 
                    self.ntbook.add(self.data_syc_tab, text=nt_title, sticky=NSEW)
                    self.tree.set(sel, 'col0', i_sel)
                    self.ntbook.select(i_sel)
            elif i_index==1:
                if not self.his_data_tab:
                    self.his_data_tab = history_pane(self)
                    self.ntbook.add(self.his_data_tab, text=nt_title, sticky=NSEW) 
                    self.tree.set(sel, 'col0', i_sel)
                    self.ntbook.select(i_sel)
            elif i_index==2:
                if not self.run_chart_tab:
                    self.run_chart_tab = run_chart_pane(self)
                    self.ntbook.add(self.run_chart_tab, text=nt_title, sticky=NSEW) 
                    self.tree.set(sel, 'col0', i_sel)
                    self.ntbook.select(i_sel)
            elif i_index==3:
                if not self.data_analysis_tab:
                    self.data_analysis_tab = data_analysis_pane(self)
                    self.ntbook.add(self.data_analysis_tab, text=nt_title, sticky=NSEW)
                    self.tree.set(sel, 'col0', i_sel)
                    self.ntbook.select(i_sel)
        else:                
            self.ntbook.select(i_per)   
    
        
class Application():
    def __init__(self, root):      
        main_frame = mainframe(root)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.grid(row=0, column=0, sticky=NSEW)
        
        root.protocol("WM_DELETE_WINDOW", self.quit_func)

    def quit_func(self):          
        root.destroy()
                
if __name__ == '__main__':   
    root=Tk() 
    #root.resizable(0, 0)
    #sysstr = platform.system()
    try:                                   # Automatic zoom if possible
        root.wm_state("zoomed")
    except TclError:                    # Manual zoom
        # get the screen dimensions
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()

        # borm: width x height + x_offset + y_offset
        geom_string = "%dx%d+0+0" % (width, height)
        root.wm_geometry(geom_string)
    root.title('股票分析器')
    default_font = font.nametofont("TkDefaultFont")
    default_font.configure(size=10)  
    root.option_add("*Font", default_font)
    Application(root)
    root.geometry('800x600')
    root.mainloop()
