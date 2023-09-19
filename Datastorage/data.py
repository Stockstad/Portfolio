import json
__package__ = None

def load(filename):
    projects = []
    try:
        file = open(filename)
        data = json.load(file)

        for i in data:
            if "project_id" in i:
                projects.append(i)
        sorted_projects = sorted(projects, key=lambda x: x["project_id"])
        return sorted_projects
    except:
        return None

def get_project_cont(db):
    return len(db)
    
def get_project(db, id):
    for i in db:
        if i["project_id"] == id: #What if multiple projects happen to have the same id?
            return i
    return None

def search(db, sort_by, sort_order, search, techniques, search_fields):
    search_db = db.copy()
    for i in search_db:
      i["project_id"] = str(i["project_id"]) #Is this okay?

    response = []
    for project in search_db:
        if search_fields == None:
            for key in project:
                if project[key] == search and techniques_allowed(project, techniques):
                        response.append(project)
        elif len(search_fields) == 0:
            return []
        
        else:
            for field in search_fields:
                if project[field] == search and techniques_allowed(project, techniques):
                        response.append(project)
    sorted_list = sorted(response, key=lambda x: x[sort_by])
    if sort_order == "desc":
        print("Debug")
        return sorted_list.reverse()
    else:
        return sorted_list


def techniques_allowed(pro, tech):
    if len(tech) > 0:
        return all(t in pro["techniques_used"] for t in tech)
    else:
        return True
    







db = load("data.json")


item = search(db, "project_id", "desc", "TDP003", [], ["course_id"])
print(item)
