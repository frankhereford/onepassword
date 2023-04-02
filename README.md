# onepassword
A playground for OnePassword Integrations

## Useful Commands
Base64 encode the credentials to allow the sync service to talk to 1PW
`cat 1password-credentials.json | base64 | tr '/+' '_-' | tr -d '=' | tr -d '\n'`