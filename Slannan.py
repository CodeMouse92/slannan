#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pygtk
pygtk.require('2.0')
import gtk, pango, gobject
import sqlite3
import datetime
import webbrowser
import os, sys

filename = ""
scaledscore = 0

#Benny is the working dictionary set for SLANNAN.

#BACKGROUND: Benny is a talking book that guides Ella and Slannen. Thus, it really
#doesn't take much imagination to figure out that his name should be lent to the
#program's dictionaries.

benny = []
benny_heston = {}
benny_des = {}
benny_cdate = {}
benny_mdate = {}
benny_comments = {}

g_bug_name = ""
g_des = ""
g_heston = 0
g_cdate = ""
g_mdate = ""
g_comments = ""

#This is the liststore for Char.
CharList = gtk.ListStore(str, str, int, str, str, str)

#These are the undo and redo dictionaries for Koopootuk.
            
b_1 = []
bhes_1 = {}
bdes_1 = {}
bcdate_1 = {}
bmdate_1 = {}
bcom_1 = {}
            
b_2 = []
bhes_2 = {}
bdes_2 = {}
bcdate_2 = {}
bmdate_2 = {}
bcom_2 = {}
            
b_3 = []
bhes_3 = {}
bdes_3 = {}
bcdate_3 = {}
bmdate_3 = {}
bcom_3 = {}
            
b_4 = []
bhes_4 = {}
bdes_4 = {}
bcdate_4 = {}
bmdate_4 = {}
bcom_4 = {}
            
b_5 = []
bhes_5 = {}
bdes_5 = {}
bcdate_5 = {}
bmdate_5 = {}
bcom_5 = {}
            
b_6 = []
bhes_6 = {}
bdes_6 = {}
bcdate_6 = {}
bmdate_6 = {}
bcom_6 = {}
            
b_7 = []
bhes_7 = {}
bdes_7 = {}
bcdate_7 = {}
bmdate_7 = {}
bcom_7 = {}
            
b_8 = []
bhes_8 = {}
bdes_8 = {}
bcdate_8 = {}
bmdate_8 = {}
bcom_8 = {}
            
b_9 = []
bhes_9 = {}
bdes_9 = {}
bcdate_9 = {}
bmdate_9 = {}
bcom_9 = {}
            
b_10 = []
bhes_10 = {}
bdes_10 = {}
bcdate_10 = {}
bmdate_10 = {}
bcom_10 = {}
            
b_r1 = []
bhes_r1 = {}
bdes_r1 = {}
bcdate_r1 = {}
bmdate_r1 = {}
bcom_r1 = {}
            
b_r2 = []
bhes_r2 = {}
bdes_r2 = {}
bcdate_r2 = {}
bmdate_r2 = {}
bcom_r2 = {}
            
b_r3 = []
bhes_r3 = {}
bdes_r3 = {}
bcdate_r3 = {}
bmdate_r3 = {}
bcom_r3 = {}
            
b_r4 = []
bhes_r4 = {}
bdes_r4 = {}
bcdate_r4 = {}
bmdate_r4 = {}
bcom_r4 = {}
            
b_r5 = []
bhes_r5 = {}
bdes_r5 = {}
bcdate_r5 = {}
bmdate_r5 = {}
bcom_r5 = {}
            
b_r6 = []
bhes_r6 = {}
bdes_r6 = {}
bcdate_r6 = {}
bmdate_r6 = {}
bcom_r6 = {}
            
b_r7 = []
bhes_r7 = {}
bdes_r7 = {}
bcdate_r7 = {}
bmdate_r7 = {}
bcom_r7 = {}
            
b_r8 = []
bhes_r8 = {}
bdes_r8 = {}
bcdate_r8 = {}
bmdate_r8 = {}
bcom_r8 = {}
            
b_r9 = []
bhes_r9 = {}
bdes_r9 = {}
bcdate_r9 = {}
bmdate_r9 = {}
bcom_r9 = {}
            
b_r10 = []
bhes_r10 = {}
bdes_r10 = {}
bcdate_r10 = {}
bmdate_r10 = {}
bcom_r10 = {}


class Slannan:
    
    def delete_event(self, event, widget, data=None):
        #Closes the application.
        gtk.main_quit()
        return False
                
    
    def __init__(self):
        
        def Areida(function, projectname):
            #Areida is the database bridge.
            
            #BACKGROUND: Areida is Ella's best friend in the movie, though the 
            #usage of the name for this module is a play on words - "a-READ-a"
                
            global filename, CharList, benny, benny_des, benny_heston, benny_cdate, benny_mdate, benny_comments
            
            spinner.show()
            
            if function == "create":
                
                try:
                    conn = sqlite3.connect(projectname)
                    c = conn.cursor()
                                    
                    c.execute('''create table bugs (id, bug text, heston int, description string, 
                            createdate text, moddate text, comments text)''')
                                
                    conn.commit()
                    c.close()
                            
                    save_item.set_sensitive(True)
                    saveas_item.set_sensitive(True)
                    save_tb.set_sensitive(True)
                    saveas_tb.set_sensitive(True)
                    close_item.set_sensitive(True)
                    close_tb.set_sensitive(True)
                    createbug_item.set_sensitive(True)
                    add_tb.set_sensitive(True)
                except sqlite3.OperationalError:
                    message = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, "The file already exists. Creation canceled.")
                    response = message.run()
                    message.destroy()
                    filename = ""
                            
            elif function == "load":
                global benny, benny_heston, benny_des, benny_cdate, benny_mdate, benny_comments
                
                conn = sqlite3.connect(projectname)
                
                c = conn.cursor()
                    
                c.execute("SELECT Count(*) FROM bugs")
                Result = c.fetchall()
                count = Result[0][0]
                idx = 0
                    
                while idx <= count:
                    row = c.execute("SELECT bug FROM bugs WHERE id = ?", (idx,) ).fetchone()
                    if row:
                        bug_name = str(row[0])
                        benny.append(bug_name)
                            
                    row = c.execute("SELECT heston FROM bugs WHERE id = ?", (idx,) ).fetchone()
                    if row:
                        benny_heston[bug_name] = row[0]
                            
                    row = c.execute("SELECT createdate FROM bugs WHERE id = ?", (idx,) ).fetchone()
                    if row:
                        benny_cdate[bug_name] = str(row[0])
                            
                    row = c.execute("SELECT moddate FROM bugs WHERE id = ?", (idx,) ).fetchone()
                    if row:
                        benny_mdate[bug_name] = str(row[0])
                            
                    row = c.execute("SELECT description FROM bugs WHERE id = ?", (idx,) ).fetchone()
                    if row:
                        benny_des[bug_name] = str(row[0])
                            
                    row = c.execute("SELECT comments FROM bugs WHERE id = ?", (idx,) ).fetchone()
                    if row:
                        benny_comments[bug_name] = str(row[0])
                        
                    idx = idx + 1
                    
                conn.commit()
                c.close()
                try:
                    Char()
                except ValueError:
                    pass
                
                save_item.set_sensitive(True)
                saveas_item.set_sensitive(True)
                save_tb.set_sensitive(True)
                saveas_tb.set_sensitive(True)
                close_item.set_sensitive(True)
                close_tb.set_sensitive(True)
                createbug_item.set_sensitive(True)
                add_tb.set_sensitive(True)
                            
            elif function == "save":
                conn = sqlite3.connect(projectname)
                c = conn.cursor()
                    
                c.execute('''drop table bugs''')
                c.execute('''create table bugs (id, bug text, heston int, description string, 
                        createdate text, moddate text, comments text)''')
                if benny:
                    midx = benny.index(max(benny))
                    idx = 0
                    while idx <= midx:
                        work = benny[idx]
                        c.execute('''insert into bugs values (?, ?, ?, ?, ?, ?, ?)''', (idx, work, benny_heston[work], benny_des[work], benny_cdate[work], benny_mdate[work], benny_comments[work]))
                        idx = idx + 1
                    
                conn.commit()
                c.close()
                    
            elif function == "saveas":
                conn = sqlite3.connect(projectname)
                c = conn.cursor()
                    
                
                c.execute('''create table bugs (id, bug text, heston int, description string, 
                        createdate text, moddate text, comments text)''')
                if benny:
                    midx = benny.index(max(benny))
                    idx = 0
                    while idx <= midx:
                        work = benny[idx]
                        c.execute('''insert into bugs values (?, ?, ?, ?, ?, ?, ?)''', (idx, work, benny_des[work], benny_heston[work], benny_cdate[work], benny_mdate[work], benny_comments[work]))
                        idx = idx + 1
                        
                conn.commit()
                c.close()
                
                
            elif function == "close":
                benny = []
                benny_heston = {}
                benny_des = {}
                benny_cdate = {}
                benny_mdate = {}
                benny_comments = {}
                Koopootuk("reset")
                CharList.clear()
                filename = ""
                
                bru_name.set_text("Bug Name: ")
                bru_des.set_text("Description: ")
                bru_hes.set_text("Heston Rank: ")
                bru_mdate.set_text("Date Created: ")
                bru_cdate.set_text("Date Last Modified: ")
                bru_com.set_text("Comments: ")
                
                vb_luc.hide()
                vb_man.hide()
                bru.show()
                
                save_item.set_sensitive(False)
                saveas_item.set_sensitive(False)
                close_item.set_sensitive(False)
                save_tb.set_sensitive(False)
                saveas_tb.set_sensitive(False)
                close_item.set_sensitive(False)
                close_tb.set_sensitive(False)
                undo_item.set_sensitive(False)
                undo_tb.set_sensitive(False)
                redo_item.set_sensitive(False)
                redo_tb.set_sensitive(False)
                createbug_item.set_sensitive(False)
                modifybug_item.set_sensitive(False)
                deletebug_item.set_sensitive(False)
                add_tb.set_sensitive(False)
                edit_tb.set_sensitive(False)
                delete_tb.set_sensitive(False)
                
            spinner.hide()
                
        def Lucinda(bug_name, heston, des, comments):
            #Lucinda creates bugs.
            
            #BACKGROUND: Lucinda is infamous for her horrible fairy gifts (including the one 
            #she gave to Ella. Essentially, she creates "bugs".
                
            global CharList, benny, benny_des, benny_heston, benny_cdate, benny_mdate, benny_comments
            
            spinner.show()
            
            Koopootuk("record")
            now = datetime.datetime.now()
            cdate = str(now.strftime("%m-%d-%y %H:%M"))
            mdate = cdate
            benny.append(bug_name)
            benny_heston[bug_name] = heston
            benny_des[bug_name] = des
            benny_cdate[bug_name] = cdate
            benny_mdate[bug_name] = mdate
            benny_comments[bug_name] = comments
            
            CharList.clear()
            Char()
            
            spinner.hide()
                        

        def Nish(bug_name):
            #Nish destroys bugs.
            
            #BACKGROUND: Nish is an ogre. Once he agrees to help Slannen and Ella in the movie,
            #he helps squash a number of problems. Thus, "Nish" destroys bug data.
                
            global benny, benny_heston, benny_des, benny_cdate, benny_mdate, benny_comments
            
            spinner.show()
            
            Koopootuk("record")
            
            benny.remove(bug_name)
            del benny_heston[bug_name]
            del benny_des[bug_name]
            del benny_cdate[bug_name]
            del benny_mdate[bug_name]
            del benny_comments[bug_name]
            CharList.clear()
            Char()
            
            spinner.hide()

        def Mandy(bug_name, hes, des, com):
            #Mandy changes the modifiable properties on a bug.
            
            #BACKGROUND: Mandy does a lot of creating, and is Benny's girlfriend. In the book and movie both, 
            #she finds clever ways to circumvent problems, thus "Mandy" modifies bug properties.
                
            global benny_comments, benny_des, benny_heston
            
            spinner.show()
            
            Koopootuk("record")
            now = datetime.datetime.now()
            
            benny_heston[bug_name] = hes
            benny_des[bug_name] = des
            benny_comments[bug_name] = com
            benny_mdate[bug_name] = str(now.strftime("%m-%d-%y %H:%M"))
            
            CharList.clear()
            Char()
            
            spinner.hide()
        
        def Koopootuk(function):
            #Koopootuk creates and stores the undo/redo dictionaries.
            
            #BACKGROUND: Koopootuk is a friendly giant who talks at length with Char
            #about how to change the treatment of giants. Thus, "Koopootuk" turns back
            #the clock with the undo/redo functions.
            
            global CharList, benny, benny_heston, benny_des, benny_cdate, benny_mdate, benny_comments, b_10, b_9, b_8, b_7, b_6, b_5, b_4, b_3, b_2, b_1, bhes_10, bhes_9, bhes_8, bhes_7, bhes_6, bhes_5, bhes_4, bhes_3, bhes_2, bhes_1, bdes_10, bdes_9, bdes_8, bdes_7, bdes_6, bdes_5, bdes_4, bdes_3, bdes_2, bdes_1, bcdate_10, bcdate_9, bcdate_8, bcdate_7, bcdate_6, bcdate_5, bcdate_4, bcdate_3, bcdate_2, bcdate_1, bmdate_10, bmdate_9, bmdate_8, bmdate_7, bmdate_6, bmdate_5, bmdate_4, bmdate_3, bmdate_2, bmdate_1, bcom_10, bcom_9, bcom_8, bcom_7, bcom_6, bcom_5, bcom_4, bcom_3, bcom_2, bcom_1, b_r10, b_r9, b_r8, b_r7, b_r6, b_r5, b_r4, b_r3, b_r2, b_r1, bhes_r10, bhes_r9, bhes_r8, bhes_r7, bhes_r6, bhes_r5, bhes_r4, bhes_r3, bhes_r2, bhes_r1, bdes_r10, bdes_r9, bdes_r8, bdes_r7, bdes_r6, bdes_r5, bdes_r4, bdes_r3, bdes_r2, bdes_r1, bcdate_r10, bcdate_r9, bcdate_r8, bcdate_r7, bcdate_r6, bcdate_r5, bcdate_r4, bcdate_r3, bcdate_r2, bcdate_r1, bmdate_r10, bmdate_r9, bmdate_r8, bmdate_r7, bmdate_r6, bmdate_r5, bmdate_r4, bmdate_r3, bmdate_r2, bmdate_r1, bcom_r10, bcom_r9, bcom_r8, bcom_r7, bcom_r6, bcom_r5, bcom_r4, bcom_r3, bcom_r2, bcom_r1
            
            #The record function records the dictionaries in the undo dictionaries.
            
            spinner.show()
            
            if function == "record":
                
                b_10 = b_9[:]
                b_9 = b_8[:]
                b_8 = b_7[:]
                b_7 = b_6[:]
                b_6 = b_5[:]
                b_5 = b_4[:]
                b_4 = b_3[:]
                b_3 = b_2[:]
                b_2 = b_1[:]
                b_1 = benny[:]
                
                bhes_10 = bhes_9.copy()
                bhes_9 = bhes_8.copy()
                bhes_8 = bhes_7.copy()
                bhes_7 = bhes_6.copy()
                bhes_6 = bhes_5.copy()
                bhes_5 = bhes_4.copy()
                bhes_4 = bhes_3.copy()
                bhes_3 = bhes_2.copy()
                bhes_2 = bhes_1.copy()
                bhes_1 = benny_heston.copy()
                
                bdes_10 = bdes_9.copy()
                bdes_9 = bdes_8.copy()
                bdes_8 = bdes_7.copy()
                bdes_7 = bdes_6.copy()
                bdes_6 = bdes_5.copy()
                bdes_5 = bdes_4.copy()
                bdes_4 = bdes_3.copy()
                bdes_3 = bdes_2.copy()
                bdes_2 = bdes_1.copy()
                bdes_1 = benny_des.copy()
                
                bcdate_10 = bcdate_9.copy()
                bcdate_9 = bcdate_8.copy()
                bcdate_8 = bcdate_7.copy()
                bcdate_7 = bcdate_6.copy()
                bcdate_6 = bcdate_5.copy()
                bcdate_5 = bcdate_4.copy()
                bcdate_4 = bcdate_3.copy()
                bcdate_3 = bcdate_2.copy()
                bcdate_2 = bcdate_1.copy()
                bcdate_1 = benny_cdate.copy()
                
                bmdate_10 = bmdate_9.copy()
                bmdate_9 = bmdate_8.copy()
                bmdate_8 = bmdate_7.copy()
                bmdate_7 = bmdate_6.copy()
                bmdate_6 = bmdate_5.copy()
                bmdate_5 = bmdate_4.copy()
                bmdate_4 = bmdate_3.copy()
                bmdate_3 = bmdate_2.copy()
                bmdate_2 = bmdate_1.copy()
                bmdate_1 = benny_mdate.copy()
                
                bcom_10 = bcom_9.copy()
                bcom_9 = bcom_8.copy()
                bcom_8 = bcom_7.copy()
                bcom_7 = bcom_6.copy()
                bcom_6 = bcom_5.copy()
                bcom_5 = bcom_4.copy()
                bcom_4 = bcom_3.copy()
                bcom_3 = bcom_2.copy()
                bcom_2 = bcom_1.copy()
                bcom_1 = benny_comments.copy()

                b_r1 = []
                bhes_r1 = {}
                bdes_r1 = {}
                bcdate_r1 = {}
                bmdate_r1 = {}
                bcom_r1 = {}
                            
                b_r2 = []
                bhes_r2 = {}
                bdes_r2 = {}
                bcdate_r2 = {}
                bmdate_r2 = {}
                bcom_r2 = {}
                            
                b_r3 = []
                bhes_r3 = {}
                bdes_r3 = {}
                bcdate_r3 = {}
                bmdate_r3 = {}
                bcom_r3 = {}
                            
                b_r4 = []
                bhes_r4 = {}
                bdes_r4 = {}
                bcdate_r4 = {}
                bmdate_r4 = {}
                bcom_r4 = {}
                            
                b_r5 = []
                bhes_r5 = {}
                bdes_r5 = {}
                bcdate_r5 = {}
                bmdate_r5 = {}
                bcom_r5 = {}
                            
                b_r6 = []
                bhes_r6 = {}
                bdes_r6 = {}
                bcdate_r6 = {}
                bmdate_r6 = {}
                bcom_r6 = {}
                            
                b_r7 = []
                bhes_r7 = {}
                bdes_r7 = {}
                bcdate_r7 = {}
                bmdate_r7 = {}
                bcom_r7 = {}
                            
                b_r8 = []
                bhes_r8 = {}
                bdes_r8 = {}
                bcdate_r8 = {}
                bmdate_r8 = {}
                bcom_r8 = {}
                            
                b_r9 = []
                bhes_r9 = {}
                bdes_r9 = {}
                bcdate_r9 = {}
                bmdate_r9 = {}
                bcom_r9 = {}
                            
                b_r10 = []
                bhes_r10 = {}
                bdes_r10 = {}
                bcdate_r10 = {}
                bmdate_r10 = {}
                bcom_r10 = {}
                
                if b_1 == []:
                    undo_item.set_sensitive(False)
                    undo_tb.set_sensitive(False)
                elif b_1 != []:
                    undo_item.set_sensitive(True)
                    undo_tb.set_sensitive(True)
                    
                if b_r1 == []:
                    redo_item.set_sensitive(False)
                    redo_tb.set_sensitive(False)
                elif b_r1 != []:
                    redo_item.set_sensitive(True)
                    redo_tb.set_sensitive(True)
                
            #The undo function shifts the current dictionaries to the redo dictionaries, and the last undo dictionaries to the current dictionaries.
            elif function == "undo":

                b_r10 = b_r9[:]
                b_r9 = b_r8[:]
                b_r8 = b_r7[:]
                b_r7 = b_r6[:]
                b_r6 = b_r5[:]
                b_r5 = b_r4[:]
                b_r4 = b_r3[:]
                b_r3 = b_r2[:]
                b_r2 = b_r1[:]
                b_r1 = benny[:]
                benny = b_1[:]
                b_1 = b_2[:]
                b_2 = b_3[:]
                b_3 = b_4[:]
                b_4 = b_5[:]
                b_5 = b_6[:]
                b_6 = b_7[:]
                b_7 = b_8[:]
                b_8 = b_9[:]
                b_9 = b_10[:]
                b_10 = []
                
                bhes_r10 = bhes_r9.copy()
                bhes_r9 = bhes_r8.copy()
                bhes_r8 = bhes_r7.copy()
                bhes_r7 = bhes_r6.copy()
                bhes_r6 = bhes_r5.copy()
                bhes_r5 = bhes_r4.copy()
                bhes_r4 = bhes_r3.copy()
                bhes_r3 = bhes_r2.copy()
                bhes_r2 = bhes_r1.copy()
                bhes_r1 = benny_heston.copy()
                benny_heston = bhes_1.copy()
                bhes_1 = bhes_2.copy()
                bhes_2 = bhes_3.copy()
                bhes_3 = bhes_4.copy()
                bhes_4 = bhes_5.copy()
                bhes_5 = bhes_6.copy()
                bhes_6 = bhes_7.copy()
                bhes_7 = bhes_8.copy()
                bhes_8 = bhes_9.copy()
                bhes_9 = bhes_10.copy()
                bhes_10 = []
                
                bdes_r10 = bdes_r9.copy()
                bdes_r9 = bdes_r8.copy()
                bdes_r8 = bdes_r7.copy()
                bdes_r7 = bdes_r6.copy()
                bdes_r6 = bdes_r5.copy()
                bdes_r5 = bdes_r4.copy()
                bdes_r4 = bdes_r3.copy()
                bdes_r3 = bdes_r2.copy()
                bdes_r2 = bdes_r1.copy()
                bdes_r1 = benny_des.copy()
                benny_des = bdes_1.copy()
                bdes_1 = bdes_2.copy()
                bdes_2 = bdes_3.copy()
                bdes_3 = bdes_4.copy()
                bdes_4 = bdes_5.copy()
                bdes_5 = bdes_6.copy()
                bdes_6 = bdes_7.copy()
                bdes_7 = bdes_8.copy()
                bdes_8 = bdes_9.copy()
                bdes_9 = bdes_10.copy()
                bdes_10 = []
                
                bcdate_r10 = bcdate_r9.copy()
                bcdate_r9 = bcdate_r8.copy()
                bcdate_r8 = bcdate_r7.copy()
                bcdate_r7 = bcdate_r6.copy()
                bcdate_r6 = bcdate_r5.copy()
                bcdate_r5 = bcdate_r4.copy()
                bcdate_r4 = bcdate_r3.copy()
                bcdate_r3 = bcdate_r2.copy()
                bcdate_r2 = bcdate_r1.copy()
                bcdate_r1 = benny_cdate.copy()
                benny_cdate = bcdate_1.copy()
                bcdate_1 = bcdate_2.copy()
                bcdate_2 = bcdate_3.copy()
                bcdate_3 = bcdate_4.copy()
                bcdate_4 = bcdate_5.copy()
                bcdate_5 = bcdate_6.copy()
                bcdate_6 = bcdate_7.copy()
                bcdate_7 = bcdate_8.copy()
                bcdate_8 = bcdate_9.copy()
                bcdate_9 = bcdate_10.copy()
                bcdate_10 = []
                
                bmdate_r10 = bmdate_r9.copy()
                bmdate_r9 = bmdate_r8.copy()
                bmdate_r8 = bmdate_r7.copy()
                bmdate_r7 = bmdate_r6.copy()
                bmdate_r6 = bmdate_r5.copy()
                bmdate_r5 = bmdate_r4.copy()
                bmdate_r4 = bmdate_r3.copy()
                bmdate_r3 = bmdate_r2.copy()
                bmdate_r2 = bmdate_r1.copy()
                bmdate_r1 = benny_mdate.copy()
                benny_mdate = bmdate_1.copy()
                bmdate_1 = bmdate_2.copy()
                bmdate_2 = bmdate_3.copy()
                bmdate_3 = bmdate_4.copy()
                bmdate_4 = bmdate_5.copy()
                bmdate_5 = bmdate_6.copy()
                bmdate_6 = bmdate_7.copy()
                bmdate_7 = bmdate_8.copy()
                bmdate_8 = bmdate_9.copy()
                bmdate_9 = bmdate_10.copy()
                bmdate_10 = []
                
                bcom_r10 = bcom_r9.copy()
                bcom_r9 = bcom_r8.copy()
                bcom_r8 = bcom_r7.copy()
                bcom_r7 = bcom_r6.copy()
                bcom_r6 = bcom_r5.copy()
                bcom_r5 = bcom_r4.copy()
                bcom_r4 = bcom_r3.copy()
                bcom_r3 = bcom_r2.copy()
                bcom_r2 = bcom_r1.copy()
                bcom_r1 = benny_comments.copy()
                benny_comments = bcom_1.copy()
                bcom_1 = bcom_2.copy()
                bcom_2 = bcom_3.copy()
                bcom_3 = bcom_4.copy()
                bcom_4 = bcom_5.copy()
                bcom_5 = bcom_6.copy()
                bcom_6 = bcom_7.copy()
                bcom_7 = bcom_8.copy()
                bcom_8 = bcom_9.copy()
                bcom_9 = bcom_10.copy()
                bcom_10 = []
                
                CharList.clear()
                Char()
                
                if b_1 == []:
                    undo_item.set_sensitive(False)
                    undo_tb.set_sensitive(False)
                elif b_1 != []:
                    undo_item.set_sensitive(True)
                    undo_tb.set_sensitive(True)
                    
                if b_r1 == []:
                    redo_item.set_sensitive(False)
                    redo_tb.set_sensitive(False)
                elif b_r1 != []:
                    redo_item.set_sensitive(True)
                    redo_tb.set_sensitive(True)
                
            #The redo function does the exact opposite of the undo function.
            elif function == "redo":
                
                b_10 = b_9[:]
                b_9 = b_8[:]
                b_8 = b_7[:]
                b_7 = b_6[:]
                b_6 = b_5[:]
                b_5 = b_4[:]
                b_4 = b_3[:]
                b_3 = b_2[:]
                b_2 = b_1[:]
                b_1 = benny[:]
                benny = b_r1[:]
                b_r1 = b_r2[:]
                b_r2 = b_r3[:]
                b_r3 = b_r4[:]
                b_r4 = b_r5[:]
                b_r5 = b_r6[:]
                b_r6 = b_r7[:]
                b_r7 = b_r8[:]
                b_r8 = b_r9[:]
                b_r9 = b_r10[:]
                b_r10 = []
                
                bhes_10 = bhes_9.copy()
                bhes_9 = bhes_8.copy()
                bhes_8 = bhes_7.copy()
                bhes_7 = bhes_6.copy()
                bhes_6 = bhes_5.copy()
                bhes_5 = bhes_4.copy()
                bhes_4 = bhes_3.copy()
                bhes_3 = bhes_2.copy()
                bhes_2 = bhes_1.copy()
                bhes_1 = benny_heston.copy()
                benny_heston = bhes_r1.copy()
                bhes_r1 = bhes_r2.copy()
                bhes_r2 = bhes_r3.copy()
                bhes_r3 = bhes_r4.copy()
                bhes_r4 = bhes_r5.copy()
                bhes_r5 = bhes_r6.copy()
                bhes_r6 = bhes_r7.copy()
                bhes_r7 = bhes_r8.copy()
                bhes_r8 = bhes_r9.copy()
                bhes_r9 = bhes_r10.copy()
                bhes_r10 = []

                bdes_10 = bdes_9.copy()
                bdes_9 = bdes_8.copy()
                bdes_8 = bdes_7.copy()
                bdes_7 = bdes_6.copy()
                bdes_6 = bdes_5.copy()
                bdes_5 = bdes_4.copy()
                bdes_4 = bdes_3.copy()
                bdes_3 = bdes_2.copy()
                bdes_2 = bdes_1.copy()
                bdes_1 = benny_des.copy()
                benny_des = bdes_r1.copy()
                bdes_r1 = bdes_r2.copy()
                bdes_r2 = bdes_r3.copy()
                bdes_r3 = bdes_r4.copy()
                bdes_r4 = bdes_r5.copy()
                bdes_r5 = bdes_r6.copy()
                bdes_r6 = bdes_r7.copy()
                bdes_r7 = bdes_r8.copy()
                bdes_r8 = bdes_r9.copy()
                bdes_r9 = bdes_r10.copy()
                bdes_r10 = []

                bcdate_10 = bcdate_9.copy()
                bcdate_9 = bcdate_8.copy()
                bcdate_8 = bcdate_7.copy()
                bcdate_7 = bcdate_6.copy()
                bcdate_6 = bcdate_5.copy()
                bcdate_5 = bcdate_4.copy()
                bcdate_4 = bcdate_3.copy()
                bcdate_3 = bcdate_2.copy()
                bcdate_2 = bcdate_1.copy()
                bcdate_1 = benny_cdate.copy()
                benny_cdate = bcdate_r1.copy()
                bcdate_r1 = bcdate_r2.copy()
                bcdate_r2 = bcdate_r3.copy()
                bcdate_r3 = bcdate_r4.copy()
                bcdate_r4 = bcdate_r5.copy()
                bcdate_r5 = bcdate_r6.copy()
                bcdate_r6 = bcdate_r7.copy()
                bcdate_r7 = bcdate_r8.copy()
                bcdate_r8 = bcdate_r9.copy()
                bcdate_r9 = bcdate_r10.copy()
                bcdate_r10 = []
                
                bmdate_10 = bmdate_9.copy()
                bmdate_9 = bmdate_8.copy()
                bmdate_8 = bmdate_7.copy()
                bmdate_7 = bmdate_6.copy()
                bmdate_6 = bmdate_5.copy()
                bmdate_5 = bmdate_4.copy()
                bmdate_4 = bmdate_3.copy()
                bmdate_3 = bmdate_2.copy()
                bmdate_2 = bmdate_1.copy()
                bmdate_1 = benny_mdate.copy()
                benny_mdate = bmdate_r1.copy()
                bmdate_r1 = bmdate_r2.copy()
                bmdate_r2 = bmdate_r3.copy()
                bmdate_r3 = bmdate_r4.copy()
                bmdate_r4 = bmdate_r5.copy()
                bmdate_r5 = bmdate_r6.copy()
                bmdate_r6 = bmdate_r7.copy()
                bmdate_r7 = bmdate_r8.copy()
                bmdate_r8 = bmdate_r9.copy()
                bmdate_r9 = bmdate_r10.copy()
                bmdate_r10 = []
                
                bcom_10 = bcom_9.copy()
                bcom_9 = bcom_8.copy()
                bcom_8 = bcom_7.copy()
                bcom_7 = bcom_6.copy()
                bcom_6 = bcom_5.copy()
                bcom_5 = bcom_4.copy()
                bcom_4 = bcom_3.copy()
                bcom_3 = bcom_2.copy()
                bcom_2 = bcom_1.copy()
                bcom_1 = benny_comments.copy()
                benny_comments = bcom_r1.copy()
                bcom_r1 = bcom_r2.copy()
                bcom_r2 = bcom_r3.copy()
                bcom_r3 = bcom_r4.copy()
                bcom_r4 = bcom_r5.copy()
                bcom_r5 = bcom_r6.copy()
                bcom_r6 = bcom_r7.copy()
                bcom_r7 = bcom_r8.copy()
                bcom_r8 = bcom_r9.copy()
                bcom_r9 = bcom_r10.copy()
                bcom_r10 = []
                
                CharList.clear()
                Char()
                
                if b_1 == []:
                    undo_item.set_sensitive(False)
                    undo_tb.set_sensitive(False)
                elif b_1 != []:
                    undo_item.set_sensitive(True)
                    undo_tb.set_sensitive(True)
                    
                if b_r1 == []:
                    redo_item.set_sensitive(False)
                    redo_tb.set_sensitive(False)
                elif b_r1 != []:
                    redo_item.set_sensitive(True)
                    redo_tb.set_sensitive(True)
                
            elif function == "reset":
                b_1 = []
                bhes_1 = {}
                bdes_1 = {}
                bcdate_1 = {}
                bmdate_1 = {}
                bcom_1 = {}
                            
                b_2 = []
                bhes_2 = {}
                bdes_2 = {}
                bcdate_2 = {}
                bmdate_2 = {}
                bcom_2 = {}
                            
                b_3 = []
                bhes_3 = {}
                bdes_3 = {}
                bcdate_3 = {}
                bmdate_3 = {}
                bcom_3 = {}
                            
                b_4 = []
                bhes_4 = {}
                bdes_4 = {}
                bcdate_4 = {}
                bmdate_4 = {}
                bcom_4 = {}
                            
                b_5 = []
                bhes_5 = {}
                bdes_5 = {}
                bcdate_5 = {}
                bmdate_5 = {}
                bcom_5 = {}
                            
                b_6 = []
                bhes_6 = {}
                bdes_6 = {}
                bcdate_6 = {}
                bmdate_6 = {}
                bcom_6 = {}
                            
                b_7 = []
                bhes_7 = {}
                bdes_7 = {}
                bcdate_7 = {}
                bmdate_7 = {}
                bcom_7 = {}
                            
                b_8 = []
                bhes_8 = {}
                bdes_8 = {}
                bcdate_8 = {}
                bmdate_8 = {}
                bcom_8 = {}
                            
                b_9 = []
                bhes_9 = {}
                bdes_9 = {}
                bcdate_9 = {}
                bmdate_9 = {}
                bcom_9 = {}
                            
                b_10 = []
                bhes_10 = {}
                bdes_10 = {}
                bcdate_10 = {}
                bmdate_10 = {}
                bcom_10 = {}
                            
                b_r1 = []
                bhes_r1 = {}
                bdes_r1 = {}
                bcdate_r1 = {}
                bmdate_r1 = {}
                bcom_r1 = {}
                            
                b_r2 = []
                bhes_r2 = {}
                bdes_r2 = {}
                bcdate_r2 = {}
                bmdate_r2 = {}
                bcom_r2 = {}
                            
                b_r3 = []
                bhes_r3 = {}
                bdes_r3 = {}
                bcdate_r3 = {}
                bmdate_r3 = {}
                bcom_r3 = {}
                            
                b_r4 = []
                bhes_r4 = {}
                bdes_r4 = {}
                bcdate_r4 = {}
                bmdate_r4 = {}
                bcom_r4 = {}
                            
                b_r5 = []
                bhes_r5 = {}
                bdes_r5 = {}
                bcdate_r5 = {}
                bmdate_r5 = {}
                bcom_r5 = {}
                            
                b_r6 = []
                bhes_r6 = {}
                bdes_r6 = {}
                bcdate_r6 = {}
                bmdate_r6 = {}
                bcom_r6 = {}
                            
                b_r7 = []
                bhes_r7 = {}
                bdes_r7 = {}
                bcdate_r7 = {}
                bmdate_r7 = {}
                bcom_r7 = {}
                            
                b_r8 = []
                bhes_r8 = {}
                bdes_r8 = {}
                bcdate_r8 = {}
                bmdate_r8 = {}
                bcom_r8 = {}
                            
                b_r9 = []
                bhes_r9 = {}
                bdes_r9 = {}
                bcdate_r9 = {}
                bmdate_r9 = {}
                bcom_r9 = {}
                            
                b_r10 = []
                bhes_r10 = {}
                bdes_r10 = {}
                bcdate_r10 = {}
                bmdate_r10 = {}
                bcom_r10 = {}
                
                if b_1 == []:
                    undo_item.set_sensitive(False)
                    undo_tb.set_sensitive(False)
                elif b_1 != []:
                    undo_item.set_sensitive(True)
                    undo_tb.set_sensitive(True)
                    
                if b_r1 == []:
                    redo_item.set_sensitive(False)
                    redo_tb.set_sensitive(False)
                elif b_r1 != []:
                    redo_item.set_sensitive(True)
                    redo_tb.set_sensitive(True)
                
            spinner.hide()
        
        def Char():
            #Char converts bug list to pygtk liststore, and calculates the scaled bug score.
            
            #BACKGROUND: Char is the handsome prince who wants the best for the kingdom.
            #There is little reason for this module being named after him, tho the extension
            #could be made that he has access to the royal library.
            
            global benny, benny_heston, benny_des, benny_cdate, benny_mdate, benny_comments, scaledscore
            
            spinner.show()
            
            midx = benny.index(max(benny))
            idx = 0
            scaledscore = 0
            while idx <= midx:
                work = benny[idx]
                scaledscore = scaledscore + benny_heston[work]
                lbl_scaledscore.set_text("Scaled Score: " + str(scaledscore))
                CharList.append([work, benny_des[work], benny_heston[work], benny_cdate[work], benny_mdate[work], benny_comments[work]])
                idx = idx + 1
                
            spinner.hide()
            
        def Brumhilda(bug_name):
            #Brumhilda loads a bug's values into the detail panel.
            
            #BACKGROUND: Brumhilda is Slannen's odd love interest. There is
            #no reason for this module being named "Brumhilda", except we ran
            #out of good protag names.
            
            global benny_heston, benny_des, benny_cdate, benny_mdate, benny_comments
            
            spinner.show()
            
            bru_name.set_text("Bug Name: " + bug_name)
            bru_des.set_text("Description: " + benny_des[bug_name])
            bru_hes.set_text("Heston Rank: H-" + str(benny_heston[bug_name]))
            bru_mdate.set_text("Date Created: " + benny_mdate[bug_name])
            bru_cdate.set_text("Date Last Modified: " + benny_cdate[bug_name])
            bru_com.set_text("Comments: " + benny_comments[bug_name])

            spinner.hide()
        
        def new_event(event, data=None):
            global filename

            if filename == "":
                chooser = gtk.FileChooserDialog(title="Choose Save Location...",action=gtk.FILE_CHOOSER_ACTION_SAVE, buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
                filter = gtk.FileFilter()
                filter.set_name("Slannan Files")
                filter.add_pattern("*.hes")
                chooser.add_filter(filter)
                
                response = chooser.run()
                if response == gtk.RESPONSE_OK:
                    filename = chooser.get_filename()
                    win.set_title("Slannan Bug Tracker - " + filename)
                    Areida("create", filename)
                
                elif response == gtk.RESPONSE_CANCEL:
                    pass
                chooser.destroy()
            else:
                label = gtk.Label("Do you want to save your changes before closing?")
                confirmclose = gtk.Dialog("Save Changes?", None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_YES, gtk.RESPONSE_ACCEPT, gtk.STOCK_NO, gtk.RESPONSE_REJECT))
                confirmclose.vbox.pack_start(label)
                label.show()
                response = confirmclose.run()
                if response == gtk.RESPONSE_ACCEPT:
                    Areida("save", filename)
                    
                    chooser = gtk.FileChooserDialog(title="Choose Save Location...",action=gtk.FILE_CHOOSER_ACTION_SAVE, buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
                    filter = gtk.FileFilter()
                    filter.set_name("Slannan Files")
                    filter.add_pattern("*.hes")
                    chooser.add_filter(filter)
                    
                    response = chooser.run()
                    if response == gtk.RESPONSE_OK:
                        filename = chooser.get_filename()
                        win.set_title("Slannan Bug Tracker - " + filename)
                        Areida("close", "")
                        Areida("create", filename)
                        
                    elif response == gtk.RESPONSE_CANCEL:
                        pass
                    chooser.destroy()
                elif response == gtk.RESPONSE_REJECT:
                    chooser = gtk.FileChooserDialog(title="Choose Save Location...",action=gtk.FILE_CHOOSER_ACTION_SAVE, buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
                    filter = gtk.FileFilter()
                    filter.set_name("Slannan Files")
                    filter.add_pattern("*.hes")
                    chooser.add_filter(filter)
                    
                    response = chooser.run()
                    if response == gtk.RESPONSE_OK:
                        filename = chooser.get_filename()
                        win.set_title("Slannan Bug Tracker - " + filename)
                        Areida("close", "")
                        Areida("create", filename)
                    
                    elif response == gtk.RESPONSE_CANCEL:
                        pass
                    chooser.destroy()
                confirmclose.destroy()
                
        def open_event(event, data=None):
            global filename
             
            if filename == "":
                chooser = gtk.FileChooserDialog(title="Open...",action=gtk.FILE_CHOOSER_ACTION_OPEN, buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
                filter = gtk.FileFilter()
                filter.set_name("Slannan Files")
                filter.add_pattern("*.hes")
                chooser.add_filter(filter)
                
                response = chooser.run()
                if response == gtk.RESPONSE_OK:
                    filename = chooser.get_filename()
                    Areida("load", filename)
                    win.set_title("Slannan Bug Tracker - " + filename)
                elif response == gtk.RESPONSE_CANCEL:
                    pass
                chooser.destroy()
            else:
                label = gtk.Label("Do you want to save your changes before closing?")
                confirmclose = gtk.Dialog("Save Changes?", None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_YES, gtk.RESPONSE_ACCEPT, gtk.STOCK_NO, gtk.RESPONSE_REJECT))
                confirmclose.vbox.pack_start(label)
                label.show()
                response = confirmclose.run()
                if response == gtk.RESPONSE_ACCEPT:
                    Areida("save", filename)
                    
                    chooser = gtk.FileChooserDialog(title="Open...",action=gtk.FILE_CHOOSER_ACTION_OPEN, buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
                    filter = gtk.FileFilter()
                    filter.set_name("Slannan Files")
                    filter.add_pattern("*.hes")
                    chooser.add_filter(filter)
                    
                    response = chooser.run()
                    if response == gtk.RESPONSE_OK:
                        filename = chooser.get_filename()
                        win.set_title("Slannan Bug Tracker - " + filename)
                        Areida("close", "")
                        Areida("load", filename)
                    elif response == gtk.RESPONSE_CANCEL:
                        pass
                    chooser.destroy()
                elif response == gtk.RESPONSE_REJECT:
                    chooser = gtk.FileChooserDialog(title="Open...",action=gtk.FILE_CHOOSER_ACTION_OPEN, buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
                    filter = gtk.FileFilter()
                    filter.set_name("Slannan Files")
                    filter.add_pattern("*.hes")
                    chooser.add_filter(filter)
                    
                    response = chooser.run()
                    if response == gtk.RESPONSE_OK:
                        filename = chooser.get_filename()
                        win.set_title("Slannan Bug Tracker - " + filename)
                        Areida("close", "")
                        Areida("load", filename)
                    elif response == gtk.RESPONSE_CANCEL:
                        pass
                    chooser.destroy()
                confirmclose.destroy()
            
        def save_event(event, data=None):
            global filename
            
            Areida("save", filename)
            
        def saveas_event(event, data=None):
            global filename
            
            chooser = gtk.FileChooserDialog(title="Choose Save Location...",action=gtk.FILE_CHOOSER_ACTION_SAVE, buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
            filter = gtk.FileFilter()
            filter.set_name("Slannan Files")
            filter.add_pattern("*.hes")
            chooser.add_filter(filter)
            
            response = chooser.run()
            if response == gtk.RESPONSE_OK:
                try:
                    filename = chooser.get_filename()
                    win.set_title("Slannan Bug Tracker - " + filename)
                    Areida("saveas", filename)
                except sqlite3.OperationalError:
                    message = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, "The file already exists!")
                    response = message.run()
                    message.destroy()
            elif response == gtk.RESPONSE_CANCEL:
                pass
            chooser.destroy()
            
        def close_event(event, data=None):
            global filename

            label = gtk.Label("Do you want to save your changes before closing?")
            confirmclose = gtk.Dialog("Save Changes?", None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_YES, gtk.RESPONSE_ACCEPT, gtk.STOCK_NO, gtk.RESPONSE_REJECT))
            confirmclose.vbox.pack_start(label)
            label.show()
            response = confirmclose.run()
            if response == gtk.RESPONSE_ACCEPT:
                Areida("save", filename)
                Areida("close", "")
                filename = ""
                win.set_title("Slannan Bug Tracker")
            elif response == gtk.RESPONSE_REJECT:
                Areida("close", "")
                filename = ""
                win.set_title("Slannan Bug Tracker")
            confirmclose.destroy()
            
        def quit_event(event, data=None):
            global filename
            
            if filename != "":
                label = gtk.Label("Do you want to save your changes before closing?")
                confirmclose = gtk.Dialog("Save Changes?", None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_YES, gtk.RESPONSE_ACCEPT, gtk.STOCK_NO, gtk.RESPONSE_REJECT))
                confirmclose.vbox.pack_start(label)
                label.show()
                response = confirmclose.run()
                if response == gtk.RESPONSE_ACCEPT:
                    Areida("save", filename)
                    Areida("close", "")
                    filename = ""
                    win.set_title("Slannen Bug Tracker")
                    self.delete_event("delete_event", "process")
                elif response == gtk.RESPONSE_REJECT:
                    Areida("close", "")
                    filename = ""
                    win.set_title("Slannen Bug Tracker")
                    self.delete_event("delete_event", "process")
            else:
                self.delete_event("delete_event", "process")
            
        def undo_event(event, data=None):
            Koopootuk("undo")
            
        def redo_event(event, data=None):
            Koopootuk("redo")
            
        def view_event(event, data=None):
            select1, select2 = CharTree.get_selection().get_selected()
            selected = select1.get_value(select2, 0)
            Brumhilda(selected)
            modifybug_item.set_sensitive(True)
            deletebug_item.set_sensitive(True)
            edit_tb.set_sensitive(True)
            delete_tb.set_sensitive(True)
                        
        def add_event(event, data=None):
            bru.hide()
            vb_man.hide()
            vb_luc.show()
            
        def modify_event(event, data=None):
            global g_bug_name, benny_des, benny_heston, benny_comments
            
            try:
                select1, select2 = CharTree.get_selection().get_selected()
                g_bug_name = select1.get_value(select2, 0)
            except:
                exit
                
            txt_des_m.set_text(benny_des[g_bug_name])
            spn_hes_m.set_value(benny_heston[g_bug_name])
            txt_com_m.set_text(benny_comments[g_bug_name])
                
            bru.hide()
            vb_luc.hide()
            vb_man.show()
            
        def remove_event(event, data=None):
            select1, select2 = CharTree.get_selection().get_selected()
            selection = select1.get_value(select2, 0)
            
            Nish(selection)
            
        def help_event(event, data=None):
            if sys.platform.startswith('darwin'):
                os.system('open', 'SlannanHelp.pdf')
            elif sys.platform.startswith('linux'):
                os.system('xdg-open', 'SlannanHelp.pdf')
            elif sys.platform.startswith('win32'):
                os.startfile("SlannanHelp.pdf")
            else:
                message = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, 'Your operating system may not be supported. To access documentation, open the "SlannanHelp.pdf" file in this program\'s root directory.')
                response = message.run()
                message.destroy()
            
        def online_event(event, data=None):
            url = "http://www.mousepawgames.com"
            webbrowser.open(url, 2, 1)
        
        def about_event(event, data=None):
            about = gtk.AboutDialog()
            about.set_program_name("Slannan Bug Tracker")
            about.set_version("1.0")
            about.set_copyright("Copyright (C) 2011 MousePaw Games. All Rights Reserved.")
            about.set_comments("Slannan is a simple, local-system bug tracker. It is the first to use the 'Heston Scale' method of bug tracking, invented by MousePaw Games founder Jason C. McDonald.")
            about.set_license("This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License along with this program.  If not, see http://www.gnu.org/licenses/.")
            about.set_wrap_license(True)
            about.set_website("http://mousepawgames.com")
            authors = ['Jason C. McDonald']
            about.set_authors(authors)
            response = about.run()
            about.destroy()
            
        def addaccept_event(event, data=None):
            name = txt_name.get_text()
            hes = spn_hes.get_value()
            des = txt_des.get_text()
            com = txt_com.get_text()
            
            try:
                idx = benny.index(name)
            except:
                if name != "" and hes > -1 and hes < 6:
                    Lucinda(name, hes, des, com)
                    txt_name.set_text("")
                    spn_hes.set_value(0)
                    txt_des.set_text("")
                    txt_com.set_text("")
                    vb_luc.hide()
                    vb_man.hide()
                    bru.show()
                else:
                    message = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, '"Bug Name" and "Heston Scale" are required fields.')
                    response = message.run()
                    message.destroy()
                exit
            else:
                message = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, 'This bug already exists! All bugs must have unique names.')
                response = message.run()
                message.destroy()
            
        def modifyaccept_event(event, data=None):
            global g_bug_name
            
            hes = spn_hes_m.get_value()
            des = txt_des_m.get_text()
            com = txt_com_m.get_text()
            
            Mandy(g_bug_name, hes, des, com)
            vb_luc.hide()
            vb_man.hide()
            bru.show()
        
        def cancel_event(event, data=None):
            vb_luc.hide()
            vb_man.hide()
            bru.show()
            
        def status_push(event, widget, status):
            statusbar.push(contextid, status)
            return
        
        def status_pop(event, data=None):
            statusbar.pop(contextid)
            return
        
        #GUI Code -->
        
        #Create the window and vbox.
        win = gtk.Window()
        win.resize(640, 480)
        win.set_title("Slannan Bug Tracker")
        icon = gtk.gdk.pixbuf_new_from_file("slannan.png")
        gtk.window_set_default_icon(icon)
        
        vbox = gtk.VBox()
        win.add(vbox)
        
        win.connect("delete_event", quit_event)
        
        #Menu Bar -->
        menu_bar = gtk.MenuBar()
                
        file_menu = gtk.Menu()
        
        new_item = gtk.ImageMenuItem("_New")
        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_NEW, gtk.ICON_SIZE_MENU)
        new_item.set_image(image)
        file_menu.append(new_item)
        new_item.show()
        new_item.connect("activate", new_event)
        new_item.connect("enter-notify-event", status_push, "Create a new, empty project.")
        new_item.connect("leave-notify-event", status_pop)
        
        open_item = gtk.ImageMenuItem("_Open")
        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_OPEN, gtk.ICON_SIZE_MENU)
        open_item.set_image(image)
        file_menu.append(open_item)
        open_item.show()
        open_item.connect("activate", open_event)
        open_item.connect("enter-notify-event", status_push, "Open a project.")
        open_item.connect("leave-notify-event", status_pop)
        
        save_item = gtk.ImageMenuItem("_Save")
        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_SAVE, gtk.ICON_SIZE_MENU)
        save_item.set_image(image)
        file_menu.append(save_item)
        save_item.show()
        save_item.set_sensitive(False)
        save_item.connect("activate", save_event)
        save_item.connect("enter-notify-event", status_push, "Save project.")
        save_item.connect("leave-notify-event", status_pop)
        
        saveas_item = gtk.ImageMenuItem("Save _As...")
        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_SAVE_AS, gtk.ICON_SIZE_MENU)
        saveas_item.set_image(image)
        file_menu.append(saveas_item)
        saveas_item.show()
        saveas_item.set_sensitive(False)
        saveas_item.connect("activate", saveas_event)
        saveas_item.connect("enter-notify-event", status_push, "Save a copy of the project.")
        saveas_item.connect("leave-notify-event", status_pop)
        
        close_item = gtk.ImageMenuItem("_Close")
        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
        close_item.set_image(image)
        file_menu.append(close_item)
        close_item.show()
        close_item.set_sensitive(False)
        close_item.connect("activate", close_event)
        close_item.connect("enter-notify-event", status_push, "Close project.")
        close_item.connect("leave-notify-event", status_pop)
        
        separator1 = gtk.MenuItem()
        file_menu.append(separator1)
        separator1.show()
        
        quit_item = gtk.ImageMenuItem(gtk.STOCK_QUIT, "_Quit")
        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_QUIT, gtk.ICON_SIZE_MENU)
        quit_item.set_image(image)
        file_menu.append(quit_item)
        quit_item.show()
        quit_item.connect("activate", quit_event)
        quit_item.connect("enter-notify-event", status_push, "Quit Slannan.")
        quit_item.connect("leave-notify-event", status_pop)
        
        edit_menu = gtk.Menu()
        
        undo_item = gtk.ImageMenuItem("_Undo")
        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_UNDO, gtk.ICON_SIZE_MENU)
        undo_item.set_image(image)
        edit_menu.append(undo_item)
        undo_item.show()
        undo_item.set_sensitive(False)
        undo_item.connect("activate", undo_event)
        undo_item.connect("enter-notify-event", status_push, "Undo last action.")
        undo_item.connect("leave-notify-event", status_pop)
        
        redo_item = gtk.ImageMenuItem("_Redo")
        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_REDO, gtk.ICON_SIZE_MENU)
        redo_item.set_image(image)
        edit_menu.append(redo_item)
        redo_item.show()
        redo_item.set_sensitive(False)
        redo_item.connect("activate", redo_event)
        redo_item.connect("enter-notify-event", status_push, "Redo last undone action.")
        redo_item.connect("leave-notify-event", status_pop)
        
        separator2 = gtk.MenuItem()
        edit_menu.append(separator2)
        separator2.show()
        
        createbug_item = gtk.ImageMenuItem("_Create Bug")
        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_ADD, gtk.ICON_SIZE_MENU)
        createbug_item.set_image(image)
        edit_menu.append(createbug_item)
        createbug_item.show()
        createbug_item.set_sensitive(False)
        createbug_item.connect("activate", add_event)
        createbug_item.connect("enter-notify-event", status_push, "Create a new bug.")
        createbug_item.connect("leave-notify-event", status_pop)
        
        modifybug_item = gtk.ImageMenuItem("_Modify Bug")
        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_EDIT, gtk.ICON_SIZE_MENU)
        modifybug_item.set_image(image)
        edit_menu.append(modifybug_item)
        modifybug_item.show()
        modifybug_item.set_sensitive(False)
        modifybug_item.connect("activate", modify_event)
        modifybug_item.connect("enter-notify-event", status_push, "Modify the selected bug.")
        modifybug_item.connect("leave-notify-event", status_pop)
        
        deletebug_item = gtk.ImageMenuItem("_Delete Bug")
        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_DELETE, gtk.ICON_SIZE_MENU)
        deletebug_item.set_image(image)
        edit_menu.append(deletebug_item)
        deletebug_item.show()
        deletebug_item.connect("activate", remove_event)
        deletebug_item.connect("enter-notify-event", status_push, "Delete the selected bug.")
        deletebug_item.connect("leave-notify-event", status_pop)
        deletebug_item.set_sensitive(False)
        
        help_menu = gtk.Menu()
        
        help_item = gtk.ImageMenuItem("_Help")
        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_HELP, gtk.ICON_SIZE_MENU)
        help_item.set_image(image)
        help_menu.append(help_item)
        help_item.show()
        help_item.connect("activate", help_event)
        help_item.connect("enter-notify-event", status_push, "Read help documentation.")
        help_item.connect("leave-notify-event", status_pop)
        
        separator3 = gtk.MenuItem()
        help_menu.append(separator3)
        separator3.show()
        
        online_item = gtk.ImageMenuItem("MousePaw Games _Online")
        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_HOME, gtk.ICON_SIZE_MENU)
        online_item.set_image(image)
        help_menu.append(online_item)
        online_item.show()
        online_item.connect("activate", online_event)
        online_item.connect("enter-notify-event", status_push, "Visit the MousePaw Games website.")
        online_item.connect("leave-notify-event", status_pop)
        
        about_item = gtk.ImageMenuItem("_About")
        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_ABOUT, gtk.ICON_SIZE_MENU)
        about_item.set_image(image)
        help_menu.append(about_item)
        about_item.show()
        about_item.connect("activate", about_event)
        about_item.connect("enter-notify-event", status_push, "About Slannan")
        about_item.connect("leave-notify-event", status_pop)
        
        filemenu_item = gtk.MenuItem("_File")
        filemenu_item.set_submenu(file_menu)
        menu_bar.append(filemenu_item)
        filemenu_item.show()
        
        editmenu_item = gtk.MenuItem("_Edit")
        editmenu_item.set_submenu(edit_menu)
        menu_bar.append(editmenu_item)
        editmenu_item.show()
        
        helpmenu_item = gtk.MenuItem("_Help")
        helpmenu_item.set_submenu(help_menu)
        menu_bar.append(helpmenu_item)
        helpmenu_item.show()
        
        vbox.pack_start(menu_bar, False, False, 0)
        menu_bar.show()
        
        #<-- Menu Bar
        
        #Toolbar -->
        
        toolbar = gtk.Toolbar()
        
        toolbar.set_style(gtk.TOOLBAR_ICONS)

        new_tb = gtk.ToolButton(gtk.STOCK_NEW)
        toolbar.add(new_tb)
        new_tb.show()
        new_tb.connect("clicked", new_event)
        
        open_tb = gtk.ToolButton(gtk.STOCK_OPEN)
        toolbar.insert(open_tb, -1)
        open_tb.show()
        open_tb.connect("clicked", open_event)
        
        save_tb = gtk.ToolButton(gtk.STOCK_SAVE)
        toolbar.insert(save_tb, -1)
        save_tb.show()
        save_tb.set_sensitive(False)
        save_tb.connect("clicked", save_event)
        
        saveas_tb = gtk.ToolButton(gtk.STOCK_SAVE_AS)
        toolbar.insert(saveas_tb, -1)
        saveas_tb.show()
        saveas_tb.set_sensitive(False)
        saveas_tb.connect("clicked", saveas_event)
        
        close_tb = gtk.ToolButton(gtk.STOCK_CLOSE)
        toolbar.insert(close_tb, -1)
        close_tb.show()
        close_tb.set_sensitive(False)
        close_tb.connect("clicked", close_event)
        
        sep_tb = gtk.SeparatorToolItem()
        toolbar.insert(sep_tb, -1)
        sep_tb.show()
        
        undo_tb = gtk.ToolButton(gtk.STOCK_UNDO)
        toolbar.insert(undo_tb, -1)
        undo_tb.show()
        undo_tb.set_sensitive(False)
        undo_tb.connect("clicked", undo_event)
        
        redo_tb = gtk.ToolButton(gtk.STOCK_REDO)
        toolbar.insert(redo_tb, -1)
        redo_tb.show()
        redo_tb.set_sensitive(False)
        redo_tb.connect("clicked", redo_event)
        
        sep2_tb = gtk.SeparatorToolItem()
        toolbar.insert(sep2_tb, -1)
        sep2_tb.show()
        
        add_tb = gtk.ToolButton(gtk.STOCK_ADD)
        toolbar.insert(add_tb, -1)
        add_tb.show()
        add_tb.set_sensitive(False)
        add_tb.connect("clicked", add_event)
        
        edit_tb = gtk.ToolButton(gtk.STOCK_EDIT)
        toolbar.insert(edit_tb, -1)
        edit_tb.show()
        edit_tb.set_sensitive(False)
        edit_tb.connect("clicked", modify_event)
        
        delete_tb = gtk.ToolButton(gtk.STOCK_DELETE)
        toolbar.insert(delete_tb, -1)
        delete_tb.show()
        delete_tb.connect("clicked", remove_event)
        delete_tb.set_sensitive(False)
        
        sep3_tb = gtk.SeparatorToolItem()
        toolbar.insert(sep3_tb, -1)
        sep3_tb.show()
        
        help_tb = gtk.ToolButton(gtk.STOCK_HELP)
        toolbar.insert(help_tb, -1)
        help_tb.show()
        help_tb.connect("clicked", help_event)
        
        vbox.pack_start(toolbar, False, False, 0)
        toolbar.show()
        
        
        #<-- Toolbar
        
        #Create the pane and add it to the window.
        pane = gtk.VPaned()
        vbox.pack_start(pane, True, True, 0)
        
        #Tree View -->
        CharTree = gtk.TreeView(CharList)
        CharCol_Bug = gtk.TreeViewColumn('Bug Name')
        CharCol_Des = gtk.TreeViewColumn('Description')
        CharCol_Hes = gtk.TreeViewColumn('Heston Rank')
        CharCol_Mod = gtk.TreeViewColumn('Date Last Modified')
        CharCol_Cre = gtk.TreeViewColumn('Date Created')
        CharCol_Com = gtk.TreeViewColumn('Comments')
        CharTree.append_column(CharCol_Bug)
        CharTree.append_column(CharCol_Des)
        CharTree.append_column(CharCol_Hes)
        CharTree.append_column(CharCol_Mod)
        CharTree.append_column(CharCol_Cre)
        CharTree.append_column(CharCol_Com)
            
        cell_bug = gtk.CellRendererText()
        cell_des = gtk.CellRendererText()
        cell_hes = gtk.CellRendererText()
        cell_mod = gtk.CellRendererText()
        cell_cre = gtk.CellRendererText()
        cell_com = gtk.CellRendererText()
            
        cell_bug.set_property('cell-background', 'white')
        cell_des.set_property('cell-background', 'yellow')
        cell_hes.set_property('cell-background', 'white')
        cell_mod.set_property('cell-background', 'yellow')
        cell_cre.set_property('cell-background', 'white')
        cell_com.set_property('cell-background', 'yellow')
            
        CharCol_Bug.pack_start(cell_bug, True)
        CharCol_Des.pack_start(cell_des, True)
        CharCol_Hes.pack_start(cell_hes, True)
        CharCol_Mod.pack_start(cell_mod, True)
        CharCol_Cre.pack_start(cell_cre, True)
        CharCol_Com.pack_start(cell_com, True)
            
        CharCol_Bug.set_attributes(cell_bug, text=0)
        CharCol_Des.set_attributes(cell_des, text=1)
        CharCol_Hes.set_attributes(cell_hes, text=2)
        CharCol_Mod.set_attributes(cell_mod, text=3)
        CharCol_Cre.set_attributes(cell_cre, text=4)
        CharCol_Com.set_attributes(cell_com, text=5)
            
        CharCol_Bug.set_resizable(True)
        CharCol_Des.set_resizable(True)
        CharCol_Hes.set_resizable(True)
        CharCol_Mod.set_resizable(True)
        CharCol_Cre.set_resizable(True)
        CharCol_Com.set_resizable(True)
            
        CharCol_Bug.set_sort_column_id(0)
        CharCol_Des.set_sort_column_id(1)
        CharCol_Hes.set_sort_column_id(2)
        CharCol_Mod.set_sort_column_id(3)
        CharCol_Cre.set_sort_column_id(4)
        CharCol_Com.set_sort_column_id(5)
        
        CharTree.connect("cursor-changed", view_event, "CharTree")
        
        scrolled1 = gtk.ScrolledWindow(None, None)
        scrolled1.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC) 
        scrolled1.add_with_viewport(CharTree)
        scrolled1.show()   
        pane.pack1(scrolled1, True, False)
        CharTree.show()
        
        #<-- Tree View
        
        #Control Panel Base -->
        fixed = gtk.Fixed()
        scrolled2 = gtk.ScrolledWindow(None, None)
        scrolled2.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC) 
        scrolled2.add_with_viewport(fixed)
        scrolled2.show()
        fixed.show()
        pane.pack2(scrolled2, True, True)
        #<-- Control Panel Base
        
        #Brumhilda Control Panel -->
        bru = gtk.VBox()
        fixed.put(bru, 0, 0)
        
        bru_name = gtk.Label("Bug Name:")
        ali_name = gtk.Alignment(xalign=0.0, xscale=0.0)
        ali_name.add(bru_name)
        bru.pack_start(ali_name, False, False, 5)
        bru_name.show()
        ali_name.show()
        
        bru_des = gtk.Label("Description:")
        ali_des = gtk.Alignment(xalign=0.0, xscale=0.0)
        ali_des.add(bru_des)
        bru.pack_start(ali_des, False, False, 5)
        bru_des.show()
        ali_des.show()
        
        bru_hes = gtk.Label("Heston Rank:")
        ali_hes = gtk.Alignment(xalign=0.0, xscale=0.0)
        ali_hes.add(bru_hes)
        bru.pack_start(ali_hes, False, False, 5)
        bru_hes.show()
        ali_hes.show()
        
        bru_mdate = gtk.Label("Date Created:")
        ali_mdate = gtk.Alignment(xalign=0.0, xscale=0.0)
        ali_mdate.add(bru_mdate)
        bru.pack_start(ali_mdate, False, False, 5)
        bru_mdate.show()
        ali_mdate.show()
        
        bru_cdate = gtk.Label("Date Last Modified:")
        ali_cdate = gtk.Alignment(xalign=0.0, xscale=0.0)
        ali_cdate.add(bru_cdate)
        bru.pack_start(ali_cdate, False, False, 5)
        bru_cdate.show()
        ali_cdate.show()
        
        bru_com = gtk.Label("Comments:")
        ali_com = gtk.Alignment(xalign=0.0, xscale=0.0)
        ali_com.add(bru_com)
        bru.pack_start(ali_com, False, False, 5)
        bru_com.show()
        ali_com.show()
        
        bru.show()
        
        #<--Brumhilda Control Panel
        
        #Lucinda Control Panel -->
        
        vb_luc = gtk.VBox()
        fixed.put(vb_luc, 0, 0)
        
        lbl_luc = gtk.Label("Create Bug")
        vb_luc.pack_start(lbl_luc, False, False, 5)
        lbl_luc.show()
        
        hb_name = gtk.HBox()
        lbl_name = gtk.Label("Bug Name:")
        hb_name.pack_start(lbl_name, False, False, 5)
        lbl_name.show()
        txt_name = gtk.Entry()
        hb_name.pack_start(txt_name, False, False, 5)
        txt_name.show()
        vb_luc.pack_start(hb_name, False, False, 5)
        hb_name.show()
        
        hb_des = gtk.HBox()
        lbl_des = gtk.Label("Description:")
        lbl_des.show()
        hb_des.pack_start(lbl_des, False, False, 5)
        txt_des = gtk.Entry()
        txt_des.show()
        hb_des.pack_start(txt_des, False, False, 5)
        vb_luc.pack_start(hb_des, False, False, 5)
        hb_des.show()
        
        adj_hes = gtk.Adjustment(0, 0, 5, 1, 0, 0)
        
        hb_hes = gtk.HBox()
        lbl_hes = gtk.Label("Heston Rank:")
        hb_hes.pack_start(lbl_hes, False, False, 5)
        lbl_hes.show()
        spn_hes = gtk.SpinButton(adj_hes, 1, 0)
        hb_hes.pack_start(spn_hes, False, False, 5)
        spn_hes.show()
        vb_luc.pack_start(hb_hes, False, False, 5)
        hb_hes.show()
        
        hb_com = gtk.HBox()
        lbl_com = gtk.Label("Comments:")
        hb_com.pack_start(lbl_com, False, False, 5)
        lbl_com.show()
        txt_com = gtk.Entry()
        hb_com.pack_start(txt_com, False, False, 5)
        txt_com.show()
        vb_luc.pack_start(hb_com, False, False, 5)
        hb_com.show()
        
        hb_btns = gtk.HBox()
        btn_submit = gtk.Button(stock=gtk.STOCK_APPLY)
        hb_btns.pack_start(btn_submit, False, False, 5)
        btn_submit.show()
        btn_submit.connect("clicked", addaccept_event)
        btn_cancel = gtk.Button(stock=gtk.STOCK_CANCEL)
        hb_btns.pack_start(btn_cancel, False, False, 5)
        btn_cancel.show()
        btn_cancel.connect("clicked", cancel_event)
        vb_luc.pack_start(hb_btns, False, False, 5)
        hb_btns.show()
        
        #<-- Lucinda Control Panel
        
        #Mandy Control Panel -->
        
        vb_man = gtk.VBox()
        fixed.put(vb_man, 0, 0)
        
        lbl_man = gtk.Label("Modify Bug")
        vb_man.pack_start(lbl_man, False, False, 5)
        lbl_man.show()
        
        hb_des_m = gtk.HBox()
        lbl_des_m = gtk.Label("Description:")
        lbl_des_m.show()
        hb_des_m.pack_start(lbl_des_m, False, False, 5)
        txt_des_m = gtk.Entry()
        txt_des_m.show()
        hb_des_m.pack_start(txt_des_m, False, False, 5)
        vb_man.pack_start(hb_des_m, False, False, 5)
        hb_des_m.show()
        
        adj_hes_m = gtk.Adjustment(0, 0, 5, 1, 0, 0)
        
        hb_hes_m = gtk.HBox()
        lbl_hes_m = gtk.Label("Heston Rank:")
        hb_hes_m.pack_start(lbl_hes_m, False, False, 5)
        lbl_hes_m.show()
        spn_hes_m = gtk.SpinButton(adj_hes_m, 1, 0)
        hb_hes_m.pack_start(spn_hes_m, False, False, 5)
        spn_hes_m.show()
        vb_man.pack_start(hb_hes_m, False, False, 5)
        hb_hes_m.show()
        
        hb_com_m = gtk.HBox()
        lbl_com_m = gtk.Label("Comments:")
        hb_com_m.pack_start(lbl_com_m, False, False, 5)
        lbl_com_m.show()
        txt_com_m = gtk.Entry()
        hb_com_m.pack_start(txt_com_m, False, False, 5)
        txt_com_m.show()
        vb_man.pack_start(hb_com_m, False, False, 5)
        hb_com_m.show()
        
        hb_btns_man = gtk.HBox()
        btn_submit_m = gtk.Button(stock=gtk.STOCK_APPLY)
        hb_btns_man.pack_start(btn_submit_m, False, False, 5)
        btn_submit_m.show()
        btn_submit_m.connect("clicked", modifyaccept_event)
        btn_cancel_m = gtk.Button(stock=gtk.STOCK_CANCEL)
        hb_btns_man.pack_start(btn_cancel_m, False, False, 5)
        btn_cancel_m.show()
        btn_cancel_m.connect("clicked", cancel_event)
        vb_man.pack_start(hb_btns_man, False, False, 5)
        hb_btns_man.show()
        
        #<--Mandy Control Panel
        
        #Statusbar and Spinner-->

        statusbar = gtk.Statusbar()
        statusbar.show()
        
        spinner = gtk.Spinner()
        spinner.start()
        statusbar.add(spinner)
        
        lbl_scaledscore = gtk.Label("Scaled Score: " + str(scaledscore))
        statusbar.add(lbl_scaledscore)
        lbl_scaledscore.show()
        
        contextid = statusbar.get_context_id("statusbar")
        
        vbox.pack_start(statusbar, False, True, 0)
        #<-- Statusbar and Spinner

        #Show the pane and window.
        pane.show()
        vbox.show()
        win.show()
        
        #<-- GUI Code

            
def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    Slannan()
    main()
