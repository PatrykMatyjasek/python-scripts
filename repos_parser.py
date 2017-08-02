import json
import requests

r = requests.get("https://api.github.com/orgs/intelsdi-x/repos?per_page=100")
a = json.loads(r.text)
repos = []
for b in a:
    repos.append(b["html_url"])
r = requests.get("https://api.github.com/orgs/intelsdi-x/repos?per_page=100&page=2")
a = json.loads(r.text)
for b in a:
    repos.append(b["html_url"])

print len(repos)

glides = []
godeps = []
for repo in repos:
    if "snap" in repo:
        u = repo.split("/")[-1]
        glide = requests.get("https://raw.githubusercontent.com/intelsdi-x/"+u+"/master/glide.yaml")
        if glide.status_code == 404:
                godep = requests.get("https://raw.githubusercontent.com/intelsdi-x/"+u+"/master/Godeps/Godeps.json")
                godeps.append(godep.text)
                if godep.status_code == 404:
                        print repo
        glides.append(glide.text)

fl = open("glides", "w")
for glid in glides:
    fl.write(str(glid))
fl.close()

fl = open("glides", "r")
a = fl.readlines()
dependencies = {}
for line in a:
    if line.startswith("package: "):
        package = line.split("/")[-1].replace("\n", "")
    elif line.startswith("- package: "):
        dependency = line.split(" ")[-1].replace("\n", "")
        if dependency in dependencies.keys():
            dependencies[dependency].append(package)
        else:
            dependencies[dependency] = []
            dependencies[dependency].append(package)

for godep in godeps:
    try:
        deps = json.loads(godep)
    except:
        continue
    dependencies[deps["ImportPath"]] = []
    for dep in deps["Deps"]:
        dependencies[deps["ImportPath"]].append(dep["ImportPath"])

print dependencies
