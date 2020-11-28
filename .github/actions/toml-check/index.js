const core = require('@actions/core');
const github = require('@actions/github');
const toml = require('toml');
const fs = require('fs');
const { exit } = require('process');

const loadTomlFile = filePath => toml.parse(fs.readFileSync(filePath, 'utf8'));
const withGithubWorkspacePath = path => `${process.env.GITHUB_WORKSPACE}/${path}`

var status = true;

try {
  const schema = loadTomlFile(withGithubWorkspacePath(core.getInput('path-to-schema')));
} catch (e) {
  console.log('ERROR: Schema could not be loaded')
  core.setOutput('status', false);
  exit(2)
}

const challengesPath = withGithubWorkspacePath('challenges/');

fs.readdir(challengesPath, (err, folder) => {
  if (err) {
    console.log('ERROR: Could not open challenges/')
    core.setOutput('status', false);
    return
  }
  folder.forEach(folder => {
    console.log('______________________________________________________')
    console.log('CHALLENGE: ' + folder)

    const filepath = `${challengesPath}/${folder}/challenge.toml`;
    try {
      const data = loadTomlFile(filepath);
      
      // validate
      Object.keys(schema).forEach(key => {
        // validate fields are present
        if (!(key in data)) {
          status = false;
          console.log(`ERROR: In ${folder} toml file: ${key} field is missing`)
        }

        // validate type
        switch (schema[key]) {
          case "array":
            if (!Array.isArray(data[key])) {
              status = false;
              console.log(`ERROR: In ${folder} toml file: ${key} field is of the wrong type. It should be type array`)
            }
            break;
          default:
            if (typeof data[key] !== schema[key]) {
              status = false;
              console.log(`ERROR: In ${folder} toml file: ${key} field is of the wrong type. It should be type ${schema[key]}`)
            }
        }

        // special validation
        if (key === 'files' && Array.isArray(data[key])) {
          data[key].forEach(file => {
            if ('description' in data && typeof data['description'] === "string") {
              if (data['description'].search(new RegExp(`\[.+\]\(${file}\)`, 'gi')) === -1) {
                status = false;
                console.log(`ERROR: In ${folder} toml file: Description is missing link to ${file}`)
              }

              const matches = data['description'].match(/\[.+\]\(([-a-zA-Z0-9()_.].+)\)/i);
              
              matches.forEach((val, i) => {
                if (i % 2 === 1) {
                  if (!data['files'].includes(val)) {
                    status = false;
                    console.log(`ERROR: In ${folder} toml file: ${val} is missing in files`)
                  }
                }
              })
            }
          })
        }
      })
    } catch (e) {
      console.log(`ERROR: In ${folder} toml file on line ${e.line}, column ${e.column}: ${e.message}`);
      status = false;
    }        
  });
})

core.setOutput("status", status);

try {
  // Get the JSON webhook payload for the event that triggered the workflow
  const payload = JSON.stringify(github.context.payload, undefined, 2)
  console.log(`The event payload: ${payload}`);
} catch (error) {
  core.setFailed(error.message);
}