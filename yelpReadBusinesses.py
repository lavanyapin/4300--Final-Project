import json
import re 

businesses = open("yelp_academic_dataset_business.json")
f = open("sql_business_script.txt", "w")
i = open('business_ids.txt', "w")
i.write("{")

business_list = []
acc = 0
for line in businesses:
  if acc >= 2000:
     break
  b = json.loads(line)
  if b["is_open"] == 1:
      lst = b["categories"]
      if lst != None:
        if ("Hotels" in lst or "Hotels & Travel" in lst or "Arts & Entertainment" in lst) and \
          ("Fashion" not in lst and "Restaurants" not in lst and "Coffee & Tea" not in lst and \
          "Automotive" not in lst and "Shopping" not in lst and "Car Rental" not in lst):
          id = b["business_id"]
          name = re.sub(r'[^a-zA-Z0-9 ]', '', b["name"].lower())
          city = re.sub(r'[^a-zA-Z0-9 ]', '', b["city"].lower())
          state = b["state"].lower()
          latitude =str(b["latitude"]).lower()
          longitude = str(b['longitude']).lower()
          stars = str(b["stars"]).lower()
          num_revs =str(b["review_count"]).lower()
          f.write("INSERT INTO businesses VALUE(\'"+id+"\', \'"+name+"\', \'"+city+"\', \'"+state+"\', "+latitude+", "+longitude+", "+stars+", "+num_revs+");\n")
          i.write("\""+id+"\",\n")
          acc += 1
           

businesses.close()
i.write('}')
f.write(']')
f.close()

