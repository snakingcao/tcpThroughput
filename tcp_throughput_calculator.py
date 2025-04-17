import tkinter as tk
from tkinter import ttk
import math

class TCPThroughputCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("TCP协议最大传输速率计算器")
        self.root.geometry("600x600")
        self.root.resizable(True, True)
        
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
        main_frame = ttk.Frame(self.root, padding="20 20 20 20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 输入参数区域
        input_frame = ttk.LabelFrame(main_frame, text="输入参数", padding="10 10 10 10")
        input_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 带宽输入
        ttk.Label(input_frame, text="线路带宽:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.bandwidth_entry = ttk.Entry(input_frame, width=15)
        self.bandwidth_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        self.bandwidth_entry.insert(0, "100")
        
        # 带宽单位选择
        self.bandwidth_unit = tk.StringVar(value="Mbps")
        bandwidth_unit_combo = ttk.Combobox(input_frame, textvariable=self.bandwidth_unit, 
                                          values=["kbps", "Mbps", "Gbps"], width=10, state="readonly")
        bandwidth_unit_combo.grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        
        # RTT输入
        ttk.Label(input_frame, text="往返延时 (ms):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.rtt_entry = ttk.Entry(input_frame, width=15)
        self.rtt_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        self.rtt_entry.insert(0, "50")
        
        # 线程数输入
        ttk.Label(input_frame, text="传输线程数量:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.threads_entry = ttk.Entry(input_frame, width=15)
        self.threads_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        self.threads_entry.insert(0, "1")
        
        # 计算按钮
        calculate_button = ttk.Button(input_frame, text="计算", command=self.calculate_throughput)
        calculate_button.grid(row=3, column=1, sticky=tk.W, padx=5, pady=15)
        
        # 结果区域
        result_frame = ttk.LabelFrame(main_frame, text="计算结果", padding="10 10 10 10")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 结果显示
        ttk.Label(result_frame, text="TCP理论最大速率:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.result_label = tk.Label(result_frame, text="--", font=("Arial", 10, "bold"), fg="red")
        self.result_label.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        # 计算依据说明
        self.calculation_basis_label = ttk.Label(result_frame, text="", wraplength=500, justify="left")
        self.calculation_basis_label.grid(row=2, column=0, columnspan=3, sticky=tk.W, padx=5, pady=5)
        
        # 结果单位选择
        ttk.Label(result_frame, text="显示单位:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.result_unit = tk.StringVar(value="Mbps")
        result_unit_combo = ttk.Combobox(result_frame, textvariable=self.result_unit, 
                                       values=["bps", "kbps", "Mbps", "Gbps"], width=10, state="readonly")
        result_unit_combo.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        result_unit_combo.bind("<<ComboboxSelected>>", lambda e: self.update_result_display())
        
        # 计算公式说明
        formula_frame = ttk.LabelFrame(main_frame, text="计算公式说明", padding="10 10 10 10")
        formula_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        formula_text = "TCP理论最大速率 = 窗口大小 / RTT * 线程数\n"
        formula_text += "窗口大小默认为TCP最大窗口大小 (64KB)\n"
        formula_text += "实际速率可能受多种因素影响，如网络拥塞、丢包率等"
        
        formula_label = ttk.Label(formula_frame, text=formula_text, wraplength=500, justify="left")
        formula_label.pack(fill=tk.BOTH, expand=True)
        
        # 存储最后计算的结果（以bps为单位）
        self.last_result_bps = 0
    
    def calculate_throughput(self):
        try:
            # 获取输入值
            bandwidth_value = float(self.bandwidth_entry.get())
            rtt_ms = float(self.rtt_entry.get())
            threads = int(self.threads_entry.get())
            
            # 验证输入
            if bandwidth_value <= 0 or rtt_ms <= 0 or threads <= 0:
                self.result_label.config(text="请输入有效的正数值")
                return
            
            # 将带宽转换为bps
            bandwidth_unit = self.bandwidth_unit.get()
            if bandwidth_unit == "kbps":
                bandwidth_bps = bandwidth_value * 1000
            elif bandwidth_unit == "Mbps":
                bandwidth_bps = bandwidth_value * 1000000
            elif bandwidth_unit == "Gbps":
                bandwidth_bps = bandwidth_value * 1000000000
            
            # TCP窗口大小（默认最大为64KB）
            tcp_window_size = 64 * 1024  # 字节
            
            # 计算理论最大速率 (bps)
            # 公式: 窗口大小(bits) / RTT(s) * 线程数
            throughput_bps = (tcp_window_size * 8) / (rtt_ms / 1000) * threads
            
            # 考虑带宽限制
            throughput_bps = min(throughput_bps, bandwidth_bps)
            
            # 保存结果
            self.last_result_bps = throughput_bps
            
            # 更新显示
            self.update_result_display()
            
            # 更新计算依据说明
            self.update_calculation_basis(bandwidth_value, bandwidth_unit, rtt_ms, threads, tcp_window_size, throughput_bps, bandwidth_bps)
            
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

    def update_calculation_basis(self, bandwidth_value, bandwidth_unit, rtt_ms, threads, tcp_window_size, throughput_bps, bandwidth_bps):
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
        
        # 计算RTT（秒）
        rtt_s = rtt_ms / 1000
        
        # 计算理论值（不考虑带宽限制）
        theoretical_bps = window_size_bits / rtt_s * threads
        
        # 准备计算依据说明文本
        basis_text = "计算依据说明:\n"
        basis_text += f"1. 输入参数: 带宽={bandwidth_str}, RTT={rtt_ms}ms, 线程数={threads}\n"
        basis_text += f"2. TCP窗口大小: {tcp_window_size} 字节 ({window_size_bits} 比特)\n"
        basis_text += f"3. 理论计算: {window_size_bits} 比特 ÷ {rtt_s} 秒 × {threads} 线程 = {theoretical_bps:.2f} bps\n"
        
        # 如果受带宽限制，添加说明
        if throughput_bps < theoretical_bps:
            basis_text += f"4. 受带宽限制: 结果被限制为 {bandwidth_bps} bps\n"
        
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

if __name__ == "__main__":
    root = tk.Tk()
    app = TCPThroughputCalculator(root)
    root.mainloop()