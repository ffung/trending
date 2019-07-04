# trending


## Features

RSS Feed for trending hashtags and words in Amsterdam area.

Following RSS Feeds are exposed
- `<host>:<port>/hashtags`
- `<host>:<port>/words`

Other URLS will return a 404 error.
PS: analysis is not real time as of yet.

## CI/CD pipeline
Included in the setup is some groundwork to create an AWS pipeline for running this application using Terraform.

See the `pipeline` folder.


## Development / testing

### Run unittests / coverage report
```
python setup.py test
```
