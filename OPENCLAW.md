## himalaya CERN Mail setup workflow

This is an instruction for OpenClaw to setup himalaya to access CERN email account with OAuth2 authentication.

1. **Check himalaya installation**: Check if himalaya is successful installled with needed oauth2 feature by running `himalaya --version`. You should see `+oauth2` in the output.
- If himalaya is not installed: run `cargo install himalaya --locked`.
- If himalaya is installed but you don't see `+oauth2`:
    - Check himalaya installation location: run `which himalaya`.
    - Uninstall himalaya: run `cargo uninstall himalaya` or `brew uninstall himalaya`
    - Reinstall himalaya with oauth2 support: run `cargo install himalaya --locked`.

2. **Setup access token retrieval command**

- **Setup venv**: Create a python virtual environment and install the required dependencies:

```bash
cd ~/.openclaw/workspace/email_oauth2
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

- **Initialize token retrieval command**: Ask User to run the following command and wait for the User's response.

```bash
cd ~/.openclaw/workspace/email_oauth2
source venv/bin/activate
python get_cern_token.py
# This will open a browser window for user to login with CERN account and grant permission to the app. After successful login, you should see the access token printed in the terminal.
```

3. **Config himalaya**

- **Get PATH_TO_PYTHON**: run `realapth ~/.openclaw/workspace/email_oauth2/venv/bin/python`
- **Get PATH_TO_GET_CERN_TOKEN_PY**: run `realpath ~/.openclaw/workspace/email_oauth2/get_cern_token.py`
- **Ask User for the email address**: for the CERN account
- **Edit config file**: Add the following example config (Replace `<EMAIL_ADDRESS>`, `PATH_TO_PYTHON`, and `PATH_TO_GET_CERN_TOKEN_PY` with the actual values) to himalaya config file located at:
   - `~/.config/himalaya/config.toml` if in Linux
   - `~/Library/Application Support/himalaya/config.toml` if in MacOS

Example config
```
[accounts.cern]
email = <EMAIL_ADDRESS>

[accounts.cern.backend]
type = "imap"
host = "outlook.office365.com"
port = 993
encryption.type = "tls"
login = "xuliang.zhu@cern.ch"

[accounts.cern.backend.auth]
type = "oauth2"
method = "xoauth2"
client-id = "543725ae-fd38-436a-a717-009b1a8137be"
auth-url = "https://login.microsoftonline.com/cern.ch/oauth2/v2.0/authorize"
token-url = "https://login.microsoftonline.com/cern.ch/oauth2/v2.0/token"
pkce=true
scopes = ["https://outlook.office.com/IMAP.AccessAsUser.All"]
access-token.cmd = <PATH_TO_PYTHON PATH_TO_GET_CERN_TOKEN_PY>

[accounts.cern.sender]
type = "smtp"
host = "smtp.office365.com"
port = 587
encryption.type = "start-tls"
login = "xuliang.zhu@cern.ch"

[accounts.cern.sender.auth]
type = "oauth2"
method = "xoauth2"
client-id = "543725ae-fd38-436a-a717-009b1a8137be"
auth-url = "https://login.microsoftonline.com/cern.ch/oauth2/v2.0/authorize"
token-url = "https://login.microsoftonline.com/cern.ch/oauth2/v2.0/token"
pkce=true
scopes = ["https://outlook.office.com/SMTP.Send"]
access-token.cmd = <PATH_TO_PYTHON PATH_TO_GET_CERN_TOKEN_PY>
```

4. **Test the setup**: Run `himalaya envelope list -a cern`. If you see the list of emails in your inbox, then the setup is successful.

5. **Done**
