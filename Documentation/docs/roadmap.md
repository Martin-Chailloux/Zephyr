# Roadmap


### Priority

-  rmb in Users List does not cancel it

- Turbine:
    - modeling build: version num + dont overwrite to build over an existing version
    - export modeling: use version num input

    - Create basic processes for modeling -> rigging -> shot
        Think about pipeline details later

- ExportsTable:
    - mvd
    - context menu

- rigging: build from geo and extra ingredients

- Recipes: finish required features
    - ComponentBrowser: remove work components (wait for more exports, for debug purposes)

---

### Missing features
- Recipes:
    - toolbar buttons: refresh, autofill, copy, paste, ingredient groups

- Turbine:
    - Jobs list filters
    - relaunch a process from the jobs list

- Users:
    - per project information
        - roles (sup / lead / graphist / pipe)
        - favorite_assets
        - recent_assets
   --> probably a Contributor/Member/PrUser/SubUser document in project_documents, with source_user and the needed extra fields
      it is a user with extra project-related fields
      can be found with BreezeApp.sub_user

- switch User and Projects
    - ui to create them

- Admin tab: Guis to create and manage db items
    - Users (for the current project): add users to project / assign roles
    - Stage Templates
        - process assignment
        - create, delete, icon, color, label, category_filters, assigned_users, etc

- Asset groups

- Asset data / properties

- User roles and permissions

---

### Cleans & Refactors
- popups:
    - transform every popup into browsers with a toolbar style

- rework subwidgets hierarchy, move them under Gui/..., utils can probably be removed entirely:
    - chronometer to Api/utils
    - external toolbar
    - searchbar
    - groups all icon stuff in a single file

- mvd: confo and simplify from new knowledge, update stages' mouse events using component tree's code

- SoftwareClasses: sub-classes for in/out, file management, etc.

---

### Qol & Upgrades to existing and working features
- work versions panel: disable when no stages are selected (or a version cannot be created)

- process_launcher:
    - cache, remember selected processes and inputs for each context: stage: process ; process: inputs
    - preset the input's height and use scroll area to have a fixed size window

- Turbine:
    - refresh jobs on tab shown
    - show processes and steps duration
    - relaunch from the jobs list

- copy/paste users and statuses with ctrl+C/ctrl+V

- StageTemplateList assignment:
    - warn if a used stage template is about to be deleted
    - ui to omit or keep them
    - gui to edit recipes

- save the gui's state between instances

- add error messages to steps in step viewer's tree

- Stage Templates: status and users history

- Asset browser:
    - favorites / recent

- Ingredient Slots: components history
