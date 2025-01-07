from MangoEngine import project_dialog


def create_project():
    categories =["Character", "Props", "Element", "Decor", "Sequence", "Sandbox", "Library"]
    project_dialog.create_project(name="Dev", categories=categories)

if __name__ == '__main__':
    project = project_dialog.get_project("Dev")
    project.add_category("zahoieaj")