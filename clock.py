import tkinter as tk
from math import cos, sin, pi
from datetime import datetime,timedelta
 
class ClockApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("表盘时钟")
        self.geometry("800x700")
        self.configure(bg='white') # 创建gui的title,大小，背景
 
        self.motto_label = tk.Label(self, text="欢迎使用时钟系统！",font=('楷体', 16,'bold'), bg='white') # 创建欢迎语
        self.motto_label.pack() # .pack() 是在 tkinter 中用于将部件（widget）显示在窗口上的方法
        
        self.canvas = tk.Canvas(self, width=400, height=360, bg='white', highlightthickness=0)
        self.canvas.pack() #创建画布并显示
 
        self.time_label = tk.Label(self, font=('Helvetica', 16), bg='white')
        self.time_label.pack(pady=10) # 创建时间标签并显示
 
        self.date_label = tk.Label(self, font=('Helvetica', 12), bg='white')
        self.date_label.pack() # 创建日期标签并显示
 
        self.hour_hand = None  # 保存时针图像对象
        self.minute_hand = None  # 保存分针图像对象
        self.second_hand = None  # 保存秒针图像对象

        # 创建一个变量储存当前显示的时制，初始为24小时制
        self.time_format=tk.StringVar(value="24小时制")

        self.format_label=tk.Label(self,textvariable=self.time_format,font=('Helvetica',12),bg='white')
        self.format_label.pack()

        # 创建一个按钮，用于切换制度
        self.toggle_format_button=tk.Button(self,text="切换24/12制度",command=self.toggle_time_format,bg='white')
        self.toggle_format_button.pack()

        # 创建一个输入，让用户通过输入设定闹钟时间
        self.alarm_entry = tk.Entry(self, font=('Helvetica', 16))
        self.alarm_entry.pack()

        # 创建一个按钮，点击后开始设置闹钟
        self.set_alarm_button = tk.Button(self, text="设置闹钟", command=self.set_alarm, font=('Helvetica', 14))
        self.set_alarm_button.pack()

        # 定义一个变量保存闹钟时间
        self.alarm_time=None

        # 用于指示闹钟是否响过
        self.alarm_flag=False

        # 创建一个按钮，点击后开始设置倒计时
        self.set_timer_button = tk.Button(self, text="设置定时器", command=self.set_timer, font=('Helvetica', 14))
        self.set_timer_button.pack()


        self.draw_clock() # 调用函数绘制时钟
        self.update_clock() # 根据当前时间更新时钟
    
    # 该函数用于实现闹钟功能
    def set_alarm(self):
        # 删除之前的标签
        if hasattr(self, 'output_ok'):
            self.output_ok.destroy()
        if hasattr(self, 'output_alarm'):
            self.output_alarm.destroy()
        if hasattr(self, 'output_error'):
            self.output_error.destroy()

        alarm_time_str = self.alarm_entry.get()
        try:
            alarm_time = datetime.strptime(alarm_time_str, '%H:%M')
            self.alarm_time = alarm_time
            self.alarm_flag = False
            self.output_ok=tk.Label(self,text="闹钟设置成功！,设置时间为"+str(alarm_time.hour)+":"+str(alarm_time.minute),font=('Helvetica', 12), bg='white')
            self.output_ok.pack()
                         
        except ValueError:
            self.output_error=tk.Label(self,text="无效的时间格式。请使用HH:MM格式。",font=('Helvetica', 12), bg='white')
            self.output_error.pack()

    # 该函数用于设置定时器
    def set_timer(self):
        count_down_timer_app = CountdownTimerApp()


    def toggle_time_format(self):
        current_format=self.time_format.get()
        if current_format == "24小时制":
            self.time_format.set("12小时制")
        else:
            self.time_format.set("24小时制")
 
    def draw_clock(self):
        center_x = 200
        center_y = 200
        radius = 150
 
        # 绘制表盘
        self.canvas.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius,
                                width=2, outline='blue')
 
        # 绘制刻度线和小时标识
        for i in range(12):
            angle = (i / 12) * 2 * pi -1/3 * pi
            x1 = center_x + cos(angle) * (radius - 10)
            y1 = center_y + sin(angle) * (radius - 10)
            x2 = center_x + cos(angle) * radius
            y2 = center_y + sin(angle) * radius
            self.canvas.create_line(x1, y1, x2, y2, width=3)
            hour_x = center_x + cos(angle) * (radius - 25)
            hour_y = center_y + sin(angle) * (radius - 25)
            self.canvas.create_text(hour_x, hour_y, text=str(i+1), font=('Helvetica', 12), fill='black')
 
    def update_clock(self):
        current_time = datetime.now().time()
        current_date = datetime.now().date()

        if self.alarm_time is not None and self.alarm_flag is False:
            if current_time.hour==self.alarm_time.hour and current_time.minute==self.alarm_time.minute:
                popup = tk.Toplevel(self)
                popup.title("闹钟时间到")
                alarm_label = tk.Label(popup, text="闹钟时间到！！！")
                alarm_label.pack()
                close_button = tk.Button(popup, text="关闭弹出窗口", command=popup.destroy)
                close_button.pack()
                self.alarm_flag=True
                

        # 根据制度标签更新时间标签
        current_format=self.time_format.get()
        if current_format == "24小时制":
            time_str = current_time.strftime('%H:%M:%S')
        else:
            time_str = current_time.strftime('%I:%M:%S:%p')
        self.time_label.config(text=time_str)
 
        # 更新日期标签
        date_str = current_date.strftime('%Y-%m-%d')
        self.date_label.config(text=date_str)
 
        # 删除上一次的时针和分针图像
        if self.hour_hand:
            self.canvas.delete(self.hour_hand)
        if self.minute_hand:
            self.canvas.delete(self.minute_hand)
 
        # 更新时针
        hour = current_time.hour
        minute = current_time.minute
        second = current_time.second
 
        hour_angle = ((hour % 12) + minute / 60 + second / 3600) * (2 * pi / 12) - pi / 2
        hour_length = hour_x = 200 + cos(hour_angle) * 60
        hour_y = 200 + sin(hour_angle) * 60
        self.hour_hand = self.canvas.create_line(200, 200, hour_x, hour_y, width=4, fill='brown')
        
        # 更新分针
        minute_angle = ((minute + second / 60) / 60) * (2 * pi) - pi / 2
        minute_length = 90
        minute_x = 200 + cos(minute_angle) * minute_length
        minute_y = 200 + sin(minute_angle) * minute_length
        self.minute_hand = self.canvas.create_line(200, 200, minute_x, minute_y, width=3, fill='green')
 
        # 更新秒针
        second_angle = (second / 60.0) * (2 * pi) - pi / 2
        second_length = 120
        second_x = 200 + cos(second_angle) * second_length
        second_y = 200 + sin(second_angle) * second_length
        if self.second_hand:
            self.canvas.delete(self.second_hand)
        self.second_hand = self.canvas.create_line(200, 200, second_x, second_y, width=2, fill='red')
 
        self.after(1000, self.update_clock)


class CountdownTimerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("倒计时定时器")
        self.geometry("400x300")

        self.time_label = tk.Label(self, text="00:00:00", font=('Helvetica', 36), bg='white')
        self.time_label.pack(pady=20)

        self.time_entry = tk.Entry(self, font=('Helvetica', 16))
        self.time_entry.insert(0, "00:05:00")  # 默认设置为5分钟
        self.time_entry.pack()

        self.start_button = tk.Button(self, text="开始倒计时", command=self.start_countdown, font=('Helvetica', 14))
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(self, text="停止倒计时", command=self.stop_countdown, font=('Helvetica', 14), state=tk.DISABLED)
        self.stop_button.pack()

        self.remaining_time = timedelta()
        self.timer_running = False

    def start_countdown(self):
        if not self.timer_running:
            input_time = self.time_entry.get()
            try:
                hours, minutes, seconds = map(int, input_time.split(':'))
                self.remaining_time = timedelta(hours=hours, minutes=minutes, seconds=seconds)
                self.update_timer()
                self.timer_running = True
                self.start_button.config(state=tk.DISABLED)
                self.stop_button.config(state=tk.NORMAL)
            except ValueError:
                self.time_label.config(text="无效的时间格式")
        else:
            self.update_timer()

    def update_timer(self):
        if self.remaining_time.total_seconds() > 0:
            self.time_label.config(text=str(self.remaining_time).rjust(8, '0'))
            self.remaining_time -= timedelta(seconds=1)
            self.after(1000, self.update_timer)
        else:
            self.time_label.config(text="时间到！")
            self.timer_running = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

    def stop_countdown(self):
        self.timer_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    app = ClockApp()
    app.mainloop()