import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import math
import re
from language_resources import text_resources

class TCPThroughputCalculator:
    # 程序版本和信息
    VERSION = "1.0.0"
    LICENSE = "MIT License"
    AUTHOR = "曹宇"
    AUTHOR_EMAIL = "sankingcao@gmail.com"

    def create_menu(self):
        menubar = tk.Menu(self.root)
        # 语言菜单
        language_menu = tk.Menu(menubar, tearoff=0)
        language_menu.add_command(label="中文", command=lambda: self.set_language("zh_CN"))
        language_menu.add_command(label="English", command=lambda: self.set_language("en_US"))
        menubar.add_cascade(label=self.texts["menu_language"], menu=language_menu)
        # 关于菜单
        menubar.add_command(label=self.texts["about_button"], command=self.show_about)
        self.root.config(menu=menubar)

    def __init__(self, root):
        self.root = root
        
        # 设置默认语言
        self.current_language = "zh_CN"
        self.texts = text_resources[self.current_language]
        
        self.root.title(self.texts["window_title"])
        self.root.geometry("750x700")
        self.root.resizable(False, False)
        
        # 窗口居中显示
        self.center_window()
        
        # 设置样式
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Arial", 10))
        self.style.configure("TButton", font=("Arial", 10))
        self.style.configure("TEntry", font=("Arial", 10))
        
        self.create_widgets()
        # 添加菜单栏
        self.create_menu()

    def create_widgets(self):
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10 10 10 10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=2)
        
        # 上半部分框架
        top_frame = ttk.Frame(main_frame)
        top_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
        top_frame.columnconfigure(0, weight=1)
        top_frame.columnconfigure(1, weight=1)
        
        # 左侧参数区（包含基本参数和高级参数）
        left_frame = ttk.Frame(top_frame)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        left_frame.columnconfigure(0, weight=1)
        

        input_frame = ttk.LabelFrame(left_frame, text=self.texts["basic_params"], padding="10 10 10 10")
        input_frame.pack(fill=tk.X, expand=False, padx=0, pady=(0, 10))
        # 带宽输入
        bandwidth_label = ttk.Label(input_frame, text=self.texts["bandwidth"])
        bandwidth_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.create_tooltip(bandwidth_label, self.texts["bandwidth_tooltip"])
        self.bandwidth_entry = ttk.Entry(input_frame, width=12)
        self.bandwidth_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        self.bandwidth_entry.insert(0, "100")
        # 添加输入验证
        self.bandwidth_entry.bind("<FocusOut>", lambda e: self.validate_input(self.bandwidth_entry, 0.1, 10000, self.texts["bandwidth"].replace(":", "")))
        self.bandwidth_unit = tk.StringVar(value="Mbps")
        bandwidth_unit_combo = ttk.Combobox(input_frame, textvariable=self.bandwidth_unit, values=["kbps", "Mbps", "Gbps"], width=8, state="readonly")
        bandwidth_unit_combo.grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        # RTT输入
        rtt_label = ttk.Label(input_frame, text=self.texts["rtt"])
        rtt_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.create_tooltip(rtt_label, self.texts["rtt_tooltip"])
        self.rtt_entry = ttk.Entry(input_frame, width=12)
        self.rtt_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        self.rtt_entry.insert(0, "50")
        # 添加输入验证
        self.rtt_entry.bind("<FocusOut>", lambda e: self.validate_input(self.rtt_entry, 1, 1000, "RTT"))
        # 线程数输入
        threads_label = ttk.Label(input_frame, text=self.texts["threads"])
        threads_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.create_tooltip(threads_label, self.texts["threads_tooltip"])
        self.threads_entry = ttk.Entry(input_frame, width=12)
        self.threads_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        self.threads_entry.insert(0, "1")
        # 添加输入验证
        self.threads_entry.bind("<FocusOut>", lambda e: self.validate_input(self.threads_entry, 1, 128, self.texts["threads"].replace(":", ""), True))

        advanced_frame = ttk.LabelFrame(left_frame, text=self.texts["advanced_params"], padding="10 10 10 10")
        advanced_frame.pack(fill=tk.X, expand=False, padx=0, pady=(0, 10))
        window_size_label = ttk.Label(advanced_frame, text=self.texts["window_size"])
        window_size_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.create_tooltip(window_size_label, self.texts["window_size_tooltip"])
        self.window_size_entry = ttk.Entry(advanced_frame, width=12)
        self.window_size_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        self.window_size_entry.insert(0, "64")
        # 添加输入验证
        self.window_size_entry.bind("<FocusOut>", lambda e: self.validate_input(self.window_size_entry, 8, 16384, self.texts["window_size"].replace(":", "").replace(" (KB)", "")))
        ttk.Label(advanced_frame, text=self.texts["window_size_default"]).grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        mss_label = ttk.Label(advanced_frame, text=self.texts["mss"])
        mss_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.create_tooltip(mss_label, self.texts["mss_tooltip"])
        self.mss_entry = ttk.Entry(advanced_frame, width=12)
        self.mss_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        self.mss_entry.insert(0, "1460")
        # 添加输入验证
        self.mss_entry.bind("<FocusOut>", lambda e: self.validate_input(self.mss_entry, 536, 9000, "MSS"))
        ttk.Label(advanced_frame, text=self.texts["mss_default"]).grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        packet_loss_label = ttk.Label(advanced_frame, text=self.texts["packet_loss"])
        packet_loss_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.create_tooltip(packet_loss_label, self.texts["packet_loss_tooltip"])
        self.packet_loss_entry = ttk.Entry(advanced_frame, width=12)
        self.packet_loss_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        self.packet_loss_entry.insert(0, "0")
        # 添加输入验证
        self.packet_loss_entry.bind("<FocusOut>", lambda e: self.validate_input(self.packet_loss_entry, 0, 30, self.texts["packet_loss"].replace(":", "").replace(" (%)", "")))
        ttk.Label(advanced_frame, text=self.texts["packet_loss_default"]).grid(row=2, column=2, sticky=tk.W, padx=5, pady=5)
        jitter_label = ttk.Label(advanced_frame, text=self.texts["jitter"])
        jitter_label.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.create_tooltip(jitter_label, self.texts["jitter_tooltip"])
        self.jitter_entry = ttk.Entry(advanced_frame, width=12)
        self.jitter_entry.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        self.jitter_entry.insert(0, "0")
        # 添加输入验证
        self.jitter_entry.bind("<FocusOut>", lambda e: self.validate_input(self.jitter_entry, 0, 200, self.texts["jitter"].replace(":", "").replace(" (ms)", "")))
        ttk.Label(advanced_frame, text=self.texts["jitter_default"]).grid(row=3, column=2, sticky=tk.W, padx=5, pady=5)
        congestion_label = ttk.Label(advanced_frame, text=self.texts["congestion"])
        congestion_label.grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.create_tooltip(congestion_label, self.texts["congestion_tooltip"])
        self.congestion_algorithm = tk.StringVar(value="Reno")
        congestion_combo = ttk.Combobox(advanced_frame, textvariable=self.congestion_algorithm, values=["Reno", "CUBIC", "BBR", "Westwood"], width=12, state="readonly")
        congestion_combo.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Label(advanced_frame, text=self.texts["congestion_default"]).grid(row=4, column=2, sticky=tk.W, padx=5, pady=5)

        # 右侧结果区
        right_frame = ttk.Frame(top_frame)
        right_frame.grid(row=0, column=1, sticky="nsew")
        right_frame.columnconfigure(0, weight=1)

        # 创建一个容器框架来包含结果框架和计算按钮
        result_container = ttk.Frame(right_frame)
        result_container.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        result_frame = ttk.LabelFrame(result_container, text=self.texts["result_frame"], padding="10 10 10 10")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=(0, 5))
        ttk.Label(result_frame, text=self.texts["throughput"]).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.result_label = tk.Label(result_frame, text="--", font=("Arial", 10, "bold"), fg="red")
        self.result_label.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Label(result_frame, text=self.texts["display_unit"]).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.result_unit = tk.StringVar(value="Mbps")
        result_unit_combo = ttk.Combobox(result_frame, textvariable=self.result_unit, values=["bps", "kbps", "Mbps", "Gbps"], width=8, state="readonly")
        result_unit_combo.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        result_unit_combo.bind("<<ComboboxSelected>>", lambda e: self.update_result_display())
        self.calculation_basis_label = ttk.Label(result_frame, text="", wraplength=350, justify="left")
        self.calculation_basis_label.grid(row=2, column=0, columnspan=3, sticky=tk.W, padx=5, pady=5)

        # 创建按钮容器框架
        button_container = ttk.Frame(result_container)
        button_container.pack(pady=5, fill=tk.X)
        button_container.columnconfigure(0, weight=1)
        button_container.columnconfigure(1, weight=1)
        
        # 计算按钮
        calculate_button = ttk.Button(button_container, text=self.texts["calculate_button"], command=self.calculate_throughput)
        calculate_button.grid(row=0, column=0, padx=5, sticky="e")
        

        # 下半部分的计算公式说明
        formula_frame = ttk.LabelFrame(main_frame, text=self.texts["formula_frame"], padding="10 10 10 10")
        formula_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(10, 0))
        formula_label = ttk.Label(formula_frame, text=self.texts["formula_text"], wraplength=700, justify="left")
        formula_label.pack(fill=tk.BOTH, expand=True)
        self.last_result_bps = 0
    
    def calculate_throughput(self):
        try:
            # 获取基本输入值
            bandwidth_value = float(self.bandwidth_entry.get())
            rtt_ms = float(self.rtt_entry.get())
            threads = int(self.threads_entry.get())
            
            # 获取高级参数输入值
            window_size_kb = float(self.window_size_entry.get())
            mss_bytes = float(self.mss_entry.get())
            packet_loss_percent = float(self.packet_loss_entry.get())
            jitter_ms = float(self.jitter_entry.get())
            congestion_algorithm = self.congestion_algorithm.get()
            
            # 验证基本输入参数范围
            error_msg = None
            if bandwidth_value <= 0:
                error_msg = self.texts["error_bandwidth_positive"]
            elif bandwidth_value > 10000 and self.bandwidth_unit.get() == "Gbps":
                error_msg = self.texts["error_bandwidth_too_large"]
            elif rtt_ms <= 0:
                error_msg = self.texts["error_rtt_positive"]
            elif rtt_ms > 1000:
                error_msg = self.texts["error_rtt_too_large"]
            elif threads <= 0:
                error_msg = self.texts["error_threads_positive"]
            elif threads > 128:
                error_msg = self.texts["error_threads_too_large"]
            
            # 验证高级参数范围
            elif window_size_kb <= 0:
                error_msg = self.texts["error_window_size_positive"]
            elif window_size_kb > 16384:
                error_msg = self.texts["error_window_size_too_large"]
            elif mss_bytes <= 0:
                error_msg = self.texts["error_mss_positive"]
            elif mss_bytes < 536:
                error_msg = self.texts["error_mss_too_small"]
            elif mss_bytes > 9000:
                error_msg = self.texts["error_mss_too_large"]
            elif packet_loss_percent < 0 or packet_loss_percent > 100:
                error_msg = self.texts["error_packet_loss_range"]
            elif packet_loss_percent > 30:
                error_msg = self.texts["error_packet_loss_too_large"]
            elif jitter_ms < 0:
                error_msg = self.texts["error_jitter_negative"]
            elif jitter_ms > 200:
                error_msg = self.texts["error_jitter_too_large"]
                
            if error_msg:
                self.result_label.config(text=error_msg)
                return
            
            # 将带宽转换为bps
            bandwidth_unit = self.bandwidth_unit.get()
            if bandwidth_unit == "kbps":
                bandwidth_bps = bandwidth_value * 1000
            elif bandwidth_unit == "Mbps":
                bandwidth_bps = bandwidth_value * 1000000
            elif bandwidth_unit == "Gbps":
                bandwidth_bps = bandwidth_value * 1000000000
            
            # TCP窗口大小（用户输入，默认为64KB）
            tcp_window_size = window_size_kb * 1024  # 字节
            
            # 考虑网络抖动对RTT的影响
            effective_rtt_ms = rtt_ms + jitter_ms
            
            # 基础计算理论最大速率 (bps)
            # 公式: 窗口大小(bits) / RTT(s) * 线程数
            base_throughput_bps = (tcp_window_size * 8) / (effective_rtt_ms / 1000) * threads
            
            # 考虑丢包率的影响 (使用Mathis模型)
            # 对于不同的拥塞控制算法，调整系数
            if packet_loss_percent > 0:
                if congestion_algorithm == "Reno":
                    c_factor = 1.22
                    throughput_with_loss = (mss_bytes * 8 / (effective_rtt_ms / 1000)) * (c_factor / math.sqrt(packet_loss_percent / 100))
                    base_throughput_bps = min(base_throughput_bps, throughput_with_loss * threads)
                elif congestion_algorithm == "CUBIC":
                    c_factor = 1.5
                    throughput_with_loss = (mss_bytes * 8 / (effective_rtt_ms / 1000)) * (c_factor / math.sqrt(packet_loss_percent / 100))
                    base_throughput_bps = min(base_throughput_bps, throughput_with_loss * threads)
                elif congestion_algorithm == "BBR":
                    # BBR主要受带宽限制，丢包影响较小，但丢包率大于0时应略有影响，且不能高于无丢包速率
                    loss_factor = max(0.0, 1 - (packet_loss_percent / 100))
                    mss_factor = mss_bytes / 1460
                    bbr_no_loss = base_throughput_bps
                    bbr_with_loss = bbr_no_loss * loss_factor * mss_factor
                    base_throughput_bps = min(bbr_no_loss, bbr_with_loss)
                elif congestion_algorithm == "Westwood":
                    c_factor = 1.35
                    throughput_with_loss = (mss_bytes * 8 / (effective_rtt_ms / 1000)) * (c_factor / math.sqrt(packet_loss_percent / 100))
                    base_throughput_bps = min(base_throughput_bps, throughput_with_loss * threads)
            else:
                # 无丢包情况下，MSS对吞吐率的影响
                # MSS影响所有算法的吞吐率，不仅仅是BBR
                mss_factor = mss_bytes / 1460
                if congestion_algorithm == "BBR":
                    base_throughput_bps *= mss_factor
                elif congestion_algorithm in ["Reno", "CUBIC", "Westwood"]:
                    # 其他算法也受MSS影响，但影响程度较小
                    mss_impact_factor = 0.95 + (0.05 * (mss_bytes / 1460))
                    base_throughput_bps *= mss_impact_factor
            
            # 考虑带宽限制
            throughput_bps = min(base_throughput_bps, bandwidth_bps)
            
            # 保存结果
            self.last_result_bps = throughput_bps
            
            # 更新显示
            self.update_result_display()
            
            # 更新计算依据说明
            self.update_calculation_basis(
                bandwidth_value, bandwidth_unit, rtt_ms, threads, 
                tcp_window_size, throughput_bps, bandwidth_bps,
                window_size_kb, mss_bytes, packet_loss_percent, jitter_ms, congestion_algorithm
            )
            
        except ValueError:
            self.result_label.config(text=self.texts["error_invalid_input"])
    
    def update_result_display(self):
        if self.last_result_bps == 0:
            return
            
        # 根据选择的单位转换结果
        result_unit = self.result_unit.get()
        if result_unit == "bps":
            result_value = self.last_result_bps
            unit_text = "bps"
        elif result_unit == "kbps":
            result_value = self.last_result_bps / 1000
            unit_text = "kbps"
        elif result_unit == "Mbps":
            result_value = self.last_result_bps / 1000000
            unit_text = "Mbps"
        elif result_unit == "Gbps":
            result_value = self.last_result_bps / 1000000000
            unit_text = "Gbps"
        
        # 格式化显示结果
        if result_value < 0.01:
            formatted_result = f"{result_value:.6f}"
        elif result_value < 0.1:
            formatted_result = f"{result_value:.4f}"
        elif result_value < 10:
            formatted_result = f"{result_value:.2f}"
        else:
            formatted_result = f"{result_value:.1f}"
            
        self.result_label.config(text=f"{formatted_result} {unit_text}", font=("Arial", 10, "bold"), fg="red")

    def update_calculation_basis(self, bandwidth_value, bandwidth_unit, rtt_ms, threads, 
                                tcp_window_size, throughput_bps, bandwidth_bps,
                                window_size_kb, mss_bytes, packet_loss_percent, jitter_ms, congestion_algorithm):
        """更新计算依据说明"""
        # 格式化带宽值显示
        if bandwidth_unit == "kbps":
            bandwidth_str = f"{bandwidth_value} kbps ({bandwidth_bps} bps)"
        elif bandwidth_unit == "Mbps":
            bandwidth_str = f"{bandwidth_value} Mbps ({bandwidth_bps} bps)"
        elif bandwidth_unit == "Gbps":
            bandwidth_str = f"{bandwidth_value} Gbps ({bandwidth_bps} bps)"
        
        # 计算窗口大小（比特）
        window_size_bits = tcp_window_size * 8
        
        # 计算有效RTT（秒）
        effective_rtt_ms = rtt_ms + jitter_ms
        effective_rtt_s = effective_rtt_ms / 1000
        
        # 计算基础理论值（不考虑带宽和丢包限制）
        base_theoretical_bps = window_size_bits / effective_rtt_s * threads
        
        # 准备计算依据说明文本
        basis_text = self.texts["calculation_basis"] + "\n"
        basis_text += self.texts["basic_params_basis"].format(bandwidth_str, rtt_ms, threads) + "\n"
        basis_text += self.texts["advanced_params_basis"].format(window_size_kb, mss_bytes, packet_loss_percent, jitter_ms, congestion_algorithm) + "\n"
        
        # 添加有效RTT说明（如果有抖动）
        if jitter_ms > 0:
            basis_text += self.texts["effective_rtt"].format(rtt_ms, jitter_ms, effective_rtt_ms) + "\n"
            next_point = 4
        else:
            next_point = 3
        
        # 添加基础理论计算
        basis_text += self.texts["basic_theory"].format(next_point, window_size_bits, effective_rtt_s, threads, base_theoretical_bps) + "\n"
        next_point += 1
        
        # 如果有丢包，添加丢包影响说明
        if packet_loss_percent > 0:
            if congestion_algorithm == "Reno":
                basis_text += self.texts["packet_loss_impact_reno"].format(next_point, packet_loss_percent) + "\n"
            elif congestion_algorithm == "CUBIC":
                basis_text += self.texts["packet_loss_impact_cubic"].format(next_point, packet_loss_percent) + "\n"
            elif congestion_algorithm == "BBR":
                basis_text += self.texts["packet_loss_impact_bbr"].format(next_point, packet_loss_percent) + "\n"
            elif congestion_algorithm == "Westwood":
                basis_text += self.texts["packet_loss_impact_westwood"].format(next_point, packet_loss_percent) + "\n"
            next_point += 1
        
        # 如果受带宽限制，添加说明
        if throughput_bps < base_theoretical_bps:
            basis_text += self.texts["bandwidth_limit"].format(next_point, bandwidth_bps) + "\n"
        
        # 更新标签文本
        self.calculation_basis_label.config(text=basis_text)
    
    def center_window(self):
        """将窗口居中显示在屏幕上"""
        # 更新窗口信息，确保获取正确的窗口尺寸
        self.root.update_idletasks()
        
        # 获取屏幕宽度和高度
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # 获取窗口宽度和高度
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        
        # 计算居中位置的x和y坐标
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # 设置窗口位置
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def show_about(self):
        """显示关于对话框"""
        about_text = self.texts["about_text"].format(
            self.VERSION, self.LICENSE, self.AUTHOR, self.AUTHOR_EMAIL
        )
        
        messagebox.showinfo(self.texts["about_title"], about_text)
        
    def set_language(self, lang):
        if self.current_language != lang:
            self.current_language = lang
            self.texts = text_resources[self.current_language]
            self.root.title(self.texts["window_title"])
            for widget in self.root.winfo_children():
                widget.destroy()
            self.create_widgets()
            self.create_menu()
            if hasattr(self, 'last_result_bps') and self.last_result_bps > 0:
                self.update_result_display()
    
    def create_tooltip(self, widget, text):
        """为控件创建悬停提示"""
        def enter(event):
            # 创建提示窗口
            x, y, _, _ = widget.bbox("insert")
            x += widget.winfo_rootx() + 25
            y += widget.winfo_rooty() + 25
            
            # 创建一个顶层窗口
            self.tooltip = tk.Toplevel(widget)
            self.tooltip.wm_overrideredirect(True)  # 无边框窗口
            self.tooltip.wm_geometry(f"+{x}+{y}")
            
            # 创建提示标签
            label = ttk.Label(self.tooltip, text=text, justify="left",
                             background="#ffffe0", relief="solid", borderwidth=1,
                             font=("Arial", "9", "normal"), padding=(5, 2))
            label.pack()
        
        def leave(event):
            # 销毁提示窗口
            if hasattr(self, "tooltip"):
                self.tooltip.destroy()
        
        # 绑定鼠标进入和离开事件
        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)

    def validate_input(self, entry_widget, min_value, max_value, param_name, is_int=False):
        """验证输入值是否在指定范围内"""
        try:
            value = entry_widget.get().strip()
            if not value:  # 如果为空，不处理
                return
                 
            if is_int:
                value = int(value)
            else:
                value = float(value)
                 
            if value < min_value:
                messagebox.showwarning(self.texts["input_out_of_range"], self.texts["param_not_less_than"].format(param_name, min_value))
                entry_widget.delete(0, tk.END)
                entry_widget.insert(0, str(min_value))
            elif value > max_value:
                messagebox.showwarning(self.texts["input_out_of_range"], self.texts["param_not_greater_than"].format(param_name, max_value))
                entry_widget.delete(0, tk.END)
                entry_widget.insert(0, str(max_value))
        except ValueError:
            messagebox.showerror(self.texts["input_error"], self.texts["param_must_be_valid"].format(param_name))
            entry_widget.delete(0, tk.END)
            if is_int:
                entry_widget.insert(0, str(int(min_value)))
            else:
                entry_widget.insert(0, str(min_value))

if __name__ == "__main__":
    root = tk.Tk()
    app = TCPThroughputCalculator(root)
    root.mainloop()