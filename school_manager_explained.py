"""
مشروع تطويري: برنامج إدارة الطلاب والفصول
------------------------------------------
هذه النسخة (شرح) مخصصة للتعليم، وليست النسخة النهائية للاستخدام فقط.

الفكرة:
- يكون عندنا فصول (مثل: الأول، الثاني...)
- وكل فصل يحتوي على طلاب
- كل طالب له: اسم، عمر، رقم هوية، درجة، وحالة (ناجح / راسب)
- نخزّن البيانات في ملف (JSON) حتى لا تضيع بعد إغلاق البرنامج
- نعرض الطلاب في واجهة رسومية باستخدام Tkinter

ملاحظة:
- كل جزء في الكود تحته تعليق يشرح:
  * لماذا كتبنا هذا السطر؟
  * ماذا يفعل؟
  * ما فائدته في البرنامج؟
"""

# -------------------------------------------------
# 1) استيراد المكتبات اللازمة
# -------------------------------------------------

# مكتبة tkinter: لإنشاء الواجهة الرسومية (نافذة + أزرار + حقول)
import tkinter as tk

# من tkinter نستورد ttk (نسخة محسّنة من العناصر) و messagebox (نوافذ رسائل تنبيه)
from tkinter import ttk, messagebox

# مكتبة json: نستخدمها لحفظ بيانات الطلاب والفصول في ملف بصيغة JSON
import json

# من pathlib نستورد Path: للتعامل مع مسارات الملفات بسهولة
from pathlib import Path


# -------------------------------------------------
# 2) تعريف ملف تخزين البيانات
# -------------------------------------------------

# هنا نحدد اسم ملف التخزين الذي سيحفظ فيه البرنامج بيانات الفصول والطلاب.
# Path("school_data.json") يعني ملف اسمه school_data.json في نفس مجلد البرنامج.
DATA_FILE = Path("school_data.json")


# -------------------------------------------------
# 3) هيكلة البيانات في الذاكرة
# -------------------------------------------------

# هذا القاموس (dictionary) سيحمل بيانات الفصول والطلاب أثناء تشغيل البرنامج.
# الشكل سيكون كالتالي تقريباً:
# {
#   "الأول": [
#       {"name": "راكان", "age": 10, "id": "123", "grade": 90, "status": "ناجح"},
#       {"name": "محمد", "age": 11, "id": "456", "grade": 40, "status": "راسب"}
#   ],
#   "الثاني": [
#       {... طلاب آخرون ...}
#   ]
# }
classes_data = {}  # في البداية يكون فارغ، ثم نعبّيه من الملف أو من إدخال المستخدم


# -------------------------------------------------
# 4) دالة حفظ البيانات في ملف JSON
# -------------------------------------------------

def save_data():
    """
    تحفظ البيانات الموجودة في القاموس classes_data داخل ملف JSON.

    لماذا نحتاجها؟
    - حتى لو أغلق المستخدم البرنامج، تبقى بيانات الطلاب محفوظة.
    - في المرة القادمة يمكننا تحميلها وعدم البدء من الصفر.
    """
    try:
        # نفتح الملف بوضع الكتابة "w" وترميز utf-8 لدعم اللغة العربية
        with DATA_FILE.open("w", encoding="utf-8") as f:
            # نكتب القاموس بصيغة JSON
            # ensure_ascii=False حتى لا تتحول الأحرف العربية إلى رموز
            # indent=2 فقط لتنسيق الملف وجعله مقروءاً
            json.dump(classes_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        # في حال حدوث خطأ أثناء الحفظ، نطبع رسالة في الكونسول (لن يظهر للمستخدم العادي)
        print("Error saving data:", e)


# -------------------------------------------------
# 5) دالة تحميل البيانات من ملف JSON (إن وجد)
# -------------------------------------------------

def load_data():
    """
    تقرأ ملف JSON (إن وجد) وتعيد تعبئة القاموس classes_data بالبيانات القديمة.

    فائدتها:
    - استرجاع بيانات الطلاب والفصول عند تشغيل البرنامج مرة أخرى.
    """
    global classes_data  # نحتاج global لأننا سنعدّل المتغير الخارجي

    # نتأكد أولاً أن الملف موجود فعلاً حتى لا يحدث خطأ
    if DATA_FILE.exists():
        try:
            # نفتح الملف للقراءة
            with DATA_FILE.open("r", encoding="utf-8") as f:
                data = json.load(f)  # نحمّل محتوى الملف كـ dict

                # نتأكد أن البيانات عبارة عن قاموس قبل تخزينها
                if isinstance(data, dict):
                    classes_data = data
        except Exception as e:
            print("Error loading data:", e)


# -------------------------------------------------
# 6) دالة إضافة فصل جديد
# -------------------------------------------------

def add_class():
    """
    تقرأ اسم الفصل من حقل الإدخال،
    ثم تضيفه إلى القاموس classes_data إن لم يكن موجوداً.
    """
    # نقرأ النص المكتوب في حقل اسم الفصل
    class_name = entry_class.get().strip()

    # إذا كان الحقل فارغاً، نعرض رسالة خطأ للمستخدم
    if not class_name:
        messagebox.showerror("خطأ", "رجاءً أدخل اسم الفصل.")
        return

    # إذا كان الفصل موجوداً مسبقاً، نعرض رسالة إخبار فقط
    if class_name in classes_data:
        messagebox.showinfo("تنبيه", "هذا الفصل موجود مسبقاً.")
        return

    # إذا كان جديداً، نضيفه كفصل بقائمة طلاب فارغة
    classes_data[class_name] = []

    # نحفظ التغييرات في الملف
    save_data()

    # نخبر المستخدم أن العملية تمت بنجاح
    messagebox.showinfo("تم", f"تمت إضافة الفصل: {class_name}")


# -------------------------------------------------
# 7) دالة إضافة طالب إلى فصل
# -------------------------------------------------

def add_student():
    """
    تقرأ بيانات الطالب من حقول الإدخال
    (الاسم، العمر، رقم الهوية، الدرجة، واسم الفصل)
    ثم تضيف الطالب إلى الفصل المناسب.
    """
    # نقرأ اسم الفصل من حقل الفصل
    class_name = entry_class.get().strip()

    # نقرأ كل بيانات الطالب من الحقول
    name = entry_student_name.get().strip()
    age = entry_student_age.get().strip()
    student_id = entry_student_id.get().strip()
    grade = entry_student_grade.get().strip()

    # أولاً: نتأكد أن كل الحقول غير فارغة
    if not class_name or not name or not age or not student_id or not grade:
        messagebox.showerror("خطأ", "رجاءً أدخل كل بيانات الطالب واسم الفصل.")
        return

    # ثانياً: نتحقق أن العمر رقم صحيح
    if not age.isdigit():
        messagebox.showerror("خطأ", "العمر يجب أن يكون رقمًا صحيحًا.")
        return

    # ثالثاً: نتحقق أن رقم الهوية رقم (هنا فقط نتأكد أنه أرقام، بدون شروط أخرى)
    if not student_id.isdigit():
        messagebox.showerror("خطأ", "رقم الهوية يجب أن يحتوي على أرقام فقط.")
        return

    # رابعاً: نحاول تحويل الدرجة إلى رقم (تقبل الكسور مثل 89.5)
    try:
        grade_value = float(grade)
    except ValueError:
        messagebox.showerror("خطأ", "الدرجة يجب أن تكون رقمًا (مثلاً 75 أو 89.5).")
        return

    # خامساً: نتأكد أن الفصل موجود، إذا لم يكن موجوداً نُخبر المستخدم
    if class_name not in classes_data:
        messagebox.showerror("خطأ", "الفصل غير موجود. أضفه أولاً من زر (إضافة فصل).")
        return

    # هنا نحدد حالة الطالب بناءً على الدرجة
    # إذا الدرجة >= 50 يكون الطالب ناجح، غير ذلك راسب
    status = "ناجح" if grade_value >= 50 else "راسب"

    # ننشئ قاموس يمثل طالب واحد
    student = {
        "name": name,
        "age": int(age),      # نحول العمر إلى int
        "id": student_id,
        "grade": grade_value, # الدرجة float
        "status": status,
    }

    # نضيف الطالب إلى قائمة طلاب هذا الفصل
    classes_data[class_name].append(student)

    # نحفظ التغييرات في الملف
    save_data()

    # نعرض رسالة نجاح
    messagebox.showinfo("تم", f"تمت إضافة الطالب: {name} إلى الفصل: {class_name}")

    # أخيراً: نفرغ حقول بيانات الطالب لتسهيل إدخال طالب جديد
    entry_student_name.delete(0, tk.END)
    entry_student_age.delete(0, tk.END)
    entry_student_id.delete(0, tk.END)
    entry_student_grade.delete(0, tk.END)


# -------------------------------------------------
# 8) دالة عرض طلاب فصل معيّن في نافذة جديدة (جدول)
# -------------------------------------------------

def show_class_students():
    """
    تفتح نافذة جديدة تحتوي على جدول (Treeview)
    يعرض كل طلاب الفصل الذي تم إدخال اسمه.
    """
    # نقرأ اسم الفصل من حقل الإدخال
    class_name = entry_class.get().strip()

    # إذا اسم الفصل فارغ أو غير موجود في البيانات نعرض رسالة خطأ
    if not class_name or class_name not in classes_data:
        messagebox.showerror("خطأ", "رجاءً أدخل اسم فصل موجود أولاً.")
        return

    # نأخذ قائمة الطلاب لهذا الفصل
    students = classes_data[class_name]

    # إذا لا يوجد أي طالب في هذا الفصل نعرض رسالة إخبار
    if not students:
        messagebox.showinfo("تنبيه", "لا يوجد طلاب في هذا الفصل حتى الآن.")
        return

    # ننشئ نافذة جديدة فرعية (Toplevel) داخل البرنامج
    win = tk.Toplevel(root)
    win.title(f"طلاب الفصل: {class_name}")
    win.geometry("650x350")

    # نستخدم Treeview لعرض جدول
    # الأعمدة: الاسم، العمر، رقم الهوية، الدرجة، الحالة
    columns = ("name", "age", "id", "grade", "status")
    tree = ttk.Treeview(win, columns=columns, show="headings")

    # نحدد العناوين الظاهرة في رأس العمود
    tree.heading("name", text="الاسم")
    tree.heading("age", text="العمر")
    tree.heading("id", text="رقم الهوية")
    tree.heading("grade", text="الدرجة")
    tree.heading("status", text="الحالة")

    # نحدد عرض كل عمود ومحاذاته
    for col in columns:
        tree.column(col, width=120, anchor="center")

    # نضع الجدول في النافذة ونسمح له بالتمدد مع النافذة
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    # نضيف كل طالب كسطر (صف) في الجدول
    for st in students:
        tree.insert(
            "",                # لا يوجد أب (عنصر رئيسي)
            tk.END,            # نضيفه في النهاية
            values=(
                st["name"],
                st["age"],
                st["id"],
                st["grade"],
                st["status"]
            )
        )


# -------------------------------------------------
# 9) إنشاء الواجهة الرئيسية (نافذة البرنامج)
# -------------------------------------------------

# ننشئ كائن root وهو النافذة الرئيسية للبرنامج
root = tk.Tk()

# نضع عنوان للنافذة يظهر في شريط العنوان
root.title("مشروع: إدارة الطلاب والفصول (نسخة مشروحة)")

# نضبط حجم النافذة (العرض × الارتفاع) بالبيكسل
root.geometry("500x500")


# -------------------------------------------------
# 10) عناصر إدخال وواجهة المستخدم
# -------------------------------------------------

# أولاً: حقل اسم الفصل
label_class = ttk.Label(root, text="اسم الفصل:")
label_class.pack(anchor="w", padx=10, pady=(10, 0))

entry_class = ttk.Entry(root)
entry_class.pack(fill="x", padx=10, pady=5)

btn_add_class = ttk.Button(root, text="إضافة فصل", command=add_class)
btn_add_class.pack(padx=10, pady=5)


# ثانياً: إطار لبيانات الطالب (مجموعة منظمة)
frame_student = ttk.LabelFrame(root, text="بيانات الطالب")
frame_student.pack(fill="both", expand=False, padx=10, pady=10)

# حقل اسم الطالب
label_student_name = ttk.Label(frame_student, text="اسم الطالب:")
label_student_name.pack(anchor="w", pady=(5, 0))

entry_student_name = ttk.Entry(frame_student)
entry_student_name.pack(fill="x", pady=2)

# حقل عمر الطالب
label_student_age = ttk.Label(frame_student, text="العمر:")
label_student_age.pack(anchor="w", pady=(5, 0))

entry_student_age = ttk.Entry(frame_student)
entry_student_age.pack(fill="x", pady=2)

# حقل رقم الهوية
label_student_id = ttk.Label(frame_student, text="رقم الهوية:")
label_student_id.pack(anchor="w", pady=(5, 0))

entry_student_id = ttk.Entry(frame_student)
entry_student_id.pack(fill="x", pady=2)

# حقل الدرجة
label_student_grade = ttk.Label(frame_student, text="الدرجة:")
label_student_grade.pack(anchor="w", pady=(5, 0))

entry_student_grade = ttk.Entry(frame_student)
entry_student_grade.pack(fill="x", pady=2)

# زر إضافة الطالب
btn_add_student = ttk.Button(root, text="إضافة طالب", command=add_student)
btn_add_student.pack(padx=10, pady=5)

# زر عرض طلاب الفصل
btn_show_class = ttk.Button(root, text="عرض طلاب هذا الفصل", command=show_class_students)
btn_show_class.pack(padx=10, pady=5)


# -------------------------------------------------
# 11) تحميل البيانات السابقة وتشغيل الحلقة الرئيسية
# -------------------------------------------------

# نحاول تحميل بيانات قديمة (إن وجدت) قبل تشغيل الواجهة
load_data()

# نبدأ الحلقة الرئيسية للواجهة (لازم دائماً في أي برنامج Tkinter)
root.mainloop()
