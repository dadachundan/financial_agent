"""is_chinese_filename: the downloader's pre-download skip rule for Chinese content."""
import pytest

from zsxq_common import is_chinese_filename


@pytest.mark.parametrize("name", [
    "中文版-瑞银—宁德时代（300750）2026年第一季度业绩：交付加速驱动稳健超预期-译文.pdf",
    "CHS_斯坦福2026年人工智能指数AIIndex报告英文版423页.pdf",
    "富创精密(688409)公司深度报告：国内半导体零部件领军企业，平台化布局释放长期价值.pdf",
    "存储行业报告：AI推理需求重塑存储范式，国产存储迎产业升级期-国信证券.pdf",
])
def test_chinese_content(name):
    assert is_chinese_filename(name)


@pytest.mark.parametrize("name", [
    "Nomura-Zhongji InnoLight （300308）We expect secular growth beyond 2027...-260706.pdf",
    "QS2027世界未来技能指数报告英文版64页.pdf",
    "AI驱动下的电力重构：美国数据中心能源需求新图景（英文）.pdf",
    "附件：ISRG-财报-251022.pdf",
    "高盛—贵州茅台—市场化计划第四号：非标准SKU建议零售价基于供需关系上调；买入.pdf",
    "MS-Meta的Muse生态与能力持续扩张.pdf",
    "JPM-应流股份（603308.SH）：全球燃气轮机与航空发动机瓶颈赛道的稀缺中国标的.pdf",
])
def test_english_content(name):
    assert not is_chinese_filename(name)
