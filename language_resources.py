#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
语言资源文件 - 提供中英文界面文本
版本: 1.0.0
作者: 曹宇
许可证: MIT License
"""

# 语言资源字典
text_resources = {
    "zh_CN": {
        # 窗口标题
        "window_title": "TCP协议最大传输速率计算器",
        
        # 基本参数
        "basic_params": "基本参数",
        "bandwidth": "线路带宽:",
        "bandwidth_tooltip": "线路带宽决定理论最大速率上限，适用于评估链路瓶颈或高带宽专线环境\n建议范围: 0.1-10000",
        "rtt": "往返延时 (ms):",
        "rtt_tooltip": "往返延时（RTT）越大，窗口受限下吞吐量越低，卫星链路/跨洲通信时尤为明显\n建议范围: 1-1000ms",
        "threads": "传输线程数量:",
        "threads_tooltip": "多线程适用于高延迟/高带宽场景，能突破单连接窗口限制\n建议范围: 1-128",
        
        # 高级参数
        "advanced_params": "高级参数",
        "window_size": "TCP窗口大小 (KB):",
        "window_size_tooltip": "窗口越大，长距离/高带宽链路下吞吐量越高，适合大文件传输\n建议范围: 8-16384KB",
        "window_size_default": "默认: 64KB",
        "mss": "MSS (字节):",
        "mss_tooltip": "最大段大小（Maximum Segment Size）越大，协议开销越低，适合局域网/高质量链路，公网/隧道环境建议适当减小\n建议范围: 536-9000字节",
        "mss_default": "默认: 1460字节",
        "packet_loss": "丢包率 (%):",
        "packet_loss_tooltip": "丢包率高时TCP拥塞窗口收缩，适用于公网/无线/跨国链路\n建议范围: 0-30%",
        "packet_loss_default": "默认: 0%",
        "jitter": "网络抖动 (ms):",
        "jitter_tooltip": "抖动大时RTT波动，适用于无线/移动/跨国链路\n建议范围: 0-200ms",
        "jitter_default": "默认: 0ms",
        "congestion": "拥塞控制算法:",
        "congestion_tooltip": "不同算法适合不同网络环境，Reno适合低丢包，BBR适合高带宽高延迟",
        "congestion_default": "默认: Reno",
        
        # 计算结果
        "result_frame": "计算结果",
        "throughput": "TCP理论最大速率:",
        "display_unit": "显示单位:",
        
        # 菜单栏
        "menu_language": "语言",
        
        # 按钮
        "calculate_button": "计算",
        "about_button": "关于",
        "language_button": "English",
        
        # 计算公式说明
        "formula_frame": "计算公式说明",
        "formula_text": "基础公式: TCP理论最大速率 = 窗口大小 / RTT * 线程数\n\n考虑丢包率的Mathis模型: BW = (MSS/RTT) * (C/sqrt(p))\n其中，C是与拥塞控制算法相关的常数，p是丢包率\n\n影响TCP吞吐量的因素及参数取值范围:\n- 线路带宽: 建议范围 0.1-10000，取决于实际网络环境\n- 往返延时（RTT）: 建议范围 1-1000ms，跨洲/卫星通信需关注\n- 传输线程数: 建议范围 1-128，多线程适用于高延迟/高带宽场景\n- 窗口大小: 建议范围 8-16384KB，长距离/高带宽链路建议加大\n- 最大段大小（MSS）: 建议范围 536-9000字节，局域网可调大，公网建议适中\n- 丢包率: 建议范围 0-30%，公网/无线链路需关注\n- 网络抖动: 建议范围 0-200ms，移动/无线/跨国链路需关注\n- 拥塞控制算法: 选择适合场景的算法，Reno适合低丢包，BBR适合高带宽高延迟",
        
        # 计算依据说明
        "calculation_basis": "计算依据说明:",
        "basic_params_basis": "1. 基本参数: 带宽={0}, RTT={1}ms, 线程数={2}",
        "advanced_params_basis": "2. 高级参数: 窗口大小={0}KB, MSS={1}字节, 丢包率={2}%, 网络抖动={3}ms, 拥塞控制={4}",
        "effective_rtt": "3. 有效RTT: {0}ms + {1}ms(抖动) = {2}ms",
        "basic_theory": "{0}. 基础理论计算: {1} 比特 ÷ {2} 秒 × {3} 线程 = {4:.2f} bps",
        "packet_loss_impact_reno": "{0}. 丢包影响: 使用Mathis模型计算Reno算法在{1}%丢包率下的吞吐量",
        "packet_loss_impact_cubic": "{0}. 丢包影响: 使用修正Mathis模型计算CUBIC算法在{1}%丢包率下的吞吐量",
        "packet_loss_impact_bbr": "{0}. 丢包影响: BBR算法对丢包率{1}%的适应性较好",
        "packet_loss_impact_westwood": "{0}. 丢包影响: 使用修正Mathis模型计算Westwood算法在{1}%丢包率下的吞吐量",
        "bandwidth_limit": "{0}. 受带宽限制: 结果被限制为 {1} bps",
        
        # 错误消息
        "error_bandwidth_positive": "带宽必须为正数",
        "error_bandwidth_too_large": "带宽值过大，请检查输入",
        "error_rtt_positive": "RTT必须为正数",
        "error_rtt_too_large": "RTT值过大(>1000ms)，请确认是否正确",
        "error_threads_positive": "线程数必须为正整数",
        "error_threads_too_large": "线程数过大(>128)，可能不切实际",
        "error_window_size_positive": "窗口大小必须为正数",
        "error_window_size_too_large": "窗口大小过大(>16384KB)，请确认是否正确",
        "error_mss_positive": "MSS必须为正数",
        "error_mss_too_small": "MSS过小(<536字节)，可能影响性能",
        "error_mss_too_large": "MSS过大(>9000字节)，超出常规范围",
        "error_packet_loss_range": "丢包率必须在0-100%之间",
        "error_packet_loss_too_large": "丢包率过高(>30%)，TCP传输可能不可用",
        "error_jitter_negative": "网络抖动不能为负数",
        "error_jitter_too_large": "网络抖动过大(>200ms)，请确认是否正确",
        "error_invalid_input": "请输入有效的数值",
        
        # 输入验证消息
        "input_out_of_range": "输入超出范围",
        "param_not_less_than": "{0}不应小于{1}",
        "param_not_greater_than": "{0}不应大于{1}",
        "input_error": "输入错误",
        "param_must_be_valid": "{0}必须是有效的数值",
        
        # 关于对话框
        "about_title": "关于",
        "about_text": "TCP协议最大传输速率计算器\n\n版本: {0}\n许可证: {1}\n作者: {2}\n邮箱：{3}\n\n本软件是一个开源工具，用于计算TCP协议在不同网络环境下的理论最大传输速率。\n它考虑了多种影响因素，包括带宽、延迟、丢包率、窗口大小等参数。\n\n项目地址: https://github.com/yourusername/tcpThroughput"
    },
    
    "en_US": {
        # Window title
        "window_title": "TCP Throughput Calculator",
        
        # Basic parameters
        "basic_params": "Basic Parameters",
        "bandwidth": "Bandwidth:",
        "bandwidth_tooltip": "Bandwidth determines the theoretical maximum throughput. Suitable for evaluating link bottlenecks or high-bandwidth dedicated lines.\nRecommended: 0.1-10000",
        "rtt": "RTT (ms):",
        "rtt_tooltip": "Round Trip Time (RTT) affects throughput under window limitation. Especially important for satellite/intercontinental links.\nRecommended: 1-1000ms",
        "threads": "Threads:",
        "threads_tooltip": "Multiple threads help break single connection window limits in high-latency/high-bandwidth scenarios.\nRecommended: 1-128",
        
        # Advanced parameters
        "advanced_params": "Advanced Parameters",
        "window_size": "TCP Window Size (KB):",
        "window_size_tooltip": "Larger window increases throughput for long-distance/high-bandwidth links.\nRecommended: 8-16384KB",
        "window_size_default": "Default: 64KB",
        "mss": "MSS (bytes):",
        "mss_tooltip": "Maximum Segment Size. Larger MSS reduces protocol overhead.\nRecommended: 536-9000 bytes",
        "mss_default": "Default: 1460 bytes",
        "packet_loss": "Packet Loss (%):",
        "packet_loss_tooltip": "High loss shrinks TCP congestion window.\nRecommended: 0-30%",
        "packet_loss_default": "Default: 0%",
        "jitter": "Jitter (ms):",
        "jitter_tooltip": "Jitter causes RTT fluctuation.\nRecommended: 0-200ms",
        "jitter_default": "Default: 0ms",
        "congestion": "Congestion Control:",
        "congestion_tooltip": "Different algorithms suit different networks. Reno for low loss, BBR for high bandwidth-delay.",
        "congestion_default": "Default: Reno",
        
        # Result
        "result_frame": "Result",
        "throughput": "TCP Theoretical Max Throughput:",
        "display_unit": "Display Unit:",
        
        # 菜单栏
        "menu_language": "Language",
        
        # Buttons
        "calculate_button": "Calculate",
        "about_button": "About",
        "language_button": "中文",
        
        # 计算公式说明
        "formula_frame": "Formula Explanation",
        "formula_text": "Basic Formula: TCP Maximum Throughput = Window Size / RTT * Number of Threads\n\nMathis Model with Packet Loss: BW = (MSS/RTT) * (C/sqrt(p))\nWhere C is a constant related to the congestion control algorithm, and p is the packet loss rate\n\nFactors affecting TCP throughput and parameter ranges:\n- Bandwidth: Recommended range 0.1-10000, depends on actual network environment\n- RTT: Recommended range 1-1000ms, critical for intercontinental/satellite communications\n- Number of Threads: Recommended range 1-128, multiple threads suitable for high-latency/high-bandwidth scenarios\n- Window Size: Recommended range 8-16384KB, increase for long-distance/high-bandwidth links\n- MSS: Recommended range 536-9000 bytes, larger for LANs, moderate for public networks\n- Packet Loss: Recommended range 0-30%, critical for public/wireless links\n- Network Jitter: Recommended range 0-200ms, critical for mobile/wireless/international links\n- Congestion Control Algorithm: Choose algorithm suitable for scenario, Reno for low packet loss, BBR for high-bandwidth high-latency",
        
        # 计算依据说明
        "calculation_basis": "Calculation Basis:",
        "basic_params_basis": "1. Basic Parameters: Bandwidth={0}, RTT={1}ms, Threads={2}",
        "advanced_params_basis": "2. Advanced Parameters: Window Size={0}KB, MSS={1}bytes, Packet Loss={2}%, Jitter={3}ms, Congestion Control={4}",
        "effective_rtt": "3. Effective RTT: {0}ms + {1}ms(jitter) = {2}ms",
        "basic_theory": "{0}. Basic Theoretical Calculation: {1} bits ÷ {2} seconds × {3} threads = {4:.2f} bps",
        "packet_loss_impact_reno": "{0}. Packet Loss Impact: Using Mathis model to calculate Reno algorithm throughput with {1}% packet loss",
        "packet_loss_impact_cubic": "{0}. Packet Loss Impact: Using modified Mathis model to calculate CUBIC algorithm throughput with {1}% packet loss",
        "packet_loss_impact_bbr": "{0}. Packet Loss Impact: BBR algorithm has good adaptability to {1}% packet loss",
        "packet_loss_impact_westwood": "{0}. Packet Loss Impact: Using modified Mathis model to calculate Westwood algorithm throughput with {1}% packet loss",
        "bandwidth_limit": "{0}. Bandwidth Limited: Result is limited to {1} bps",
        
        # 错误消息
        "error_bandwidth_positive": "Bandwidth must be positive",
        "error_bandwidth_too_large": "Bandwidth value too large, please check input",
        "error_rtt_positive": "RTT must be positive",
        "error_rtt_too_large": "RTT value too large (>1000ms), please confirm",
        "error_threads_positive": "Number of threads must be a positive integer",
        "error_threads_too_large": "Number of threads too large (>128), may be unrealistic",
        "error_window_size_positive": "Window size must be positive",
        "error_window_size_too_large": "Window size too large (>16384KB), please confirm",
        "error_mss_positive": "MSS must be positive",
        "error_mss_too_small": "MSS too small (<536 bytes), may affect performance",
        "error_mss_too_large": "MSS too large (>9000 bytes), exceeds normal range",
        "error_packet_loss_range": "Packet loss must be between 0-100%",
        "error_packet_loss_too_large": "Packet loss too high (>30%), TCP transmission may be unavailable",
        "error_jitter_negative": "Network jitter cannot be negative",
        "error_jitter_too_large": "Network jitter too large (>200ms), please confirm",
        "error_invalid_input": "Please enter valid values",
        
        # 输入验证消息
        "input_out_of_range": "Input Out of Range",
        "param_not_less_than": "{0} should not be less than {1}",
        "param_not_greater_than": "{0} should not be greater than {1}",
        "input_error": "Input Error",
        "param_must_be_valid": "{0} must be a valid number",
        
        # 关于对话框
        "about_title": "About",
        "about_text": "TCP Maximum Throughput Calculator\n\nVersion: {0}\nLicense: {1}\nAuthor: {2}\nEmail: {3}\n\nThis software is an open-source tool for calculating the theoretical maximum transmission rate of TCP protocol in different network environments.\nIt considers various factors including bandwidth, latency, packet loss rate, window size, and other parameters.\n\nProject URL: https://github.com/yourusername/tcpThroughput"
    }
}