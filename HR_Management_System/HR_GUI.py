import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import psycopg2

# ── database connection ────────────────────────────────────────────────────────
def get_connection():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        database="HR_Management_System",
        user="postgres",
        password="crazy"
    )

# ── colour palette ─────────────────────────────────────────────────────────────
BG       = "#0f1117"
SIDEBAR  = "#161b27"
CARD     = "#1e2535"
ACCENT   = "#4f8ef7"
ACCENT2  = "#38d9a9"
TEXT     = "#e2e8f0"
SUBTEXT  = "#7c8db5"
SUCCESS  = "#38d9a9"
WARNING  = "#f87171"
ORANGE   = "#fb923c"
ENTRY_BG = "#2a3347"
BTN_BG   = "#4f8ef7"
BTN_FG   = "#ffffff"
GOLD     = "#fbbf24"

FONT   = ("Consolas", 10)
FONT_B = ("Consolas", 10, "bold")
FONT_H = ("Consolas", 14, "bold")
FONT_SM= ("Consolas", 9)

# ══════════════════════════════════════════════════════════════════════════════
# RBAC PERMISSION MATRIX
# Each role maps to allowed page names
# ══════════════════════════════════════════════════════════════════════════════
ROLE_PERMISSIONS = {
    "admin": [
        "Dashboard", "Employees", "Departments", "Salary",
        "Attendance", "Applicants", "Interviews", "Users", "Reports"
    ],
    "hr": [
        "Dashboard", "Employees", "Departments", "Salary",
        "Attendance", "Applicants", "Interviews", "Reports"
    ],
    "finance": [
        "Dashboard", "Salary", "Reports"
    ],
    "operations": [
        "Dashboard", "Employees", "Departments", "Applicants",
        "Interviews", "Reports"
    ],
    # Legacy roles kept for backward compatibility
    "manager": [
        "Dashboard", "Employees", "Departments", "Salary",
        "Attendance", "Applicants", "Interviews", "Reports"
    ],
    "developer": ["Dashboard"],
    "designer":  ["Dashboard"],
    "employee":  ["Dashboard"],
}

# Report access per role
ROLE_REPORTS = {
    "admin": None,  # None means ALL reports
    "hr": [
        "Hiring Summary — Applicants",
        "Interview Results Report",
        "Selected Candidates Only",
        "Department Wise Employee Count",
        "Employees With Most Absences (All Time)",
        "Employees With More Than 3 Absences",
        "Monthly Attendance Summary",
        "Newly Hired Employees",
        "User Roles — RBAC",
    ],
    "finance": [
        "Salary Report — All Employees",
        "Department Wise Salary Total",
        "Employees Earning Above Average Salary",
    ],
    "operations": [
        "Department Wise Employee Count",
        "Newly Hired Employees",
        "Hiring Summary — Applicants",
        "Interview Results Report",
        "Selected Candidates Only",
    ],
    "manager": None,
}

# Attendance edit restriction — only HR can add/update/delete attendance
ATTENDANCE_EDIT_ROLES = {"admin", "hr"}


# ══════════════════════════════════════════════════════════════════════════════
# DATABASE SETUP — run once to create the new RBAC tables
# ══════════════════════════════════════════════════════════════════════════════
SQL_SETUP = """
-- Drop and recreate users/roles tables with new department-aware structure

DO $$ BEGIN
    -- Add department column to users if it doesn't exist
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name='users' AND column_name='department'
    ) THEN
        ALTER TABLE users ADD COLUMN department VARCHAR(20) DEFAULT 'general';
    END IF;
END $$;

-- Update rolee table to support new roles if needed
ALTER TABLE rolee DROP CONSTRAINT IF EXISTS chk_role_name;
ALTER TABLE rolee ADD CONSTRAINT chk_role_name
    CHECK (role_name IN (
        'admin','employee','hr','developer','designer',
        'manager','finance','operations',
        'senior_manager','junior','director'
    ));

-- Insert the 4 required department users if they don't exist
INSERT INTO users (user_id, user_name, user_password, department) VALUES
(101, 'admin_user',  'admin123',  'admin'),
(102, 'hr_user',     'hr123',     'hr'),
(103, 'finance_user','finance123','finance'),
(104, 'ops_user',    'ops123',    'operations')
ON CONFLICT (user_id) DO NOTHING;

-- Assign roles to the 4 department users
INSERT INTO rolee (role_id, user_id, role_name) VALUES
(101, 101, 'admin'),
(102, 102, 'hr'),
(103, 103, 'finance'),
(104, 104, 'operations')
ON CONFLICT (role_id) DO NOTHING;
"""

def run_setup():
    """Run DB setup silently on startup."""
    try:
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute(SQL_SETUP)
        conn.commit()
        conn.close()
    except Exception:
        pass  # Tables may already be configured; not fatal


# ══════════════════════════════════════════════════════════════════════════════
# LOGIN WINDOW
# ══════════════════════════════════════════════════════════════════════════════
class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("HR System — Secure Login")
        self.geometry("460x480")
        self.configure(bg=BG)
        self.resizable(False, False)
        self.logged_in_role = None
        self.logged_in_user = None
        self._build()

    def _build(self):
        # Header
        header = tk.Frame(self, bg=ACCENT, height=6)
        header.pack(fill="x")

        tk.Label(self, text="⬡", bg=BG, fg=ACCENT,
                 font=("Consolas", 32, "bold")).pack(pady=(28, 0))
        tk.Label(self, text="HR DEPARTMENT", bg=BG, fg=TEXT,
                 font=("Consolas", 18, "bold")).pack()
        tk.Label(self, text="Role-Based Access Control System", bg=BG, fg=SUBTEXT,
                 font=FONT_SM).pack(pady=(2, 28))

        form = tk.Frame(self, bg=BG)
        form.pack()

        # Username
        tk.Label(form, text="USERNAME", bg=BG, fg=SUBTEXT, font=FONT_SM,
                 anchor="w").grid(row=0, column=0, sticky="w", pady=(0, 2))
        self.v_user = tk.StringVar()
        u_entry = tk.Entry(form, textvariable=self.v_user, bg=ENTRY_BG, fg=TEXT,
                           insertbackground=TEXT, font=FONT, relief="flat",
                           width=32, bd=0)
        u_entry.grid(row=1, column=0, pady=(0, 16), ipady=8, padx=2)
        tk.Frame(form, bg=ACCENT, height=2).grid(row=2, column=0, sticky="ew")

        # Password
        tk.Label(form, text="PASSWORD", bg=BG, fg=SUBTEXT, font=FONT_SM,
                 anchor="w").grid(row=3, column=0, sticky="w", pady=(12, 2))
        self.v_pass = tk.StringVar()
        p_entry = tk.Entry(form, textvariable=self.v_pass, bg=ENTRY_BG, fg=TEXT,
                           insertbackground=TEXT, font=FONT, relief="flat",
                           width=32, bd=0, show="●")
        p_entry.grid(row=4, column=0, pady=(0, 16), ipady=8, padx=2)
        tk.Frame(form, bg=ACCENT, height=2).grid(row=5, column=0, sticky="ew")

        # Login button
        tk.Button(self, text="SIGN IN  →", command=self.attempt_login,
                  bg=ACCENT, fg=BTN_FG, font=FONT_B, relief="flat",
                  padx=24, pady=10, cursor="hand2",
                  activebackground=ACCENT2, activeforeground=BG
                  ).pack(pady=28)

        self.err_label = tk.Label(self, text="", bg=BG, fg=WARNING, font=FONT_SM)
        self.err_label.pack()

        # Hint box
        hint = tk.Frame(self, bg=CARD, padx=16, pady=10)
        hint.pack(fill="x", padx=40, pady=(0, 16))
        tk.Label(hint, text="Default Accounts", bg=CARD, fg=ACCENT, font=FONT_SM).pack(anchor="w")
        hints = [
            ("Admin",      "admin_user",   "admin123"),
            ("HR",         "hr_user",      "hr123"),
            ("Finance",    "finance_user", "finance123"),
            ("Operations", "ops_user",     "ops123"),
        ]
        for dept, usr, pwd in hints:
            tk.Label(hint, text=f"  {dept:<12} {usr:<16} {pwd}",
                     bg=CARD, fg=SUBTEXT, font=FONT_SM).pack(anchor="w")

        u_entry.focus()
        self.bind("<Return>", lambda e: self.attempt_login())

    def attempt_login(self):
        uname = self.v_user.get().strip()
        pwd   = self.v_pass.get().strip()
        if not uname or not pwd:
            self.err_label.config(text="⚠  Please enter username and password.")
            return
        try:
            conn = get_connection()
            cur  = conn.cursor()
            cur.execute("""
                SELECT r.role_name, u.user_name
                FROM users u
                JOIN rolee r ON u.user_id = r.user_id
                WHERE u.user_name = %s AND u.user_password = %s
            """, (uname, pwd))
            row = cur.fetchone()
            conn.close()
            if row:
                self.logged_in_role = row[0]
                self.logged_in_user = row[1]
                self.destroy()
            else:
                self.err_label.config(text="✗  Invalid username or password.")
        except Exception as ex:
            messagebox.showerror("DB Error", str(ex))


# ══════════════════════════════════════════════════════════════════════════════
# MAIN APP
# ══════════════════════════════════════════════════════════════════════════════
class HRApp(tk.Tk):
    def __init__(self, role, username):
        super().__init__()
        self.role     = role
        self.username = username
        self.allowed  = ROLE_PERMISSIONS.get(role, ["Dashboard"])
        self.title(f"HR System  —  {role.upper()} Portal")
        self.geometry("1200x720")
        self.configure(bg=BG)
        self.resizable(True, True)
        self._build_layout()
        self._build_sidebar()
        self._frames = {}
        self._load_all_frames()
        self.show_frame("Dashboard")

    def _build_layout(self):
        # Top bar
        topbar = tk.Frame(self, bg=SIDEBAR, height=38)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)
        tk.Label(topbar, text=f"  HR DEPARTMENT MANAGEMENT SYSTEM",
                 bg=SIDEBAR, fg=ACCENT, font=FONT_B).pack(side="left", padx=8)
        role_colors = {"admin": WARNING, "hr": ACCENT, "finance": GOLD,
                       "operations": SUCCESS, "manager": ACCENT2}
        rc = role_colors.get(self.role, SUBTEXT)
        tk.Label(topbar,
                 text=f"● {self.username.upper()}  [{self.role.upper()}]  —  {date.today()}  ",
                 bg=SIDEBAR, fg=rc, font=FONT_SM).pack(side="right")

        # Main layout
        self.sidebar_frame = tk.Frame(self, bg=SIDEBAR, width=210)
        self.sidebar_frame.pack(side="left", fill="y")
        self.sidebar_frame.pack_propagate(False)
        self.main_frame = tk.Frame(self, bg=BG)
        self.main_frame.pack(side="left", fill="both", expand=True)

    def _build_sidebar(self):
        tk.Frame(self.sidebar_frame, bg=ACCENT, height=3).pack(fill="x")

        role_colors = {"admin": WARNING, "hr": ACCENT, "finance": GOLD,
                       "operations": SUCCESS, "manager": ACCENT2}
        rc = role_colors.get(self.role, SUBTEXT)

        info = tk.Frame(self.sidebar_frame, bg=SIDEBAR, pady=14)
        info.pack(fill="x", padx=12)
        tk.Label(info, text="⬡", bg=SIDEBAR, fg=rc,
                 font=("Consolas", 22, "bold")).pack()
        tk.Label(info, text=self.role.upper(), bg=SIDEBAR, fg=rc,
                 font=FONT_B).pack()
        tk.Label(info, text="DEPARTMENT PORTAL", bg=SIDEBAR, fg=SUBTEXT,
                 font=FONT_SM).pack()

        tk.Frame(self.sidebar_frame, bg=CARD, height=1).pack(fill="x", padx=14, pady=6)

        # Nav items — only show pages this role can access
        all_pages = [
            ("Dashboard",   "Dashboard",   "◈"),
            ("Employees",   "Employees",   "◉"),
            ("Departments", "Departments", "◫"),
            ("Salary",      "Salary",      "◎"),
            ("Attendance",  "Attendance",  "◷"),
            ("Applicants",  "Applicants",  "◌"),
            ("Interviews",  "Interviews",  "◈"),
            ("Reports",     "Reports",     "◧"),
            ("Users",       "Users",       "◉"),
        ]

        for label, page, icon in all_pages:
            if page not in self.allowed:
                continue
            btn = tk.Button(
                self.sidebar_frame, text=f" {icon}  {label}", anchor="w",
                bg=SIDEBAR, fg=TEXT, font=FONT,
                bd=0, padx=16, pady=9, cursor="hand2",
                activebackground=CARD, activeforeground=ACCENT,
                command=lambda p=page: self.show_frame(p)
            )
            btn.pack(fill="x")

        tk.Frame(self.sidebar_frame, bg=CARD, height=1).pack(
            fill="x", padx=14, pady=6, side="bottom")
        tk.Button(self.sidebar_frame, text=" ← Logout", anchor="w",
                  bg=SIDEBAR, fg=WARNING, font=FONT,
                  bd=0, padx=16, pady=9, cursor="hand2",
                  command=self.logout).pack(fill="x", side="bottom")

    def logout(self):
        self.destroy()
        main()

    def _load_all_frames(self):
        frame_map = {
            "Dashboard":   Dashboard,
            "Employees":   EmployeesPage,
            "Departments": DepartmentsPage,
            "Salary":      SalaryPage,
            "Attendance":  AttendancePage,
            "Applicants":  ApplicantsPage,
            "Interviews":  InterviewsPage,
            "Reports":     ReportsPage,
            "Users":       UsersPage,
        }
        for page_name in self.allowed:
            FrameClass = frame_map.get(page_name)
            if not FrameClass:
                continue
            frame = FrameClass(self.main_frame, self)
            self._frames[frame.name] = frame
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    def show_frame(self, name):
        if name not in self.allowed:
            messagebox.showwarning("Access Denied",
                f"Your role ({self.role.upper()}) does not have access to '{name}'.")
            return
        if name not in self._frames:
            return
        frame = self._frames[name]
        frame.lift()
        if hasattr(frame, "refresh"):
            frame.refresh()


# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════
class Table(tk.Frame):
    def __init__(self, parent, columns, **kw):
        super().__init__(parent, bg=BG, **kw)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("HR.Treeview",
                        background=CARD, foreground=TEXT,
                        fieldbackground=CARD, rowheight=30, font=FONT)
        style.configure("HR.Treeview.Heading",
                        background=SIDEBAR, foreground=ACCENT,
                        font=FONT_B, relief="flat")
        style.map("HR.Treeview",
                  background=[("selected", ACCENT)],
                  foreground=[("selected", BG)])
        vsb = ttk.Scrollbar(self, orient="vertical")
        hsb = ttk.Scrollbar(self, orient="horizontal")
        self.tv = ttk.Treeview(self, columns=columns, show="headings",
                               style="HR.Treeview",
                               yscrollcommand=vsb.set,
                               xscrollcommand=hsb.set)
        vsb.configure(command=self.tv.yview)
        hsb.configure(command=self.tv.xview)
        for col in columns:
            self.tv.heading(col, text=col.replace("_", " ").title())
            self.tv.column(col, anchor="center", width=130, minwidth=80)
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")
        self.tv.pack(fill="both", expand=True)

    def load(self, rows):
        self.tv.delete(*self.tv.get_children())
        for i, row in enumerate(rows):
            tag = "even" if i % 2 == 0 else "odd"
            self.tv.insert("", "end", values=row, tags=(tag,))
        self.tv.tag_configure("even", background=CARD)
        self.tv.tag_configure("odd",  background="#232b3e")

    def selected_values(self):
        sel = self.tv.selection()
        if not sel:
            return None
        return self.tv.item(sel[0])["values"]


def make_entry(parent, label, row, col=0, width=22):
    tk.Label(parent, text=label, bg=CARD, fg=SUBTEXT, font=FONT_SM
             ).grid(row=row, column=col*2, sticky="w", padx=(12, 4), pady=5)
    var = tk.StringVar()
    tk.Entry(parent, textvariable=var, bg=ENTRY_BG, fg=TEXT,
             insertbackground=TEXT, font=FONT, relief="flat", width=width
             ).grid(row=row, column=col*2+1, sticky="ew", padx=(0, 12), pady=5)
    return var


def make_combo(parent, label, row, col, values, width=20):
    tk.Label(parent, text=label, bg=CARD, fg=SUBTEXT, font=FONT_SM
             ).grid(row=row, column=col*2, sticky="w", padx=(12, 4), pady=5)
    var = tk.StringVar()
    ttk.Combobox(parent, textvariable=var, values=values,
                 state="readonly", width=width, font=FONT
                 ).grid(row=row, column=col*2+1, sticky="ew", padx=(0, 12), pady=5)
    return var


def action_btn(parent, text, command, color=None):
    if color is None:
        color = BTN_BG
    return tk.Button(parent, text=text, command=command,
                     bg=color, fg=BTN_FG, font=FONT_B,
                     relief="flat", padx=14, pady=6, cursor="hand2",
                     activebackground=ACCENT2, activeforeground=BG)


def page_title(parent, title, subtitle=""):
    hdr = tk.Frame(parent, bg=BG)
    hdr.pack(fill="x", padx=24, pady=(16, 0))
    tk.Label(hdr, text=title, bg=BG, fg=ACCENT, font=FONT_H).pack(anchor="w")
    if subtitle:
        tk.Label(hdr, text=subtitle, bg=BG, fg=SUBTEXT, font=FONT_SM).pack(anchor="w")
    tk.Frame(parent, bg=ACCENT, height=2).pack(fill="x", padx=24, pady=(4, 10))


def rbac_badge(parent, role):
    """Show a coloured access-level badge in the page header."""
    colors = {"admin": WARNING, "hr": ACCENT, "finance": GOLD,
              "operations": SUCCESS, "manager": ACCENT2}
    c = colors.get(role, SUBTEXT)
    badge = tk.Frame(parent, bg=BG)
    badge.pack(anchor="e", padx=24)
    tk.Label(badge, text=f"  ACCESS: {role.upper()}  ",
             bg=c, fg=BG, font=FONT_SM, padx=4, pady=2).pack(side="right")


# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
class Dashboard(tk.Frame):
    name = "Dashboard"

    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        page_title(self, "Dashboard",
                   f"Welcome, {app.username.upper()}  —  Role: {app.role.upper()}")
        self.cards_frame = tk.Frame(self, bg=BG)
        self.cards_frame.pack(fill="x", padx=24)
        self.bottom = tk.Frame(self, bg=BG)
        self.bottom.pack(fill="both", expand=True, padx=24, pady=12)

    def refresh(self):
        for w in self.cards_frame.winfo_children(): w.destroy()
        for w in self.bottom.winfo_children(): w.destroy()
        self._draw_cards()
        self._draw_bottom()

    def _q(self, query):
        try:
            conn = get_connection(); cur = conn.cursor()
            cur.execute(query)
            val = cur.fetchone()[0]; conn.close()
            return val or 0
        except:
            return "—"

    def _draw_cards(self):
        role = self.app.role
        all_stats = [
            ("Total Employees",
             "SELECT COUNT(*) FROM employee",
             ACCENT, ["admin","hr","operations","manager"]),
            ("Departments",
             "SELECT COUNT(DISTINCT dep_name) FROM department",
             ACCENT2, ["admin","hr","operations","manager"]),
            ("Pending Applicants",
             "SELECT COUNT(*) FROM applicant WHERE a_status='pending'",
             SUCCESS, ["admin","hr","operations","manager"]),
            (f"Absent Today",
             "SELECT COUNT(*) FROM attendance_table WHERE status='absent' AND att_date=current_date",
             WARNING, ["admin","hr","manager"]),
            ("Total Payroll (Net)",
             "SELECT COALESCE(SUM(amount+bonus-deductions),0) FROM salary",
             GOLD, ["admin","finance","manager"]),
            ("Active Employees",
             "SELECT COUNT(*) FROM employee WHERE employment_status='full-time'",
             ACCENT2, ["admin","hr","finance","operations","manager"]),
        ]
        shown = [s for s in all_stats if role in s[3]]
        for i, (label, q, color, _) in enumerate(shown):
            card = tk.Frame(self.cards_frame, bg=CARD, padx=20, pady=14)
            card.grid(row=0, column=i, padx=8, pady=6, sticky="ew")
            self.cards_frame.columnconfigure(i, weight=1)
            tk.Frame(card, bg=color, height=3).pack(fill="x", pady=(0, 8))
            tk.Label(card, text=str(self._q(q)), bg=CARD, fg=color,
                     font=("Consolas", 24, "bold")).pack()
            tk.Label(card, text=label, bg=CARD, fg=SUBTEXT, font=FONT_SM).pack()

    def _draw_bottom(self):
        role = self.app.role
        left  = tk.Frame(self.bottom, bg=BG)
        left.pack(side="left", fill="both", expand=True, padx=(0, 8))
        right = tk.Frame(self.bottom, bg=BG)
        right.pack(side="left", fill="both", expand=True, padx=(8, 0))

        # Left panel — role dependent
        if role in ("admin", "hr", "manager"):
            tk.Label(left, text="Top 5 Paid Employees",
                     bg=BG, fg=TEXT, font=FONT_B).pack(anchor="w", pady=(0, 4))
            t1 = Table(left, ["first_name", "last_name", "amount"])
            t1.pack(fill="both", expand=True)
            try:
                conn = get_connection(); cur = conn.cursor()
                cur.execute("SELECT e.first_name,e.last_name,s.amount "
                            "FROM employee e JOIN salary s ON e.employee_id=s.employee_id "
                            "ORDER BY s.amount DESC LIMIT 5")
                t1.load(cur.fetchall()); conn.close()
            except Exception as ex:
                messagebox.showerror("DB Error", str(ex))

        elif role == "finance":
            tk.Label(left, text="Department Salary Totals",
                     bg=BG, fg=TEXT, font=FONT_B).pack(anchor="w", pady=(0, 4))
            t1 = Table(left, ["department", "total_net_pay"])
            t1.pack(fill="both", expand=True)
            try:
                conn = get_connection(); cur = conn.cursor()
                cur.execute("SELECT d.dep_name, SUM(s.amount+s.bonus-s.deductions) "
                            "FROM salary s JOIN employee e ON s.employee_id=e.employee_id "
                            "JOIN department d ON e.employee_id=d.employee_id "
                            "GROUP BY d.dep_name ORDER BY 2 DESC")
                t1.load(cur.fetchall()); conn.close()
            except Exception as ex:
                messagebox.showerror("DB Error", str(ex))

        elif role == "operations":
            tk.Label(left, text="Department Headcount",
                     bg=BG, fg=TEXT, font=FONT_B).pack(anchor="w", pady=(0, 4))
            t1 = Table(left, ["department", "employee_count"])
            t1.pack(fill="both", expand=True)
            try:
                conn = get_connection(); cur = conn.cursor()
                cur.execute("SELECT d.dep_name, COUNT(e.employee_id) "
                            "FROM department d JOIN employee e ON d.employee_id=e.employee_id "
                            "GROUP BY d.dep_name ORDER BY 2 DESC")
                t1.load(cur.fetchall()); conn.close()
            except Exception as ex:
                messagebox.showerror("DB Error", str(ex))

        # Right panel — role dependent
        if role in ("admin", "hr", "manager"):
            tk.Label(right, text="Today's Attendance Summary",
                     bg=BG, fg=TEXT, font=FONT_B).pack(anchor="w", pady=(0, 4))
            t2 = Table(right, ["status", "count"])
            t2.pack(fill="both", expand=True)
            try:
                conn = get_connection(); cur = conn.cursor()
                cur.execute("SELECT status, COUNT(*) FROM attendance_table "
                            "WHERE att_date=current_date GROUP BY status")
                rows = cur.fetchall(); conn.close()
                t2.load(rows if rows else [("No records for today", "")])
            except Exception as ex:
                messagebox.showerror("DB Error", str(ex))

        elif role == "finance":
            tk.Label(right, text="Recent Payroll Entries",
                     bg=BG, fg=TEXT, font=FONT_B).pack(anchor="w", pady=(0, 4))
            t2 = Table(right, ["employee", "amount", "net_pay", "payment_date"])
            t2.pack(fill="both", expand=True)
            try:
                conn = get_connection(); cur = conn.cursor()
                cur.execute("SELECT e.first_name||' '||e.last_name, s.amount, "
                            "(s.amount+s.bonus-s.deductions), s.payment_date "
                            "FROM salary s JOIN employee e ON s.employee_id=e.employee_id "
                            "ORDER BY s.payment_date DESC LIMIT 8")
                t2.load(cur.fetchall()); conn.close()
            except Exception as ex:
                messagebox.showerror("DB Error", str(ex))

        elif role == "operations":
            tk.Label(right, text="Recent Applicants",
                     bg=BG, fg=TEXT, font=FONT_B).pack(anchor="w", pady=(0, 4))
            t2 = Table(right, ["name", "position", "status"])
            t2.pack(fill="both", expand=True)
            try:
                conn = get_connection(); cur = conn.cursor()
                cur.execute("SELECT applicant_name, a_position, a_status "
                            "FROM applicant ORDER BY applicant_id DESC LIMIT 8")
                t2.load(cur.fetchall()); conn.close()
            except Exception as ex:
                messagebox.showerror("DB Error", str(ex))


# ══════════════════════════════════════════════════════════════════════════════
# REPORTS  — filtered by role
# ══════════════════════════════════════════════════════════════════════════════
ALL_REPORTS = {
    # ── Finance Reports ──────────────────────────────────────────────────────
    "Salary Report — All Employees": """
        SELECT e.first_name||' '||e.last_name AS employee,
               d.dep_name AS department,
               s.amount AS basic_salary, s.bonus, s.deductions,
               (s.amount+s.bonus-s.deductions) AS net_pay,
               s.payment_date
        FROM employee e
        JOIN salary s ON e.employee_id=s.employee_id
        JOIN department d ON e.employee_id=d.employee_id
        ORDER BY net_pay DESC
    """,
    "Department Wise Salary Total": """
        SELECT d.dep_name AS department,
               SUM(s.amount) AS total_basic,
               SUM(s.bonus) AS total_bonus,
               SUM(s.deductions) AS total_deductions,
               SUM(s.amount+s.bonus-s.deductions) AS total_net
        FROM salary s
        JOIN employee e ON s.employee_id=e.employee_id
        JOIN department d ON e.employee_id=d.employee_id
        GROUP BY d.dep_name ORDER BY total_net DESC
    """,
    "Employees Earning Above Average Salary": """
        SELECT e.first_name||' '||e.last_name AS employee,
               e.job_role, s.amount
        FROM employee e
        JOIN salary s ON e.employee_id=s.employee_id
        WHERE s.amount > (SELECT AVG(amount) FROM salary)
        ORDER BY s.amount DESC
    """,
    # ── HR / Attendance Reports ───────────────────────────────────────────────
    "Employees With Most Absences (All Time)": """
        SELECT e.first_name||' '||e.last_name AS employee,
               e.job_role, COUNT(*) AS total_absences
        FROM attendance_table a
        JOIN employee e ON a.employee_id=e.employee_id
        WHERE a.status='absent'
        GROUP BY e.first_name, e.last_name, e.job_role
        ORDER BY total_absences DESC
    """,
    "Employees With More Than 3 Absences": """
        SELECT e.first_name||' '||e.last_name AS employee,
               e.job_role, COUNT(*) AS absences
        FROM attendance_table a
        JOIN employee e ON a.employee_id=e.employee_id
        WHERE a.status='absent'
        GROUP BY e.first_name, e.last_name, e.job_role
        HAVING COUNT(*) > 3
        ORDER BY absences DESC
    """,
    "Monthly Attendance Summary": """
        SELECT TO_CHAR(att_date,'YYYY-MM') AS month,
               status, COUNT(*) AS total
        FROM attendance_table
        GROUP BY month, status
        ORDER BY month DESC, status
    """,
    # ── Operations / Hiring Reports ───────────────────────────────────────────
    "Hiring Summary — Applicants": """
        SELECT a_status AS status,
               COUNT(*) AS total_applicants,
               ROUND(COUNT(*)*100.0/(SELECT COUNT(*) FROM applicant),1) AS percentage
        FROM applicant
        GROUP BY a_status
    """,
    "Interview Results Report": """
        SELECT a.applicant_name, a.a_position,
               i.i_result, i.i_date, a.a_status
        FROM interview_table i
        JOIN applicant a ON i.applicant_id=a.applicant_id
        ORDER BY i.i_date DESC
    """,
    "Selected Candidates Only": """
        SELECT a.applicant_name, a.a_position, i.i_result, i.i_date
        FROM applicant a
        JOIN interview_table i ON a.applicant_id=i.applicant_id
        WHERE a.a_status='selected'
        ORDER BY i.i_date DESC
    """,
    "Department Wise Employee Count": """
        SELECT d.dep_name AS department,
               COUNT(e.employee_id) AS total_employees
        FROM department d
        JOIN employee e ON d.employee_id=e.employee_id
        GROUP BY d.dep_name
        ORDER BY total_employees DESC
    """,
    "Newly Hired Employees": """
        SELECT first_name||' '||last_name AS employee,
               job_role, employment_status, hire_date
        FROM employee
        ORDER BY hire_date DESC
    """,
    # ── Admin Only ────────────────────────────────────────────────────────────
    "User Roles — RBAC": """
        SELECT u.user_name, r.role_name
        FROM users u JOIN rolee r ON u.user_id=r.user_id
        ORDER BY r.role_name
    """,
    "Full Employee Payroll Report": """
        SELECT e.employee_id, e.first_name||' '||e.last_name AS name,
               d.dep_name, s.payroll_id, s.amount,
               s.bonus, s.deductions,
               (s.amount+s.bonus-s.deductions) AS net_pay,
               s.payment_date
        FROM employee e
        JOIN salary s ON e.employee_id=s.employee_id
        JOIN department d ON e.employee_id=d.employee_id
        ORDER BY s.payment_date DESC
    """,
}


class ReportsPage(tk.Frame):
    name = "Reports"

    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app

        # Filter reports by role
        allowed_keys = ROLE_REPORTS.get(app.role)
        if allowed_keys is None:
            self.reports = ALL_REPORTS  # admin / manager: all
        else:
            self.reports = {k: v for k, v in ALL_REPORTS.items() if k in allowed_keys}

        page_title(self, "Reports",
                   f"Showing {len(self.reports)} report(s) available to role: {app.role.upper()}")

        top = tk.Frame(self, bg=BG)
        top.pack(fill="x", padx=24, pady=(0, 10))

        tk.Label(top, text="Select Report:", bg=BG, fg=TEXT, font=FONT
                 ).pack(side="left", padx=(0, 8))
        self.v_report = tk.StringVar(value=list(self.reports.keys())[0] if self.reports else "")
        ttk.Combobox(top, textvariable=self.v_report,
                     values=list(self.reports.keys()),
                     state="readonly", width=48, font=FONT
                     ).pack(side="left", padx=(0, 12))
        action_btn(top, "▶  Run", self._run).pack(side="left")
        self.count_lbl = tk.Label(top, text="", bg=BG, fg=SUBTEXT, font=FONT_SM)
        self.count_lbl.pack(side="right", padx=12)

        self.table_frame = tk.Frame(self, bg=BG)
        self.table_frame.pack(fill="both", expand=True, padx=24, pady=(0, 12))

    def refresh(self):
        pass

    def _run(self):
        for w in self.table_frame.winfo_children():
            w.destroy()
        key = self.v_report.get()
        if not key or key not in self.reports:
            return
        query = self.reports[key]
        try:
            conn = get_connection(); cur = conn.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            cols = [desc[0] for desc in cur.description]
            conn.close()
            tbl = Table(self.table_frame, cols)
            tbl.pack(fill="both", expand=True)
            tbl.load(rows)
            self.count_lbl.config(text=f"{len(rows)} rows returned")
        except Exception as ex:
            messagebox.showerror("DB Error", str(ex))


# ══════════════════════════════════════════════════════════════════════════════
# EMPLOYEES  (admin, hr, operations, manager)
# ══════════════════════════════════════════════════════════════════════════════
class EmployeesPage(tk.Frame):
    name = "Employees"

    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        can_edit = app.role in ("admin", "hr", "manager")
        page_title(self, "Employees",
                   "Read-only for Operations role" if not can_edit else "")

        form = tk.Frame(self, bg=CARD, pady=10)
        form.pack(fill="x", padx=24, pady=(0, 10))
        form.columnconfigure((1, 3), weight=1)

        self.v_id     = make_entry(form, "Employee ID",  0, 0)
        self.v_fname  = make_entry(form, "First Name",   0, 1)
        self.v_lname  = make_entry(form, "Last Name",    1, 0)
        self.v_email  = make_entry(form, "Email",        1, 1)
        self.v_cnic   = make_entry(form, "CNIC",         2, 0)
        self.v_addr   = make_entry(form, "Address",      2, 1)
        self.v_phone  = make_entry(form, "Phone No",     3, 0)
        self.v_bdate  = make_entry(form, "Birth Date (YYYY-MM-DD)", 3, 1)
        self.v_hdate  = make_entry(form, "Hire Date (YYYY-MM-DD)",  4, 0)
        self.v_status = make_combo(form, "Employment Status", 4, 1,
                                   ["full-time","part-time","internship","contract"])
        self.v_role   = make_combo(form, "Job Role", 5, 0,
                                   ["manager","hr","developer","designer"])

        btn_row = tk.Frame(form, bg=CARD)
        btn_row.grid(row=6, column=0, columnspan=4, pady=8, padx=12, sticky="w")

        if can_edit:
            action_btn(btn_row, "➕ Add",    self.add).pack(side="left", padx=4)
            action_btn(btn_row, "✏  Update", self.update, ACCENT2).pack(side="left", padx=4)
            action_btn(btn_row, "✕  Delete", self.delete, WARNING).pack(side="left", padx=4)
        action_btn(btn_row, "↺  Clear", self.clear, ENTRY_BG).pack(side="left", padx=4)

        if not can_edit:
            tk.Label(btn_row,
                     text="  ⚑  VIEW ONLY — Operations role cannot modify employee records",
                     bg=CARD, fg=GOLD, font=FONT_SM).pack(side="left", padx=8)

        cols = ["employee_id","first_name","last_name","email","phone_no",
                "employment_status","job_role","hire_date"]
        self.table = Table(self, cols)
        self.table.pack(fill="both", expand=True, padx=24, pady=(0, 12))
        self.table.tv.bind("<<TreeviewSelect>>", self.on_select)

    def refresh(self):
        try:
            conn = get_connection(); cur = conn.cursor()
            cur.execute("SELECT employee_id,first_name,last_name,email,phone_no,"
                        "employment_status,job_role,hire_date FROM employee ORDER BY employee_id")
            self.table.load(cur.fetchall()); conn.close()
        except Exception as ex:
            messagebox.showerror("DB Error", str(ex))

    def on_select(self, _):
        vals = self.table.selected_values()
        if not vals: return
        try:
            conn = get_connection(); cur = conn.cursor()
            cur.execute("SELECT * FROM employee WHERE employee_id=%s", (vals[0],))
            row = cur.fetchone(); conn.close()
        except: return
        if not row: return
        fields = [self.v_id, self.v_fname, self.v_lname, self.v_email,
                  self.v_cnic, self.v_addr, self.v_phone, self.v_bdate,
                  self.v_status, self.v_role, self.v_hdate]
        for var, val in zip(fields, row):
            var.set(str(val) if val is not None else "")

    def _vals(self):
        return (self.v_id.get(), self.v_fname.get(), self.v_lname.get(),
                self.v_email.get(), self.v_cnic.get(), self.v_addr.get(),
                self.v_phone.get(), self.v_bdate.get(), self.v_status.get(),
                self.v_role.get(), self.v_hdate.get())

    def add(self):
        v = self._vals()
        if not all(v): messagebox.showwarning("Input", "Please fill all fields."); return
        try:
            conn = get_connection(); cur = conn.cursor()
            cur.execute("INSERT INTO employee VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", v)
            conn.commit(); conn.close(); self.refresh(); self.clear()
            messagebox.showinfo("Success", "Employee added.")
        except Exception as ex:
            messagebox.showerror("DB Error", str(ex))

    def update(self):
        v = self._vals()
        if not v[0]: messagebox.showwarning("Input", "Select a row first."); return
        try:
            conn = get_connection(); cur = conn.cursor()
            cur.execute("""UPDATE employee SET first_name=%s,last_name=%s,email=%s,
                           cnic=%s,address=%s,phone_no=%s,birth_date=%s,
                           employment_status=%s,job_role=%s,hire_date=%s
                           WHERE employee_id=%s""", v[1:] + (v[0],))
            conn.commit(); conn.close(); self.refresh()
            messagebox.showinfo("Success", "Employee updated.")
        except Exception as ex:
            messagebox.showerror("DB Error", str(ex))

    def delete(self):
        eid = self.v_id.get()
        if not eid: messagebox.showwarning("Input", "Select a row first."); return
        if not messagebox.askyesno("Confirm", f"Delete employee {eid}?"): return
        try:
            conn = get_connection(); cur = conn.cursor()
            cur.execute("DELETE FROM employee WHERE employee_id=%s", (eid,))
            conn.commit(); conn.close(); self.refresh(); self.clear()
            messagebox.showinfo("Success", "Employee deleted.")
        except Exception as ex:
            messagebox.showerror("DB Error", str(ex))

    def clear(self):
        for v in [self.v_id, self.v_fname, self.v_lname, self.v_email,
                  self.v_cnic, self.v_addr, self.v_phone, self.v_bdate,
                  self.v_hdate, self.v_status, self.v_role]:
            v.set("")


# ══════════════════════════════════════════════════════════════════════════════
# DEPARTMENTS
# ══════════════════════════════════════════════════════════════════════════════
class DepartmentsPage(tk.Frame):
    name = "Departments"

    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        can_edit = app.role in ("admin", "hr", "manager")
        page_title(self, "Departments",
                   "Read-only for Operations role" if not can_edit else "")

        form = tk.Frame(self, bg=CARD, pady=10)
        form.pack(fill="x", padx=24, pady=(0, 10))
        form.columnconfigure((1, 3), weight=1)

        self.v_depid = make_entry(form, "Dep ID",      0, 0)
        self.v_empid = make_entry(form, "Employee ID", 0, 1)
        self.v_name  = make_combo(form, "Department",  1, 0,
                                  ["it","design","management","hr"])

        btn_row = tk.Frame(form, bg=CARD)
        btn_row.grid(row=2, column=0, columnspan=4, pady=8, padx=12, sticky="w")

        if can_edit:
            action_btn(btn_row, "➕ Add",    self.add).pack(side="left", padx=4)
            action_btn(btn_row, "✕  Delete", self.delete, WARNING).pack(side="left", padx=4)
        action_btn(btn_row, "↺  Clear", self.clear, ENTRY_BG).pack(side="left", padx=4)

        if not can_edit:
            tk.Label(btn_row,
                     text="  ⚑  VIEW ONLY — Operations role cannot modify departments",
                     bg=CARD, fg=GOLD, font=FONT_SM).pack(side="left", padx=8)

        self.table = Table(self, ["dep_id","employee_id","dep_name","first_name","last_name"])
        self.table.pack(fill="both", expand=True, padx=24, pady=(0, 12))
        self.table.tv.bind("<<TreeviewSelect>>", self.on_select)

    def refresh(self):
        try:
            conn = get_connection(); cur = conn.cursor()
            cur.execute("SELECT d.dep_id,d.employee_id,d.dep_name,"
                        "e.first_name,e.last_name FROM department d "
                        "JOIN employee e ON d.employee_id=e.employee_id ORDER BY d.dep_id")
            self.table.load(cur.fetchall()); conn.close()
        except Exception as ex:
            messagebox.showerror("DB Error", str(ex))

    def on_select(self, _):
        vals = self.table.selected_values()
        if vals:
            self.v_depid.set(vals[0]); self.v_empid.set(vals[1]); self.v_name.set(vals[2])

    def add(self):
        if not all([self.v_depid.get(), self.v_empid.get(), self.v_name.get()]):
            messagebox.showwarning("Input", "Fill all fields."); return
        try:
            conn = get_connection(); cur = conn.cursor()
            cur.execute("INSERT INTO department VALUES (%s,%s,%s)",
                        (self.v_depid.get(), self.v_empid.get(), self.v_name.get()))
            conn.commit(); conn.close(); self.refresh(); self.clear()
        except Exception as ex:
            messagebox.showerror("DB Error", str(ex))

    def delete(self):
        did = self.v_depid.get()
        if not did: return
        try:
            conn = get_connection(); cur = conn.cursor()
            cur.execute("DELETE FROM department WHERE dep_id=%s", (did,))
            conn.commit(); conn.close(); self.refresh(); self.clear()
        except Exception as ex:
            messagebox.showerror("DB Error", str(ex))

    def clear(self):
        self.v_depid.set(""); self.v_empid.set(""); self.v_name.set("")


# ══════════════════════════════════════════════════════════════════════════════
# SALARY  (admin, hr, finance, manager — finance is READ ONLY)
# ══════════════════════════════════════════════════════════════════════════════
class SalaryPage(tk.Frame):
    name = "Salary"

    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        can_edit = app.role in ("admin", "hr", "manager")
        page_title(self, "Salary / Payroll",
                   "Finance role has read-only access to payroll data" if not can_edit else "")

        form = tk.Frame(self, bg=CARD, pady=10)
        form.pack(fill="x", padx=24, pady=(0, 10))
        form.columnconfigure((1, 3), weight=1)

        self.v_pid    = make_entry(form, "Payroll ID",   0, 0)
        self.v_empid  = make_entry(form, "Employee ID",  0, 1)
        self.v_amt    = make_entry(form, "Amount",       1, 0)
        self.v_bonus  = make_entry(form, "Bonus",        1, 1)
        self.v_deduct = make_entry(form, "Deductions",   2, 0)
        self.v_pdate  = make_entry(form, "Payment Date (YYYY-MM-DD)", 2, 1)

        btn_row = tk.Frame(form, bg=CARD)
        btn_row.grid(row=3, column=0, columnspan=4, pady=8, padx=12, sticky="w")

        if can_edit:
            action_btn(btn_row, "➕ Add",    self.add).pack(side="left", padx=4)
            action_btn(btn_row, "✏  Update", self.update, ACCENT2).pack(side="left", padx=4)
            action_btn(btn_row, "✕  Delete", self.delete, WARNING).pack(side="left", padx=4)
        action_btn(btn_row, "↺  Clear", self.clear, ENTRY_BG).pack(side="left", padx=4)

        if not can_edit:
            tk.Label(btn_row,
                     text="  ⚑  VIEW ONLY — Finance role can view but not modify payroll",
                     bg=CARD, fg=GOLD, font=FONT_SM).pack(side="left", padx=8)

        cols = ["payroll_id","employee_id","first_name","amount",
                "bonus","deductions","net_pay","payment_date"]
        self.table = Table(self, cols)
        self.table.pack(fill="both", expand=True, padx=24, pady=(0, 12))
        self.table.tv.bind("<<TreeviewSelect>>", self.on_select)

    def refresh(self):
        try:
            conn = get_connection(); cur = conn.cursor()
            cur.execute("SELECT s.payroll_id,s.employee_id,e.first_name,"
                        "s.amount,s.bonus,s.deductions,"
                        "(s.amount+s.bonus-s.deductions) AS net_pay,s.payment_date "
                        "FROM salary s JOIN employee e ON s.employee_id=e.employee_id "
                        "ORDER BY s.payroll_id")
            self.table.load(cur.fetchall()); conn.close()
        except Exception as ex:
            messagebox.showerror("DB Error", str(ex))

    def on_select(self, _):
        vals = self.table.selected_values()
        if vals:
            self.v_pid.set(vals[0]); self.v_empid.set(vals[1])
            self.v_amt.set(vals[3]); self.v_bonus.set(vals[4])
            self.v_deduct.set(vals[5]); self.v_pdate.set(vals[7])

    def add(self):
        v = (self.v_pid.get(), self.v_empid.get(), self.v_amt.get(),
             self.v_bonus.get(), self.v_deduct.get(), self.v_pdate.get())
        if not all(v): messagebox.showwarning("Input", "Fill all fields."); return
        try:
            conn = get_connection(); cur = conn.cursor()
            cur.execute("INSERT INTO salary VALUES (%s,%s,%s,%s,%s,%s)", v)
            conn.commit(); conn.close(); self.refresh(); self.clear()
        except Exception as ex:
            messagebox.showerror("DB Error", str(ex))

    def update(self):
        pid = self.v_pid.get()
        if not pid: return
        try:
            conn = get_connection(); cur = conn.cursor()
            cur.execute("UPDATE salary SET employee_id=%s,amount=%s,bonus=%s,"
                        "deductions=%s,payment_date=%s WHERE payroll_id=%s",
                        (self.v_empid.get(), self.v_amt.get(), self.v_bonus.get(),
                         self.v_deduct.get(), self.v_pdate.get(), pid))
            conn.commit(); conn.close(); self.refresh()
        except Exception as ex:
            messagebox.showerror("DB Error", str(ex))

    def delete(self):
        pid = self.v_pid.get()
        if not pid: return
        try:
            conn = get_connection(); cur = conn.cursor()
            cur.execute("DELETE FROM salary WHERE payroll_id=%s", (pid,))
            conn.commit(); conn.close(); self.refresh(); self.clear()
        except Exception as ex:
            messagebox.showerror("DB Error", str(ex))

    def clear(self):
        for v in [self.v_pid, self.v_empid, self.v_amt,
                  self.v_bonus, self.v_deduct, self.v_pdate]:
            v.set("")


# ══════════════════════════════════════════════════════════════════════════════
# ATTENDANCE  — ONLY HR AND ADMIN CAN ADD / EDIT / DELETE
# ══════════════════════════════════════════════════════════════════════════════
class AttendancePage(tk.Frame):
    name = "Attendance"

    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        can_edit = app.role in ATTENDANCE_EDIT_ROLES
        page_title(self, "Attendance",
                   "Only HR and Admin roles may modify attendance records")

        form = tk.Frame(self, bg=CARD, pady=10)
        form.pack(fill="x", padx=24, pady=(0, 10))
        form.columnconfigure((1, 3), weight=1)

        self.v_aid   = make_entry(form, "Attendance ID", 0, 0)
        self.v_empid = make_entry(form, "Employee ID",   0, 1)
        self.v_stat  = make_combo(form, "Status", 1, 0,
                                  ["present","absent","leave"])
        self.v_date  = make_entry(form, "Date (YYYY-MM-DD)", 1, 1)

        btn_row = tk.Frame(form, bg=CARD)
        btn_row.grid(row=2, column=0, columnspan=4, pady=8, padx=12, sticky="w")

        if can_edit:
            action_btn(btn_row, "➕ Add",    self.add).pack(side="left", padx=4)
            action_btn(btn_row, "✏  Update", self.update, ACCENT2).pack(side="left", padx=4)
            action_btn(btn_row, "✕  Delete", self.delete, WARNING).pack(side="left", padx=4)
        action_btn(btn_row, "↺  Clear", self.clear, ENTRY_BG).pack(side="left", padx=4)

        if not can_edit:
            tk.Label(btn_row,
                     text="  ⚑  VIEW ONLY — Only HR/Admin may modify attendance",
                     bg=CARD, fg=GOLD, font=FONT_SM).pack(side="left", padx=8)

        cols = ["attendance_id","employee_id","first_name","status","att_date"]
        self.table = Table(self, cols)
        self.table.pack(fill="both", expand=True, padx=24, pady=(0, 12))
        self.table.tv.bind("<<TreeviewSelect>>", self.on_select)

    def refresh(self):
        try:
            conn = get_connection(); cur = conn.cursor()
            cur.execute("SELECT a.attendance_id,a.employee_id,e.first_name,"
                        "a.status,a.att_date FROM attendance_table a "
                        "JOIN employee e ON a.employee_id=e.employee_id "
                        "ORDER BY a.att_date DESC, a.attendance_id")
            self.table.load(cur.fetchall()); conn.close()
        except Exception as ex:
            messagebox.showerror("DB Error", str(ex))

    def on_select(self, _):
        vals = self.table.selected_values()
        if vals:
            self.v_aid.set(vals[0]); self.v_empid.set(vals[1])
            self.v_stat.set(vals[3]); self.v_date.set(vals[4])

    def add(self):
        if self.app.role not in ATTENDANCE_EDIT_ROLES:
            messagebox.showerror("Access Denied", "Only HR/Admin can add attendance records.")
            return
        aid = self.v_aid.get()
        empid = self.v_empid.get()
        adate = self.v_date.get()
        stat = self.v_stat.get()
        if not all([aid, empid, adate, stat]):
            messagebox.showwarning("Input", "Fill all fields.");
            return
        try:
            conn = get_connection();
            cur = conn.cursor()
            # auto-fetch employee name so employee_name column is never NULL
            cur.execute("SELECT first_name || ' ' || last_name FROM employee WHERE employee_id=%s",
                        (empid,))
            row = cur.fetchone()
            if not row:
                messagebox.showerror("Error", f"No employee found with ID {empid}.");
                conn.close();
                return
            emp_name = row[0]
            cur.execute("""INSERT INTO attendance_table
                           (attendance_id, employee_id, employee_name, status, att_date)
                           VALUES (%s, %s, %s, %s, %s)""",
                        (aid, empid, emp_name, stat, adate))
            conn.commit();
            conn.close();
            self.refresh();
            self.clear()
            messagebox.showinfo("Success", "Attendance record added.")
        except Exception as ex:
            messagebox.showerror("DB Error", str(ex))

    def update(self):
        if self.app.role not in ATTENDANCE_EDIT_ROLES:
            messagebox.showerror("Access Denied", "Only HR/Admin can update attendance records.")
            return
        aid = self.v_aid.get()
        if not aid: messagebox.showwarning("Input", "Select row first"); return
        try:
            conn = get_connection(); cur = conn.cursor()
            cur.execute("""UPDATE attendance_table
                           SET employee_id=%s, att_date=%s, status=%s
                           WHERE attendance_id=%s""",
                        (self.v_empid.get(), self.v_date.get(),
                         self.v_stat.get(), aid))
            conn.commit(); conn.close(); self.refresh()
            messagebox.showinfo("Success", "Attendance updated.")
        except Exception as ex:
            messagebox.showerror("DB Error", str(ex))

    def delete(self):
        if self.app.role not in ATTENDANCE_EDIT_ROLES:
            messagebox.showerror("Access Denied", "Only HR/Admin can delete attendance records.")
            return
        aid = self.v_aid.get()
        if not aid: return
        try:
            conn = get_connection(); cur = conn.cursor()
            cur.execute("DELETE FROM attendance_table WHERE attendance_id=%s", (aid,))
            conn.commit(); conn.close(); self.refresh(); self.clear()
        except Exception as ex:
            messagebox.showerror("DB Error", str(ex))

    def clear(self):
        for v in [self.v_aid, self.v_empid, self.v_stat, self.v_date]:
            v.set("")


# ══════════════════════════════════════════════════════════════════════════════
# APPLICANTS
# ══════════════════════════════════════════════════════════════════════════════
class ApplicantsPage(tk.Frame):
    name = "Applicants"

    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        can_edit = app.role in ("admin", "hr", "manager")
        page_title(self, "Applicants",
                   "Operations role — read-only access" if not can_edit else "")

        form = tk.Frame(self, bg=CARD, pady=10)
        form.pack(fill="x", padx=24, pady=(0, 10))
        form.columnconfigure((1, 3), weight=1)

        self.v_aid  = make_entry(form, "Applicant ID",   0, 0)
        self.v_name = make_entry(form, "Applicant Name", 0, 1)
        self.v_pos  = make_combo(form, "Position", 1, 0,
                                 ["manager","hr","developer","designer"])
        self.v_stat = make_combo(form, "Status",   1, 1,
                                 ["pending","selected","rejected"])

        btn_row = tk.Frame(form, bg=CARD)
        btn_row.grid(row=2, column=0, columnspan=4, pady=8, padx=12, sticky="w")

        if can_edit:
            action_btn(btn_row, "➕ Add",    self.add).pack(side="left", padx=4)
            action_btn(btn_row, "✏  Update", self.update, ACCENT2).pack(side="left", padx=4)
            action_btn(btn_row, "✕  Delete", self.delete, WARNING).pack(side="left", padx=4)
        action_btn(btn_row, "↺  Clear", self.clear, ENTRY_BG).pack(side="left", padx=4)

        if not can_edit:
            tk.Label(btn_row,
                     text="  ⚑  VIEW ONLY — Operations role cannot modify applicant records",
                     bg=CARD, fg=GOLD, font=FONT_SM).pack(side="left", padx=8)

        self.table = Table(self, ["applicant_id","applicant_name","a_position","a_status"])
        self.table.pack(fill="both", expand=True, padx=24, pady=(0, 12))
        self.table.tv.bind("<<TreeviewSelect>>", self.on_select)

    def refresh(self):
        try:
            conn = get_connection(); cur = conn.cursor()
            cur.execute("SELECT * FROM applicant ORDER BY applicant_id")
            self.table.load(cur.fetchall()); conn.close()
        except Exception as ex:
            messagebox.showerror("DB Error", str(ex))

    def on_select(self, _):
        vals = self.table.selected_values()
        if vals:
            self.v_aid.set(vals[0]); self.v_name.set(vals[1])
            self.v_pos.set(vals[2]); self.v_stat.set(vals[3])

    def add(self):
        v = (self.v_aid.get(), self.v_name.get(),
             self.v_pos.get(), self.v_stat.get())
        if not all(v): messagebox.showwarning("Input", "Fill all fields."); return
        try:
            conn = get_connection(); cur = conn.cursor()
            cur.execute("INSERT INTO applicant VALUES (%s,%s,%s,%s)", v)
            conn.commit(); conn.close(); self.refresh(); self.clear()
        except Exception as ex:
            messagebox.showerror("DB Error", str(ex))

    def update(self):
        aid = self.v_aid.get()
        if not aid: return
        try:
            conn = get_connection(); cur = conn.cursor()
            cur.execute("UPDATE applicant SET applicant_name=%s,a_position=%s,"
                        "a_status=%s WHERE applicant_id=%s",
                        (self.v_name.get(), self.v_pos.get(), self.v_stat.get(), aid))
            conn.commit(); conn.close(); self.refresh()
        except Exception as ex:
            messagebox.showerror("DB Error", str(ex))

    def delete(self):
        aid = self.v_aid.get()
        if not aid: return
        try:
            conn = get_connection(); cur = conn.cursor()
            cur.execute("DELETE FROM applicant WHERE applicant_id=%s", (aid,))
            conn.commit(); conn.close(); self.refresh(); self.clear()
        except Exception as ex:
            messagebox.showerror("DB Error", str(ex))

    def clear(self):
        for v in [self.v_aid, self.v_name, self.v_pos, self.v_stat]:
            v.set("")


# ══════════════════════════════════════════════════════════════════════════════
# INTERVIEWS
# ══════════════════════════════════════════════════════════════════════════════
class InterviewsPage(tk.Frame):
    name = "Interviews"

    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        can_edit = app.role in ("admin", "hr", "manager")
        page_title(self, "Interviews",
                   "Operations role — read-only access" if not can_edit else "")

        form = tk.Frame(self, bg=CARD, pady=10)
        form.pack(fill="x", padx=24, pady=(0, 10))
        form.columnconfigure((1, 3), weight=1)

        self.v_iid  = make_entry(form, "Interview ID", 0, 0)
        self.v_apid = make_entry(form, "Applicant ID", 0, 1)
        self.v_res  = make_combo(form, "Result", 1, 0, ["pass","fail","pending"])
        self.v_date = make_entry(form, "Date (YYYY-MM-DD)", 1, 1)

        btn_row = tk.Frame(form, bg=CARD)
        btn_row.grid(row=2, column=0, columnspan=4, pady=8, padx=12, sticky="w")

        if can_edit:
            action_btn(btn_row, "➕ Add",    self.add).pack(side="left", padx=4)
            action_btn(btn_row, "✏  Update", self.update, ACCENT2).pack(side="left", padx=4)
            action_btn(btn_row, "✕  Delete", self.delete, WARNING).pack(side="left", padx=4)
        action_btn(btn_row, "↺  Clear", self.clear, ENTRY_BG).pack(side="left", padx=4)

        if not can_edit:
            tk.Label(btn_row,
                     text="  ⚑  VIEW ONLY — Operations role cannot modify interview records",
                     bg=CARD, fg=GOLD, font=FONT_SM).pack(side="left", padx=8)

        cols = ["interview_id","applicant_id","applicant_name","i_result","i_date"]
        self.table = Table(self, cols)
        self.table.pack(fill="both", expand=True, padx=24, pady=(0, 12))
        self.table.tv.bind("<<TreeviewSelect>>", self.on_select)

    def refresh(self):
        try:
            conn = get_connection(); cur = conn.cursor()
            cur.execute("SELECT i.interview_id,i.applicant_id,a.applicant_name,"
                        "i.i_result,i.i_date FROM interview_table i "
                        "JOIN applicant a ON i.applicant_id=a.applicant_id "
                        "ORDER BY i.i_date DESC")
            self.table.load(cur.fetchall()); conn.close()
        except Exception as ex:
            messagebox.showerror("DB Error", str(ex))

    def on_select(self, _):
        vals = self.table.selected_values()
        if vals:
            self.v_iid.set(vals[0]); self.v_apid.set(vals[1])
            self.v_res.set(vals[3]); self.v_date.set(vals[4])

    def add(self):
        v = (self.v_iid.get(), self.v_apid.get(),
             self.v_res.get(), self.v_date.get())
        if not all(v): messagebox.showwarning("Input", "Fill all fields."); return
        try:
            conn = get_connection(); cur = conn.cursor()
            cur.execute("INSERT INTO interview_table VALUES (%s,%s,%s,%s)", v)
            conn.commit(); conn.close(); self.refresh(); self.clear()
        except Exception as ex:
            messagebox.showerror("DB Error", str(ex))

    def update(self):
        iid = self.v_iid.get()
        if not iid: return
        try:
            conn = get_connection(); cur = conn.cursor()
            cur.execute("UPDATE interview_table SET applicant_id=%s,i_result=%s,"
                        "i_date=%s WHERE interview_id=%s",
                        (self.v_apid.get(), self.v_res.get(), self.v_date.get(), iid))
            conn.commit(); conn.close(); self.refresh()
        except Exception as ex:
            messagebox.showerror("DB Error", str(ex))

    def delete(self):
        iid = self.v_iid.get()
        if not iid: return
        try:
            conn = get_connection(); cur = conn.cursor()
            cur.execute("DELETE FROM interview_table WHERE interview_id=%s", (iid,))
            conn.commit(); conn.close(); self.refresh(); self.clear()
        except Exception as ex:
            messagebox.showerror("DB Error", str(ex))

    def clear(self):
        for v in [self.v_iid, self.v_apid, self.v_res, self.v_date]:
            v.set("")


# ══════════════════════════════════════════════════════════════════════════════
# USERS & ROLES  (admin only)
# ══════════════════════════════════════════════════════════════════════════════
class UsersPage(tk.Frame):
    name = "Users"

    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        page_title(self, "Users & Roles  —  Admin Only",
                   "Manage system users and their assigned roles")

        form = tk.Frame(self, bg=CARD, pady=10)
        form.pack(fill="x", padx=24, pady=(0, 10))
        form.columnconfigure((1, 3), weight=1)

        self.v_uid   = make_entry(form, "User ID",   0, 0)
        self.v_uname = make_entry(form, "Username",  0, 1)
        self.v_upass = make_entry(form, "Password",  1, 0)
        self.v_udept = make_combo(form, "Department", 1, 1,
                                  ["admin","hr","finance","operations","general"])
        self.v_rid   = make_entry(form, "Role ID",   2, 0)
        self.v_role  = make_combo(form, "Role Name", 2, 1,
                                  ["admin","hr","finance","operations",
                                   "manager","employee","developer","designer"])

        btn_row = tk.Frame(form, bg=CARD)
        btn_row.grid(row=3, column=0, columnspan=4, pady=8, padx=12, sticky="w")
        action_btn(btn_row, "➕ Add User+Role", self.add_user).pack(side="left", padx=4)
        action_btn(btn_row, "✕  Delete User",   self.delete_user, WARNING).pack(side="left", padx=4)
        action_btn(btn_row, "↺  Clear",         self.clear, ENTRY_BG).pack(side="left", padx=4)

        self.table = Table(self, ["user_id","user_name","department","role_id","role_name"])
        self.table.pack(fill="both", expand=True, padx=24, pady=(0, 12))
        self.table.tv.bind("<<TreeviewSelect>>", self.on_select)

    def refresh(self):
        try:
            conn = get_connection(); cur = conn.cursor()
            cur.execute("""SELECT u.user_id, u.user_name,
                                  COALESCE(u.department,'general'),
                                  r.role_id, r.role_name
                           FROM users u
                           JOIN rolee r ON u.user_id=r.user_id
                           ORDER BY u.user_id""")
            self.table.load(cur.fetchall()); conn.close()
        except Exception as ex:
            messagebox.showerror("DB Error", str(ex))

    def on_select(self, _):
        vals = self.table.selected_values()
        if vals:
            self.v_uid.set(vals[0]); self.v_uname.set(vals[1])
            self.v_udept.set(vals[2]); self.v_rid.set(vals[3])
            self.v_role.set(vals[4])

    def add_user(self):
        uid   = self.v_uid.get()
        uname = self.v_uname.get()
        upass = self.v_upass.get()
        udept = self.v_udept.get()
        rid   = self.v_rid.get()
        role  = self.v_role.get()
        if not all([uid, uname, upass, udept, rid, role]):
            messagebox.showwarning("Input", "Fill all fields."); return
        try:
            conn = get_connection(); cur = conn.cursor()
            cur.execute("INSERT INTO users (user_id,user_name,user_password,department) "
                        "VALUES (%s,%s,%s,%s)", (uid, uname, upass, udept))
            cur.execute("INSERT INTO rolee (role_id,user_id,role_name) VALUES (%s,%s,%s)",
                        (rid, uid, role))
            conn.commit(); conn.close(); self.refresh(); self.clear()
            messagebox.showinfo("Success", f"User '{uname}' added with role '{role}'.")
        except Exception as ex:
            messagebox.showerror("DB Error", str(ex))

    def delete_user(self):
        uid = self.v_uid.get()
        if not uid: messagebox.showwarning("Input", "Select a user first."); return
        if not messagebox.askyesno("Confirm", f"Delete user {uid} and their role?"): return
        try:
            conn = get_connection(); cur = conn.cursor()
            cur.execute("DELETE FROM rolee WHERE user_id=%s", (uid,))
            cur.execute("DELETE FROM users WHERE user_id=%s", (uid,))
            conn.commit(); conn.close(); self.refresh(); self.clear()
            messagebox.showinfo("Success", "User deleted.")
        except Exception as ex:
            messagebox.showerror("DB Error", str(ex))

    def clear(self):
        for v in [self.v_uid, self.v_uname, self.v_upass,
                  self.v_udept, self.v_rid, self.v_role]:
            v.set("")


# ══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════
def main():
    run_setup()   # ensure DB columns / new users exist
    login = LoginWindow()
    login.mainloop()
    if login.logged_in_role:
        app = HRApp(login.logged_in_role, login.logged_in_user)
        app.mainloop()

if __name__ == "__main__":
    main()
