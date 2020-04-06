import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import japanize_matplotlib

matplotlib.font_manager._rebuild()
sns.set(font="IPAexGothic")



#%%
# 東京都_新型コロナウイルス陽性患者発表詳細
df_patients = pd.read_csv('130001_tokyo_covid19_patients.csv')
df_patients['公表_年月日'] = pd.to_datetime(df_patients['公表_年月日'], format='%Y-%m-%d')

#%%
# 縦軸に日付、横軸に年代をとった、日別・年代別陽性患者数の集計表を作る
df_tmp = df_patients[['公表_年月日', '患者_年代']]
df_tmp['人数'] = 1
df_tmp2 = df_tmp.pivot(columns='患者_年代', values='人数' )
df_tmp = pd.concat([df_tmp['公表_年月日'], df_tmp2], axis=1).fillna(0)
df_tmp = df_tmp[['公表_年月日', '10歳未満', '10代',  '20代', '30代', '40代', '50代', '60代', '70代', '80代', '90代']]
df_tmp = df_tmp.groupby('公表_年月日').sum()
df_dairy_patients = df_tmp.resample('D').mean().fillna(0)

#%%
# 曜日が日本語(日〜金)の日時ラベルを作る
week = {'Sun': '日', 'Mon': '月', 'Tue': '火', 'Wed': '水', 'Thu': '木', 'Fri': '金', 'Sat': '土'}
date_monthday = list(df_dairy_patients.index.strftime('%m/%d'))
date_week = [week[x] for x in list(df_dairy_patients.index.strftime('%a'))]
date_label = [f'{monthday}({week})' for monthday, week in zip(date_monthday, date_week)]

#%%
# 縦軸に年代、横軸に日付をとった陽性患者数のヒートマップ(日数指定)
d = 30
fig, ax = plt.subplots(figsize=(18, 7))
# plt.tick_params(axis='both', which='major', labelsize=10, labelbottom=True, bottom=False, top = True, labeltop=False)
chart = sns.heatmap(df_dairy_patients[(-d):].T, square=True, annot=True, cbar=False, cmap='Reds', linewidths=.5, xticklabels=date_label[-d:], ax=ax)

# plt.show()
ax.set_title('東京都_新型コロナウイルス陽性患者発表詳細')
_ = chart.set_yticklabels(chart.get_yticklabels(), rotation=0)
plt.savefig('patients.png')