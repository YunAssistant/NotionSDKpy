import json
# {
#     "filter": {
#         "or": [
#             {
#                 "property": "Description",
#                 "rich_text": {
#                     "contains": "fish"
#                 }
#             },
#             {
#                 "and": [
#                     {
#                         "property": "Food group",
#                         "select": {
#                             "equals": "🥦Vegetable"
#                         }
#                     },
#                     {
#                         "property": "Is protein rich?",
#                         "checkbox": {
#                             "equals": true
#                         }
#                     }
#                 ]
#             }
#         ]
#     }
# }
class Filter:
    rule_list = {
        "Tags":"multi_select",
        "Name":"text",
        # Add Corresponding Name Here
    }

    # For more filter condition, query https://developers.notion.com/reference/post-database-query-filter#multi-select-filter-condition
    text_filter_map = {
        "==": "equals",
        "!=": "does_not_equal",
        "\c": "contains",
        "\C": "does_not_contain",
        "^=": "starts_with",
        "$=": "ends_with",
        "\s": "is_empty",
        "\S": "is_not_empty"
    }

    multiselect_filter_map = {
        "\c": "contains",
        "\C": "does_not_contain",
        "\s": "is_empty",
        "\S": "is_not_empty"
    }

    number_filter_map = {
        '==': "equals",
        '!=': 'does_not_equal',
        '>>': 'greater_than',
        '<<': 'less_than',
        '>=': 'greater_than_or_equal_to',
        '<=': 'less_than_or_equal_to',
        '\s': 'is_empty',
        '\S': 'is_not_empty'
    }


    @staticmethod
    def make_kv(name1, name2, rule, value): # name1:property name, name2:type name, rule: contains/equal, value: contains value
        data = {"property": name1, name2: { rule:value }}
        j = json.dumps(data,ensure_ascii=False)
        return j

    @staticmethod
    def make_and_json(s1,s2):
        rule_and = {"and": [json.loads(s1),json.loads(s2)]}
        j = json.dumps(rule_and,ensure_ascii=False)
        return j

    @staticmethod
    def make_or_json(s1,s2):
        rule_or = {"or": [json.loads(s1),json.loads(s2)]}
        j = json.dumps(rule_or,ensure_ascii=False)
        return j

    @staticmethod
    def make_property(r):
        name = ''
        op = ''
        value = ''
        for key in Filter.rule_list:
            index = r.find(key)
            if index != -1:
                index = index + len(key)
                name = r[:index]
                op = r[index : index+2]
                value = r[index+2:]
                break
        if name == '' :
            print("Rule not found")
            return
        type = Filter.rule_list[name]
        if type == "text" : rule_method = Filter.text_filter_map[op]
        elif type == "multi_select": rule_method = Filter.multiselect_filter_map[op]
        elif type == "number": rule_method = Filter.number_filter_map[op]
        else:
            rule_method = ''
            print("Rules Not Covered or Rule not correct.")
            return
        j = Filter.make_kv(name, type, rule_method, value)
        # print(j)
        return j

    @staticmethod
    def process_string(s):
        list = []
        tag = ''
        for c in s:
            if c == '&' or c == '|' or c == '(' or c == ')':
                if tag:
                    list.append(tag)
                    tag = ''
                list.append(c)
            else: tag = tag + c
        if tag: list.append(tag)
        stack = []
        pl = []
        # print(list)
        for c in list:
            if c == '&' or c == '|' or c == '(' or c == ')':
                if c == ')':
                    while stack and stack[-1] != '(':
                        pl.append(stack.pop())
                    stack.pop()
                elif c == '&':
                    while stack and stack[-1] == '&':
                        pl.append(stack.pop())
                    stack.append('&')
                elif c == '|':
                    while stack and stack[-1] == '|':
                        pl.append(stack.pop())
                    stack.append(c)
                else:
                    stack.append(c)
            else:
                pl.append(c)

        while stack:
            pl.append(stack.pop())

        return pl

    @staticmethod
    def make_filter(s):
        res = []
        pl = Filter.process_string(s)
        print(pl)
        for c in pl:
            if c == '&' or c == '|' or c == '(' or c == ')':
                s1 = res.pop()
                s2 = res.pop()
                if c == '&':
                    res.append(Filter.make_and_json(s1, s2))
                elif c == '|':
                    print(s1)
                    print(s2)
                    res.append(Filter.make_or_json(s1, s2))
                else:
                    pass
            else:
                res.append(Filter.make_property(c))

        if len(res) == 0: print("something error")
        # print(res[0])
        j = json.loads(res[0])
        return j
