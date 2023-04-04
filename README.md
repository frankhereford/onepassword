# An exploration in to the 1Password Dev Tools

## Discovery Day Sprint 2023

### Intent
This repository contains proof on concept work intended to show that 1Password can be used as a centralized secret store and integrated into other systems, such that it can be only and authoritative store of secrets.

This comes with a number of benefits including:
* Need to rotate a secret? 
  * Set it once in the 1Password App and you're done!
* Need to have a reminder when to rotate? 
  * 1Password would love to remind you.
* Need to avoid having to keep track of the shapes of JSON blobs with secrets in them? 
  * Just make a 1Password entry of whatever complexity. The 1Password entry is the shape.

## Prerequisites

* You must have deploy a `One Password Connect` service.
  * For this demo, the API is found at https://nothingbut.flowers.
    * A `404` is the correct response if you hit the URL without the correct headers or a meaningful request.
  * This service comes in the form of a pair of docker images.
    * One is a relay service, which is responsible for talking to the 1Password service out over the internet
    * The other is an API service, used by your own apps to query the contents of vaults in your 1Password account.
  * The two containers must be supplied with a configuration string which is a base64 encoded string of a JSON blob. The JSON is generated via the `op` command, and which does not contain secrets per se. 
  * There is no need to share it, and we shouldn't, but, it wouldn't be bad if we did.
    * It contains essentially an indication of which account the connect server is relaying information for.
    * It does **_not_** contain permission or the ability to read the contents of any vaults.
* The deployed service can be deployed locally on machines which need to use it so that that no cross-internet traffic to your 1Password Connect API.
  * This is ultra-paranoia mode. It's entirely fine to allow API requests to traverse the internet with proper SSL/TLS support configured.
  * This demonstration uses an endpoint available on the wider internet at https://nothingbut.flowers.
* It can also easily be deployed using the provided `1pw_cloudformation.yaml` file to run as a ECS cluster with compute power delivered as-used via Fargate.
  * For our use case, this would be absurdly cheap to run.
* Have a single secret stored in the GitHub repo's Action Secrets: `OP_CONNECT_TOKEN`
  * Essentially, every application which needs to access the API will need a token to do so.
  * These tokens are generated via the 1Password website, and they can be limited by vault and can be given an expiry date, optionally.
* Create a python `venv`, and install the libraries listed in `requirements.txt` so that you can run `compute_answer.py`.

## Repository contents
1) `1pw_cloudformation.yaml`: Infra as code, taken from the 1PW docs
1) `env-template`: Copy this file to `.env` and provide you Connect Access Token, generated via the 1Password Website
1) `requirements.txt`: The required python libraries to install in your venv
1) `compute_answer.py`: A python script which uses the onepassword python library to request a particular secret. It also prompts the user for a string. The secret and the string are concatenated together and a SHA1 hash is taken of the result. This hash is then printed. This value can be used to check the GitHub action's result.
1) `sha_computer.json`: A JSON file, which you can change the value of the `input` key to whatever you want. A GitHub action will update the `shaWithSecret` value in this file using the same method as `compute_answer.py`.
1) `.github/workflows/main_deployment.yml`: A GitHub action which when you push to the repo, will get the same secret that `compute_answer.py` gets and compute the SHA hash in the same fashion using the value in the `input` key found in `sha_computer.json`. It will then update the key `shaWithSecret` in the `sha_computer.json` file. It will then commit and push the updated file up to the repo on GitHub. In order to make that **write** operation into the repo, the GitHub action will get the GitHub Personal Access Token required from 1Password. 