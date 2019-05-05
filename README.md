# BFL-web
A Flask-based web application for BFL
Developed by: Fangzhou Sun, Robert Shelton, Ben Hadinger, Nathan Smith 

# Backend Python Installation

Install Anaconda Python 3.6 version at https://www.anaconda.com/download/

Install the latest Gurobi, follow the instruction at http://www.gurobi.com/downloads/get-anaconda
Or use command

```
conda config --add channels http://conda.anaconda.org/gurobi
conda install gurobi
```
You will need to get a Gurobi free academic license at http://www.gurobi.com/downloads/licenses/license-center

Install Flask and Waitress
```
conda install flask waitress
```
# frontend Vue.js Installation 
`npm install vue`

## Build Setup

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report
```

For a detailed explanation on how things work, check out the [guide](http://vuejs-templates.github.io/webpack/) and [docs for vue-loader](http://vuejs.github.io/vue-loader).

# Usage

For development, `cd` to the project folder, then use `python myapp.py` to start the server.

Next in a different terminal `cd` into the `frontend` folder and run `npm run dev` to start the client in dev mode

A Waitress production server can be started by `python production.py`.

# Git Workflow

## Goals
- Keep master branch free of errors.
- Make small feature pull requests
- Commit code often

## Bad practice
- Never push to master
- Don't work on a feature on an isolated branch for an entire semester
- - Make consistent pull request to keep master from falling to far behind
- - This will create reduce merge conflicts in the future

## Adding a new feature
- Start on master branch if on a different branch `git checkout master`
- Make sure your local version of master is up-to-date `git pull`
- Create a new branch for the code you want to add `git checkout -b <branch-name>`
- Write code `git add <files changed>`, commit code `git commit -m "what you did"`, 
    push to create upstream branch on GitHub `git push --set-upstream origin <name-of-branch>`
- Go to GitHub and create a pull request for master and wait for team members to review



