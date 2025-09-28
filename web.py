import  urllib.request

with urllib.request.urlopen("https://mit.edu") as f:
    print(f.read())

BASE_URL = "https://hz.mit.edu/drawings"
ID = "46oyeqalv1"

for x in range(500):
    print(urllib.request.post(f'{BASE_URL}/set_pixel'),
          data= {
            "image": 
          }


          )
