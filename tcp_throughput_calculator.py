import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import math
import re

class TCPThroughputCalculator:
    # 程序版本和信息
    VERSION = "1.0.0"
    LICENSE = "MIT License"
    AUTHOR = "曹宇"
    AUTHOR_EMAIL = "sankingcao@gmail.com"

    
    def __init__(self, root):
        self.root = root
        self.root.title("TCP协议最大传输速率计算器")
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

        input_frame = ttk.LabelFrame(left_frame, text="基本参数", padding="10 10 10 10")
        input_frame.pack(fill=tk.X, expand=False, padx=0, pady=(0, 10))
        # 带宽输入
        bandwidth_label = ttk.Label(input_frame, text="线路带宽:")
        bandwidth_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.create_tooltip(bandwidth_label, "线路带宽决定理论最大速率上限，适用于评估链路瓶颈或高带宽专线环境\n建议范围: 0.1-10000")
        self.bandwidth_entry = ttk.Entry(input_frame, width=12)
        self.bandwidth_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        self.bandwidth_entry.insert(0, "100")
        # 添加输入验证
        self.bandwidth_entry.bind("<FocusOut>", lambda e: self.validate_input(self.bandwidth_entry, 0.1, 10000, "带宽"))
        self.bandwidth_unit = tk.StringVar(value="Mbps")
        bandwidth_unit_combo = ttk.Combobox(input_frame, textvariable=self.bandwidth_unit, values=["kbps", "Mbps", "Gbps"], width=8, state="readonly")
        bandwidth_unit_combo.grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        # RTT输入
        rtt_label = ttk.Label(input_frame, text="往返延时 (ms):")
        rtt_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.create_tooltip(rtt_label, "RTT越大，窗口受限下吞吐量越低，卫星链路/跨洲通信时尤为明显\n建议范围: 1-1000ms")
        self.rtt_entry = ttk.Entry(input_frame, width=12)
        self.rtt_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        self.rtt_entry.insert(0, "50")
        # 添加输入验证
        self.rtt_entry.bind("<FocusOut>", lambda e: self.validate_input(self.rtt_entry, 1, 1000, "RTT"))
        # 线程数输入
        threads_label = ttk.Label(input_frame, text="传输线程数量:")
        threads_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.create_tooltip(threads_label, "多线程适用于高延迟/高带宽场景，能突破单连接窗口限制\n建议范围: 1-128")
        self.threads_entry = ttk.Entry(input_frame, width=12)
        self.threads_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        self.threads_entry.insert(0, "1")
        # 添加输入验证
        self.threads_entry.bind("<FocusOut>", lambda e: self.validate_input(self.threads_entry, 1, 128, "线程数", True))

        advanced_frame = ttk.LabelFrame(left_frame, text="高级参数", padding="10 10 10 10")
        advanced_frame.pack(fill=tk.X, expand=False, padx=0, pady=(0, 10))
        window_size_label = ttk.Label(advanced_frame, text="TCP窗口大小 (KB):")
        window_size_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.create_tooltip(window_size_label, "窗口越大，长距离/高带宽链路下吞吐量越高，适合大文件传输\n建议范围: 8-16384KB")
        self.window_size_entry = ttk.Entry(advanced_frame, width=12)
        self.window_size_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        self.window_size_entry.insert(0, "64")
        # 添加输入验证
        self.window_size_entry.bind("<FocusOut>", lambda e: self.validate_input(self.window_size_entry, 8, 16384, "窗口大小"))
        ttk.Label(advanced_frame, text="默认: 64KB").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        mss_label = ttk.Label(advanced_frame, text="MSS (字节):")
        mss_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.create_tooltip(mss_label, "MSS越大，协议开销越低，适合局域网/高质量链路，公网/隧道环境建议适当减小\n建议范围: 536-9000字节")
        self.mss_entry = ttk.Entry(advanced_frame, width=12)
        self.mss_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        self.mss_entry.insert(0, "1460")
        # 添加输入验证
        self.mss_entry.bind("<FocusOut>", lambda e: self.validate_input(self.mss_entry, 536, 9000, "MSS"))
        ttk.Label(advanced_frame, text="默认: 1460字节").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        packet_loss_label = ttk.Label(advanced_frame, text="丢包率 (%):")
        packet_loss_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.create_tooltip(packet_loss_label, "丢包率高时TCP拥塞窗口收缩，适用于公网/无线/跨国链路\n建议范围: 0-30%")
        self.packet_loss_entry = ttk.Entry(advanced_frame, width=12)
        self.packet_loss_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        self.packet_loss_entry.insert(0, "0")
        # 添加输入验证
        self.packet_loss_entry.bind("<FocusOut>", lambda e: self.validate_input(self.packet_loss_entry, 0, 30, "丢包率"))
        ttk.Label(advanced_frame, text="默认: 0%").grid(row=2, column=2, sticky=tk.W, padx=5, pady=5)
        jitter_label = ttk.Label(advanced_frame, text="网络抖动 (ms):")
        jitter_label.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.create_tooltip(jitter_label, "抖动大时RTT波动，适用于无线/移动/跨国链路\n建议范围: 0-200ms")
        self.jitter_entry = ttk.Entry(advanced_frame, width=12)
        self.jitter_entry.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        self.jitter_entry.insert(0, "0")
        # 添加输入验证
        self.jitter_entry.bind("<FocusOut>", lambda e: self.validate_input(self.jitter_entry, 0, 200, "网络抖动"))
        ttk.Label(advanced_frame, text="默认: 0ms").grid(row=3, column=2, sticky=tk.W, padx=5, pady=5)
        congestion_label = ttk.Label(advanced_frame, text="拥塞控制算法:")
        congestion_label.grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.create_tooltip(congestion_label, "不同算法适合不同网络环境，Reno适合低丢包，BBR适合高带宽高延迟")
        self.congestion_algorithm = tk.StringVar(value="Reno")
        congestion_combo = ttk.Combobox(advanced_frame, textvariable=self.congestion_algorithm, values=["Reno", "CUBIC", "BBR", "Westwood"], width=12, state="readonly")
        congestion_combo.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Label(advanced_frame, text="默认: Reno").grid(row=4, column=2, sticky=tk.W, padx=5, pady=5)

        # 右侧结果区
        right_frame = ttk.Frame(top_frame)
        right_frame.grid(row=0, column=1, sticky="nsew")
        right_frame.columnconfigure(0, weight=1)

        # 创建一个容器框架来包含结果框架和计算按钮
        result_container = ttk.Frame(right_frame)
        result_container.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        result_frame = ttk.LabelFrame(result_container, text="计算结果", padding="10 10 10 10")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=(0, 5))
        ttk.Label(result_frame, text="TCP理论最大速率:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.result_label = tk.Label(result_frame, text="--", font=("Arial", 10, "bold"), fg="red")
        self.result_label.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Label(result_frame, text="显示单位:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
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
        calculate_button = ttk.Button(button_container, text="计算", command=self.calculate_throughput)
        calculate_button.grid(row=0, column=0, padx=5, sticky="e")
        
        # 关于按钮
        about_button = ttk.Button(button_container, text="关于", command=self.show_about)
        about_button.grid(row=0, column=1, padx=5, sticky="w")

        # 下半部分的计算公式说明
        formula_frame = ttk.LabelFrame(main_frame, text="计算公式说明", padding="10 10 10 10")
        formula_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(10, 0))
        formula_text = "基础公式: TCP理论最大速率 = 窗口大小 / RTT * 线程数\n\n"
        formula_text += "考虑丢包率的Mathis模型: BW = (MSS/RTT) * (C/sqrt(p))\n"
        formula_text += "其中，C是与拥塞控制算法相关的常数，p是丢包率\n\n"
        formula_text += "影响TCP吞吐量的因素及参数取值范围:\n"
        formula_text += "- 线路带宽: 建议范围 0.1-10000，取决于实际网络环境\n"
        formula_text += "- RTT: 建议范围 1-1000ms，跨洲/卫星通信需关注\n"
        formula_text += "- 传输线程数: 建议范围 1-128，多线程适用于高延迟/高带宽场景\n"
        formula_text += "- 窗口大小: 建议范围 8-16384KB，长距离/高带宽链路建议加大\n"
        formula_text += "- MSS: 建议范围 536-9000字节，局域网可调大，公网建议适中\n"
        formula_text += "- 丢包率: 建议范围 0-30%，公网/无线链路需关注\n"
        formula_text += "- 网络抖动: 建议范围 0-200ms，移动/无线/跨国链路需关注\n"
        formula_text += "- 拥塞控制算法: 选择适合场景的算法，Reno适合低丢包，BBR适合高带宽高延迟"
        formula_label = ttk.Label(formula_frame, text=formula_text, wraplength=700, justify="left")
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
                error_msg = "带宽必须为正数"
            elif bandwidth_value > 10000 and self.bandwidth_unit.get() == "Gbps":
                error_msg = "带宽值过大，请检查输入"
            elif rtt_ms <= 0:
                error_msg = "RTT必须为正数"
            elif rtt_ms > 1000:
                error_msg = "RTT值过大(>1000ms)，请确认是否正确"
            elif threads <= 0:
                error_msg = "线程数必须为正整数"
            elif threads > 128:
                error_msg = "线程数过大(>128)，可能不切实际"
            
            # 验证高级参数范围
            elif window_size_kb <= 0:
                error_msg = "窗口大小必须为正数"
            elif window_size_kb > 16384:
                error_msg = "窗口大小过大(>16384KB)，请确认是否正确"
            elif mss_bytes <= 0:
                error_msg = "MSS必须为正数"
            elif mss_bytes < 536:
                error_msg = "MSS过小(<536字节)，可能影响性能"
            elif mss_bytes > 9000:
                error_msg = "MSS过大(>9000字节)，超出常规范围"
            elif packet_loss_percent < 0 or packet_loss_percent > 100:
                error_msg = "丢包率必须在0-100%之间"
            elif packet_loss_percent > 30:
                error_msg = "丢包率过高(>30%)，TCP传输可能不可用"
            elif jitter_ms < 0:
                error_msg = "网络抖动不能为负数"
            elif jitter_ms > 200:
                error_msg = "网络抖动过大(>200ms)，请确认是否正确"
                
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
            self.result_label.config(text="请输入有效的数值")
    
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
        basis_text = "计算依据说明:\n"
        basis_text += f"1. 基本参数: 带宽={bandwidth_str}, RTT={rtt_ms}ms, 线程数={threads}\n"
        basis_text += f"2. 高级参数: 窗口大小={window_size_kb}KB, MSS={mss_bytes}字节, "
        basis_text += f"丢包率={packet_loss_percent}%, 网络抖动={jitter_ms}ms, 拥塞控制={congestion_algorithm}\n"
        
        # 添加有效RTT说明（如果有抖动）
        if jitter_ms > 0:
            basis_text += f"3. 有效RTT: {rtt_ms}ms + {jitter_ms}ms(抖动) = {effective_rtt_ms}ms\n"
            next_point = 4
        else:
            next_point = 3
        
        # 添加基础理论计算
        basis_text += f"{next_point}. 基础理论计算: {window_size_bits} 比特 ÷ {effective_rtt_s} 秒 × {threads} 线程 = {base_theoretical_bps:.2f} bps\n"
        next_point += 1
        
        # 如果有丢包，添加丢包影响说明
        if packet_loss_percent > 0:
            if congestion_algorithm == "Reno":
                basis_text += f"{next_point}. 丢包影响: 使用Mathis模型计算Reno算法在{packet_loss_percent}%丢包率下的吞吐量\n"
            elif congestion_algorithm == "CUBIC":
                basis_text += f"{next_point}. 丢包影响: 使用修正Mathis模型计算CUBIC算法在{packet_loss_percent}%丢包率下的吞吐量\n"
            elif congestion_algorithm == "BBR":
                basis_text += f"{next_point}. 丢包影响: BBR算法对丢包率{packet_loss_percent}%的适应性较好\n"
            elif congestion_algorithm == "Westwood":
                basis_text += f"{next_point}. 丢包影响: 使用修正Mathis模型计算Westwood算法在{packet_loss_percent}%丢包率下的吞吐量\n"
            next_point += 1
        
        # 如果受带宽限制，添加说明
        if throughput_bps < base_theoretical_bps:
            basis_text += f"{next_point}. 受带宽限制: 结果被限制为 {bandwidth_bps} bps\n"
        
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
        about_text = f"TCP协议最大传输速率计算器\n\n"
        about_text += f"版本: {self.VERSION}\n"
        about_text += f"许可证: {self.LICENSE}\n"
        about_text += f"作者: {self.AUTHOR}\n"
        about_text += f"邮箱：{self.AUTHOR_EMAIL}\n\n"
        about_text += "本软件是一个开源工具，用于计算TCP协议在不同网络环境下的理论最大传输速率。\n"
        about_text += "它考虑了多种影响因素，包括带宽、延迟、丢包率、窗口大小等参数。\n\n"
        about_text += "项目地址: https://github.com/yourusername/tcpThroughput"
        
        messagebox.showinfo("关于", about_text)
    
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
                messagebox.showwarning("输入超出范围", f"{param_name}不应小于{min_value}")
                entry_widget.delete(0, tk.END)
                entry_widget.insert(0, str(min_value))
            elif value > max_value:
                messagebox.showwarning("输入超出范围", f"{param_name}不应大于{max_value}")
                entry_widget.delete(0, tk.END)
                entry_widget.insert(0, str(max_value))
        except ValueError:
            messagebox.showerror("输入错误", f"{param_name}必须是有效的数值")
            entry_widget.delete(0, tk.END)
            if is_int:
                entry_widget.insert(0, str(int(min_value)))
            else:
                entry_widget.insert(0, str(min_value))

if __name__ == "__main__":
    root = tk.Tk()
    app = TCPThroughputCalculator(root)
    root.mainloop()