import requests
import pandas as pd
username="heqiucan"
url=f"https://api.github.com/users/{username}/repos"
response=requests.get(url)
if response.status_code != 200:
    print("请求失败:",response.text)
    exit()
repos=response.json()
print(f"成功获取{len(repos)}个仓库")
data=[]
for repo in repos:
    data.append({
        "name":repo["name"],
        "description":repo["description"],
        "stars":repo["stargazers_count"],
        "forks":repo["forks_count"],
        "language":repo["language"],
        })
df=pd.DataFrame(data)
print("\n原始数据(前五行):")
print(df.head())
df_sorted=df.sort_values(by="stars",ascending=False)
print("\nStar数排序后的前五个仓库:")
print(df_sorted.head())
max_stars=df[df["stars"]==df["stars"].max()]
print(max_stars)
min_stars = df[df["stars"] == df["stars"].min()]
print(min_stars)
lang_count=df["language"].value_counts()
print(lang_count)
df_sorted.to_csv("my_repos_analysis.csv",index=False,encoding="utf-8-sig")
print("\n分析结果已保存到 my_repos_analysis.csv")