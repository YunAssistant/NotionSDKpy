# NotionSDKpy
基于Notion SDK的Python API，支持创建数据库以及Filter查询

## 前言

> 该项目为最近的一个项目里抽离出来的NotionSDK，一些功能可能不具有通用性。但底层接口都设计成了可扩展的形式，支持后续改进。

整个项目基于[ramnes的SDK](https://github.com/ramnes/notion-sdk-py)进行开发

- 解决了原版SDK库使用Requests库时可能会遇到的ProxyError问题
- 增加了Filter，支持复杂查询规则

## 使用方法

下面简单说明一下使用方法，目前仍在开发阶段，后续会更新完整教程(#TODO)

```python
from notion_client import Client, Filter
NOTION_TOKEN = os.getenv("NOTION_TOKEN", "")

# 初始化 Client
notion = Client(auth=NOTION_TOKEN)

# 初始化 Filter 
list = Filter.rule_list
list["property_name"] = "type" # 增加对应property name的type
```

Client创建数据库、查询数据库：

```python
def example():
    # Search for an item
    print("\nSearching for the word 'People' ")
    results = notion.search(query="People").get("results")
    print(len(results))
    result = results[0]
    print("The result is: ", result["object"])
    pprint(result["properties"])

    database_id = result["id"]  # store the database id in a variable for future use

    # Create a new page
    your_name = "123123123"
    gh_uname = "123123123123123123123"
    new_page = {
        "Name": {"title": [{"text": {"content": your_name}}]},
        "Tags": {"type": "multi_select", "multi_select": [{"name": "python"}]},
        "GitHub": {
            "type": "rich_text",
            "rich_text": [
                {
                    "type": "text",
                    "text": {"content": gh_uname},
                },
            ],
        },
    }
    notion.pages.create(parent={"database_id": database_id}, properties=new_page)
    print("You were added to the People database!")

    # Query a database
    name = input("\n\nEnter the name of the person to search in People: ")
    results = notion.databases.query(
        **{
            "database_id": database_id,
            "filter": {"property": "Name", "text": {"contains": name}},
        }
    ).get("results")

    no_of_results = len(results)

    if no_of_results == 0:
        print("No results found.")
        sys.exit()

    print(f"No of results found: {len(results)}")

    result = results[0]

    print(f"The first result is a {result['object']} with id {result['id']}.")
    print(f"This was created on {result['created_time']}")
```

Filter首先通过list增加`property_name`和`type`的关系，比如自定义`Film_Title`对应的是`text`，则可以直接初始化时添加到list中，查询的时候使用：`Film_Title==神秘海域`进行查询，若要进行复杂查询方式，则使用：`(Film_Title==神秘海域&Tags\c在看)|(Tags\c心愿单)`。

目前的开发支持`multi_select`、`text`和`number`三种类型，以及对应规则如下：

![image-20220424124757945](https:cdn.jsdelivr.net/gh/mryun820/blogImages/202204241247032.png)

具体查询时可使用：

```python
my_filter = Filter.make_filter("string")
results = notion.databases.query(
    **{
        "database_id": database_id,
        "filter": my_filter, # 自定义查询方式
    }
).get("results")
pprint(results) # 打印结果
```





