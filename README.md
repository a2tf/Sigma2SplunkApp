# Sigma2SplunkApp
The tool to automatically deploy sigma rules into a individual Splunk App.

## Description
This tool uses Sigma2SplunkAlert from Patrick Bareiss to deploy Sigma Detection rules automatically in a splunk app chosen by the user. You can define which sigma rules should be implemented with a whitelist, these whitelist files getting automatically checked for their existence. This tool should be used on a Splunk Search Head.

## Installation
Follow the requirements according to [Sigma2SplunkAlert](https://github.com/P4T12ICK/Sigma2SplunkAlert).

It is needed that you clone the Sigma and Sigma2SplunkAlert repositories to a central git folder (e.g. /home/user/git).

## Usage
1. Prepare your config to launch sigma2splunkapp:  
 a) create your specific Sigma2SplunkAlert config and reference it in the config.yml with it's name  
 b) create your specific Sigma2SplunkAlert whitelisting config and reference it in the config.yml with it's name  
 c) define which sigma rules should be used to create your savedsearches.conf  
 d) define which sigma rules should be created with a whitelist  
 e) define your global settings (e.g. where is your git path, where is splunk located, what is the name of whitelisting app)  
 f) execute  


```usage: sigma2splunkapp.py [-h] configuration```

## Example
config.yml
```Sigma2SplunkApp:
    git_path: '/home/user/git'
    splunk_path: '/opt/splunk'
    whitelist_app: 'sigma_whitelist'
Sigma2SplunkAlert:
    standard_config: 'config.yml'
    whitelist_config: 'config_whitelist.yml'
sigma:
    sigma_config: 'splunk-all.yml'
    sigma_rules:
        - '/rules/windows/process_creation/win_encoded_iex.yml'
        - '/rules/windows/sysmon/*.yml'
    sigma_rules_whitelist:
        - 'sysmon_ads_executable.yml'
        - 'sysmon_cactustorch.yml'
        - 'sysmon_cobaltstrike_process_injection.yml'
```

Now running:
```sigma2splunkapp.py config/config.yml```

creates the following output:
```
Creating Rule: /home/user/git/sigma//rules/windows/process_creation/win_encoded_iex.yml
Creating Rule: /home/user/git/sigma//rules/windows/sysmon/sysmon_ads_executable.yml
Creating Rule: /home/user/git/sigma//rules/windows/sysmon/sysmon_cactustorch.yml
and so on for each created rule...
--------------------------------
File (savedsearches.conf) written to: /home/user/git/Sigma2SplunkApp/Sigma2SplunkApp/output/savedsearches.conf
--------------------------------
Checking now the whitelist file existence in your Splunk Whitelist App, showing missing files:
CACTUSTORCH_Remote_Thread_Creation_whitelist.csv
--------------------------------
Finished
 ```
So it shows you the process of detection rule creation and writes the savedsearch.conf output in the projects output folder (check Sigma2SplunkAlert repository for output).

It also checks for missing whitelisting lookup files in your specific whitelist app.

## Next Steps
- README better writeup
- Code optimization
- Write the output savedsearches.conf directly into splunk app
- debug/refresh splunk after changing savedsearches.conf

## Credits
- Patrick Bareiss for writing the Sigma2SplunkAlert tool, Sigma2SplunkApp is in the end just a wrapper around it
