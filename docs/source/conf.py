project = "Sensu Go Ansible Collection"
copyright = "2019, XLAB Steampunk"
author = "XLAB Steampunk"

extensions = [
    "sphinx_rtd_theme",
]
exclude_patterns = []

html_theme = "sphinx_rtd_theme"
html_context = {
    "display_github": True,
    "github_user": "sensu",
    "github_repo": "sensu-go-ansible",
    "github_version": "master",
    "conf_py_path": "/docs/source/",
}
