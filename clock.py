import tkinter as tk
from math import cos, sin, pi
from datetime import datetime,timedelta

# 时钟APP类 
class ClockApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("表盘时钟")
        self.geometry("700x700")
        self.configure(bg='white') # 创建gui的title,大小，背景
        
        # 创建PhotoImage对象并加载图标图片
        icon_image = tk.PhotoImage(file="./images/icon.png")
        self.call('wm', 'iconphoto', self._w, icon_image)
 
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

        # 用于指示是否进行过整点报时
        self.hour_flag=False

        # 创建一个按钮，点击后开始设置倒计时
        self.set_timer_button = tk.Button(self, text="设置定时器", command=self.set_timer, font=('Helvetica', 14))
        self.set_timer_button.pack()

        # 创建一个按钮，点击后开始跳出世界时钟界面
        self.set_timer_button = tk.Button(self, text="打开世界时钟", command=self.set_world_timer, font=('Helvetica', 14))
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

        # 根据输入设置闹钟
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

    # 该函数用于设置世界时钟
    def set_world_timer(self):
        world_clock_app = WorldClockApp()

    # 该函数用于切换24/12小时显示制度
    def toggle_time_format(self):
        current_format=self.time_format.get()
        if current_format == "24小时制":
            self.time_format.set("12小时制")
        else:
            self.time_format.set("24小时制")
    
    # 该函数用于绘制表盘与时分秒针
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
    
    # 该函数用于更新主表盘的时钟
    def update_clock(self):
        current_time = datetime.now().time()
        current_date = datetime.now().date()

        # 判断是否调用闹钟
        if self.alarm_time is not None and self.alarm_flag is False:
            if current_time.hour==self.alarm_time.hour and current_time.minute==self.alarm_time.minute:
                alarm_popup = tk.Toplevel(self)
                alarm_popup.title("闹钟时间到")
                alarm_label = tk.Label(alarm_popup, text="闹钟时间到！！！")
                alarm_label.pack()
                close_button = tk.Button(alarm_popup, text="关闭弹出窗口", command=alarm_popup.destroy)
                close_button.pack()
                self.alarm_flag=True
        
        # 设置整点报时
        if current_time.minute == 0 and self.hour_flag is False:
            hour_popup = tk.Toplevel(self)
            hour_popup.title("整点报时")
            alarm_label = tk.Label(hour_popup, text="现在是北京时间"+str(current_time.hour)+"点整")
            alarm_label.pack()
            close_button = tk.Button(hour_popup, text="关闭弹出窗口", command=hour_popup.destroy)
            close_button.pack()
            self.hour_flag=True
        if current_time.minute!=0 and self.hour_flag is True:
            self.hour_flag=False

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

# 定时器类
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

        self.start_button = tk.Button(self, text="开始倒计时", command=self.start_countdown, font=('Helvetica', 14),state=tk.DISABLED)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(self, text="停止倒计时", command=self.stop_countdown, font=('Helvetica', 14), state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        self.reset_button = tk.Button(self, text="重置定时器", command=self.reset_countdown, font=('Helvetica', 14))
        self.reset_button.pack()

        self.remaining_time = timedelta()
        self.timer_running = False

    # 开始倒计时
    def start_countdown(self):
        self.timer_running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.update_timer()
        

    # 在倒计时的过程中更新界面
    def update_timer(self):
        if self.remaining_time.total_seconds() > 0 and self.timer_running is True:
            self.time_label.config(text=str(self.remaining_time).rjust(8, '0'))
            self.remaining_time -= timedelta(seconds=1)
            self.after(1000, self.update_timer)
        elif self.remaining_time.total_seconds() <= 0:
            self.time_label.config(text="时间到！")
            self.timer_running = False
            self.begin_flag = False
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.DISABLED)

    # 停止倒计时
    def stop_countdown(self):
        self.timer_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
    
    # 重置定时器
    def reset_countdown(self):
        input_time = self.time_entry.get()
        self.timer_running = False
        try:
            hours, minutes, seconds = map(int, input_time.split(':'))
            self.remaining_time = timedelta(hours=hours, minutes=minutes, seconds=seconds)
            self.time_label.config(text=str(self.remaining_time).rjust(8, '0'))
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            
        except ValueError:
            self.time_label.config(text="无效的时间格式")


# 世界时钟类
class WorldClockApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("世界时钟")
        self.geometry("1200x600")
        self.configure(bg='white')

        self.motto_label = tk.Label(self, text="欢迎使用世界时钟系统！", font=('楷体', 16, 'bold'), bg='white')
        self.motto_label.pack()

        self.clock_frames = []  # 存储时钟小部件的列表
        self.time_formats = []  # 存储时制标签的列表
        self.locations = ['UTC', 'New York', 'London', 'Paris', 'Tokyo']  # 添加不同城市的时钟

        for location in self.locations:
            frame = tk.Frame(self, bg='white')
            frame.pack(side=tk.LEFT, padx=20)
            label = tk.Label(frame, text=location, font=('Helvetica', 16), bg='white')
            label.pack()
            clock = self.create_clock(frame)
            self.clock_frames.append(clock)
            self.time_formats.append(tk.StringVar(value="24小时制"))

        self.update_world_clocks()

    # 创建世界时钟
    def create_clock(self, frame):
        canvas = tk.Canvas(frame, width=200, height=180, bg='white', highlightthickness=0)
        canvas.pack()

        time_label = tk.Label(frame, font=('Helvetica', 16), bg='white')
        time_label.pack(pady=10)

        self.hour_hand = None
        self.minute_hand = None
        self.second_hand = None

        return {
            'canvas': canvas,
            'time_label': time_label,
            'hour_hand': None,
            'minute_hand': None,
            'second_hand': None
        }

    # 更新世界时钟
    def update_world_clocks(self):
        for i, location in enumerate(self.locations):
            current_time = datetime.now()
            time_format = self.time_formats[i].get()
            timezone_diff = 0

            if location == 'UTC':
                timezone_diff = 0
            elif location == 'New York':
                timezone_diff = -5
            elif location == 'London':
                timezone_diff = 0
            elif location == 'Paris':
                timezone_diff = 1
            elif location == 'Tokyo':
                timezone_diff = 9

            current_time += timedelta(hours=timezone_diff)

            if time_format == "24小时制":
                time_str = current_time.strftime('%H:%M:%S')
            else:
                time_str = current_time.strftime('%I:%M:%S:%p')

            self.clock_frames[i]['time_label'].config(text=f"{location}: {time_str}")

            self.update_clock(self.clock_frames[i], current_time)

        self.after(1000, self.update_world_clocks)

    # 更新世界时钟指针
    def update_clock(self, clock_frame, current_time):
        hour = current_time.hour
        minute = current_time.minute
        second = current_time.second

        if clock_frame['hour_hand']:
            clock_frame['canvas'].delete(clock_frame['hour_hand'])
        if clock_frame['minute_hand']:
            clock_frame['canvas'].delete(clock_frame['minute_hand'])

        hour_angle = ((hour % 12) + minute / 60 + second / 3600) * (2 * pi / 12) - pi / 2
        hour_length = 40
        hour_x = 100 + cos(hour_angle) * hour_length
        hour_y = 90 + sin(hour_angle) * hour_length
        clock_frame['hour_hand'] = clock_frame['canvas'].create_line(100, 90, hour_x, hour_y, width=4, fill='brown')

        minute_angle = ((minute + second / 60) / 60) * (2 * pi) - pi / 2
        minute_length = 70
        minute_x = 100 + cos(minute_angle) * minute_length
        minute_y = 90 + sin(minute_angle) * minute_length
        clock_frame['minute_hand'] = clock_frame['canvas'].create_line(100, 90, minute_x, minute_y, width=3, fill='green')


if __name__ == "__main__":
    app = ClockApp()
    app.mainloop()


