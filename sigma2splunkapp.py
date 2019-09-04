#!/usr/bin/env python3
# Copyright 2019 - a2tf
import yaml
import sys
import os
import glob
import subprocess
from subprocess import DEVNULL
import argparse
from classes.Configuration import Configuration

def main():
    parser = argparse.ArgumentParser(
        description='Convert Sigma rules to Splunk App.')
    parser.add_argument('configuration', action='store', help='filepath containing the Sigma2SplunkApp Configuration')

    arguments = parser.parse_args()
    
    # Read Configuration
    config_yml = openSigma2SplunkAppConfiguration(arguments.configuration)
    config = Configuration(config_yml)
    
    # Define parameters to execute Sigma2SplunkAlert commands
    param_sc = "-sc " + config.git_path + "/Sigma2SplunkAlert/sigma_config/" + config.sigma_config
    param_t = "-t " + config.git_path + "/Sigma2SplunkAlert/templates/" + config.S2SA_template_config
    executable = config.git_path + "/Sigma2SplunkAlert/sigma2splunkalert"
    # store all the savedsearches
    savedsearches = []
    # store effectively whitelisted sigma rules with full path
    eff_whitelisted = []
    # Iterate through Sigma Rules
    for sigma_object in config.sigma_rules:
        sigma_rules_path = config.git_path + "/sigma/" + sigma_object
        sigma_path = glob.glob(sigma_rules_path)
        for sigma_rule in sigma_path:
            
            param_c = "-c " + config.git_path + "/Sigma2SplunkAlert/config/" + config.S2SA_standard_config
            # Iterate over Whitelist
            for w in config.sigma_rules_whitelist:
                # create Sigma2SplunkAlert parameters
                if w == os.path.basename(sigma_rule):                  
                    param_c = "-c " + config.git_path + "/Sigma2SplunkAlert/config/" + config.S2SA_whitelist_config
                    eff_whitelisted.append(os.path.abspath(sigma_rule))
            
            # Execute Sigma2SplunkAlert & save output to list    
            command = executable + " " + param_c + " " + param_sc + " " + param_t + " " + sigma_rule
            print("Creating Rule: " + sigma_rule)
            out = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=DEVNULL, universal_newlines=True)
            output = out.stdout
            if "Failure" in output:
                    print("Failure Rule: " +sigma_rule)
            # Delete all newlines
            output = os.linesep.join([n for n in output.splitlines() if n])    
            savedsearches.append(output)
    # Add according newlines
    towrite = "\n\n".join(savedsearches)
    writepath = "output/savedsearches.conf"
    # write file
    file = open(writepath, "w")
    file.write(towrite)
    file.close()
    print("--------------------------------")
    print("File (savedsearches.conf) written to: " + os.path.abspath(writepath))
    print("--------------------------------")
    print("Checking now the whitelist file existence in your Splunk Whitelist App, showing missing files:")
    checkWhitelistExistence(eff_whitelisted, config.splunk_path + "/etc/apps/" + config.whitelist_app)
    print("--------------------------------")
    print("Finished")
    
    
# Copied from Sigma2SplunkAlert - Patrick Bareiss
def openSigma2SplunkAppConfiguration(converter_config_path):
    # Load Sigma2SplunkApp configuration
    with open(converter_config_path, 'r') as stream:
        try:
            converter_config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            print("Failure to read the Sigma2SplunkApp configuration")
            sys.exit(1)
    return converter_config

def checkWhitelistExistence(rules, splunk_whitelist_path):
    lookupfolder = splunk_whitelist_path + "/lookups/"
    for r in rules:
        # create filename according to Sigma2SplunkAlert
        sigma_rule = openSigmaDetectionRule(r)
        file_name = sigma_rule["title"] + "_whitelist.csv"
        file_name = file_name.replace(" ", "_")
        file_name = file_name.replace("/", "_")
        file_name = file_name.replace("(", "")
        file_name = file_name.replace(")", "")
        lookupfile = lookupfolder + file_name
        if not os.path.exists(lookupfile):
            print (file_name)
    
# Copied from Sigma2SplunkAlert - Patrick Bareiss            
def openSigmaDetectionRule(rule_path):
    # Load Sigma detection rule
    with open(rule_path, 'r') as stream:
        try:
            sigma_uc = list(yaml.safe_load_all(stream))[0]
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(1)
    return sigma_uc


if __name__ == '__main__':
    main()