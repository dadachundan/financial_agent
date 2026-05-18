"""China industrial robot market — top suppliers 2025."""
import matplotlib.pyplot as plt

names = ['Estun', 'Fanuc', 'Inovance', 'ABB', 'Yaskawa', 'KUKA',
         'Siasun', 'Efort', 'Others (domestic)', 'Others (foreign)']
share = [10.5, 10.2, 9.4, 7.0, 6.8, 6.0, 5.5, 4.2, 24.4, 16.0]
colors = ['#C0392B', '#7F8C8D', '#2E5C9E', '#7F8C8D', '#7F8C8D',
          '#7F8C8D', '#2E8B57', '#2E8B57', '#5DADE2', '#BDC3C7']

fig, ax = plt.subplots(figsize=(8, 8))
wedges, texts, autotexts = ax.pie(
    share, labels=names, colors=colors,
    autopct='%1.1f%%', startangle=110,
    pctdistance=0.78,
    textprops={'fontsize': 10},
)
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(9)

ax.set_title('China Industrial Robot Market — Shipment Share, 2025 (illustrative)\n'
             'Estun #1 domestic and #1 overall, per MIR Industry data',
             fontsize=12.5, pad=14)
fig.tight_layout()
plt.savefig('/Users/x/projects/financial_agent/reports/charts/estun_china_robot_share.png',
            dpi=150, bbox_inches='tight')
print('saved')
