# Roadmap


### Priority

- Turbine:
    - build from an empty stage, it creates a work component from scratch

    - Create processes to be able to do: modeling -> rigging -> shot

- better ExportsTable:
    - mvd
    - context menu

- ComponentBrowser: remove work components (wait for more exports, for debug purposes)

- Turbine:
    - Jobs list filters

### Missing features

- Recipes:
    - toolbar buttons: refresh, autofill, copy, paste, ingredient groups

- Work versions:
    - list versions from all work components
    - work components from a same stage should never have the same version numbers

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

- SoftwareClasses: subclasses for in/out, file management, etc.

---

### Qol & Upgrades to existing and working features

- StageList: bug sometimes when editing a user that has just been edited and refresh has not happened yet

- work versions panel: disable when no stages are selected (or a version cannot be created)

- process_launcher:
    - preset the input's height and use scroll area to have a fixed size window

- Turbine:
    - show processes and steps duration

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
