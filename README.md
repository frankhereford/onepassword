# An exploration in to the 1Password Dev Tools

## Discovery Day Spring 2023

### Intent
This repository contains proof-of-concept work intended to show that 1Password can be used as a centralized secret store and integrated into other systems, such that it can be only and authoritative store of secrets.

This comes with a number of benefits including:
* Need to rotate a secret? 
  * Set it once in the 1Password App and you're done!
  * This works no matter how many apps or places that secret is used.
* Need to have a reminder when to rotate? 
  * 1Password would love to remind you.
* Need to avoid having to keep track of the shapes of JSON blobs with secrets in them? 
  * Just make a 1Password entry of whatever complexity.
    * The 1Password entry is the shape, if you will.
    * When requesting multiple passwords, you can define your secret request as a JSON or JSON-like object, and the results will be provided in a shape specified by the JSON request definition.
      * See [here](https://github.com/frankhereford/onepassword/blob/main/compute_answer.py#L29-L36) for an minimal example.

## Prerequisites, Setup, and Considerations

* You must have deployment of a `One Password Connect` service.
  * For this demo, the deployment provides an API found at https://nothingbut.flowers.
    * A `404` is the correct response if you hit the URL without the correct headers or a meaningful request.
  * This service comes in the form of a pair of docker images.
    * One is a relay service, which is responsible for talking to the 1Password service out over the internet
    * The other is an API service, used by your own apps to query the contents of vaults in your 1Password account.
  * The two containers must be supplied with a configuration value which is a base64 encoded string of a JSON blob. The JSON is generated via the `op` command and does not contain secrets *per se*. 
  * There is no need to share it, and we shouldn't. That said, it wouldn't be bad if we did. It just is useful to no one except ourselves.
    * It contains essentially an indication of which account the connect server is relaying information for.
    * It does **_not_** contain permission or the ability to read the contents of any vaults.
* The API service can be deployed locally on machines which need to access secrets so that that no cross-internet traffic occurs between your app and the 1Password Connect API.
  * This is ultra-paranoia mode. It's entirely fine to allow API requests to traverse the internet with proper SSL/TLS support configured.
    * Realistically, one must understand that all of our secrets traverse the internet daily as we use the 1Password app.
  * This demonstration uses an endpoint available on the wider internet at https://nothingbut.flowers with an AWS ACM supplied certificate, which will auto-renew.
  * Multiple API endpoints can be deployed if needed.
* Using AWS, the API service can be deployed using the provided `1pw_cloudformation.yaml` file to run as a ECS cluster with compute power delivered via Fargate. We'd only pay for what we use, meaning no dedicated EC2 instance required.
  * For our use case, this would be absurdly cheap to run.
* Because this repo contains a demonstration of GitHub integrations using 1Password as a secret store, there must be single secret stored in the GitHub repo's Action Secrets: `OP_CONNECT_TOKEN`
  * Essentially, every application which needs to access our secrets API will need a token to do so.
  * These tokens are generated via the 1Password website, and they are granted vault access on a vault-by-vault basis. They can be given an expiry date, optionally, which is good practice.
  * There can be as many tokens generated as needed.
    * A token can be thought of as the same as a user-like-entity in 1Password. Just like if Jane Doe, a member of the DTS team, is given an account with access to certain vaults which she can read and write, then a One Password Connect API server can use a provided token to access vaults to which that token has permission to read and write.
  * These tokens are **very secret** secrets. Depending on what vault they can read and the accessability of a One Password Connect API, they very well can be considered keys to the kingdom.
* Create a python `venv`, and install the libraries listed in `requirements.txt` so that you can run `compute_answer.py`.

## Repository contents
1) `1pw_cloudformation.yaml`: Infra as code, taken from the 1PW docs
1) `env-template`: Copy this file to `.env` and provide a 1Password Connect Access Token, generated via the 1Password Website
1) `requirements.txt`: The required python libraries to install in your venv
1) `compute_answer.py`: A python script which uses the onepassword python library to request a particular secret. It also prompts the user for a string. The secret and the string are concatenated together and a SHA1 hash is taken of the result. This hash is then printed. This value can be used to check the GitHub action's result.
1) `sha_computer.json`: A JSON file, which you can change the value of the `input` key to whatever you want. A GitHub action will update the `shaWithSecret` value in this file using the same method as `compute_answer.py`.
1) `.github/workflows/main_deployment.yml`: A GitHub action which when you push to the repo, will get the same secret that `compute_answer.py` gets and compute the SHA hash in the same fashion using the value in the `input` key found in `sha_computer.json`. It will then update the key `shaWithSecret` in the `sha_computer.json` file. It will then commit and push the updated file up to the repo on GitHub. In order to make that **write** operation into the repo, the GitHub action will get the GitHub Personal Access Token required from 1Password. 