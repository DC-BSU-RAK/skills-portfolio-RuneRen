"""
************************************

        Alexa Tell Me A Joke

************************************
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os

DATA_FILE = "studentMarks.txt"

# Utility functions

def calculate_grade(percent: float) -> str:
    if percent >= 70:
        return "A"
    if percent >= 60:
        return "B"
    if percent >= 50:
        return "C"
    if percent >= 40:
        return "D"
    return "F"

def load_students(filename=DATA_FILE):
    students = []
    if not os.path.exists(filename):
        open(filename, "w").close()
        return students

    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = [ln.strip() for ln in f if ln.strip()]
        for line in lines:
            parts = [p.strip() for p in line.split(",")]
            if len(parts) < 6:
                continue
            code, name = parts[0], parts[1]
            try:
                c1, c2, c3, exam = int(parts[2]), int(parts[3]), int(parts[4]), int(parts[5])
            except ValueError:
                continue
            cw_total = c1 + c2 + c3
            overall = cw_total + exam
            percent = (overall / 160) * 100
            grade = calculate_grade(percent)
            students.append({
                "code": code,
                "name": name,
                "c1": c1,
                "c2": c2,
                "c3": c3,
                "cw_total": cw_total,
                "exam": exam,
                "overall": overall,
                "percent": percent,
                "grade": grade
            })
    except Exception as exc:
        messagebox.showerror("Load Error", f"Could not read {filename}:\n{exc}")
    return students

def save_students(students, filename=DATA_FILE):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            for s in students:
                f.write(f"{s['code']},{s['name']},{s['c1']},{s['c2']},{s['c3']},{s['exam']}\n")
    except Exception as exc:
        messagebox.showerror("Save Error", f"Could not write to {filename}:\n{exc}")

# Tkinter App

class StudentManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Manager")
        self.geometry("1000x650")
        self.minsize(900, 500)
        self.configure(bg="#f7f7f8")

        self.style = ttk.Style(self)
        self._configure_style()

        self.students = load_students()
        self._create_menu()
        self._create_header()
        self._create_table()
        self._create_statusbar()
        self._populate_table()

    def _configure_style(self):
        try:
            self.style.theme_use("clam")
        except Exception:
            pass
        self.style.configure(".", background="#f7f7f8", font=("Segoe UI", 10))
        self.style.configure("TLabel", background="#f7f7f8")
        self.style.configure("Accent.TButton", relief="flat", padding=6)
        self.style.configure("Treeview", font=("Consolas", 10), rowheight=28)
        self.style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        try:
            self.style.map("Treeview", background=[("selected", "#dbeafe")], foreground=[("selected", "#0b3d91")])
        except Exception:
            pass

    def _create_menu(self):
        menubar = tk.Menu(self)
        # File Menu
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="View All Students", command=self.view_all)
        filemenu.add_command(label="View Individual Student", command=self.view_individual)
        sort_sub = tk.Menu(filemenu, tearoff=0)
        sort_sub.add_command(label="Sort by Overall (Ascending)", command=lambda: self.sort_records(True))
        sort_sub.add_command(label="Sort by Overall (Descending)", command=lambda: self.sort_records(False))
        filemenu.add_cascade(label="Sort Records", menu=sort_sub)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        # Edit Menu
        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label="Add Student", command=self.add_student)
        editmenu.add_command(label="Delete Student", command=self.delete_student)
        editmenu.add_command(label="Update Student", command=self.update_student)
        menubar.add_cascade(label="Edit", menu=editmenu)

        # Stats Menu
        statsmenu = tk.Menu(menubar, tearoff=0)
        statsmenu.add_command(label="Show Highest Overall", command=self.show_highest)
        statsmenu.add_command(label="Show Lowest Overall", command=self.show_lowest)
        menubar.add_cascade(label="Stats", menu=statsmenu)

        # Help Menu
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="How to use", command=self.show_help)
        helpmenu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.config(menu=menubar)

    def _create_header(self):
        header_frame = ttk.Frame(self, padding=(14,12,14,6))
        header_frame.pack(fill=tk.X)
        ttk.Label(header_frame, text="Student Manager", font=("Segoe UI", 16, "bold")).pack(side=tk.LEFT)

        search_frame = ttk.Frame(header_frame)
        search_frame.pack(side=tk.RIGHT)
        self.search_var = tk.StringVar()
        ent = ttk.Entry(search_frame, textvariable=self.search_var)
        ent.pack(side=tk.LEFT, ipadx=10, ipady=2)
        ent.bind("<Return>", lambda e: self.filter_table())
        ttk.Button(search_frame, text="Search", command=self.filter_table, style="Accent.TButton").pack(side=tk.LEFT, padx=(6,0))
        ttk.Button(search_frame, text="Clear", command=self.clear_filter).pack(side=tk.LEFT, padx=(6,0))

    def _create_table(self):
        container = ttk.Frame(self, padding=(12,8,12,8))
        container.pack(fill=tk.BOTH, expand=True)

        columns = ("code","name","c1","c2","c3","cw_total","exam","percent","grade")
        self.tree = ttk.Treeview(container, columns=columns, show="headings", selectmode="browse")
        self.tree.heading("code", text="Student #"); self.tree.column("code", width=90, anchor=tk.CENTER)
        self.tree.heading("name", text="Name"); self.tree.column("name", width=300, anchor=tk.W)
        for col,width in [("c1",55),("c2",55),("c3",55),("cw_total",80),("exam",70),("percent",80),("grade",60)]:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=width, anchor=tk.CENTER)

        vsb = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(row=0,column=0,sticky="nsew"); vsb.grid(row=0,column=1,sticky="ns"); hsb.grid(row=1,column=0,sticky="ew")
        container.rowconfigure(0, weight=1); container.columnconfigure(0, weight=1)
        self.tree.bind("<Double-1>", self.on_row_double_click)

    def _create_statusbar(self):
        bar = ttk.Frame(self, relief=tk.FLAT)
        bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_var = tk.StringVar(value=f"Loaded {len(self.students)} students")
        ttk.Label(bar, textvariable=self.status_var, anchor=tk.W, padding=6).pack(fill=tk.X)

   
    # Table functions
    
    def _populate_table(self, students=None):
        for r in self.tree.get_children(): self.tree.delete(r)
        src = students if students else self.students
        for s in src:
            self.tree.insert("", tk.END, iid=s["code"], values=(
                s["code"],s["name"],s["c1"],s["c2"],s["c3"],s["cw_total"],s["exam"],f"{s['percent']:.2f}",s["grade"]
            ))
        self.status_var.set(f"Displayed {len(src)} students")

    def view_all(self):
        self.students = load_students()
        self._populate_table()
        self.status_var.set(f"Displayed {len(self.students)} students")

    def filter_table(self):
        q = self.search_var.get().strip().lower()
        if not q: self._populate_table(); return
        filtered = [s for s in self.students if q in s["name"].lower() or q==s["code"].lower()]
        self._populate_table(filtered)

    def clear_filter(self):
        self.search_var.set("")
        self._populate_table()

    def on_row_double_click(self, event):
        sel = self.tree.selection()
        if sel:
            code = sel[0]
            student = next((s for s in self.students if s["code"]==code), None)
            if student: self._show_student_detail(student)

    def _show_student_detail(self, s):
        lines = [
            f"Name: {s['name']}",
            f"Student #: {s['code']}",
            f"Coursework 1: {s['c1']}",
            f"Coursework 2: {s['c2']}",
            f"Coursework 3: {s['c3']}",
            f"Coursework Total: {s['cw_total']} / 60",
            f"Exam: {s['exam']} / 100",
            f"Overall: {s['overall']} / 160",
            f"Percentage: {s['percent']:.2f}%",
            f"Grade: {s['grade']}"
        ]
        messagebox.showinfo("Student Detail", "\n".join(lines))

   
    # Individual student 
    
    def view_individual(self):
        code = simpledialog.askstring("Individual Student", "Enter Student Number:")
        if not code:
            return
        student = next((s for s in self.students if s["code"] == code.strip()), None)
        if not student:
            messagebox.showinfo("Not found", "Student not found.")
            return
        # Populate table with only this student
        self._populate_table([student])
        self.status_var.set(f"Showing individual student: {student['code']} - {student['name']}")

    
    # Add / Update / Delete
   
    def add_student(self):
        self._student_form("Add Student")

    def update_student(self, code_or_none=None):
        self._student_form("Update Student", code_or_none)

    def delete_student(self, code_or_none=None):
        code = code_or_none or simpledialog.askstring("Delete Student", "Enter student number to delete:")
        if not code: return
        student = next((s for s in self.students if s["code"]==code.strip()), None)
        if not student: messagebox.showinfo("Not found", "Student not found."); return
        if not messagebox.askyesno("Confirm Delete", f"Delete {student['code']} - {student['name']}?"): return
        self.students = [s for s in self.students if s["code"]!=student["code"]]
        save_students(self.students)
        self._populate_table()
        self.status_var.set(f"Deleted student {student['code']}")

    def _student_form(self, title, code_or_none=None):
        student = next((s for s in self.students if s["code"]==code_or_none), None) if code_or_none else None
        win = tk.Toplevel(self)
        win.title(title); win.transient(self); win.grab_set()
        frm = ttk.Frame(win, padding=12); frm.pack(fill=tk.BOTH, expand=True)
        entries = {}
        fields = [("code","Student Code"),("name","Name"),("c1","Coursework 1"),("c2","Coursework 2"),
                  ("c3","Coursework 3"),("exam","Exam")]
        for i,(key,label) in enumerate(fields):
            ttk.Label(frm,text=label).grid(row=i,column=0,sticky=tk.W,pady=6)
            ent = ttk.Entry(frm,width=36); ent.grid(row=i,column=1,pady=6,padx=(8,0)); entries[key]=ent
        if student:
            entries["code"].insert(0, student["code"]); entries["code"].config(state="disabled")
            entries["name"].insert(0, student["name"])
            entries["c1"].insert(0, str(student["c1"])); entries["c2"].insert(0, str(student["c2"]))
            entries["c3"].insert(0, str(student["c3"])); entries["exam"].insert(0, str(student["exam"]))

        def submit():
            code = entries["code"].get().strip(); name = entries["name"].get().strip()
            try: c1=int(entries["c1"].get()); c2=int(entries["c2"].get()); c3=int(entries["c3"].get()); exam=int(entries["exam"].get())
            except ValueError: messagebox.showerror("Invalid","Marks must be integers."); return
            if not name: messagebox.showerror("Invalid","Name required"); return
            if not all(0<=m<=20 for m in (c1,c2,c3)) or not 0<=exam<=100:
                messagebox.showerror("Invalid","Marks out of range"); return
            cw_total=c1+c2+c3; overall=cw_total+exam; percent=(overall/160)*100; grade=calculate_grade(percent)
            data={"code":code,"name":name,"c1":c1,"c2":c2,"c3":c3,"cw_total":cw_total,"exam":exam,
                  "overall":overall,"percent":percent,"grade":grade}
            if student: self.students[self.students.index(student)] = data
            else: self.students.append(data)
            save_students(self.students); self._populate_table(); win.destroy()
            self.status_var.set(f"{title} completed: {code}")

        ttk.Button(frm,text="Submit",command=submit,style="Accent.TButton").grid(row=len(fields),column=0,columnspan=2,pady=(8,6))

 
    # Sorting and stats
  
    def sort_records(self, ascending=True):
        self.students.sort(key=lambda s: s["percent"], reverse=not ascending)
        save_students(self.students)
        self._populate_table()
        self.status_var.set(f"Sorted records ({'ascending' if ascending else 'descending'})")

    def show_highest(self):
        if not self.students: messagebox.showinfo("No data","No students"); return
        top=max(self.students,key=lambda s:s["percent"]); self._populate_table([top])
        self.status_var.set(f"Highest overall: {top['code']} - {top['name']}")

    def show_lowest(self):
        if not self.students: messagebox.showinfo("No data","No students"); return
        low=min(self.students,key=lambda s:s["percent"]); self._populate_table([low])
        self.status_var.set(f"Lowest overall: {low['code']} - {low['name']}")

   
    # Help/About
    
    def show_help(self):
        messagebox.showinfo("How to Use","Double-click rows to view, File to sort or view and exit app, Edit to add, delete, or update data, search by name or code.")

    def show_about(self):
        messagebox.showinfo("About","Student Manager\nSupports Add/Update/Delete/Sort.")


# Run

if __name__ == "__main__":
    app = StudentManager()
    try:
        app.iconbitmap("studentmanagericon.ico")
    except Exception:
        pass
    app.mainloop()
