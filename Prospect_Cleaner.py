prospects = []
import csv, string, re

def process_name(i):
    m = re.search(r"\s\|[a-z,A-Z,\-,\s]*$", i["name"])#remove linkedin text
    if(m is not None):
        i["name"] = i["name"][:m.start()] + i["name"][m.end():]
    m = re.search(r"on\sLinkedIn.*", i["name"])#remove linkedin text
    if(m is not None):
        i["name"] = i["name"][:m.start()] + i["name"][m.end():]
    m = ""
    #strip nicknames and areas
    while m is not None:
        m = re.search(r"\([a-z,A-Z,\s]*\)", i["name"])

        if(m is not None):
            # print  m.string[m.start():m.end()] # strips locations and names
            i["name"] = i["name"][:m.start()] + i["name"][m.end():]
    #strip attached company names
    print i["name"]
    m = re.search(r"\sat\s.*$", i["name"])
    if(m is not None):
        #fixing name
        i["name"] = i["name"][:m.start()] + i["name"][m.end():]
        #additional source for company name
        company =  m.string[m.start():m.end()]
        if(i.get("company") is None):
            m = re.search(r"\s*at\s*", company)#remove linkedin text
            if(m is not None):
                i["company"] = company[:m.start()] + company[m.end():]

    print i["name"]
    #strip titles MSIT, MBA
    m = re.search(r",\s.*$", i["name"])
    if(m is not None):
        i["name"] = i["name"][:m.start()] + i["name"][m.end():]
    #strip titles pt MS SHRM-SCP
    m = re.search(r"MS\s*.*$", i["name"])
    if(m is not None):
        i["name"] = i["name"][:m.start()] + i["name"][m.end():]

    #strip remaining nicknames
    m = re.search(r"\s\".*\"", i["name"])
    if(m is not None):
        i["name"] = i["name"][:m.start()] + i["name"][m.end():]
    #get rid of jr sr doctor
    m = ""
    while m is not None:
        m = re.search(r"[D,S,J]r\.", i["name"])
        if(m is not None):
            i["name_title"] = m.string[m.start():m.end()]#store it, error on 2 titles be aware TODO
            i["name"] = i["name"][:m.start()] + i["name"][m.end():]
        else:
            i["name_title"] = ""#no name titles

    i["name"] = i["name"].rstrip()
    name = i["name"].split(" ")
    i["first_name"] = name[0]
    if(len(name) is 2):
        i["last_name"] = name[1]
        i["middle_name"] = ""
    else:
        i["middle_name"] = name[1]
        i["last_name"] = name[2]
    return i
def process_area(i):
    m = re.search(r"\sArea", i["area"])
    if(m is not None):
        i["area"] = i["area"][:m.start()] + i["area"][m.end():]
    m = re.search(r"Greater\s", i["area"])
    if(m is not None):
        i["area"] = i["area"][:m.start()] + i["area"][m.end():]
    area = i["area"].split(', ')
    if(area[0] == "United States"):
        i["city"] = ""
        i["state"] = ""
    else:
        try:
            i["city"] = area[0]
            i["state"] = area[1]
        except Exception as e:
            i["state"] = ""
    return i
def process_position(i):
    i["position"] = i["position_at"]
    #remove company
    m = re.search(r"\sat.*$", i["position"])
    if(m is not None):
        i["position"] = i["position"][:m.start()] + i["position"][m.end():]
    m = re.search(r"\s@.*$", i["position"])
    if(m is not None):
        i["position"] = i["position"][:m.start()] + i["position"][m.end():]

    return i
def process_company(i):#already clean
    # print i["company"]
    return i

with open('Prospects.csv', 'rb') as csvfile:
  prosreader = csv.reader(csvfile, delimiter =',')
  for row in prosreader:
      if(row[2] == "PositionXLocationXCompany"):
          continue
      elif(row[2] == ""):
          continue
      prospects.append({
        "linkedin_url":''.join(x for x in row[0] if x in string.printable),
        "name":''.join(x for x in row[1] if x in string.printable),
        "city_position_company":''.join(x for x in row[2] if x in string.printable)
      })

with open('Prospects-Cleaned.csv', 'wb') as csvfile:
    fieldnames = ['city', 'first_name', 'last_name', 'middle_name', 'area','linkedin_url', 'company', 'state', 'position','name_title']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for i in prospects:
        #clean name
        i = process_name(i)

        #split the city position company section
        cpc = i["city_position_company"].split(" - ")
        try:
            i["area"] = cpc[0]
            i = process_area(i)
            i["position_at"] = cpc[1]
            i = process_position(i)
            i["company"] = cpc[2]
            i = process_company(i)
        except Exception as e:
            if(i.get("area") is None):
                i["area"] = ""
            if(i.get("position_at") is None):
                i["position_at"] = ""
            if(i.get("company") is None):
                i["company"] = ""
        del i["position_at"]
        del i["name"]
        del i["city_position_company"]

        writer.writerow(i)
