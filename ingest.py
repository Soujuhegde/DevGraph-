import os

def load_readmes(folder="data/readmes"):
    """Returns a list of dicts: {project_name, content}"""
    projects = []
    for filename in os.listdir(folder):
        if filename.endswith(".md"):
            path = os.path.join(folder, filename)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            project_name = filename.replace(".md", "").replace("_", " ").title()
            projects.append({"project_name": project_name, "content": content})
    return projects

if __name__ == "__main__":
    projects = load_readmes()
    print(f"Loaded {len(projects)} projects")
    for p in projects:
        print(" -", p["project_name"], f"({len(p['content'])} chars)")
