import json
def block_div(block_no,from_name,from_address,to_name,to_address,value):
    block = f"""<div class="block b{block_no}">\n<div class="block-title">Block #{block_no}</div>\n<div class="block-details">\n<div>From : {from_name},{from_address}</div>\n<div>To: {to_name},{to_address}</div>\n<div>Value :{ value }</div>\n</div>\n</div>"""
    return block


with open('./templates/blocks.html','w+') as file:
    block = "{% extends 'dashboardPage.html' %}\n{% block content %}\n"+block_div(1,"bhanu",111,'siddu',112,500)+"\n{% endblock %}"
    file.write(block)
"""
with open('./data/blocks.json') as file:
    cont = json.load(file)

print(cont)
cont = {int(i):cont[i] for i in list(cont.keys())}
print(cont)
print(type(list(cont.keys())[0]))
"""
