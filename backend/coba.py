from pydrill.client import PyDrill
import json
import ast 

def read_csv():
  try:
    drill = PyDrill(host='localhost', port=8047)
    
    result = drill.query('''
      SELECT * FROM
      dfs.`/home/syafiq/Downloads/Compressed/data.csv`
      LIMIT 5
    ''')
    df = result.to_dataframe()
    print(df.get('columns')[0])
    meta = {}
    for i in range(0, len(df.get('columns')[0])):
      meta[i] = df.get('columns')[0][i]
    print(meta)

  except:
    print("Something's wrong") 

def read_json(): 
  try:
    drill = PyDrill(host='localhost', port=8047)
    
    result = drill.query('''
      SELECT * FROM
      `dfs.root`.`./home/syafiq/Downloads/CA_category_id.json`
      LIMIT 5
    ''')
    
    df = result.to_dataframe()['items'][0]
    data = json.loads(df)
    row1 = data[0]
    print(row1)

  except():
    pass

read_csv()



