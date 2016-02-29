# distributed-project
For distributed group project

## project map

/  
└ [resources.md](https://github.com/FilWisher/distributed-project/blob/master/resources.md) [1]   
└ [resources/](https://github.com/FilWisher/distributed-project/tree/master/resources) [2]   
└ /fixtures [3]   
└ /icarus [4]   

[1] - List of background reading resources    
[2] - PDFs of relevant articles   
[3] - Example json files for d3   
[4] - icarus simulator 

## development

### setup

Make sure you have nodejs and npm installed.

```
git clone https://github.com/filwisher/distributed-project
cd distributed-project/visualization
npm install
```

To run tests: ```npm test```
To get coverage report: ```npm run coverage```
To build app: ```npm run build```
Or to build app continuously: ```npm run build:w```

### workflow

Open visualization/assets/index.html
   , visualization/assets/main.js
   , visualization/test/tests.js
   
Run ```npm start``` from visualization/assets
Run ```npm build:w``` from visualization

Write changes into visualization/assets/main.js
Write tests into visualization/tests/test.js

Before you commit, run ```npm run cover``` to check coverage reports
