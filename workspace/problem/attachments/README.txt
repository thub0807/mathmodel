以下数据集中描述的电解质涵盖了多种锂盐和钠盐在水中的测量数据，浓度直至其溶解度极限，包括硫酸盐、硝酸盐、高氯酸盐和溴化物。数据集包含 251 条记录组成的列表，包含以下信息：

GUID：每个实验的唯一标识符
conductivity：电解质的电导率
temperature：测量电导率时的温度
RUN_ID：实验标识符
RUN_TYPE：用以表示测试运行与生产运行
timestamp：时间戳
pH：15 秒内测得的平均 pH 值
electrolyte：指定电解质组成的字典，包含以下信息：
	a. volumes：构成电解质的每种母液体积（mL）
	b. source molalities：每种母液的质量摩尔浓度
	c. source densities：每种母液密度（g/mL）
electrochemistry：提供电解质在铂电极上的电化学测试数据，包含以下信息：
	a. i：电流密度数组
	b. V：电压数组（相对于标准氢电极）
	c. t：时间数组（从测试开始计时）
	d. test_name：电化学测试方法
	e. derived_quantities：从上述数组推导得出的量